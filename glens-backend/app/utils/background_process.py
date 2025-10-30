# app/utils/background_process.py
import asyncio
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.ws_manager import send_ws_message
from app.core.ga_extractor import GAPDFExtractor
from app.models.db_models import GAFile
import json
import os

OUTPUT_DIR = Path(r"D:\Glens_data\GA")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def _run_extractor(file_path: str):
    extractor = GAPDFExtractor(file_path=file_path)
    return extractor.extract_all_data()

def _save_json(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def _remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)

async def run_extraction_in_background(file_path: str, job_id: str, db: AsyncSession):
    try:
        # WS: extraction started
        await send_ws_message(job_id, {"status": "started", "progress": 0})

        # Run extraction in a separate thread
        result = await asyncio.to_thread(_run_extractor, file_path)
        await send_ws_message(job_id, {"status": "running", "progress": 50})

        # Save JSON result
        sanitized_name = Path(file_path).name.strip().replace(" ", "_")
        save_path = OUTPUT_DIR / f"{sanitized_name}.json"
        await asyncio.to_thread(_save_json, save_path, result)

        # Fetch GAFile fresh from DB
        async with db.begin():
            ga_record_result = await db.execute(select(GAFile).where(GAFile.job_id == job_id))
            ga_record = ga_record_result.scalar_one_or_none()
            if ga_record:
                ga_record.file_path = str(save_path)
                ga_record.status = "completed"
            else:
                print(f"[BackgroundTask] GAFile not found for job_id={job_id}")

        # WS: extraction completed
        await send_ws_message(job_id, {"status": "completed", "progress": 100, "result": result})

    except Exception as e:
        print(f"[BackgroundTask] Exception occurred for job_id={job_id}: {e}")

        # Fetch GAFile to update error status
        async with db.begin():
            ga_record_result = await db.execute(select(GAFile).where(GAFile.job_id == job_id))
            ga_record = ga_record_result.scalar_one_or_none()
            if ga_record:
                ga_record.status = "error"
                ga_record.error_msg = str(e)

        # WS: send error
        await send_ws_message(job_id, {"status": "error", "message": str(e)})

    finally:
        # Cleanup temp PDF
        await asyncio.to_thread(_remove_file, file_path)
