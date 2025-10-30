import pandas as pd

def convert_excel_to_structured_json(excel_path):
    
    df_raw = pd.read_excel(excel_path, header=None)

    header_row_index = None
    for i,row in df_raw.iterrows():
        if "Manufactured Item" in row.astype(str).values:
            header_row_index = i
            break

    if header_row_index is None:
        raise ValueError("Could not find header row with 'Manufactured Item'")

    df = pd.read_excel(excel_path,header=header_row_index)

    # df = df[df.index > header_row_index]

    df = df.dropna(how='all')

    df.columns = df.columns.str.strip()

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
    
    original_row_count = len(df)
    records = df.to_dict(orient='records')
    json_record_count = len(records)

    print(f"✅ Excel data rows: {original_row_count}")
    print(f"✅ JSON records generated: {json_record_count}")

    if original_row_count != json_record_count:
        print("⚠️ Warning: Row count mismatch!")

    return records

def filter_by_bom_level(records, bom_level):
    filtered_records = [
        record for record in records
        if str(record.get("BOM Level","").strip()) == str(bom_level)
    ]

    print(f"Found {len(filtered_records)} records with BOM Level = {bom_level}")
    return filtered_records