# app/core/bom_comparison.py
import os
import pandas as pd
from typing import Dict, Any, List

from app.services.excel_comparison.loader_and_splitter import convert_excel_to_structured_json
from app.services.excel_comparison.loader_and_splitter import filter_by_bom_level
from app.services.excel_comparison.comparison_functions import compare_all_items


def run_full_comparison(file_a_path: str, file_b_path: str, bom_level: str = None) -> Dict[str, Any]:
    """
    Run full BOM comparison and return structured JSON (no API calls, no DB logic).
    """
    try:
        bom_level = str(bom_level).strip() if bom_level else "1"

        # Parse excel files
        records_a = convert_excel_to_structured_json(file_a_path)
        records_b = convert_excel_to_structured_json(file_b_path)

        # Filter by BOM level
        filtered_a = filter_by_bom_level(records_a, bom_level)
        filtered_b = filter_by_bom_level(records_b, bom_level)

        # Comparison settings
        fields_to_compare = [
            'Item', 'Item Description', 'Net Quantity',
            'Drawing Number', 'Revision Number'
        ]
        short_labels = {
            'Item': 'Item',
            'Item Description': 'Desc',
            'Net Quantity': 'Qty',
            'Drawing Number': 'Drg',
            'Revision Number': 'Rev'
        }
        status_emojis = {
            'Unchanged': '✅ Matched',
            'Modified': '❌ Modified',
            'Missing in File B': '❌ Missing in New File',
            'New in File B': '➕ Extra in New File',
            'Potential Replacement': '❌ Replaced'
        }

        # Compare
        results = compare_all_items(filtered_a, filtered_b, fields_to_compare)

        # Prepare rows
        display_rows: List[Dict[str, Any]] = []
        for result in results:
            comp = result.get("Comparison", {})
            row: Dict[str, Any] = {}
            for field in fields_to_compare:
                val_a = comp.get(field, {}).get("file_a", "")
                val_b = comp.get(field, {}).get("file_b", "")
                short = short_labels.get(field, field)
                row[f"{short} (Old)"] = val_a
                row[f"{short} (New)"] = val_b

            raw_status = result.get("Status", "Unknown")
            row["Status"] = status_emojis.get(raw_status, raw_status)
            display_rows.append(row)

        # Save JSON locally
        save_dir = os.getenv("GL_FULL_BOM_SAVE_DIR", r"D:/GL_data/full_bom_comparison")
        os.makedirs(save_dir, exist_ok=True)

        file1_base = os.path.basename(file_a_path).rsplit('.', 1)[0]
        file2_base = os.path.basename(file_b_path).rsplit('.', 1)[0]
        filename = f"{file1_base}_To_{file2_base}_comparison.json"
        save_path = os.path.normpath(os.path.join(save_dir, filename)).replace("\\", "/")

        pd.DataFrame(display_rows).to_json(save_path, orient="records", indent=4, force_ascii=False)

        # Return result (no API calls)
        return {
            "status": "success",
            "message": f"Compared {len(display_rows)} items for BOM Level: {bom_level}",
            "bom_level": bom_level,
            "file1": file1_base,
            "file2": file2_base,
            "save_path": save_path,
            "result_count": len(display_rows),
            "comparison_result": display_rows,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during comparison: {str(e)}",
            "comparison_result": [],
        }
