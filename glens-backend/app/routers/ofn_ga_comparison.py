from fastapi import (
    APIRouter, UploadFile, File, HTTPException, Depends,
    BackgroundTasks, WebSocket, Query
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.core.comparison_service import ComparisonService
# from app.models.db_models import ComparisonResult, StatusEnum
from app.models.comparison_model import ComparisonResult,StatusEnum
from app.core.database import get_session
from app.core.ws_manager import send_ws_message, register_ws, unregister_ws
from app.utils.ofn_vs_ga_utils.file_utils import sanitize_filename
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
import uuid
import os
import json
import asyncio

router = APIRouter(tags=["OFN-GA Comparison"])


# -------------------------
# Start a new comparison
# -------------------------
@router.post("/start")
async def start_comparison(
    background_tasks: BackgroundTasks,
    ga_json: UploadFile = File(...),
    ofn_json: UploadFile = File(...),
    user_id: str = Query(..., description="User ID initiating the comparison"),
    db: AsyncSession = Depends(get_session)
):
    """
    Start a new OFN vs GA comparison.
    """
    try:
        # 1️⃣ Generate unique job ID
        job_id = str(uuid.uuid4())
        print(f"\n🔹 [DEBUG] Job started: {job_id}, initiated by user: {user_id}")

        # 2️⃣ Read uploaded files
        ga_content = await ga_json.read()
        ofn_content = await ofn_json.read()
        print(f"📂 [DEBUG] Files read successfully — GA: {ga_json.filename}, OFN: {ofn_json.filename}")

        # 3️⃣ Decode JSON
        try:
            ga_data = json.loads(ga_content.decode("utf-8"))
            ofn_data = json.loads(ofn_content.decode("utf-8"))
            print(f"🧾 [DEBUG] JSON decoded successfully — GA keys: {list(ga_data.keys())[:5] if isinstance(ga_data, dict) else 'N/A'}")
        except Exception as e:
            print(f"❌ [DEBUG] JSON decoding failed: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

        # 4️⃣ Build names
        ofn_name = f"{ofn_data.get('GMM Pfaudler Quote No', 'Unknown')}_{ofn_data.get('Capacity', 'Unknown')}"
        ga_name = list(ga_data.keys())[0] if ga_data else "Unknown"
        sanitized_ofn_name = sanitize_filename(ofn_name)
        sanitized_ga_name = sanitize_filename(ga_name)
        print(f"🧩 [DEBUG] Sanitized filenames — OFN: {sanitized_ofn_name}, GA: {sanitized_ga_name}")

        # 🌐 Current IST time
        ist_now = datetime.now(ZoneInfo("Asia/Kolkata"))
        print(f"🕒 [DEBUG] Current IST Time: {ist_now}")

        # 5️⃣ Check for existing record for this user
        print(f"🔍 [DEBUG] Checking if record already exists for user_id={user_id} ...")
        result = await db.execute(
            select(ComparisonResult).where(
                and_(
                    ComparisonResult.ofn_file_name == sanitized_ofn_name,
                    ComparisonResult.ga_file_name == sanitized_ga_name,
                    ComparisonResult.user_id == user_id
                )
            )
        )
        existing_record = result.scalar_one_or_none()

        if existing_record:
            print(f"♻️ [DEBUG] Existing record found (ID={existing_record.id}), updating it...")
            existing_record.status = StatusEnum.pending
            existing_record.error_msg = None
            existing_record.comparison_result_path = None
            existing_record.job_id = job_id
            existing_record.updated_at = ist_now
            await db.commit()
            await db.refresh(existing_record)
            db_id = existing_record.id
            action = "updated"
        else:
            print("🆕 [DEBUG] Creating new comparison record...")
            new_record = ComparisonResult(
                ofn_file_name=sanitized_ofn_name,
                ga_file_name=sanitized_ga_name,
                status=StatusEnum.pending,
                job_id=job_id,
                user_id=user_id,
            )
            db.add(new_record)
            await db.commit()
            await db.refresh(new_record)
            db_id = new_record.id
            action = "created"
            print(f"✅ [DEBUG] New record created successfully (ID={db_id})")

        # 6️⃣ Run comparison in background
        print(f"🚀 [DEBUG] Scheduling background comparison task for DB_ID={db_id}")
        background_tasks.add_task(
            process_comparison_task,
            job_id,
            db_id,
            ga_data,
            ofn_data,
            db
        )

        # 7️⃣ Return immediate response
        print(f"✅ [DEBUG] Comparison started successfully — Job: {job_id}, DB_ID: {db_id}, Action: {action}\n")
        return {
            "job_id": job_id,
            "db_id": db_id,
            "status": "started",
            "record_action": action,
        }

    except Exception as e:
        print(f"🔥 [DEBUG] Exception while starting comparison: {e}\n")
        raise HTTPException(status_code=500, detail=f"Failed to start comparison: {e}")

# -------------------------
# Background task
# -------------------------
async def process_comparison_task(job_id: str, db_id: int, ga_data: dict, ofn_data: dict, db: AsyncSession):
    service = ComparisonService()
    print(f"\n🚀 [DEBUG] Background comparison started — job_id={job_id}, db_id={db_id}")
    try:
        # -----------------------------------------
        # 🔹 Mark as running
        # -----------------------------------------
        record = await db.get(ComparisonResult, db_id)
        if record:
            record.status = StatusEnum.running
            await db.commit()
            print(f"🟢 [DEBUG] Marked record {db_id} as 'running'")
        else:
            print(f"⚠️ [DEBUG] No record found in DB for db_id={db_id}")

        # -----------------------------------------
        # 🔹 Send initial WS update
        # -----------------------------------------
        await send_ws_message(job_id, {"status": "running", "progress": 0})
        print(f"📡 [DEBUG] WebSocket update sent — running 0%")

        # -----------------------------------------
        # ⚡ Run async comparison
        # -----------------------------------------
        print("⚙️ [DEBUG] Starting ComparisonService.process_comparison_async()...")
        result = await service.process_comparison_async(ga_data, ofn_data, job_id=job_id)
        print("✅ [DEBUG] Comparison completed — result obtained")

        # -----------------------------------------
        # 🗂 Save result file
        # -----------------------------------------
        ofn_name = f"{ofn_data.get('GMM Pfaudler Quote No', 'Unknown')}_{ofn_data.get('Capacity', 'Unknown')}"
        ga_name = list(ga_data.keys())[0] if ga_data else "Unknown"

        save_dir = r"D:/Glens_data/Comparison"
        os.makedirs(save_dir, exist_ok=True)
        filename = f"{sanitize_filename(ofn_name)}__{sanitize_filename(ga_name)}.json"
        save_path = os.path.join(save_dir, filename)

        print(f"💾 [DEBUG] Saving comparison result to {save_path}")
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"📁 [DEBUG] File saved successfully")

        # -----------------------------------------
        # ✅ Update DB
        # -----------------------------------------
        record = await db.get(ComparisonResult, db_id)
        if record:
            record.status = StatusEnum.completed
            record.comparison_result_path = save_path
            await db.commit()
            print(f"✅ [DEBUG] DB record updated to 'completed' for db_id={db_id}")
        else:
            print(f"⚠️ [DEBUG] Could not update record — record not found for db_id={db_id}")

        # -----------------------------------------
        # 📡 Send WS update
        # -----------------------------------------
        await send_ws_message(job_id, {
            "status": "completed",
            "progress": 100,
            "ofn_name": ofn_name,
            "ga_name": ga_name,
            "result": result,
        })
        print(f"📡 [DEBUG] Final WebSocket update sent — completed 100%")

    except Exception as e:
        print(f"🔥 [DEBUG] Exception during process_comparison_task: {e}")
        try:
            record = await db.get(ComparisonResult, db_id)
            if record:
                record.status = StatusEnum.error
                record.error_msg = str(e)
                await db.commit()
                print(f"🛑 [DEBUG] Updated DB record to 'error' for db_id={db_id}")
            else:
                print(f"⚠️ [DEBUG] No DB record found while handling error for db_id={db_id}")
        except Exception as inner_e:
            print(f"💣 [DEBUG] Error while handling exception: {inner_e}")

        await send_ws_message(job_id, {"status": "error", "error_msg": str(e)})
        print(f"📡 [DEBUG] WebSocket error update sent for job_id={job_id}")

# -------------------------
# WebSocket for progress
# -------------------------
@router.websocket("/ws/{job_id}")
async def comparison_ws(websocket: WebSocket, job_id: str):
    print(f"🟢 [WS] Connection attempt for job_id={job_id}")
    await register_ws(job_id, websocket)
    print(f"✅ [WS] Connected job_id={job_id}")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 [WS] Message from frontend ({job_id}): {data}")
    except Exception as e:
        print(f"⚠️ [WS] Closed or error for job_id={job_id}: {e}")
    finally:
        await unregister_ws(job_id, websocket)
        print(f"🔴 [WS] Disconnected for job_id={job_id}")

# -------------------------
# Get paginated comparison history (supports user & status filter)
# -------------------------
@router.get("/history")
async def get_comparison_history(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session),
):
    """
    Fetch paginated comparison records with optional filters for status and user_id.
    """
    q = select(ComparisonResult).order_by(ComparisonResult.created_at.desc())

    # apply filters
    if status:
        q = q.where(ComparisonResult.status == status)
    if user_id:
        q = q.where(ComparisonResult.user_id == user_id)

    # pagination
    q = q.limit(limit).offset(offset)

    res = await db.execute(q)
    rows = res.scalars().all()

    items = []
    for r in rows:
        items.append({
            "id": r.id,
            "job_id": r.job_id,
            "user_id": r.user_id,
            "ofn_file_name": r.ofn_file_name,
            "ga_file_name": r.ga_file_name,
            "comparison_result_path": r.comparison_result_path,
            "status": getattr(r.status, "value", r.status) if r.status is not None else None,
            "error_msg": r.error_msg,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        })

    return {
        "count": len(items),
        "items": items
    }

# -------------------------
# Get a single comparison by ID
# -------------------------
@router.get("/result/{id}")
async def get_comparison_result(id: int, db: AsyncSession = Depends(get_session)):
    """
    Return the comparison result JSON for a given record ID.
    """
    # 1️⃣ Fetch record
    q = select(ComparisonResult).where(ComparisonResult.id == id)
    res = await db.execute(q)
    record = res.scalars().first()

    if not record:
        raise HTTPException(status_code=404, detail="Comparison record not found")

    # 2️⃣ Validate file path
    file_path = record.comparison_result_path
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Comparison result file not found")

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
        "ofn_file_name": record.ofn_file_name,
        "ga_file_name": record.ga_file_name,
        "status": getattr(record.status, "value", record.status),
        "error_msg": record.error_msg,
        "created_at": record.created_at.isoformat() if record.created_at else None,
        "updated_at": record.updated_at.isoformat() if record.updated_at else None,
        "result": result_data
    }
