import json
import os
import tempfile
from app.utils.camelot_extractor import extract_table_data
# Importing other extractors
from app.services.ga_extraction.lining_spec_and_general_extractor import extract_lining_spec_and_notes
from app.services.ga_extraction.part_list_extractor import extract_part_list
from app.services.ga_extraction.design_data_extractor import extract_design_parameters
from app.services.ga_extraction.nozzle_data_extractor import process_extracted_data
from app.services.ga_extraction.moc_extractor import extract_material_of_construction
from app.services.ga_extraction.key_value_extractor import extract_key_value_pairs
from app.services.ga_extraction.motor_gearbox_extractor import extract_drive_data

class GAPDFExtractor:
    def __init__(self, file_path: str):
        """Initialize with the file path."""
        if not isinstance(file_path, str):
            raise ValueError("The file_path must be a string representing the file location.")
        
        self.file_path = file_path
        
        # Extract table data using Camelot
        self.raw_data = extract_table_data(file_path=self.file_path)

    def get_lining_and_notes(self):
        """Get Lining Specification and General Notes."""
        return extract_lining_spec_and_notes(self.file_path)

    def get_part_list(self):
        """Get the Part List from the PDF."""
        return extract_part_list(self.raw_data)

    def get_design_data(self):
        """Get the Design Data from the PDF."""
        return extract_design_parameters(self.raw_data)

    def get_nozzle_data(self):
        """Get the Nozzle Data from the PDF."""
        return process_extracted_data(self.raw_data)

    def get_material_of_construction(self):
        """Get the Material of Construction details."""
        return extract_material_of_construction(self.file_path)

    def get_key_value_pairs(self):
        """Get Key-Value Pairs."""
        return extract_key_value_pairs(self.file_path)
    
    def get_drive_data(self):
        # print("[DEBUG] extract_drive_data CALLED")
        return extract_drive_data(self.file_path)

    def extract_all_data(self):
        """Extract all data at once."""
        file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        data = {
            "Lining and Notes": self.get_lining_and_notes(),
            "Part List": self.get_part_list(),
            "Design Data": self.get_design_data(),
            "Nozzle Data": self.get_nozzle_data(),
            "Material of Construction": self.get_material_of_construction(),
            "Key-Value Pairs": self.get_key_value_pairs(),
            "Drive Data": self.get_drive_data()
        }
        return {file_name: data}

    def save_all_data(self, output_path: str):
        """Save all extracted data to a JSON file."""
        data = self.extract_all_data()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            print(f"All data saved to {output_path}")
