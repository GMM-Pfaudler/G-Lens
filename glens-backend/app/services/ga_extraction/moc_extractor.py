import json
import re
from fuzzywuzzy import fuzz
from app.utils.camelot_extractor import extract_table_data

def extract_material_of_construction(file_path):
    
    raw_data = extract_table_data(file_path=file_path)
    section_keys = {
        "INNERVESSEL": [
            "SHELL, HEADS AND BLIND COVER",
            "SHELL, HEADS & BLIND COVER",
            "WELDING NECKS FOR BODY FLANGE & NOZZLES",
            "SPLIT FLANGES",
            "GASKET FOR BODY FLANGE & NOZZLES",
            "GASKETS FOR BODY FLANGE & NOZZLES",
            "FASTENERS"
        ],
        "JACKET": [
            "SHELL, HEAD",
            "NOZZLE NECKS",
            "SORF FLANGES",
            "FLANGES",
            "COUPLINGS & PLUGS"
        ],
        "LIMPET COIL": [
            "ON SHELL LIMPET COIL ON BTM HEAD",
            "NOZZLE NECKS",
            "FLANGES",
            "SUPPORT SHELL OUTER SHELL SUPPORT SEALER RING SIDE SUPPORTS",
            "SUPPORT SHELL / SIDE SUPPORT",
            "SUPPORT SEALER RING",
            "LIMPET ON BTM HEAD AND LIMPET ON SHELL"
        ]
    }

    stop_keywords = ['LINING SPEC', 'GENERAL NOTES', 'NOTES', 'TESTING', 'SCOPE']
    
    def normalize(text):
        return re.sub(r'\s+', ' ', text.strip().upper())

    def fuzzy_match(input_str, choices, threshold=80):
        best_match = None
        best_score = 0
        for choice in choices:
            score = fuzz.partial_ratio(input_str.upper(), choice.upper())
            if score > best_score and score >= threshold:
                best_match = choice
                best_score = score
        return best_match

    normalized_section_keys = {
        section: {normalize(k): k for k in keys}
        for section, keys in section_keys.items()
    }

    output = {section: {} for section in section_keys}

    current_section = None
    start_processing = False

    for row in raw_data:
        for col_index, cell in row.items():
            cell_text = cell.strip()
            if not cell_text:
                continue

            cell_upper = cell_text.upper()

            if "MATERIAL SPECIFICATION" in cell_upper:
                start_processing = True
                continue

            if start_processing:
                matched_section = fuzzy_match(cell_upper, list(section_keys.keys()))
                if matched_section:
                    current_section = matched_section
                    continue

                if current_section:
                    matched_key = fuzzy_match(cell_text, section_keys[current_section])
                    if matched_key:
                        key_original = matched_key

                        spec = ""
                        for i in range(int(col_index) + 1, len(row)):
                            val = row.get(str(i), "").strip()
                            if val:
                                spec = re.sub(r'\s+', ' ', val)
                                break

                        if spec:
                            output[current_section][key_original] = spec

                if any(stop in cell_upper for stop in stop_keywords):
                    start_processing = False
                    break

    return output