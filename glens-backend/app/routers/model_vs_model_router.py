import os
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_session
from app.services.excel_comparison.model_vs_model_service import compare_records
from app.models.model3d_bom import Model3DBOMComparisonTbl

router = APIRouter(tags=["3D Model vs 3D Model Comparison"])

@router.post("/compare-modelBOMs")
async def compare_3d_model(
    model_a: UploadFile = File(...),
    model_b: UploadFile = File(...),
    db:AsyncSession = Depends(get_session)
):
    """
    Perform comparison between two 3D Model BOMs. Saves JSON locally, return structured results and store logs to DB.
    """
    try:
        tmp_dir = Path("tmp/3d_bom")
        tmp_dir.mkdir(parents=True,exist_ok=True)

        model_a_path = tmp_dir/model_a.filename
        model_b_path = tmp_dir/model_b.filename

        with open(model_a_path,"wb") as f:
            f.write(await model_a.read())
        with open(model_b_path,"wb") as f:
            f.write(await model_b.read())
    #===================================================================================================
        result = compare_records(model_a_path.read_bytes(),model_b_path.read_bytes())

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Comparison result is empty."
            )
    #====================================================================================================
        save_dir = Path(os.getenv("GL_MODEL_MODEL_SAVE_DIR","data/model_vs_model"))
        save_dir.mkdir(parents=True,exist_ok=True)

        model_a_base = model_a.filename.rsplit(".",1)[0]
        model_b_base = model_b.filename.rsplit(".",1)[0]
        json_filename = f"{model_a_base}_To_{model_b_base}_comparison.json"
        
        save_path = save_dir/json_filename
        with open(save_path,"w",encoding="utf-8") as f:
            json.dump(result,f,indent=4,ensure_ascii=False)
    #======================================================================================================
        existing_record = await db.execute(
            select(Model3DBOMComparisonTbl).where(
                Model3DBOMComparisonTbl.model_a_file == model_a.filename,
                Model3DBOMComparisonTbl.model_b_file == model_b.filename
            )
        )
        db_record = existing_record.scalar_one_or_none()

        if db_record:
            db_record.comparison_file_path = str(save_path)
            db_record.generation_date = datetime.now(ZoneInfo("Asia/Kolkata"))
        else:
            db_record= Model3DBOMComparisonTbl(generation_date=datetime.now(ZoneInfo("Asia/Kolkata")), comparison_file=save_path, model_a_file = model_a.filename,model_b_file=model_b.filename)
            db.add(db_record)
        await db.commit()
        await db.refresh(db_record)
    #==============================================================================================================
        return {
            "status": "success",
            "message": "Model vs Model Comparison completed successfully.",
            "db_id":db_record.id,
            "generation_date" : db_record.generation_date.isoformat(),
            "save_path" : db_record.comparison_file,
            "model_a_file" : db_record.model_a_file,
            "model_b_file" : db_record.model_b_file,
            "result_summary" : {
                "TO CREATE NEW" : len(result.get("TO CREATE NEW",[])),
                "MATCHED": len(result.get("MATCHED", [])),
                "POTENTIAL REPLACEMENTS": len(result.get("POTENTIAL REPLACEMENTS", [])),
                "UNMATCHED / MISSING": len(result.get("UNMATCHED / MISSING", [])),
                "NEWLY ADDED": len(result.get("NEWLY ADDED", [])),
                "EMPTY OR DASHED": len(result.get("EMPTY OR DASHED", [])),
            },
            "comparison_result" : result
        }
    except SQLAlchemyError as db_err:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Database Error: {str(db_err)}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comparison Failed: {str(e)}"
        )