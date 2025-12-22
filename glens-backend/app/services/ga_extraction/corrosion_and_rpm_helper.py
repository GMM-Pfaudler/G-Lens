from typing import List, Optional
import re
from app.utils.camelot_extractor import extract_table_data

def get_motor_speed_context_block(data: List[dict], keyword_threshold=6) -> Optional[str]:
    keywords = [
        "FLAMEPROOF", "FLAME PROOF", "FLP", "ELECTRIC MOTOR", "EFFICIENCY CLASS IE3", "INVERTER DUTY",
        "MAKE", "RPM", "FRAME SIZE", "VOLTAGE", "415", "FREQUENCY", "3 PHASE",
        "IP-55", "DEGREE OF PROTECTION", "GAS GROUP", "ZONE 1", "HAZARDOUS AREA",
        "TEMP. CLASS", "TEMPERATURE CLASS", "HP", "KW", "K.W.", "KVA"
    ]

    best_match_text = ''
    max_hits = 0

    for row in data:
        combined_text = ' '.join(str(cell) for cell in row.values() if cell).upper()
        normalized_text = re.sub(r'\s+', ' ', combined_text).strip()
        hits = sum(1 for kw in keywords if kw in normalized_text)
        if hits > max_hits:
            max_hits = hits
            best_match_text = normalized_text

    return best_match_text if max_hits >= keyword_threshold else None

def extract_motor_speed_from_json(data: List[dict], keyword_threshold=6) -> Optional[int]:
    keywords = [
        "FLAMEPROOF", "FLAME PROOF", "FLP", "ELECTRIC MOTOR", "EFFICIENCY CLASS IE3", "INVERTER DUTY",
        "MAKE", "RPM", "FRAME SIZE", "VOLTAGE", "415", "FREQUENCY", "3 PHASE",
        "IP-55", "DEGREE OF PROTECTION", "GAS GROUP", "ZONE 1", "HAZARDOUS AREA",
        "TEMP. CLASS", "TEMPERATURE CLASS", "HP", "KW", "K.W.", "KVA"
    ]

    best_match = ''
    max_hits = 0

    for row in data:
        combined_text = ' '.join(cell for cell in row.values() if cell).upper()
        normalized_text = re.sub(r'\s+', ' ', combined_text).strip()
        hits = sum(1 for kw in keywords if kw in normalized_text)
        if hits > max_hits:
            max_hits = hits
            best_match = normalized_text

    if max_hits < keyword_threshold:
        return None

    speed_match = re.search(r'SPEED\s*[:=]?\s*(\d+)', best_match)
    if speed_match:
        return int(speed_match.group(1))

    rpm_match = re.search(r'RPM\s*[:=]?\s*(\d+)', best_match)
    if rpm_match:
        return int(rpm_match.group(1))

    fallback_rpm = re.search(r'(\d+)\s*RPM', best_match)
    if fallback_rpm:
        return int(fallback_rpm.group(1))

    return None

def extract_gearbox_section_from_json(data: List[dict], keyword_threshold=3) -> Optional[str]:
    gearbox_keywords = [
        "GEAR BOX", "INLINE HELICAL", "BONFIGLIOLI", "MODEL NO", "RATIO", "REDUCTION", "MAKE"
    ]

    best_match = ''
    max_hits = 0

    for row in data:
        combined_text = ' '.join(cell for cell in row.values() if cell).upper()
        normalized_text = re.sub(r'\s+', ' ', combined_text).strip()
        hits = sum(1 for kw in gearbox_keywords if kw in normalized_text)
        if hits > max_hits:
            max_hits = hits
            best_match = normalized_text

    return best_match if max_hits >= keyword_threshold else None

def extract_ratio(text: str) -> Optional[float]:
    match = re.search(r'RATIO\s+([\d.]+)\s*:\s*1', text.upper())
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


def calculate_output_rpm(data: List[dict]) -> Optional[float]:
    motor_speed = extract_motor_speed_from_json(data)
    print(motor_speed)
    gearbox_section = extract_gearbox_section_from_json(data)
    gear_ratio = extract_ratio(gearbox_section) if gearbox_section else None
    print(gear_ratio)

    if motor_speed is not None and gear_ratio is not None and gear_ratio != 0:
        return int(motor_speed / gear_ratio)
    
    return None
def extract_joint_efficiency(data):
    keyword = "joint_efficiency"
    keys = []
    values = []

    for row in data:
        for key, value in row.items():
            if keyword.lower() in str(value).lower():
                raw_text = value
                labels = raw_text.split("\n")

                # Extract label keys except 'CORROSION' and 'ALLOWANCE'
                filtered_labels = [label.strip().upper() for label in labels]
                keys = [label for label in filtered_labels if label not in ['JOINT', 'EFFICIENCY','%']]

                try:
                    key_index = int(key)
                except ValueError:
                    continue  # Skip non-numeric keys

                # Sort all row keys numerically
                sorted_keys = sorted(
                    [k for k in row.keys() if k.isdigit()],
                    key=lambda x: int(x)
                )

                # Start from key_index + 1 till the end
                started = False
                for k in sorted_keys:
                    if int(k) > key_index:
                        started = True
                        value_field = row.get(k, "")
                        if value_field:
                            numerical_values = value_field.split("\n")
                            for num_val in numerical_values:
                                try:
                                    val = float(num_val.strip())
                                    values.append(val)
                                except ValueError:
                                    continue
                        if len(values) >= len(keys):
                            values = values[:len(keys)]
                            break

                break  # Found joint_efficiency, stop processing this row

    if keys and values and len(keys) == len(values):
        return {
            "JOINT EFFICIENCY": dict(zip(keys, values))
        }
    else:
        return {}

def extract_corrosion_allowance(data):
    keyword = "corrosion"
    keys = []
    values = []

    for row in data:
        for key, value in row.items():
            if keyword.lower() in str(value).lower():
                raw_text = value
                labels = raw_text.split("\n")

                # Extract label keys except 'CORROSION' and 'ALLOWANCE'
                filtered_labels = [label.strip().upper() for label in labels]
                keys = [label for label in filtered_labels if label not in ['CORROSION', 'ALLOWANCE']]

                try:
                    key_index = int(key)
                except ValueError:
                    continue  # Skip non-numeric keys

                # Sort all row keys numerically
                sorted_keys = sorted(
                    [k for k in row.keys() if k.isdigit()],
                    key=lambda x: int(x)
                )

                # Start from key_index + 1 till the end
                started = False
                for k in sorted_keys:
                    if int(k) > key_index:
                        started = True
                        value_field = row.get(k, "")
                        if value_field:
                            numerical_values = value_field.split("\n")
                            for num_val in numerical_values:
                                try:
                                    val = float(num_val.strip())
                                    values.append(val)
                                except ValueError:
                                    continue
                        if len(values) >= len(keys):
                            values = values[:len(keys)]
                            break

                break  # Found corrosion, stop processing this row

    if keys and values and len(keys) == len(values):
        return {
            "CORROSION ALLOWANCE": dict(zip(keys, values))
        }
    else:
        return {}
    