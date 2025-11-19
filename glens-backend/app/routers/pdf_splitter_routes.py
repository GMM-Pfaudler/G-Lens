import os
import re
import shutil
from fastapi import APIRouter, Form, Query, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.pdf_extract_utils import process_uploaded_pdf
from app.core.database import get_session  # your async session dependency
from app.models.pdf_split import PDFSplitResult,upsert_pdf_split_result,SplitStatusEnum  # make sure this helper is defined

router = APIRouter(
    prefix="/pdf-splitter",
    tags=["PDF Splitter"]
)

BASE_OUTPUT = "D:/Glens_data/splitted_ofn_pdfs"
os.makedirs(BASE_OUTPUT, exist_ok=True)


def sanitize_filename(name: str) -> str:
    """Replace spaces + remove unsafe characters."""
    name = name.replace(" ", "_")
    return re.sub(r"[^A-Za-z0-9@._-]", "", name)


@router.post("/split-pdf")
async def split_pdf(
    file: UploadFile, 
    user_id: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Step 1: sanitize folder name based on original PDF
    sanitized_name = sanitize_filename(os.path.splitext(file.filename)[0])

    # Step 2: construct output folder: BASE_OUTPUT/<user_id>/<file_name>
    user_folder = os.path.join(BASE_OUTPUT, sanitize_filename(user_id))
    output_folder = os.path.join(user_folder, sanitized_name)

    # Step 3: clean folder if it exists (overwrite)
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    # Step 4: save uploaded file temporarily
    temp_pdf_path = os.path.join(output_folder, f"temp_input.pdf")
    try:
        with open(temp_pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 5: Process PDF
        result = process_uploaded_pdf(temp_pdf_path, output_folder=output_folder)
        generated_files = result.get("generated_files", [])

        # Step 6: Save to DB (upsert)
        saved_result = await upsert_pdf_split_result(
            db=db,
            user_id=user_id,
            file_name=sanitized_name,
            results=generated_files,
            status=SplitStatusEnum.success
        )

        return JSONResponse({
            "success": True,
            "quote_number": result.get("quote_number"),
            "total_sections": len(result.get("sections", [])),
            "files": generated_files,
            "output_folder": output_folder,
            "db_id": saved_result.id,
            "status": "success"
        })

    except Exception as e:
        # Cleanup folder if something failed
        shutil.rmtree(output_folder, ignore_errors=True)

        # Save failure to DB
        await upsert_pdf_split_result(
            db=db,
            user_id=user_id,
            file_name=sanitized_name,
            status=SplitStatusEnum.failure,
            error_message=str(e)
        )

        return JSONResponse({
            "success": False,
            "error": str(e),
            "status": "failure"
        }, status_code=500)

# -----------------------------
# Endpoint 1: Get all PDF split records
# # -----------------------------
# @router.get("/records")
# async def get_all_records(db: AsyncSession = Depends(get_session)):
#     stmt = select(PDFSplitResult)
#     result = await db.execute(stmt)
#     records = result.scalars().all()

#     data = [
#         {
#             "id": r.id,
#             "user_id": r.user_id,
#             "file_name": r.file_name,
#             "results": r.get_results(),
#             "status": r.status,
#             "error_message": r.error_message,
#             "uploaded_on": r.uploaded_on.isoformat()
#         }
#         for r in records
#     ]

#     return JSONResponse({"success": True, "records": data})


# -----------------------------
# Endpoint 2: Get single PDF split record by ID
# -----------------------------
@router.get("/records")
async def get_all_records(
    user_id: str = Query(..., alias="user_id"),
    db: AsyncSession = Depends(get_session)
):
    print("\nReceived user_id:", user_id)

    stmt = select(PDFSplitResult).where(PDFSplitResult.user_id == user_id)
    result = await db.execute(stmt)
    records = result.scalars().all()

    data = [
        {
            "id": r.id,
            "user_id": r.user_id,
            "file_name": r.file_name,
            "results": r.get_results(),
            "status": r.status,
            "error_message": r.error_message,
            "uploaded_on": r.uploaded_on.isoformat()
        }
        for r in records
    ]

    return {"success": True, "records": data}

BASE_OUTPUT = "D:/Glens_data/splitted_ofn_pdfs"  # keep for reference if needed


# ---------------------------------
# Endpoint 1: Get single record by ID with download URLs
# ---------------------------------
@router.get("/records/{record_id}")
async def get_record(record_id: int, db: AsyncSession = Depends(get_session)):
    stmt = select(PDFSplitResult).where(PDFSplitResult.id == record_id)
    result = await db.execute(stmt)
    record = result.scalars().first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Create download URLs for each file
    results_with_links = [
        {
            "file_name": os.path.basename(f),
            "download_url": f"/pdf-splitter/download?file_path={f.replace(os.sep, '/')}"
        }
        for f in record.get_results()
    ]

    data = {
        "id": record.id,
        "user_id": record.user_id,
        "file_name": record.file_name,
        "results": results_with_links,
        "status": record.status,
        "error_message": record.error_message,
        "uploaded_on": record.uploaded_on.isoformat()
    }

    return JSONResponse({"success": True, "record": data})


# ---------------------------------
# Endpoint 2: Download a PDF file
# ---------------------------------
@router.get("/download")
async def download_pdf(file_path: str = Query(..., description="Full path to the PDF file")):
    # Validate the path to avoid directory traversal
    normalized_path = os.path.abspath(file_path)
    if not normalized_path.startswith(os.path.abspath(BASE_OUTPUT)):
        raise HTTPException(status_code=400, detail="Invalid file path")

    if not os.path.exists(normalized_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=normalized_path,
        media_type='application/pdf',
        filename=os.path.basename(normalized_path)
    )