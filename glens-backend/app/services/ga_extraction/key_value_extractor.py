import json
import re
from app.utils.camelot_extractor import extract_table_data
from app.services.ga_extraction.corrosion_and_rpm_helper import extract_corrosion_allowance,extract_joint_efficiency,extract_gearbox_section_from_json,extract_motor_speed_from_json,extract_ratio,get_motor_speed_context_block

def extract_key_value_pairs(file_path):
    raw_data = extract_table_data(file_path=file_path)

    TARGET_KEYS = [
        "TAG NO:", "VISCOSITY", "CAD FILE", "Dated","S.O. NO.","SO. NO.", "QNTY.", "PO NO.", "NDT", "WIND LOAD", "SEISMIC LOADING", "HEAT TRANSFER AREA", "TARE WEIGHT", "WEIGHT FULL OF WATER", "FASTENERS","TITLE:","CLIENT","ITEM CODE", "FOR WELD DETAIL REFER DRAWING NO.", "FOR WELD DETAIL REFER DRAWING NO.","CHECKED BY", "APPROVED BY", "PREPARED BY","JOINT EFFICIENCY"
    ]

    SECTION_HEADERS_TO_SKIP = [
        "GENERAL NOTES", "LINING SPECIFICATION", "LINING SPECIFICATIONS",
        "DO NOT SCALE", "DO NOT SCALE IF IN DOUBT","FACEOFDRIVE","MAIN WELD SEAMS OF INNER VESSEL","TEMPERATURE RANGE","STEM DIMENSION","GENERAL NOTES ","LINING SPECIFICATION GLASS "
    ]

    def normalize(text):
        return " ".join(re.sub(r'\s+', ' ', text.strip().replace("\xa0", " ")).split())

    key_value_pairs = {}

    key_value_pattern = r"^([A-Za-z0-9\s\.\-]+):\s*(.+)$"

    for row_idx, row in enumerate(raw_data):
        for col_idx, cell in row.items():
            raw_text = cell.strip()
            text = normalize(raw_text)

            if any(header in text.upper() for header in SECTION_HEADERS_TO_SKIP):
                continue

            # Address
            if "address" in text.lower():
                address_value = text.upper().replace("ADDRESS :", "").strip()
                if address_value:
                    key_value_pairs["ADDRESS"] = address_value
                continue

            # DRG. NO. & REV. NO.
            if "DRG" in raw_text.upper() and "REV" in raw_text.upper():
                lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
                
                rev_key_index = None
                rev_no = None

                for i, line in enumerate(lines):
                    if "REV" in line.upper():
                        rev_key_index = i
                        break

                for i, line in enumerate(lines):
                    if re.fullmatch(r"\d{1,2}", line):
                        rev_no = line
                        break

                label_tokens = {"DRG", "DRG. NO", "DRG. NO.", "NO", "NO.", "REV", "REV.", "REV NO", "REV. NO", "REVISION"}

                drg_parts = []
                for line in lines:
                    cleaned = line.upper().strip(" .")
                    if cleaned in label_tokens:
                        continue
                    if line == rev_no:
                        continue
                    drg_parts.append(line)

                if drg_parts:
                    drg_value = "/".join(" ".join(drg_parts).split())
                    key_value_pairs["DRG. NO."] = drg_value
                if rev_no:
                    key_value_pairs["REV. NO."] = rev_no

                continue

            match = re.match(key_value_pattern, text)
            if match:
                key, value = match.groups()

                if len(re.findall(r"[A-Za-z]", key)) < 3:
                    continue

                key_value_pairs[key] = value
                continue

            # Match known target keys like TAG NO, PO NO, etc.
            for key in TARGET_KEYS:
                if text.startswith(key):
                    for col_idx_next in range(int(col_idx) + 1, len(row)):
                        next_cell = normalize(row.get(str(col_idx_next), "").strip())
                        if next_cell:
                            if key in ("S.O. NO.", "SO. NO."):
                                next_cell = next_cell.replace(" ", "/")
                            key_value_pairs[key] = next_cell
                            break

    # Extract corrosion allowance
    corrosion_allowance = extract_corrosion_allowance(raw_data)
    if corrosion_allowance:
        key_value_pairs.update(corrosion_allowance)
    joint_efficiency = extract_joint_efficiency(raw_data)
    if joint_efficiency:
        key_value_pairs.update(joint_efficiency)
    # Motor and gearbox logic
    motor_speed = extract_motor_speed_from_json(raw_data)
    gearbox_section = extract_gearbox_section_from_json(raw_data)
    ratio = extract_ratio(gearbox_section) if gearbox_section else None

    if motor_speed is not None and ratio not in (None, 0):
        key_value_pairs["CALCULATED RPM"] = int(motor_speed / ratio)

    return {
        "KEY-VALUE PAIRS": key_value_pairs if key_value_pairs else "No matching keys found"
    }