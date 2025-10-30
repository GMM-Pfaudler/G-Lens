# app/routers/ofn_router.py
import os
import json
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from app.core.ofn_extractor import OFNPDFExtractor
from app.models.db_models import OFNFile
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

router = APIRouter(tags=["OFN"])

# IST timezone
ist_now = datetime.now(ZoneInfo("Asia/Kolkata"))

@router.post("/extract")
async def extract_ofn(file: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
    try:
        # -------------------------
        # Save uploaded PDF temporarily
        # -------------------------
        tmp_path = Path("tmp") / file.filename
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp_path, "wb") as f:
            f.write(await file.read())

        # -------------------------
        # Extract PDF (sync)
        # -------------------------
        extractor = OFNPDFExtractor(input_folder=tmp_path.parent, output_folder=tmp_path.parent)
        result = extractor.extract_single_pdf(tmp_path)

        # -------------------------
        # Save JSON result
        # -------------------------
        quote_no = str(result.get("GMM Pfaudler Quote No", "UNKNOWN")).strip()
        capacity = str(result.get("Capacity", "UNKNOWN")).strip().replace(" ", "_")
        filename = f"{quote_no}_{capacity}.json"

        save_dir = Path(r"D:\Glens_data\OFN")
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / filename

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        # -------------------------
        # Upsert DB record
        # -------------------------
        existing_result = await db.execute(select(OFNFile).where(OFNFile.file_name == filename))
        ofn_record = existing_result.scalar_one_or_none()

        if ofn_record:
            # Update existing record
            ofn_record.file_path = str(save_path)
            # ofn_record.upload_date = datetime.now(timezone.utc)
            ofn_record.upload_date = datetime.now(ZoneInfo("Asia/Kolkata"))
            ofn_record.status = 'completed'
            ofn_record.error_msg = None
        else:
            # Insert new record
            ofn_record = OFNFile(
                file_name=filename,
                file_path=str(save_path),
                # upload_date=datetime.now(timezone.utc),
                upload_date=datetime.now(ZoneInfo("Asia/Kolkata")),
                status='completed',
                error_msg=None
            )
            db.add(ofn_record)

        await db.commit()
        await db.refresh(ofn_record)

        return {"result": result, "db_id": ofn_record.id}

    except SQLAlchemyError as db_err:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error: {str(db_err)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction Failed: {str(e)}"
        )
