import os
import json
from pathlib import Path
from app.services.ofn_extraction.first_page_extractor import extract_page_1_data_from_pdf
from app.services.ofn_extraction.structured_extractor import parse_pdf_to_nested_indent
from app.services.ofn_extraction.table_extractor import extract_nozzles_and_agitator_from_pdf


class OFNPDFExtractor:
    def __init__(self, input_folder, output_folder="output"):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.keyword_groups = {
            "nozzles": ["Nozzle\nNo.", "Size", "Service", "Location", "Description"],
            "agitator": ["Type", "Sweep Diameter (in mm)"]
        }

    def extract_all_pdfs(self):
        self.output_folder.mkdir(parents=True, exist_ok=True)
        for pdf_file in self.input_folder.glob("*.pdf"):
            print(f"\nProcessing: {pdf_file.name}")
            result = self.extract_single_pdf(pdf_file)
            output_path = self.output_folder / (pdf_file.stem + ".json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Saved: {output_path.name}")

    def extract_single_pdf(self, pdf_path):
        data = {}

        # First page metadata
        first_page_data = extract_page_1_data_from_pdf(str(pdf_path))
        if isinstance(first_page_data, dict):
            data.update(first_page_data)

        # Structured bold/non-bold extraction
        structured_path = self.output_folder / "temp_structured.json"
        parse_pdf_to_nested_indent(str(pdf_path), output_path=str(structured_path))
        if structured_path.exists():
            with open(structured_path, "r", encoding="utf-8") as f:
                structured_data = json.load(f)
            data.update(structured_data)
            structured_path.unlink()  # Clean temp file

        # Table extraction
        table_data = extract_nozzles_and_agitator_from_pdf(str(pdf_path), self.keyword_groups)
        for section in table_data:
            data.setdefault("tables", []).append(section)

        return data
