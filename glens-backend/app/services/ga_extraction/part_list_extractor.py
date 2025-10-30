import re

def normalize(text):
    return re.sub(r'\s+', ' ', text or '').strip().lower()

def normalize_parts(merged_parts):
    normalized = []

    for item in merged_parts:
        part_nos = item['part_no'].split('\n')
        qtys = item['qty'].split('\n')
        descriptions = item['description'].split('\n')
        drawing_nos = item['drawing_no'].split('\n')

        count = max(len(part_nos), len(qtys), len(descriptions), len(drawing_nos))

        for i in range(count):
            part_no = part_nos[i].strip() if i < len(part_nos) else ''
            qty = qtys[i].strip() if i < len(qtys) else ''
            description = descriptions[i].strip() if i < len(descriptions) else ''
            drawing_no = drawing_nos[i].strip() if i < len(drawing_nos) else ''

            # ❌ Skip the row if any field is empty
            if not all([part_no, qty, description, drawing_no]):
                continue

            normalized.append({
                'part_no': part_no,
                'qty': qty,
                'description': description,
                'drawing_no': drawing_no
            })

    return normalized

def find_part_list_header(rows):
    """Find the header row for the part list table."""
    keywords = ['part no', 'qty', 'description', 'drg. no', 'dimension']
    for i, row in enumerate(rows):
        columns = {k: normalize(v) for k, v in row.items()}
        match_count = sum(any(kw in val for kw in keywords) for val in columns.values())
        if match_count >= 3:
            return i, columns
    return None, None

def map_columns(header_row):
    """Map normalized column headers to expected keys."""
    header_map = {}
    for col, text in header_row.items():
        text = normalize(text)
        if 'part no' in text:
            header_map.setdefault('part_no', []).append(col)
        elif 'qty' in text:
            header_map.setdefault('qty', []).append(col)
        elif 'description' in text:
            header_map.setdefault('description', []).append(col)
        elif 'drg' in text or 'dimension' in text:
            header_map.setdefault('drawing_no', []).append(col)
    return header_map

def extract_part_list(raw_data, max_empty_rows=20):

    header_idx, header_row = find_part_list_header(raw_data)

    if not header_row:
        print("No part list found.")
        return []

    column_map = map_columns(header_row)
    part_list = []
    empty_row_count = 0

    for row in raw_data[header_idx + 1:]:
        has_data = False

        for i in range(len(column_map.get('part_no', []))):
            part_no = row.get(column_map['part_no'][i], "").strip()
            if not part_no:
                continue

            has_data = True
            drawing_no_raw = row.get(column_map['drawing_no'][i], "").strip()
            drawing_no_cleaned = re.split(r'\bratio\b', drawing_no_raw, flags=re.IGNORECASE)[0].strip()
            part_entry = {
                "part_no": part_no,
                "qty": row.get(column_map['qty'][i], "").strip(),
                "description": row.get(column_map['description'][i], "").replace('\n', ' ').strip(),
                "drawing_no": drawing_no_cleaned
            }
            part_list.append(part_entry)

        if not has_data:
            empty_row_count += 1
            if empty_row_count >= max_empty_rows:
                break
        else:
            empty_row_count = 0

    return normalize_parts(part_list)