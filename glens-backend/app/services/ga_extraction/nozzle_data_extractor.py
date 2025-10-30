from rapidfuzz import fuzz
import re

def normalize(text):
    """Normalize text by trimming whitespace, converting to lowercase, and removing special characters."""
    return re.sub(r'\s+', ' ', text or '').strip().lower()

def is_valid_ref(value):
    if not value:
        return False
    
    tokens = value.strip().split()
    token_pattern = re.compile(r'^[A-Za-z][A-Za-z0-9]{0,4}$')

    for token in tokens:
        if not token_pattern.match(token):
            return False
    return True

def find_headers(data, threshold=80):
    """Find headers in the extracted data with fuzzy matching for simplified header keywords."""
    
    # Simplified target header keywords
    target_keywords = {
        "ref.": "Ref.",
        "size(dn)": "Size (DN)",
        "dn": "Size (DN)",  # Match both "dn" and "size(dn)"
        "rating": "Rating",
        "service": "Service",
        "fittings": "Fittings"
    }

    headers_mapping = {}

    # Iterate through the rows of the extracted data
    for row in data:
        found_labels = {}

        for index, value in row.items():
            value_clean = normalize(value)

            # Loop through the target keywords and check for matches using fuzzy matching
            for keyword, final_name in target_keywords.items():
                # Perform fuzzy matching
                score = fuzz.ratio(value_clean, normalize(keyword))
                
                # Match even if score is close but not exact
                if score >= threshold:
                    found_labels[final_name] = index
                    # print(f"Matched: '{value_clean}' → '{final_name}' with score: {score}")
                    break  # Stop once the best match is found

        # If all target headers are found, update the mapping and break
        if len(found_labels) >= 5:  # Check if we found at least 5 headers
            headers_mapping.update(found_labels)
            # print(f"Headers Mapping Updated: {headers_mapping}")
            break  # Only update if all target headers are matched

    return headers_mapping

def expand_multiline_rows(data):
    expanded_data = []

    for row in data:
        # Collect only non-empty values
        non_empty_values = [str(value).split("\n") for value in row.values() if value and str(value).strip()]
        
        if not non_empty_values:
            continue  # Skip fully empty row

        # Find the max number of lines
        max_lines = max(len(lines) for lines in non_empty_values)

        # Initialize a list of empty row dicts
        split_rows = [{} for _ in range(max_lines)]

        for key, value in row.items():
            lines = str(value).split("\n") if value else []
            for i in range(max_lines):
                split_rows[i][key] = lines[i].strip() if i < len(lines) else ""

        expanded_data.extend(split_rows)

    return expanded_data

def process_extracted_data(data):
    data = expand_multiline_rows(data)  # Preprocess to expand multiline rows
    
    headers_mapping = find_headers(data)

    if not headers_mapping or len(headers_mapping) < 5:
        raise ValueError("Could not find all necessary headers.")

    processed_data = []

    for row in data:
        nozzle_code = row.get(headers_mapping.get("Ref."), "").strip()
        size_dn = row.get(headers_mapping.get("Size (DN)"), "").strip()
        rating = row.get(headers_mapping.get("Rating"), "").strip()
        service = row.get(headers_mapping.get("Service"), "").strip()
        fittings = row.get(headers_mapping.get("Fittings"), "").strip()

        stop_terms = {
            "table of connections", "so. no.", "qnty.",
            "item code", "prepared by", "checked by", "approved by"
        }
        if normalize(nozzle_code) in stop_terms:
            break

        if not is_valid_ref(nozzle_code):
            continue

        if not size_dn:
            continue

        if any([nozzle_code, size_dn, rating, service, fittings]):
            processed_data.append({
                "Ref.": nozzle_code,
                "Size (DN)": size_dn,
                "Rating": rating,
                "Service": service,
                "Fittings": fittings
            })

    return processed_data