# routers/ofngacomparison.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.comparison_service import ComparisonService
from app.models.db_models import ComparisonResult
from app.core.database import get_session
from app.core.ws_manager import send_ws_message, register_ws, unregister_ws
from app.utils.ofn_vs_ga_utils.file_utils import sanitize_filename
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import uuid
import os
import json,asyncio
from sqlalchemy import select, and_

router = APIRouter(tags=["Comparison"])

# -------------------------
# Start a new comparison
# -------------------------
@router.post("/start")
async def start_comparison(
    background_tasks: BackgroundTasks,
    ga_json: UploadFile = File(...),
    ofn_json: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
):
    try:
        # 1️⃣ Generate unique job ID
        job_id = str(uuid.uuid4())

        # 2️⃣ Read uploaded files
        ga_content = await ga_json.read()
        ofn_content = await ofn_json.read()

        # 3️⃣ Decode JSON
        try:
            ga_data = json.loads(ga_content.decode("utf-8"))
            ofn_data = json.loads(ofn_content.decode("utf-8"))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

        # 4️⃣ Build names
        ofn_name = f"{ofn_data.get('GMM Pfaudler Quote No', 'Unknown')}_{ofn_data.get('Capacity', 'Unknown')}"
        ga_name = list(ga_data.keys())[0] if ga_data else "Unknown"
        sanitized_ofn_name = sanitize_filename(ofn_name)
        sanitized_ga_name = sanitize_filename(ga_name)

        # 5️⃣ Check for existing record

        # 🌐 current IST time
        ist_now = datetime.now(ZoneInfo("Asia/Kolkata"))

        result = await db.execute(
            select(ComparisonResult).where(
                ComparisonResult.ofn_file_name == sanitized_ofn_name,
                ComparisonResult.ga_file_name == sanitized_ga_name
            )
        )
        existing_record = result.scalar_one_or_none()

        if existing_record:
            # ✅ Update existing record
            existing_record.status = "pending"
            existing_record.error_msg = None
            existing_record.comparison_result_path = None
            existing_record.job_id = job_id  # Optional: store latest job_id if you have that column
            existing_record.updated_at = ist_now
            await db.commit()
            await db.refresh(existing_record)
            db_id = existing_record.id
            action = "updated"
        else:
            # 🆕 Create new record
            new_record = ComparisonResult(
                ofn_file_name=sanitized_ofn_name,
                ga_file_name=sanitized_ga_name,
                status="pending",
                job_id=job_id,
                created_at=ist_now,
            )
            db.add(new_record)
            await db.commit()
            await db.refresh(new_record)
            db_id = new_record.id
            action = "created"

        # 6️⃣ Run comparison in background
        background_tasks.add_task(
            process_comparison_task,
            job_id,
            db_id,
            ga_data,
            ofn_data,
            db
        )

        # 7️⃣ Return response
        return {
            "job_id": job_id,
            "db_id": db_id,
            "status": "started",
            "record_action": action
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start comparison: {e}")



# -------------------------
# Background task function
# -------------------------
async def process_comparison_task(job_id: str, db_id: int, ga_data: dict, ofn_data: dict, db: AsyncSession):
    service = ComparisonService()
    try:
        # Mark as running in DB
        record = await db.get(ComparisonResult, db_id)
        record.status = "running"
        await db.commit()

        # Send initial WS update
        await send_ws_message(job_id, {"status": "running", "progress": 0})

        # Process comparison
        result = service.process_comparison(ga_data, ofn_data)

        # Save comparison locally for history (optional)
        ofn_name = f"{ofn_data.get('GMM Pfaudler Quote No', 'Unknown')}_{ofn_data.get('Capacity', 'Unknown')}"
        ga_name = list(ga_data.keys())[0] if ga_data else "Unknown"

        # Save comparison file
        save_dir = r"D:/Glens_data/Comparison"
        os.makedirs(save_dir, exist_ok=True)
        filename = f"{sanitize_filename(ofn_name)}__{sanitize_filename(ga_name)}.json"
        save_path = os.path.join(save_dir, filename)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        # Update DB
        record = await db.get(ComparisonResult, db_id)
        record.status = "completed"
        record.ofn_file_name = ofn_name
        record.ga_file_name = ga_name
        record.comparison_result_path = save_path
        await db.commit()

        print("✅ Comparison result type:", type(result))
        print("✅ Comparison result content:", result)

        # Send full result over WebSocket
        await send_ws_message(job_id, {
            "status": "completed",
            "progress": 100,
            "ofn_name": ofn_name,
            "ga_name": ga_name,
            "result": result
        })

    except Exception as e:
        # Update DB as error
        record = await db.get(ComparisonResult, db_id)
        record.status = "error"
        record.error_msg = str(e)
        await db.commit()

        # WS error message
        await send_ws_message(job_id, {"status": "error", "error_msg": str(e)})

# async def process_comparison_task(job_id: str, db_id: int, ga_data: dict, ofn_data: dict, db: AsyncSession):
#     service = ComparisonService()
#     try:
#         from datetime import datetime
#         from zoneinfo import ZoneInfo

#         ist_now = datetime.now(ZoneInfo("Asia/Kolkata"))

#         # -------------------------
#         # 1️⃣ Mark as running
#         # -------------------------
#         record = await db.get(ComparisonResult, db_id)
#         record.status = "running"
#         record.updated_at = ist_now
#         await db.commit()

#         # -------------------------
#         # 2️⃣ Initial WS update
#         # -------------------------
#         await send_ws_message(job_id, {"status": "running", "progress": 0, "message": "Comparison started"})

#         # -------------------------
#         # 4️⃣ Run comparison
#         # -------------------------
#         result = await service.process_comparison_async(ga_data, ofn_data, job_id=job_id)

#         # -------------------------
#         # 5️⃣ Save comparison file
#         # -------------------------
#         ofn_name = f"{ofn_data.get('GMM Pfaudler Quote No', 'Unknown')}_{ofn_data.get('Capacity', 'Unknown')}"
#         ga_name = list(ga_data.keys())[0] if ga_data else "Unknown"

#         save_dir = r"D:/Glens_data/Comparison"
#         os.makedirs(save_dir, exist_ok=True)
#         filename = f"{sanitize_filename(ofn_name)}__{sanitize_filename(ga_name)}.json"
#         save_path = os.path.join(save_dir, filename)

#         with open(save_path, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=4, ensure_ascii=False)

#         # -------------------------
#         # 6️⃣ Update record as completed
#         # -------------------------
#         record.status = "completed"
#         record.updated_at = datetime.now(ZoneInfo("Asia/Kolkata"))
#         record.ofn_file_name = ofn_name
#         record.ga_file_name = ga_name
#         record.comparison_result_path = save_path
#         await db.commit()

#         # -------------------------
#         # 7️⃣ Final WS message
#         # -------------------------
#         await send_ws_message(job_id, {
#             "status": "completed",
#             "progress": 100,
#             "message": "Comparison completed",
#             "ofn_name": ofn_name,
#             "ga_name": ga_name,
#             "result": result
#         })

#     except Exception as e:
#         record = await db.get(ComparisonResult, db_id)
#         record.status = "error"
#         record.error_msg = str(e)
#         record.updated_at = datetime.now(ZoneInfo("Asia/Kolkata"))
#         await db.commit()

#         await send_ws_message(job_id, {"status": "error", "error_msg": str(e)})
#         print(f"❌ Comparison failed: {e}")

# -------------------------
# WebSocket endpoint
# -------------------------
# @router.websocket("/ws/{job_id}")
# async def comparison_ws(websocket: WebSocket, job_id: str):
#     await register_ws(job_id, websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()  # Keep connection alive
#     except Exception:
#         pass
#     finally:
#         await unregister_ws(job_id, websocket)

@router.websocket("/ws/{job_id}")
async def comparison_ws(websocket: WebSocket, job_id: str):
    print(f"🟢 [WS] Connection attempt from frontend for job_id={job_id}")
    await register_ws(job_id, websocket)
    print(f"✅ [WS] WebSocket connected for job_id={job_id}")

    try:
        while True:
            data = await websocket.receive_text()  # Keeps connection alive
            print(f"📩 [WS] Received from frontend ({job_id}): {data}")
    except Exception as e:
        print(f"⚠️ [WS] Connection closed or error for job_id={job_id}: {e}")
    finally:
        await unregister_ws(job_id, websocket)
        print(f"🔴 [WS] Disconnected frontend for job_id={job_id}")
