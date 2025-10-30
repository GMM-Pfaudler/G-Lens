from typing import List, Dict
from collections import defaultdict,Counter
from rapidfuzz.fuzz import token_set_ratio

def compare_part_list(standard_parts: List[Dict[str, str]], target_parts: List[Dict[str, str]]) -> List[Dict]:
    result = []

    FORCE_DESC_MATCH_KEYWORDS = [
        "gasket",
        "gl blind cover",
        "c clamp",
        "drain/vent coupling",
        "cs ptfe lined dip pipe",
        "cs ptfe lined sparger",
    ]

    SIMILARITY_THRESHOLD = 0.70

    def normalize(text: str) -> str:
        return text.strip().upper()

    def description_similarity(a: str, b: str) -> float:
        return token_set_ratio(normalize(a), normalize(b)) / 100  # Returns float between 0 and 1

    standard_by_drg = defaultdict(list)
    target_by_drg = defaultdict(list)

    for part in standard_parts:
        standard_by_drg[normalize(part["drawing_no"])].append(part)

    for part in target_parts:
        target_by_drg[normalize(part["drawing_no"])].append(part)

    matched_target_indices = defaultdict(set)
    drawing_no_counts_standard = Counter(normalize(part["drawing_no"]) for part in standard_parts)
    drawing_no_counts_target = Counter(normalize(part["drawing_no"]) for part in target_parts)

    unmatched_standard_parts = []
    unmatched_target_parts = []

    for drawing_no, std_parts in standard_by_drg.items():
        tgt_parts = target_by_drg.get(drawing_no, [])

        # Simple case: One-to-one by drawing_no
        if len(std_parts) == 1 and len(tgt_parts) == 1:
            std = std_parts[0]
            tgt = tgt_parts[0]

            status = "match" if normalize(std["qty"]) == normalize(tgt["qty"]) else "qty_mismatch"
            result.append({
                "drawing_no": drawing_no,
                "status": status,
                "standard_qty": std["qty"],
                "target_qty": tgt["qty"],
                "description": std["description"]
            })

            matched_target_indices[drawing_no].add(0)
        else:
            # Push for more complex comparison later
            unmatched_standard_parts.extend(std_parts)
            unmatched_target_parts.extend([
                tgt for i, tgt in enumerate(tgt_parts)
                if i not in matched_target_indices[drawing_no]
            ])
    
    # Handle remaining parts with duplicate drawing numbers or fuzzy descriptions
    still_unmatched_standard = []
    # still_unmatched_target = unmatched_target_parts.copy()  # clone to track what's left
    # Rebuild unmatched targets list from actual unmatched items
    already_matched_targets = set()

    for drawing_no, indices in matched_target_indices.items():
        for i in indices:
            already_matched_targets.add(id(target_by_drg[drawing_no][i]))

    # Get all target parts that were never matched
    still_unmatched_target = [
        part for part in target_parts
        if id(part) not in already_matched_targets
    ]


    for std_part in unmatched_standard_parts:
        drawing_no = normalize(std_part["drawing_no"])
        std_desc = std_part["description"]
        std_desc_lower = normalize(std_desc)
        std_qty = normalize(std_part["qty"])

        tgt_candidates = target_by_drg.get(drawing_no, [])
        match_found = False

        # If multiple std_parts or force keyword, compare by description
        force_description_check = (
            drawing_no_counts_standard[drawing_no] > 1 or
            any(keyword in std_desc_lower for keyword in FORCE_DESC_MATCH_KEYWORDS)
        )

        for i, tgt_part in enumerate(tgt_candidates):
            if i in matched_target_indices[drawing_no]:
                continue

            tgt_desc = tgt_part["description"]
            tgt_desc_lower = normalize(tgt_desc)
            tgt_qty = normalize(tgt_part["qty"])

            if not force_description_check or std_desc_lower == tgt_desc_lower:
                status = "match" if std_qty == tgt_qty else "qty_mismatch"

                result.append({
                    "drawing_no": drawing_no,
                    "status": status,
                    "standard_qty": std_qty,
                    "target_qty": tgt_qty,
                    "description": std_desc
                })

                matched_target_indices[drawing_no].add(i)
                match_found = True

                # Remove this target from future replacement logic
                if tgt_part in still_unmatched_target:
                    still_unmatched_target.remove(tgt_part)

                break

        if not match_found:
            still_unmatched_standard.append(std_part)
    
    print(f"🔍 Total still_unmatched_standard: {len(still_unmatched_standard)}")
    print(f"🔍 Total still_unmatched_target: {len(still_unmatched_target)}")

    # Final fuzzy matching for possible replacements
    while still_unmatched_standard:
        std_part = still_unmatched_standard.pop(0)  # take first unmatched standard part
        std_desc = std_part["description"]
        std_qty = normalize(std_part["qty"])

        best_match = None
        best_score = 0

        # Compare std_part description with all unmatched target parts
        for tgt_part in still_unmatched_target:
            score = description_similarity(tgt_part["description"],std_desc)
            if score > best_score:
                best_score = score
                best_match = tgt_part
            
        print(f"Best fuzzy score for STD '{std_desc}': {best_score:.2f} → Match: {best_match['description'] if best_match else 'None'}")
        if best_score >= SIMILARITY_THRESHOLD:
            # Add replacement pair
            result.append({
                "drawing_no": std_part["drawing_no"],
                "status": "possibly_replaced_by",
                "standard_qty": std_qty,
                "target_qty": best_match["qty"],
                "description": std_desc,
                "replacement_candidate": {
                    "drawing_no": best_match["drawing_no"],
                    "description": best_match["description"]
                }
            })

            # Remove the matched target from unmatched targets as well
            still_unmatched_target.remove(best_match)

        else:
            # No good match → mark missing
            result.append({
                "drawing_no": std_part["drawing_no"],
                "status": "missing_in_target",
                "standard_qty": std_part["qty"],
                "target_qty": None,
                "description": std_desc
            })

    # After all standard parts handled, mark remaining targets as extra
    for tgt_part in still_unmatched_target:
        result.append({
            "drawing_no": tgt_part["drawing_no"],
            "status": "extra_in_target",
            "standard_qty": None,
            "target_qty": tgt_part["qty"],
            "description": tgt_part["description"]
        })

    return result