from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.comparison_service import ComparisonService
from app.utils.ofn_vs_ga_utils.file_utils import sanitize_filename
import json
import os

router = APIRouter()

@router.post("/test-compare/", tags=["Comparison"])
async def test_compare(
    ga_json: UploadFile = File(...),
    ofn_json: UploadFile = File(...)
):
    try:
        # -------------------------
        # Read uploaded file bytes
        # -------------------------
        ga_content = await ga_json.read()
        ofn_content = await ofn_json.read()

        # -------------------------
        # Decode JSON safely
        # -------------------------
        try:
            ga_data = json.loads(ga_content.decode("utf-8") if isinstance(ga_content, (bytes, bytearray)) else ga_content)
            ofn_data = json.loads(ofn_content.decode("utf-8") if isinstance(ofn_content, (bytes, bytearray)) else ofn_content)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to decode GA or OFN JSON: {e}")

        # -------------------------
        # Ensure folder exists for intermediate files
        # -------------------------
        flattened_dir = r"data\flattened_files"
        os.makedirs(flattened_dir, exist_ok=True)

        # -------------------------
        # Initialize ComparisonService
        # -------------------------
        comparison_service = ComparisonService()

        # -------------------------
        # Process comparison
        # -------------------------
        # Pass JSON objects directly
        result = comparison_service.process_comparison(ga_data, ofn_data)

        # -------------------------
        # Optional: Save comparison locally for testing
        # -------------------------
        save_dir = r"D:/Glens_data/Comparison_Test"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{sanitize_filename(list(ga_data.keys())[0])}_comparison.json")
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        # -------------------------
        # Return full comparison result
        # -------------------------
        return {"status": "success", "comparison_report": result}

    except Exception as e:
        print(f"❌ Exception in process_comparison: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {e}")
