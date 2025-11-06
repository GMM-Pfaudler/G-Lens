from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks, WebSocket,Query
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.ws_manager import send_ws_message, register_ws, unregister_ws
from app.core.ga_comparison_service import GAtoGAComparisonService
from app.models.ga_ga_comparison import GAGaComparisonResult
from app.utils.ofn_vs_ga_utils.file_utils import sanitize_filename
import os, json, uuid, asyncio
from datetime import datetime, timezone
from sqlalchemy import select, and_
from zoneinfo import ZoneInfo
from typing import Optional

router = APIRouter(tags=["GA-to-GA Comparison"])

# -------------------------
# Start GA to GA Comparison
# -------------------------
@router.post("/start")
async def start_ga_to_ga_comparison(
    background_tasks: BackgroundTasks,
    ga1_json: UploadFile = File(...),
    ga2_json: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
):
    try:
        # 1️⃣ Generate unique job ID
        job_id = str(uuid.uuid4())

        # 2️⃣ Read and decode GA JSONs
        ga1_content = await ga1_json.read()
        ga2_content = await ga2_json.read()

        try:
            ga1_data = json.loads(ga1_content.decode("utf-8"))
            ga2_data = json.loads(ga2_content.decode("utf-8"))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON format: {e}")

        # 3️⃣ Create readable names
        ga1_name = list(ga1_data.keys())[0] if isinstance(ga1_data, dict) else "Unknown_GA1"
        ga2_name = list(ga2_data.keys())[0] if isinstance(ga2_data, dict) else "Unknown_GA2"
        sanitized_ga1 = sanitize_filename(ga1_name)
        sanitized_ga2 = sanitize_filename(ga2_name)

        # Current IST time
        ist_now = datetime.now(ZoneInfo("Asia/Kolkata"))

        # Check for existing record
        result = await db.execute(
            select(GAGaComparisonResult).where(
                GAGaComparisonResult.ga1_file_name == sanitized_ga1,
                GAGaComparisonResult.ga2_file_name == sanitized_ga2
            )
        )
        existing_record = result.scalar_one_or_none()

        if existing_record:
            # Update existing record
            existing_record.status = "pending"
            existing_record.error_msg = None
            existing_record.comparison_result_path = None
            existing_record.job_id = job_id
            existing_record.result_date = ist_now
            await db.commit()
            await db.refresh(existing_record)
            db_id = existing_record.id
            action = "updated"
        else:
            # Create new record
            new_record = GAGaComparisonResult(
                ga1_file_name=sanitized_ga1,
                ga2_file_name=sanitized_ga2,
                status="pending",
                job_id=job_id,
                result_date=ist_now
            )
            db.add(new_record)
            await db.commit()
            await db.refresh(new_record)
            db_id = new_record.id
            action = "created"

        # 4️⃣ Fire background task
        # background_tasks.add_task(
        #     process_ga_to_ga_task,
        #     job_id,
        #     ga1_data,
        #     ga2_data,
        #     sanitized_ga1,
        #     sanitized_ga2,
        # )

        background_tasks.add_task(
            process_ga_to_ga_task,
            job_id,
            db_id,
            ga1_data,
            ga2_data,
            sanitized_ga1,
            sanitized_ga2,
            db
        )

        # 5️⃣ Return early to frontend
        return {"job_id": job_id, "status": "started", "message": "GA-to-GA comparison started"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start GA-to-GA comparison: {e}")


# -------------------------
# Background Comparison Task
# -------------------------
# async def process_ga_to_ga_task(job_id: str, ga1_data: dict, ga2_data: dict, ga1_name: str, ga2_name: str):
#     try:
#         await send_ws_message(job_id, {"status": "running", "progress": 0})

#         # 🧠 Run actual comparison
#         service = GAtoGAComparisonService()
#         result = await service.process_comparison_ga(ga1_data, ga2_data)

#         # 🗂️ Save comparison file locally
#         save_dir = r"D:/GL_data/GA_to_GA_Comparison"
#         os.makedirs(save_dir, exist_ok=True)
#         file_name = f"{ga1_name}_To_{ga2_name}_GA_to_GA.json"
#         save_path = os.path.join(save_dir, file_name)

#         with open(save_path, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=4, ensure_ascii=False)

#         # ✅ Send success WS event
#         await send_ws_message(job_id, {
#             "status": "completed",
#             "progress": 100,
#             "ga1_name": ga1_name,
#             "ga2_name": ga2_name,
#             "result": result
#         })

#     except Exception as e:
#         await send_ws_message(job_id, {"status": "error", "error_msg": str(e)})

async def process_ga_to_ga_task(
    job_id: str,
    db_id: int,
    ga1_data: dict,
    ga2_data: dict,
    ga1_name: str,
    ga2_name: str,
    db: AsyncSession
):
    service = GAtoGAComparisonService()
    try:
        # Mark as running in DB
        record = await db.get(GAGaComparisonResult, db_id)
        record.status = "running"
        await db.commit()

        # Send initial WS update
        await send_ws_message(job_id, {"status": "running", "progress": 0})

        # Process comparison
        result = await service.process_comparison_ga(ga1_data, ga2_data)

        # Save comparison file locally
        save_dir = r"D:/Glens_data/GA_to_GA_Comparison"
        os.makedirs(save_dir, exist_ok=True)
        filename = f"{sanitize_filename(ga1_name)}__{sanitize_filename(ga2_name)}.json"
        save_path = os.path.join(save_dir, filename)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        # Update DB
        record = await db.get(GAGaComparisonResult, db_id)
        record.status = "completed"
        record.comparison_result_path = save_path
        await db.commit()

        # Send full result over WebSocket
        await send_ws_message(job_id, {
            "status": "completed",
            "progress": 100,
            "ga1_name": ga1_name,
            "ga2_name": ga2_name,
            "result": result
        })

    except Exception as e:
        record = await db.get(GAGaComparisonResult, db_id)
        record.status = "error"
        record.error_msg = str(e)
        await db.commit()
        await send_ws_message(job_id, {"status": "error", "error_msg": str(e)})

# -------------------------
# WebSocket Endpoint
# -------------------------
@router.websocket("/ws/{job_id}")
async def ga_to_ga_ws(websocket: WebSocket, job_id: str):
    print(f"🟢 [WS] Frontend connected for GA-to-GA job_id={job_id}")
    await register_ws(job_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()  # keep-alive
            print(f"📩 WS Ping ({job_id}): {data}")
    except Exception as e:
        print(f"⚠️ [WS] Closed: {e}")
    finally:
        await unregister_ws(job_id, websocket)
        print(f"🔴 [WS] Disconnected for job_id={job_id}")

# -------------------------
# Get paginated GA-to-GA comparison history
# -------------------------
@router.get("/history")
async def get_ga_ga_comparison_history(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session),
):
    """
    Return a paginated list of GA-to-GA comparison records from the database.
    """
    q = select(GAGaComparisonResult).order_by(GAGaComparisonResult.result_date.desc()).limit(limit).offset(offset)

    if status:
        q = (
            select(GAGaComparisonResult)
            .where(GAGaComparisonResult.status == status)
            .order_by(GAGaComparisonResult.result_date.desc())
            .limit(limit)
            .offset(offset)
        )

    res = await db.execute(q)
    rows = res.scalars().all()

    items = []
    for r in rows:
        items.append({
            "id": r.id,
            "job_id": r.job_id,
            "ga1_file_name": r.ga1_file_name,
            "ga2_file_name": r.ga2_file_name,
            "comparison_result_path": r.comparison_result_path,
            "status": getattr(r.status, "value", r.status) if r.status is not None else None,
            "result_date": r.result_date.isoformat() if r.result_date else None,
            "error_msg": r.error_msg,
        })

    return {"count": len(items), "items": items}


# -------------------------
# Get a single comparison by ID
# -------------------------
@router.get("/history/{comparison_id}")
async def get_ga_ga_comparison_by_id(comparison_id: int, db: AsyncSession = Depends(get_session)):
    """
    Return a single GA-to-GA comparison record by database ID.
    Includes parsed comparison result data from the stored JSON file.
    """
    q = select(GAGaComparisonResult).where(GAGaComparisonResult.id == comparison_id)
    res = await db.execute(q)
    record = res.scalars().first()

    if not record:
        raise HTTPException(status_code=404, detail="Comparison record not found")

    # Try to read comparison JSON result
    comparison_data = None
    if record.comparison_result_path and os.path.exists(record.comparison_result_path):
        try:
            with open(record.comparison_result_path, "r", encoding="utf-8") as f:
                comparison_data = json.load(f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading comparison file: {e}")
    else:
        raise HTTPException(status_code=404, detail="Comparison result file not found on server")

    return {
        "id": record.id,
        "job_id": record.job_id,
        "ga1_file_name": record.ga1_file_name,
        "ga2_file_name": record.ga2_file_name,
        "status": getattr(record.status, "value", record.status) if record.status is not None else None,
        "result_date": record.result_date.isoformat() if record.result_date else None,
        "error_msg": record.error_msg,
        "comparison_data": comparison_data,  # 🧩 full result content here
    }