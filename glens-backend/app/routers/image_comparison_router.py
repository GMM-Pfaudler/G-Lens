import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from app.utils.image_comparison_utils.pdf_comparator import compare_pdf

router = APIRouter(tags=["File/Image Comparison"])

@router.post("/compare_drawings/")
async def compare_drawings(pdf1: UploadFile = File(...), pdf2: UploadFile = File(...)):
    try:
        # 1️⃣ Save uploaded PDFs to temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp1:
            temp1.write(await pdf1.read())
            pdf1_path = temp1.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp2:
            temp2.write(await pdf2.read())
            pdf2_path = temp2.name

        # 2️⃣ Create output dir
        output_dir = tempfile.mkdtemp(prefix="drawing_comparison_")

        # 3️⃣ Perform comparison
        compare_pdf(pdf1_path, pdf2_path, output_dir)

        # 4️⃣ Find result image
        result_folder = os.path.join(output_dir, "CompareResult")
        if not os.path.exists(result_folder):
            raise HTTPException(status_code=500, detail="No comparison result generated.")

        result_images = [
            f for f in os.listdir(result_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]
        if not result_images:
            raise HTTPException(status_code=500, detail="No result image was generated.")

        result_path = os.path.join(result_folder, result_images[0])

        # ✅ Read bytes before temp folder can be deleted
        with open(result_path, "rb") as f:
            image_bytes = f.read()

        # ✅ Return as binary response (safe, consistent)
        return Response(content=image_bytes, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
