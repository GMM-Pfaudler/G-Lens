# routers/model_vs_bom_comparison.py
import os
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_session
from app.models.model_ref_bom_comparison import ModelRefBOMComparisonTbl
from app.services.excel_comparison.model_vs_bom_service import ModelVsBomService

router = APIRouter(tags=["Model vs BOM Comparison"])


@router.post("/model-bom-comparison")
async def model_bom_comparison(
    model_bom: UploadFile = File(...),
    ref_bom: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
):
    """
    Perform Model vs BOM comparison using the service.
    Saves JSON locally, logs to DB (update if exists or insert new).
    """
    try:
        # -------------------------
        # 1️⃣ Save uploaded files temporarily
        # -------------------------
        tmp_dir = Path("tmp/model_vs_bom")
        tmp_dir.mkdir(parents=True, exist_ok=True)

        model_path = tmp_dir / model_bom.filename
        ref_path = tmp_dir / ref_bom.filename

        with open(model_path, "wb") as f:
            f.write(await model_bom.read())
        with open(ref_path, "wb") as f:
            f.write(await ref_bom.read())

        # -------------------------
        # 2️⃣ Run comparison logic
        # -------------------------
        result = ModelVsBomService().compare_boms(
            model_path.read_bytes(),
            ref_path.read_bytes()
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Comparison result is empty."
            )

        # -------------------------
        # 3️⃣ Save JSON result file
        # -------------------------
        save_dir = Path(os.getenv("GL_MODEL_BOM_SAVE_DIR", "data/model_vs_bom"))
        save_dir.mkdir(parents=True, exist_ok=True)

        model_base = model_bom.filename.rsplit(".", 1)[0]
        ref_base = ref_bom.filename.rsplit(".", 1)[0]
        json_filename = f"{model_base}_To_{ref_base}_comparison.json"

        save_path = save_dir / json_filename
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        # -------------------------
        # 4️⃣ Check if record exists
        # -------------------------
        existing_query = await db.execute(
            select(ModelRefBOMComparisonTbl).where(
                ModelRefBOMComparisonTbl.model_bom_file == model_bom.filename,
                ModelRefBOMComparisonTbl.ref_bom_file == ref_bom.filename
            )
        )
        db_record = existing_query.scalar_one_or_none()

        # -------------------------
        # 5️⃣ Insert or Update record
        # -------------------------
        if db_record:
            db_record.comparison_file_path = str(save_path)
            db_record.generation_date = datetime.now(ZoneInfo("Asia/Kolkata"))
        else:
            db_record = ModelRefBOMComparisonTbl(
                generation_date=datetime.now(ZoneInfo("Asia/Kolkata")),
                comparison_file_path=str(save_path),
                model_bom_file=model_bom.filename,
                ref_bom_file=ref_bom.filename
            )
            db.add(db_record)

        await db.commit()
        await db.refresh(db_record)

        # -------------------------
        # 6️⃣ Return response
        # -------------------------
        return {
            "status": "success",
            "message": "Model vs BOM comparison completed successfully.",
            "db_id": db_record.id,
            "generation_date": db_record.generation_date.isoformat(),
            "save_path": db_record.comparison_file_path,
            "model_bom_file": db_record.model_bom_file,
            "ref_bom_file": db_record.ref_bom_file,
            "result_summary": {
                "TO CREATE NEW": len(result.get("TO CREATE NEW", [])),
                "MATCHED": len(result.get("MATCHED", [])),
                "POTENTIAL REPLACEMENTS": len(result.get("POTENTIAL REPLACEMENTS", [])),
                "UNMATCHED / MISSING": len(result.get("UNMATCHED / MISSING", [])),
                "NEWLY ADDED": len(result.get("NEWLY ADDED", [])),
                "EMPTY OR DASHED": len(result.get("EMPTY OR DASHED", [])),
            },
            "comparison_result": result  # 👈 Full data returned
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
