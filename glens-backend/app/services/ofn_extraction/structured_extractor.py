import fitz  # PyMuPDF
import json
import os
import re

def is_bold(span):
    return span['flags'] == 20 or "Bold" in span['font']

def extract_bold_lines_with_indent(page):
    lines = []
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            line_text = ""
            is_line_bold = True
            min_x0 = None
            for span in line["spans"]:
                text = span["text"].strip()
                if not text:
                    continue
                if not is_bold(span):
                    is_line_bold = False
                line_text += text + " "
                if min_x0 is None or span["bbox"][0] < min_x0:
                    min_x0 = span["bbox"][0]
            line_text = line_text.strip()
            if line_text:
                lines.append((line_text, is_line_bold, min_x0 or 0))
    return lines

def assign_nested_value(nested_dict, stack, value):
    d = nested_dict
    for key in stack[:-1]:
        if key not in d or not isinstance(d[key], dict):
            d[key] = {}
        d = d[key]
    d[stack[-1]] = value

def merge_broken_keys_recursive(data: dict) -> dict:
    if not isinstance(data, dict):
        return data
    keys = list(data.keys())
    i = 0
    merged = {}
    while i < len(keys):
        key = keys[i]
        value = data[key]
        if (value is None or value == {}) and i + 1 < len(keys):
            next_key = keys[i + 1]
            next_value = data[next_key]
            combined_key = f"{key} {next_key}"
            merged[combined_key] = merge_broken_keys_recursive(next_value)
            i += 2
        else:
            merged[key] = merge_broken_keys_recursive(value)
            i += 1
    return merged

POLICY_REGEX = re.compile(
    r"This document is confidential.*?Thank you for your cooperation\.?",
    re.DOTALL | re.IGNORECASE
)

def extract_policy_text(page):
    text = page.get_text("text")
    match = POLICY_REGEX.search(text)
    return match.group(0) if match else None

def clean_nozzle_section(nozzle_section):
    if "Top Head" in nozzle_section:
        del nozzle_section["Top Head"]
    return nozzle_section

def remove_nozzle_data(nested_dict):
    if "Nozzles" in nested_dict:
        nested_dict["Nozzles"] = clean_nozzle_section(nested_dict["Nozzles"])
    return nested_dict

def clean_agitator_section(agitator_section):
    if not isinstance(agitator_section, dict):
        return agitator_section

    # If Type is the only key, keep it — likely not a table
    if list(agitator_section.keys()) == ["Type"]:
        return agitator_section

    # Heuristic: If Type is present but there's also "Flight" or other known keys, remove it
    known_keys = {"Flight", "RPM", "KW", "Motor", "Mounting", "Speed"}
    if "Type" in agitator_section:
        other_keys = set(agitator_section.keys()) - {"Type"}
        if other_keys & known_keys:
            del agitator_section["Type"]

    return agitator_section

def remove_agitator_section(nested_dict):
    if "Agitator" in nested_dict:
        nested_dict["Agitator"] = clean_agitator_section(nested_dict["Agitator"])
    return nested_dict

def clean_accessories_section(accessories_section):
    if not isinstance(accessories_section, str):
        return accessories_section
    # Use re.sub directly with the compiled pattern without passing flags
    cleaned = re.sub(POLICY_REGEX, "", accessories_section)
    return cleaned

def clean_page_references_in_dict(d):
        """
        Recursively remove 'page x' or 'page x of y' (case-insensitive)
        from all string values in a nested dictionary or list.
        """
        if isinstance(d, dict):
            return {k: clean_page_references_in_dict(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [clean_page_references_in_dict(item) for item in d]
        elif isinstance(d, str):
            return re.sub(r"\bpage\s+\d+(\s+of\s+\d+)?\b.*", "", d, flags=re.IGNORECASE).strip()
        else:
            return d
        
def remove_policy_text_from_accessories(nested_dict):
    if "Accessories" in nested_dict:
        nested_dict["Accessories"] = clean_accessories_section(nested_dict["Accessories"])
    return nested_dict

def parse_pdf_to_nested_indent(pdf_path, output_path="output/final_output.json"):
    doc = fitz.open(pdf_path)

    nested_dict = {}
    stack = []
    indent_stack = []
    assigned_keys = set()
    policy_text = None
    shaft_closure_type = None

    for page_num in range(1, len(doc)):
        page = doc[page_num]
        lines = extract_bold_lines_with_indent(page)
        non_bold_buffer = []

        # Extract policy text from the last page
        if page_num == len(doc) - 1:
            policy_text = extract_policy_text(page)

        i = 0
        while i < len(lines):
            text, is_line_bold, x0 = lines[i]

            if is_line_bold:
                # Special case for "Shaft Closure"
                if text.strip() == "Shaft Closure":
                    if i + 1 < len(lines):
                        next_text, next_is_bold, _ = lines[i + 1]
                        if not next_is_bold:
                            shaft_closure_type = next_text.strip()
                            i += 1

                # Skip agitator "Type" table section
                if text.strip() == "Type" and stack[-2:] == ["Agitator", "Flight"]:
                    i += 1
                    continue

                # Assign non-bold buffer to previous bold key
                if non_bold_buffer and stack:
                    joined_text = " ".join(non_bold_buffer).strip()

                    # Special case: assigning "Double" or similar to "Flight"
                    known_flight_values = {"Double", "Triple", "Single", "Anchor", "PBT", "Blade", "Propeller", "Turbine", "Helical", "Gate", "Ribbon", "Hydrofoil", "Pitched Blade", "Magnetic", "Rushton"}

                    if stack[-1] == "Flight" and joined_text:
                        match = re.match(r"^(Double|Triple|Single|Anchor(?:\s*\+\s*PBT)?|PBT|Blade|Propeller|Turbine|Helical|Gate|Ribbon|Hydrofoil|Pitched\s*Blade|Magnetic|Rushton)\b", joined_text, re.IGNORECASE)
                        if match:
                            assign_nested_value(nested_dict, stack, match.group(1))
                            assigned_keys.add("Flight")
                    elif "Sweep Diameter" not in joined_text:
                        if joined_text:
                            assign_nested_value(nested_dict, stack, joined_text)
                            assigned_keys.add(stack[-1])

                    non_bold_buffer = []

                if stack and stack[-1] not in assigned_keys:
                    assign_nested_value(nested_dict, stack, None)
                    assigned_keys.add(stack[-1])

                while indent_stack and x0 <= indent_stack[-1]:
                    indent_stack.pop()
                    stack.pop()

                if text.strip() == "Shaft Closure":
                    while stack and stack[-1] not in ("Drive", "Motor"):
                        stack.pop()
                        indent_stack.pop()
                    if stack and stack[-1] == "Motor":
                        stack.pop()
                        indent_stack.pop()
                    stack.append("Shaft Closure")
                else:
                    stack.append(text)

                indent_stack.append(x0)

            else:
                non_bold_buffer.append(text)

            i += 1

        if non_bold_buffer and stack:
            joined_text = " ".join(non_bold_buffer).strip()

            # Handle known agitator flight values at page breaks
            known_flight_values = {"Double", "Triple", "Single", "Anchor", "PBT", "Blade", "Propeller", "Turbine", "Helical", "Gate", "Ribbon", "Hydrofoil", "Pitched Blade", "Magnetic", "Rushton"}

            if stack[-1] == "Flight" and joined_text:
                match = re.match(r"^(Double|Triple|Single|Anchor(?:\s*\+\s*PBT)?|PBT|Blade|Propeller|Turbine|Helical|Gate|Ribbon|Hydrofoil|Pitched\s*Blade|Magnetic|Rushton)\b", joined_text, re.IGNORECASE)
                if match:
                    assign_nested_value(nested_dict, stack, match.group(1))
                    assigned_keys.add("Flight")
            elif "Sweep Diameter" not in joined_text:
                if joined_text:
                    assign_nested_value(nested_dict, stack, joined_text)
                    assigned_keys.add(stack[-1])

        if stack and stack[-1] not in assigned_keys:
            assign_nested_value(nested_dict, stack, None)

    nested_dict = merge_broken_keys_recursive(nested_dict)

    if "Agitator" in nested_dict:
        nested_dict["Agitator"] = clean_agitator_section(nested_dict["Agitator"])
        if "Flight" in nested_dict["Agitator"]:
            val = nested_dict["Agitator"]["Flight"]
            if isinstance(val, str):
                match = re.match(
                    r"^(Double|Triple|Single|Anchor(?:\s*\+\s*PBT)?|PBT|Blade|Propeller|Turbine|Helical|Gate|Ribbon|Hydrofoil|Pitched\s*Blade|Magnetic|Rushton)\b",
                    val, re.IGNORECASE)
                nested_dict["Agitator"]["Flight"] = match.group(1) if match else val
            elif val is None:
                nested_dict["Agitator"]["Flight"] = None  # explicitly keep the key

    if "Model" in nested_dict:
        rev_match = re.search(r"\bRev\.?\s*(\d+)\b", nested_dict["Model"], re.IGNORECASE)
        if rev_match:
            nested_dict["Rev."] = rev_match.group(1)
            nested_dict["Model"] = re.sub(r"\bRev\.?\s*\d+\b", "", nested_dict["Model"], flags=re.IGNORECASE).strip()

    if shaft_closure_type:
        try:
            drive = nested_dict["Drive"] if isinstance(nested_dict.get("Drive"), dict) else {}
            shaft = drive.get("Shaft Closure", {})
            if isinstance(shaft, dict):
                shaft["Type"] = shaft_closure_type
            else:
                shaft = {"Type": shaft_closure_type}
            drive["Shaft Closure"] = shaft
            nested_dict["Drive"] = drive
        except Exception as e:
            print(f" Could not assign Shaft Closure Type safely: {e}")

    nested_dict = remove_nozzle_data(nested_dict)
    nested_dict = remove_policy_text_from_accessories(nested_dict)

    if policy_text:
        nested_dict["Policy"] = policy_text.strip()
    
    try:
        moc = nested_dict.get("Material of Construction", {})
        if isinstance(moc, dict):
            sba_val = moc.get("Spring Balance Assembly")
            if isinstance(sba_val, str):
                # Remove from 'page' onwards (case-insensitive)
                # Only remove if it's like "page 2" or "page 2 of 4"
                cleaned_val = re.sub(r"\bpage\s+\d+(\s+of\s+\d+)?\b.*", "", sba_val, flags=re.IGNORECASE).strip()
                nested_dict["Material of Construction"]["Spring Balance Assembly"] = cleaned_val
    except Exception as e:
        print(f"Could not clean Spring Balance Assembly value: {e}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nested_dict, f, indent=2, ensure_ascii=False)

    # print(f"Final output saved to: {output_path}")
