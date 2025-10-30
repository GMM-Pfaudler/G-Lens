import os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends,Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_session
from app.models.excel_comparison_models import FullBOMComparisonTbl
from app.core.bom_comparison import run_full_comparison

router = APIRouter(tags=["Full BOM Comparison"])

@router.post("/compare-full-bom")
async def compare_full_bom(
    file_a: UploadFile = File(...),
    file_b: UploadFile = File(...),
    # bom_level: str = "1",
    bom_level: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    """
    Perform full BOM comparison using the core function.
    Saves JSON locally, returns structured results, and logs to DB.
    """
    try:
        # -------------------------
        # 1️⃣ Save uploaded files temporarily
        # -------------------------
        tmp_dir = Path("tmp/full_bom")
        tmp_dir.mkdir(parents=True, exist_ok=True)

        file_a_path = tmp_dir / file_a.filename
        file_b_path = tmp_dir / file_b.filename

        with open(file_a_path, "wb") as f:
            f.write(await file_a.read())
        with open(file_b_path, "wb") as f:
            f.write(await file_b.read())

        # -------------------------
        # 2️⃣ Run comparison (core logic)
        # -------------------------
        result = run_full_comparison(str(file_a_path), str(file_b_path), bom_level)

        if result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Comparison failed")
            )

        # -------------------------
        # 3️⃣ Save record to DB
        # -------------------------
        save_path = result.get("save_path")
        file1_name = result.get("file1")
        file2_name = result.get("file2")

        existing_record = await db.execute(
            select(FullBOMComparisonTbl).where(
                FullBOMComparisonTbl.file1_name == file1_name,
                FullBOMComparisonTbl.file2_name == file2_name,
                FullBOMComparisonTbl.bom_level == bom_level
            )
        )
        db_record = existing_record.scalar_one_or_none()

        if db_record:
            # Update existing record
            db_record.comparison_file_path = save_path
            db_record.generation_date = datetime.now(ZoneInfo("Asia/Kolkata"))
        else:
            # Insert new record
            db_record = FullBOMComparisonTbl(
                generation_date=datetime.now(ZoneInfo("Asia/Kolkata")),
                comparison_file_path=save_path,
                file1_name=file1_name,
                file2_name=file2_name,
                bom_level=bom_level
            )
            db.add(db_record)

        await db.commit()
        await db.refresh(db_record)

        # -------------------------
        # 4️⃣ Return response
        # -------------------------
        return {
            "result": result,
            "db_id": db_record.id
        }

    except SQLAlchemyError as db_err:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error: {str(db_err)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comparison Failed: {str(e)}"
        )
