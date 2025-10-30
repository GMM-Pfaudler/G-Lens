from collections import Counter

def normalize(value):
    if value is None:
        return ''
    return str(value).strip()

def compare_fields(record_a, record_b, fields):
    result = {}
    for field in fields:
        val_a = normalize(record_a.get(field))
        val_b = normalize(record_b.get(field))
        result[field] = {
            'file_a': val_a,
            'file_b': val_b,
            'match': val_a == val_b
        }
    return result

def compare_unique_items(records_a, records_b, fields):
    results = []

    # Normalize Item field
    for rec in records_a + records_b:
        if 'Item' in rec:
            rec['Item'] = rec['Item'].strip()

    # Count frequency of Items
    freq_a = Counter([rec['Item'] for rec in records_a])
    freq_b = Counter([rec['Item'] for rec in records_b])

    # Filter only truly unique records
    dict_a = {rec['Item']: rec for rec in records_a if freq_a[rec['Item']] == 1}
    dict_b = {rec['Item']: rec for rec in records_b if freq_b[rec['Item']] == 1}

    unique_in_both = set(dict_a.keys()) & set(dict_b.keys())
    unique_only_in_a = set(dict_a.keys()) - unique_in_both
    unique_only_in_b = set(dict_b.keys()) - unique_in_both

    # 1. Compare matched unique items
    for item in unique_in_both:
        rec_a = dict_a[item]
        rec_b = dict_b[item]
        comparison = compare_fields(rec_a, rec_b, fields)
        all_matched = all(info['match'] for info in comparison.values())

        results.append({
            'Item': item,
            'Status': 'Unchanged' if all_matched else 'Modified',
            'Comparison': comparison
        })

    # 2. Check for replacements
    replacements = []
    used_b = set()
    used_a = set()

    for item_a in unique_only_in_a:
        rec_a = dict_a[item_a]
        prefix_a = item_a[:4]
        qty_a = normalize(rec_a.get("Net Quantity"))

        # Candidates in B with matching prefix and not used yet
        candidates = [
            item_b for item_b in unique_only_in_b - used_b
            if item_b[:4] == prefix_a
        ]

        if len(candidates) == 1:
            # Safe replacement
            item_b = candidates[0]
            rec_b = dict_b[item_b]
            comparison = compare_fields(rec_a, rec_b, fields)
            replacements.append({
                'Item (A)': item_a,
                'Item (B)': item_b,
                'Status': 'Potential Replacement',
                'Comparison': comparison
            })
            used_a.add(item_a)
            used_b.add(item_b)

        elif len(candidates) > 1:
            # Try Net Quantity match
            qty_matches = [
                item_b for item_b in candidates
                if normalize(dict_b[item_b].get("Net Quantity")) == qty_a
            ]

            if len(qty_matches) == 1:
                item_b = qty_matches[0]
                rec_b = dict_b[item_b]
                comparison = compare_fields(rec_a, rec_b, fields)
                replacements.append({
                    'Item (A)': item_a,
                    'Item (B)': item_b,
                    'Status': 'Potential Replacement',
                    'Comparison': comparison
                })
                used_a.add(item_a)
                used_b.add(item_b)

            elif len(qty_matches) == 0:
                # Fallback: use first prefix match
                item_b = candidates[0]
                rec_b = dict_b[item_b]
                comparison = compare_fields(rec_a, rec_b, fields)
                replacements.append({
                    'Item (A)': item_a,
                    'Item (B)': item_b,
                    'Status': 'Potential Replacement',
                    'Comparison': comparison
                })
                used_a.add(item_a)
                used_b.add(item_b)

    # 3. Remaining Missing in B
    for item in unique_only_in_a - used_a:
        rec_a = dict_a[item]
        comparison = {
            field: {
                'file_a': normalize(rec_a.get(field)),
                'file_b': None,
                'match': False
            }
            for field in fields
        }
        results.append({
            'Item': item,
            'Status': 'Missing in File B',
            'Comparison': comparison
        })

    # 4. Remaining New in B
    for item in unique_only_in_b - used_b:
        rec_b = dict_b[item]
        comparison = {
            field: {
                'file_a': None,
                'file_b': normalize(rec_b.get(field)),
                'match': False
            }
            for field in fields
        }
        results.append({
            'Item': item,
            'Status': 'New in File B',
            'Comparison': comparison
        })

    results.extend(replacements)

    return results

def compare_duplicate_items(records_a, records_b, fields):
    results = []

    # Normalize 'Item' and 'Net Quantity' fields
    for rec in records_a + records_b:
        if 'Item' in rec:
            rec['Item'] = rec['Item'].strip()
        if 'Net Quantity' in rec:
            rec['Net Quantity'] = normalize(rec['Net Quantity'])

    # Count Item frequency
    freq_a = Counter([rec['Item'] for rec in records_a])
    freq_b = Counter([rec['Item'] for rec in records_b])

    # Identify duplicates
    duplicate_items = {item for item in set(freq_a) | set(freq_b)
                       if freq_a.get(item, 0) > 1 or freq_b.get(item, 0) > 1}

    # Build lookup using (Item, Net Quantity) as key
    map_a = {
        (rec['Item'], rec['Net Quantity']): rec
        for rec in records_a if rec['Item'] in duplicate_items
    }

    map_b = {
        (rec['Item'], rec['Net Quantity']): rec
        for rec in records_b if rec['Item'] in duplicate_items
    }

    all_keys = set(map_a) | set(map_b)

    for key in all_keys:
        item, quantity = key
        rec_a = map_a.get(key)
        rec_b = map_b.get(key)

        if rec_a and rec_b:
            comparison = compare_fields(rec_a, rec_b, fields)
            all_matched = all(info['match'] for info in comparison.values())
            results.append({
                'Item': item,
                'Net Quantity': quantity,
                'Composite Key': f"{item} | {quantity}",
                'Status': 'Unchanged' if all_matched else 'Modified',
                'Comparison': comparison
            })
        elif rec_a and not rec_b:
            comparison = {
                field: {
                    'file_a': normalize(rec_a.get(field)),
                    'file_b': None,
                    'match': False
                }
                for field in fields
            }
            results.append({
                'Item': item,
                'Net Quantity': quantity,
                'Composite Key': f"{item} | {quantity}",
                'Status': 'Missing in File B',
                'Comparison': comparison
            })
        elif rec_b and not rec_a:
            comparison = {
                field: {
                    'file_a': None,
                    'file_b': normalize(rec_b.get(field)),
                    'match': False
                }
                for field in fields
            }
            results.append({
                'Item': item,
                'Net Quantity': quantity,
                'Composite Key': f"{item} | {quantity}",
                'Status': 'New in File B',
                'Comparison': comparison
            })

    return results

def compare_all_items(records_a, records_b, fields_to_compare):
    unique_results = compare_unique_items(records_a, records_b, fields_to_compare)
    duplicate_results = compare_duplicate_items(records_a, records_b, fields_to_compare)

    all_results = unique_results + duplicate_results

    # Group by status
    status_priority = {
        'Modified': 0,
        'Unchanged': 1,
        'Potential Replacement':2,
        'Missing in File B': 3,
        'New in File B': 4
    }

    grouped_results = sorted(all_results, key=lambda x: status_priority.get(x['Status'], 99))

    return grouped_results
