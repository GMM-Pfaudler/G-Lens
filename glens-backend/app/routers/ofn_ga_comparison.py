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
from app.core.sse_event_sender import broker
from app.utils.logger import log_event
from app.utils.log_helper import add_activity_log_async
from app.models.activity_log import LogStatusEnum
from app.routers.auth import get_current_user

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

        # --- Log: Comparison started
        await add_activity_log_async(
            db=db,
            message=f"Comparison started by user {user_id}",
            operation_type="ofn_ga_comparison",
            status=LogStatusEnum.started,
            user_id=user_id
        )
        log_event("ofn_ga_comparison", "started", f"Job {job_id} initiated by {user_id}")
        print(f"\n🔹 [DEBUG] Job started: {job_id}, initiated by user: {user_id}")

        # 2️⃣ Read uploaded files
        ga_content = await ga_json.read()
        ofn_content = await ofn_json.read()
        log_event("ofn_ga_comparison", "info", f"Files read successfully — GA: {ga_json.filename}, OFN: {ofn_json.filename}")
        print(f"📂 [DEBUG] Files read successfully — GA: {ga_json.filename}, OFN: {ofn_json.filename}")

        # 3️⃣ Decode JSON
        try:
            ga_data = json.loads(ga_content.decode("utf-8"))
            ofn_data = json.loads(ofn_content.decode("utf-8"))
            log_event("ofn_ga_comparison", "info", f"JSON decoded — GA keys: {list(ga_data.keys())[:5] if isinstance(ga_data, dict) else 'N/A'}")
            print(f"🧾 [DEBUG] JSON decoded successfully — GA keys: {list(ga_data.keys())[:5] if isinstance(ga_data, dict) else 'N/A'}")
        except Exception as e:
            log_event("ofn_ga_comparison", "error", f"JSON decoding failed: {e}")
            print(f"❌ [DEBUG] JSON decoding failed: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

        # 4️⃣ Build sanitized filenames
        ofn_name = f"{ofn_data.get('GMM Pfaudler Quote No', 'Unknown')}_{ofn_data.get('Capacity', 'Unknown')}"
        ga_name = list(ga_data.keys())[0] if ga_data else "Unknown"
        sanitized_ofn_name = sanitize_filename(ofn_name)
        sanitized_ga_name = sanitize_filename(ga_name)
        log_event("ofn_ga_comparison", "info", f"Sanitized filenames — OFN: {sanitized_ofn_name}, GA: {sanitized_ga_name}")
        print(f"🧩 [DEBUG] Sanitized filenames — OFN: {sanitized_ofn_name}, GA: {sanitized_ga_name}")

        # 🌐 Current IST time
        ist_now = datetime.now(ZoneInfo("Asia/Kolkata"))
        log_event("ofn_ga_comparison", "info", f"Current IST time: {ist_now}")
        print(f"🕒 [DEBUG] Current IST Time: {ist_now}")

        # 5️⃣ Check for existing record
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
            existing_record.status = StatusEnum.pending
            existing_record.error_msg = None
            existing_record.comparison_result_path = None
            existing_record.job_id = job_id
            existing_record.updated_at = ist_now
            await db.commit()
            await db.refresh(existing_record)
            db_id = existing_record.id
            action = "updated"
            log_event("ofn_ga_comparison", "info", f"Existing record found (ID={db_id}) — updated for new job {job_id}")
            print(f"♻️ [DEBUG] Existing record found (ID={db_id}), updated.")
        else:
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
            log_event("ofn_ga_comparison", "info", f"New record created (ID={db_id}) for job {job_id}")
            print(f"✅ [DEBUG] New record created successfully (ID={db_id})")

        # 6️⃣ Schedule background comparison
        background_tasks.add_task(
            process_comparison_task,
            job_id,
            db_id,
            ga_data,
            ofn_data,
            db,
            user_id
        )
        log_event("ofn_ga_comparison", "info", f"Background comparison task scheduled — DB_ID={db_id}, Job={job_id}")
        print(f"🚀 [DEBUG] Scheduled background comparison task for DB_ID={db_id}")

        # 7️⃣ Return response
        log_event("ofn_ga_comparison", "completed", f"Comparison started successfully — Job: {job_id}, DB_ID: {db_id}, Action: {action}")
        print(f"✅ [DEBUG] Comparison started successfully — Job: {job_id}, DB_ID: {db_id}, Action: {action}\n")

        return {
            "job_id": job_id,
            "db_id": db_id,
            "status": "started",
            "record_action": action,
        }

    except Exception as e:
        log_event("ofn_ga_comparison", "error", f"Exception during comparison start: {e}")
        print(f"🔥 [DEBUG] Exception while starting comparison: {e}\n")
        raise HTTPException(status_code=500, detail=f"Failed to start comparison: {e}")

# -------------------------
# Background task
# -------------------------
async def process_comparison_task(job_id: str, db_id: int, ga_data: dict, ofn_data: dict, db: AsyncSession, user_id: str):
    service = ComparisonService()
    try:
        record = await db.get(ComparisonResult, db_id)
        if record:
            record.status = StatusEnum.running
            await db.commit()

        # --- Add log_event for debugging / SSE
        log_event("ofn_ga_comparison", "info", f"Comparison running for OFN: {record.ofn_file_name} and GA: {record.ga_file_name}")
        await add_activity_log_async(
            db=db,
            message=f"Comparison running for OFN: {record.ofn_file_name} and GA: {record.ga_file_name}",
            operation_type="ofn_ga_comparison",
            status=LogStatusEnum.info,
            user_id=user_id
        )

        # ✅ NEW: Send "running" status update to frontend via WS and broker
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

        # -------------- Proceed with the comparison --------------
        result = await service.process_comparison_async(ga_data, ofn_data, job_id=job_id)

        ofn_name = f"{ofn_data.get('GMM Pfaudler Quote No', 'Unknown')}_{ofn_data.get('Capacity', 'Unknown')}"
        ga_name = list(ga_data.keys())[0] if ga_data else "Unknown"

        base_dir = r"D:/Glens_data/Comparison"
        user_dir = os.path.join(base_dir, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        filename = f"{sanitize_filename(ofn_name)}__{sanitize_filename(ga_name)}.json"
        save_path = os.path.join(user_dir, filename)

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        record.status = StatusEnum.completed
        record.comparison_result_path = save_path
        await db.commit()

        # --- Add completion log_event
        log_event("ofn_ga_comparison", "completed", f"Comparison completed for OFN: {ofn_name} and GA: {ga_name}")
        await add_activity_log_async(
            db=db,
            message=f"Comparison completed for OFN: {ofn_name} and GA: {ga_name}",
            operation_type="ofn_ga_comparison",
            status=LogStatusEnum.completed,
            user_id=user_id
        )

        await send_ws_message(job_id, {"status": "completed", "progress": 100})
        await broker.push({
            "event": "comparison_update",
            "data": {"db_id": db_id, "job_id": job_id, "user_id": user_id, "status": "completed"}
        })

    except Exception as e:
        record = await db.get(ComparisonResult, db_id)
        if record:
            record.status = StatusEnum.error
            record.error_msg = str(e)
            await db.commit()

        # --- Add error log_event
        log_event("ofn_ga_comparison", "error", f"Comparison failed for job {job_id}: {str(e)}")
        await add_activity_log_async(
            db=db,
            message=f"Comparison failed for job {job_id}: {str(e)}",
            operation_type="ofn_ga_comparison",
            status=LogStatusEnum.error,
            user_id=user_id
        )

        await send_ws_message(job_id, {"status": "error", "error_msg": str(e)})
        await broker.push({
            "event": "comparison_update",
            "data": {"db_id": db_id, "job_id": job_id, "user_id": user_id, "status": "error", "error_msg": str(e)}
        })


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
# @router.get("/history")
# async def get_comparison_history(
#     limit: int = Query(50, ge=1, le=500),
#     offset: int = Query(0, ge=0),
#     status: Optional[str] = Query(None),
#     user_id: Optional[str] = Query(None),
#     db: AsyncSession = Depends(get_session),
# ):
#     """
#     Fetch paginated comparison records with optional filters for status and user_id.
#     """
#     q = select(ComparisonResult).order_by(ComparisonResult.created_at.desc())

#     # apply filters
#     if status:
#         q = q.where(ComparisonResult.status == status)
#     if user_id:
#         q = q.where(ComparisonResult.user_id == user_id)

#     # pagination
#     q = q.limit(limit).offset(offset)

#     res = await db.execute(q)
#     rows = res.scalars().all()

#     items = []
#     for r in rows:
#         items.append({
#             "id": r.id,
#             "job_id": r.job_id,
#             "user_id": r.user_id,
#             "ofn_file_name": r.ofn_file_name,
#             "ga_file_name": r.ga_file_name,
#             "comparison_result_path": r.comparison_result_path,
#             "status": getattr(r.status, "value", r.status) if r.status is not None else None,
#             "error_msg": r.error_msg,
#             "created_at": r.created_at.isoformat() if r.created_at else None,
#             "updated_at": r.updated_at.isoformat() if r.updated_at else None,
#         })

#     return {
#         "count": len(items),
#         "items": items
#     }

# -------------------------
# Get paginated comparison history with userID filter (supports user & status filter)
# -------------------------
@router.get("/history")
async def get_comparison_history(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """
    Fetch paginated comparison records.
    Non-admins only see their own comparisons.
    Admins can use ?user_id= to filter others.
    """

    q = select(ComparisonResult).order_by(ComparisonResult.created_at.desc())

    # Apply role-based filter
    if current_user["role"] != "admin":
        q = q.where(ComparisonResult.user_id == current_user["user_id"])
    elif user_id:
        q = q.where(ComparisonResult.user_id == user_id)

    # q = q.where(ComparisonResult.user_id == current_user["user_id"])

    if status:
        q = q.where(ComparisonResult.status == status)

    q = q.limit(limit).offset(offset)
    res = await db.execute(q)
    rows = res.scalars().all()

    items = [
        {
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
        }
        for r in rows
    ]

    return {"count": len(items), "items": items}


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
