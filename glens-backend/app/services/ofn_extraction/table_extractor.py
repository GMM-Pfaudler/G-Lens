import fitz  # PyMuPDF
import pandas as pd

def find_column_for_keyword(df, keyword):
    """Find the column that contains the given keyword either in header or cells."""
    for col in df.columns:
        if keyword.lower() in str(col).lower():
            return col
    for col in df.columns:
        for val in df[col]:
            if pd.isna(val):
                continue
            if keyword.lower() in str(val).lower():
                return col
    return None

def extract_data_from_column(df, column):
    """Extract all non-null data from the specified column."""
    return df[column].dropna().tolist()

def extract_nozzles_and_agitator_from_pdf(pdf_path, keyword_groups):
    doc = fitz.open(pdf_path)
    results = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        tables = page.find_tables()
        # print(f"Found {len(tables.tables)} tables on page {page_num + 1}.")

        if not tables or len(tables.tables) == 0:
            # print(f"No tables found on page {page_num + 1}.")
            continue

        for idx, table in enumerate(tables.tables):
            df = table.to_pandas()
            # df = df.applymap(lambda x: str(x).strip() if pd.notna(x) else "")
            df = df.map(lambda x: str(x).strip() if pd.notna(x) else "")
            # print(f"Columns in table {idx + 1} on page {page_num + 1}: {df.columns}")

            if df.empty:
                # print(f"Table {idx + 1} on page {page_num + 1} is empty.")
                continue

            # ----- Nozzles Extraction -----
            nozzles_columns = []
            for keyword in keyword_groups["nozzles"]:
                col = find_column_for_keyword(df, keyword)
                if col:
                    nozzles_columns.append(col)

            if len(nozzles_columns) >= 2:
                nozzles_details = []
                filtered_df = pd.DataFrame()
                try:
                    filtered_df = df[df[nozzles_columns[0]].str.contains('Nozzle', case=False, na=False) &
                                 df[nozzles_columns[1]].str.contains('Size', case=False, na=False)]
                except:
                    pass

                if not filtered_df.empty:
                    starting_index_nozzles = filtered_df.index[0] + 1
                    for index, row in df.loc[starting_index_nozzles:, nozzles_columns].iterrows():
                        if row[nozzles_columns[0]] and row[nozzles_columns[1]]:
                            temp = {
                                "No.": row[nozzles_columns[0]],
                                "Size": row[nozzles_columns[1]],
                                "Service": row[nozzles_columns[2]] if len(nozzles_columns) > 2 else None,
                                "Location": row[nozzles_columns[3]] if len(nozzles_columns) > 3 else None,
                                "Description": row[nozzles_columns[4]] if len(nozzles_columns) > 4 else None
                            }
                            nozzles_details.append(temp)
                else:
                    header_matched = any("nozzle" in col.lower() for col in nozzles_columns) and \
                    any("size" in col.lower() for col in nozzles_columns)

                    if header_matched:
                        for _, row in df[nozzles_columns].iterrows():
                            if row[nozzles_columns[0]] and row[nozzles_columns[1]]:
                                temp = {
                                    "No.": row[nozzles_columns[0]],
                                    "Size": row[nozzles_columns[1]],
                                    "Service": row[nozzles_columns[2]] if len(nozzles_columns) > 2 else None,
                                    "Location": row[nozzles_columns[3]] if len(nozzles_columns) > 3 else None,
                                    "Description": row[nozzles_columns[4]] if len(nozzles_columns) > 4 else None
                                }
                                nozzles_details.append(temp)

                if nozzles_details:
                    results.append({"section": "nozzles", "nozzles_details": nozzles_details})
            # ----- Agitator Header Detection -----
            agitator_header_row = None
            for idx2, row in df.iterrows():
                row_vals = [str(v).strip().lower() for v in row if pd.notna(v)]
                if any("type" in v for v in row_vals) and any("sweep" in v for v in row_vals):
                    agitator_header_row = idx2
                    break

            if agitator_header_row is not None:
                new_header = df.iloc[agitator_header_row].tolist()
                df = df.iloc[agitator_header_row + 1:]
                df.columns = new_header
                df.reset_index(drop=True, inplace=True)

            # ----- Agitator Extraction -----
            agitator_columns = [
                col for col in df.columns
                if any(k in str(col).lower() for k in ["type", "sweep"])
            ]

            if len(agitator_columns) >= 2:
                agitator_details = []
                try:
                    for _, row in df[agitator_columns].iterrows():
                        type_val = str(row[agitator_columns[0]]).strip()
                        sweep_val = str(row[agitator_columns[1]]).strip()
                        type_val_upper = type_val.upper()
                        if not type_val or type_val_upper in {"M", "L"}:
                            continue
                        if type_val.startswith("N") and type_val[1:].isdigit():
                            continue
                        if "nozzle" in type_val.lower() or "service" in type_val.lower():
                            continue
                        if "sweep diameter" in sweep_val.lower():
                            continue

                        agitator_details.append({
                            "agitator_type": type_val,
                            "agitator_sweep_dia": sweep_val
                        })

                    if agitator_details:
                        unique_agitators = [dict(t) for t in {tuple(d.items()) for d in agitator_details}]
                        results.append({"section": "agitator", "agitator_details": unique_agitators})
                except Exception as e:
                    # print(f"Error extracting agitator (strict logic): {e}")
                    print()

            elif len(agitator_columns) == 1:
                single_col = agitator_columns[0]
                fallback_details = []
                try:
                    for _, row in df.iterrows():
                        val_raw = str(row[single_col])
                        val = val_raw.strip()
                        val_upper = val.upper()

                        if not val:
                            continue
                        if val_upper in {"M", "L"}:
                            continue
                        if val_upper.startswith("N") and val_upper[1:].isdigit():
                            continue
                        if any(bad in val.lower() for bad in [
                            "motor", "rpm", "shaft", "gear box", "top head",
                            "flight", "jacket", "cladding", "nozzle", "service"
                        ]):
                            continue

                        fallback_details.append({
                            "agitator_type": val if "type" in single_col.lower() else None,
                            "agitator_sweep_dia": val if "sweep" in single_col.lower() else None
                        })

                    if fallback_details:
                        unique_fallback = [dict(t) for t in {tuple(d.items()) for d in fallback_details}]
                        results.append({"section": "agitator_fallback", "agitator_details": unique_fallback})
                except Exception as e:
                    # print(f"Error extracting agitator (fallback logic): {e}")
                    print()
            else:
                # print(f"No matching agitator header found on page {page_num + 1}.")
                print()

    return results
