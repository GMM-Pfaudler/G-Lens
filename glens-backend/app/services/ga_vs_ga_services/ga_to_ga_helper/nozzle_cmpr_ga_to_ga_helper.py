from typing import List, Dict
from rapidfuzz.fuzz import ratio

def compare_nozzle_data(standard_nozzles: List[Dict], target_nozzles: List[Dict]) -> List[Dict]:    
    FUZZY_THRESHOLD = 0.90

    def normalize(text):
        return str(text).strip().upper()
    
    result = []

    standard_map = {nozzle["Ref."]: nozzle for nozzle in standard_nozzles}
    target_map = {nozzle["Ref."]: nozzle for nozzle in target_nozzles}

    matched_refs = set()

    # Compare nozzles from Standard GA to Target GA
    for ref, std_nozzle in standard_map.items():
        if ref in target_map:
            tgt_nozzle = target_map[ref]
            differences = {}

            for field in std_nozzle:
                std_val = str(std_nozzle.get(field, "")).strip()
                tgt_val = str(tgt_nozzle.get(field, "")).strip()

                if not std_val and not tgt_val:
                    continue 

                if field.lower() != "ref.":
                    similarity = ratio(normalize(std_val), normalize(tgt_val)) / 100
                    if similarity < FUZZY_THRESHOLD:
                        differences[field] = {
                            "standard_value": std_val,
                            "target_value": tgt_val,
                        }

            result_entry = {
                "ref.": ref,
                "status": "mismatch" if differences else "match",
                "differences": differences
            }

            # Add full_match_fields only if no differences
            if not differences:
                result_entry["full_match_fields"] = {
                    field: {
                        "standard_value": str(std_nozzle.get(field, "")).strip(),
                        "target_value": str(tgt_nozzle.get(field, "")).strip()
                    } for field in std_nozzle
                }

            result.append(result_entry)
            matched_refs.add(ref)

        else:
            # Nozzle in standard but missing in target
            differences = {
                field: {
                    "standard_value": std_nozzle.get(field),
                    "target_value": None
                } for field in std_nozzle
            }

            result.append({
                "ref.": ref,
                "status": "missing_in_target",
                "differences": differences
            })

    # Check for nozzles in Target GA that are not in Standard GA
    for ref, tgt_nozzle in target_map.items():
        if ref not in matched_refs:
            differences = {
                field: {
                    "standard_value": None,
                    "target_value": tgt_nozzle.get(field)
                } for field in tgt_nozzle
            }

            result.append({
                "ref.": ref,
                "status": "extra_in_target",
                "differences": differences
            })

    return result