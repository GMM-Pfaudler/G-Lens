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
from app.utils.logger import log_event
from app.utils.log_helper import add_activity_log_async
from app.core.sse_event_sender import broker
from app.models.ga_ga_comparison import StatusEnum
from app.models.activity_log import LogStatusEnum
from app.routers.auth import get_current_user

router = APIRouter(tags=["GA-to-GA Comparison"])

# -------------------------
# Start GA to GA Comparison
# -------------------------
@router.post("/start")
async def start_ga_to_ga_comparison(
    background_tasks: BackgroundTasks,
    ga1_json: UploadFile = File(...),
    ga2_json: UploadFile = File(...),
    user_id: str = Query(..., description="User ID initiating the comparison"),
    db: AsyncSession = Depends(get_session),
):
    try:
        # 1️⃣ Generate unique job ID
        job_id = str(uuid.uuid4())

        # Log start
        await add_activity_log_async(
            db=db,
            message=f"GA→GA comparison started by user {user_id} (Job ID: {job_id})",
            operation_type="ga_ga_comparison",
            status=LogStatusEnum.started,
            user_id=user_id
        )
        log_event("ga_ga_comparison", "started", f"Job {job_id} initiated by {user_id}")
        print(f"\n🔹 [DEBUG] GA→GA Job started: {job_id}, user: {user_id}")

        # 2️⃣ Read and decode GA JSONs
        ga1_content = await ga1_json.read()
        ga2_content = await ga2_json.read()
        try:
            ga1_data = json.loads(ga1_content.decode("utf-8"))
            ga2_data = json.loads(ga2_content.decode("utf-8"))
        except Exception as e:
            log_event("ga_ga_comparison", "error", f"JSON decoding failed: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON format: {e}")

        # 3️⃣ Create readable names
        ga1_name = list(ga1_data.keys())[0] if isinstance(ga1_data, dict) else "Unknown_GA1"
        ga2_name = list(ga2_data.keys())[0] if isinstance(ga2_data, dict) else "Unknown_GA2"
        sanitized_ga1 = sanitize_filename(ga1_name)
        sanitized_ga2 = sanitize_filename(ga2_name)

        log_event("ga_ga_comparison", "info", f"Sanitized names — GA1: {sanitized_ga1}, GA2: {sanitized_ga2}")

        # 4️⃣ Check for existing record (per user)
        result = await db.execute(
            select(GAGaComparisonResult).where(
                and_(
                    GAGaComparisonResult.ga1_file_name == sanitized_ga1,
                    GAGaComparisonResult.ga2_file_name == sanitized_ga2,
                    GAGaComparisonResult.user_id == user_id
                )
            )
        )
        existing_record = result.scalar_one_or_none()

        if existing_record:
            # Update existing record
            existing_record.status = StatusEnum.pending
            existing_record.error_msg = None
            existing_record.comparison_result_path = None
            existing_record.job_id = job_id
            await db.commit()
            await db.refresh(existing_record)
            db_id = existing_record.id
            action = "updated"
            log_event("ga_ga_comparison", "info", f"Existing record found (ID={db_id}) — updated for new job {job_id}")
        else:
            # Create new record
            new_record = GAGaComparisonResult(
                ga1_file_name=sanitized_ga1,
                ga2_file_name=sanitized_ga2,
                status=StatusEnum.pending,
                job_id=job_id,
                user_id=user_id
            )
            db.add(new_record)
            await db.commit()
            await db.refresh(new_record)
            db_id = new_record.id
            action = "created"
            log_event("ga_ga_comparison", "info", f"New GA→GA record created (ID={db_id}) for job {job_id}")

        # 5️⃣ Schedule background task
        background_tasks.add_task(
            process_ga_to_ga_task,
            job_id,
            db_id,
            ga1_data,
            ga2_data,
            sanitized_ga1,
            sanitized_ga2,
            db,
            user_id
        )

        log_event("ga_ga_comparison", "info", f"Background GA→GA task scheduled — DB_ID={db_id}, Job={job_id}")

        # 6️⃣ Return early to frontend
        return {
            "job_id": job_id,
            "db_id": db_id,
            "status": "started",
            "record_action": action
        }

    except HTTPException:
        raise
    except Exception as e:
        log_event("ga_ga_comparison", "error", f"Exception while starting GA→GA comparison: {e}")
        print(f"🔥 [DEBUG] Exception in start_ga_to_ga_comparison: {e}\n")
        raise HTTPException(status_code=500, detail=f"Failed to start GA→GA comparison: {e}")

# async def process_ga_to_ga_task(
#     job_id: str,
#     db_id: int,
#     ga1_data: dict,
#     ga2_data: dict,
#     ga1_name: str,
#     ga2_name: str,
#     db: AsyncSession
# ):
#     service = GAtoGAComparisonService()
#     try:
#         # Mark as running in DB
#         record = await db.get(GAGaComparisonResult, db_id)
#         record.status = "running"
#         await db.commit()

#         # Send initial WS update
#         await send_ws_message(job_id, {"status": "running", "progress": 0})

#         # Process comparison
#         result = await service.process_comparison_ga(ga1_data, ga2_data)

#         # Save comparison file locally
#         save_dir = r"D:/Glens_data/GA_to_GA_Comparison"
#         os.makedirs(save_dir, exist_ok=True)
#         filename = f"{sanitize_filename(ga1_name)}__{sanitize_filename(ga2_name)}.json"
#         save_path = os.path.join(save_dir, filename)
#         with open(save_path, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=4, ensure_ascii=False)

#         # Update DB
#         record = await db.get(GAGaComparisonResult, db_id)
#         record.status = "completed"
#         record.comparison_result_path = save_path
#         await db.commit()

#         # Send full result over WebSocket
#         await send_ws_message(job_id, {
#             "status": "completed",
#             "progress": 100,
#             "ga1_name": ga1_name,
#             "ga2_name": ga2_name,
#             "result": result
#         })

#     except Exception as e:
#         record = await db.get(GAGaComparisonResult, db_id)
#         record.status = "error"
#         record.error_msg = str(e)
#         await db.commit()
#         await send_ws_message(job_id, {"status": "error", "error_msg": str(e)})

async def process_ga_to_ga_task(
    job_id: str,
    db_id: int,
    ga1_data: dict,
    ga2_data: dict,
    ga1_name: str,
    ga2_name: str,
    db: AsyncSession,
    user_id: str  # ✅ add this to track logs and SSE properly
):
    service = GAtoGAComparisonService()
    try:
        # 1️⃣ Mark as running
        record = await db.get(GAGaComparisonResult, db_id)
        if record:
            record.status = StatusEnum.running
            await db.commit()

        # --- Activity Log + Event
        log_event("ga_ga_comparison", "info", f"Comparison running for GA1: {ga1_name} and GA2: {ga2_name}")
        await add_activity_log_async(
            db=db,
            message=f"GA→GA comparison running for GA1: {ga1_name} and GA2: {ga2_name}",
            operation_type="ga_ga_comparison",
            status=LogStatusEnum.info,
            user_id=user_id
        )

        # --- Send running status (for frontend updates)
        await send_ws_message(job_id, {"status": "running", "progress": 0})
        await broker.push({
            "event": "comparison_update",
            "data": {
                "db_id": db_id,
                "job_id": job_id,
                "user_id": user_id,
                "status": "running",
                "progress": 0
            }
        })

        # 2️⃣ Perform comparison
        result = await service.process_comparison_ga(ga1_data, ga2_data)

        # 3️⃣ Save comparison file
        base_dir = r"D:/Glens_data/GA_to_GA_Comparison"
        user_dir = os.path.join(base_dir, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        filename = f"{sanitize_filename(ga1_name)}__{sanitize_filename(ga2_name)}.json"
        save_path = os.path.join(user_dir, filename)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        # 4️⃣ Update DB
        record = await db.get(GAGaComparisonResult, db_id)
        record.status = StatusEnum.completed
        record.comparison_result_path = save_path
        await db.commit()

        # --- Completion log
        log_event("ga_ga_comparison", "completed", f"GA→GA comparison completed for GA1: {ga1_name} and GA2: {ga2_name}")
        await add_activity_log_async(
            db=db,
            message=f"GA→GA comparison completed for GA1: {ga1_name} and GA2: {ga2_name}",
            operation_type="ga_ga_comparison",
            status=LogStatusEnum.completed,
            user_id=user_id
        )

        # --- Final SSE/WS update
        await send_ws_message(job_id, {
            "status": "completed",
            "progress": 100,
            "ga1_name": ga1_name,
            "ga2_name": ga2_name,
            "result": result
        })
        await broker.push({
            "event": "comparison_update",
            "data": {
                "db_id": db_id,
                "job_id": job_id,
                "user_id": user_id,
                "status": "completed"
            }
        })

    except Exception as e:
        record = await db.get(GAGaComparisonResult, db_id)
        if record:
            record.status = StatusEnum.error
            record.error_msg = str(e)
            await db.commit()

        log_event("ga_ga_comparison", "error", f"GA→GA comparison failed for job {job_id}: {str(e)}")
        await add_activity_log_async(
            db=db,
            message=f"GA→GA comparison failed for job {job_id}: {str(e)}",
            operation_type="ga_ga_comparison",
            status=LogStatusEnum.error,
            user_id=user_id
        )

        await send_ws_message(job_id, {"status": "error", "error_msg": str(e)})
        await broker.push({
            "event": "comparison_update",
            "data": {
                "db_id": db_id,
                "job_id": job_id,
                "user_id": user_id,
                "status": "error",
                "error_msg": str(e)
            }
        })

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
# Get GA→GA comparison history (role-aware)
# -------------------------
@router.get("/history")
async def get_ga_ga_comparison_history(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Fetch paginated GA→GA comparison records.
    Non-admins only see their own comparisons.
    Admins can use ?user_id= to filter others.
    """
    q = select(GAGaComparisonResult).order_by(GAGaComparisonResult.created_at.desc())

    # Role-based filtering
    if current_user["role"] != "admin":
        q = q.where(GAGaComparisonResult.user_id == current_user["user_id"])
    elif user_id:
        q = q.where(GAGaComparisonResult.user_id == user_id)

    # q = q.where(GAGaComparisonResult.user_id == current_user["user_id"])

    # Optional status filter
    if status:
        q = q.where(GAGaComparisonResult.status == status)

    # Pagination
    q = q.limit(limit).offset(offset)
    res = await db.execute(q)
    rows = res.scalars().all()

    # Format response
    items = [
        {
            "id": r.id,
            "job_id": r.job_id,
            "user_id": r.user_id,
            "ga1_file_name": r.ga1_file_name,
            "ga2_file_name": r.ga2_file_name,
            "comparison_result_path": r.comparison_result_path,
            "status": getattr(r.status, "value", r.status) if r.status is not None else None,
            "error_msg": r.error_msg,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }
        for r in rows
    ]

    return {"count": len(items), "items": items}



# -------------------------
# Get a single GA→GA comparison by ID
# -------------------------
@router.get("/result/{id}")
async def get_ga_ga_comparison_result(id: int, db: AsyncSession = Depends(get_session)):
    """
    Return the GA→GA comparison result JSON for a given record ID.
    """
    # 1️⃣ Fetch record
    q = select(GAGaComparisonResult).where(GAGaComparisonResult.id == id)
    res = await db.execute(q)
    record = res.scalars().first()

    if not record:
        raise HTTPException(status_code=404, detail="GA→GA comparison record not found")

    # 2️⃣ Validate file path
    file_path = record.comparison_result_path
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="GA→GA comparison result file not found")

    # 3️⃣ Load JSON result
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            result_data = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading result file: {e}")

    # 4️⃣ Return structured payload
    return {
        "id": record.id,
        "job_id": record.job_id,
        "user_id": record.user_id,
        "ga1_file_name": record.ga1_file_name,
        "ga2_file_name": record.ga2_file_name,
        "status": getattr(record.status, "value", record.status),
        "error_msg": record.error_msg,
        "created_at": record.created_at.isoformat() if record.created_at else None,
        "updated_at": record.updated_at.isoformat() if record.updated_at else None,
        "comparison_result_path": record.comparison_result_path,
        "result": result_data
    }
