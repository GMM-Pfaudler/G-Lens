# app/routers/ga_router.py
import uuid
import os
import tempfile
import asyncio
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.models.db_models import GAFile
from app.core.database import get_session
from app.utils.background_process import run_extraction_in_background
from app.core.ws_manager import register_ws, unregister_ws, send_ws_message
from zoneinfo import ZoneInfo

router = APIRouter(tags=["GA"])

ist_now = datetime.now(ZoneInfo("Asia/Kolkata"))

# Permanent output directory
OUTPUT_DIR = Path(r"D:\Glens_data\GA")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- WebSocket route ---
@router.websocket("/ws/ga/{job_id}")
async def websocket_ga_status(websocket: WebSocket, job_id: str):
    await register_ws(job_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        await unregister_ws(job_id, websocket)
    except Exception:
        await unregister_ws(job_id, websocket)
        try:
            await websocket.close()
        except:
            pass

# --- Extraction endpoint ---
@router.post("/extract")
async def extract_ga(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
):
    # 1️⃣ Generate unique job ID
    job_id = str(uuid.uuid4())

    # 2️⃣ Save uploaded PDF to temporary file
    temp_file_path = os.path.join(tempfile.gettempdir(), f"{file.filename}")
    file_bytes = await file.read()
    await asyncio.to_thread(_write_file, temp_file_path, file_bytes)

    # 3️⃣ Create or update DB record immediately
    result = await db.execute(select(GAFile).where(GAFile.file_name == file.filename))
    ga_record = result.scalar_one_or_none()

    if ga_record:
        ga_record.status = "running"
        # ga_record.upload_date = datetime.now(timezone.utc)
        ga_record.upload_date = datetime.now(ZoneInfo("Asia/Kolkata"))
        ga_record.file_path = temp_file_path
        ga_record.error_msg = None
        ga_record.job_id = job_id
    else:
        ga_record = GAFile(
            file_name=file.filename,
            file_path=temp_file_path,
            # upload_date=datetime.now(timezone.utc),
            upload_date=datetime.now(ZoneInfo("Asia/Kolkata")),
            status="running",
            error_msg=None,
            job_id=job_id
        )
        db.add(ga_record)

    await db.commit()
    await db.refresh(ga_record)

    # 4️⃣ Send initial WebSocket message
    await send_ws_message(job_id, {"status": "started", "progress": 0})

    # 5️⃣ Run extraction in background
    background_tasks.add_task(run_extraction_in_background, temp_file_path, job_id, db)

    return {"job_id": job_id, "message": "Started"}


# --- Thread-safe helpers ---
def _write_file(path, content):
    with open(path, "wb") as f:
        f.write(content)
