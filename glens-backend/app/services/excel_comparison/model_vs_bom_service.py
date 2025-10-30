# services/model_vs_bom_service.py
import pandas as pd
import io

class ModelVsBomService:

    def convert_model_excel_to_structured_json(self, file_bytes):
        df_raw = pd.read_excel(io.BytesIO(file_bytes), header=None)
        header_row_index = None

        for i, row in df_raw.iterrows():
            if "QTY" in row.astype(str).values:
                header_row_index = i
                break

        if header_row_index is None:
            raise ValueError("❌ Could not find header row with 'QTY'")

        headers = df_raw.iloc[header_row_index].astype(str).str.strip().tolist()
        df_data = df_raw.iloc[header_row_index + 1:].copy()
        df_data.columns = headers
        df_data = df_data.reset_index(drop=True)
        df_data = df_data.dropna(how='all')

        for col in df_data.columns:
            if pd.api.types.is_datetime64_any_dtype(df_data[col]):
                df_data[col] = df_data[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)

        df_data = df_data.where(pd.notnull(df_data), None)

        records = df_data.to_dict(orient='records')
        records = [{k: ("" if v is None else v) for k, v in record.items()} for record in records]
        return records

    def convert_ref_excel_to_structured_json(self, file_bytes):
        df_raw = pd.read_excel(io.BytesIO(file_bytes), header=None)
        header_row_index = None

        for i, row in df_raw.iterrows():
            if "Manufactured Item" in row.astype(str).values:
                header_row_index = i
                break

        if header_row_index is None:
            raise ValueError("❌ Could not find header row with 'Manufactured Item'")

        df = pd.read_excel(io.BytesIO(file_bytes), header=header_row_index)
        df = df.dropna(how='all')
        df.columns = df.columns.str.strip()

        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)

        records = df.to_dict(orient='records')
        return records

    def compare_boms(self, model_bytes, ref_bytes):
        model_bom = self.convert_model_excel_to_structured_json(model_bytes)
        ref_bom = self.convert_ref_excel_to_structured_json(ref_bytes)

        # === Your comparison logic exactly as before ===
        to_create_new = []
        empty_or_dash = []
        comparable = []

        for entry in model_bom:
            keyword = str(entry.get("KEYWORDS", "")).strip()
            if not keyword:
                keyword = str(entry.get("ITEM CODE", "")).strip()

            if keyword == "TO CREATE NEW":
                to_create_new.append(entry)
            elif keyword == "" or keyword == "-":
                empty_or_dash.append(entry)
            else:
                entry["KEYWORDS"] = keyword
                comparable.append(entry)

        ref_lookup = {}
        seen_ref_keywords = set()
        for entry in ref_bom:
            item_code = str(entry.get("Item", "")).strip()
            if item_code and item_code not in seen_ref_keywords:
                ref_lookup[item_code] = entry
                seen_ref_keywords.add(item_code)

        model_keywords = set(entry["KEYWORDS"].strip() for entry in comparable)
        ref_keywords = set(ref_lookup.keys())

        matched, missing, newly_added = [], [], []

        for entry in comparable:
            keyword = entry["KEYWORDS"].strip()
            ref_entry = ref_lookup.get(keyword)

            if ref_entry:
                field_comparison = {}
                fields = [
                    ("KEYWORDS", "Item"),
                    ("REVISION NUMBER", "Revision Number"),
                    ("DRG. NO. / DIMENSION", "Drawing Number"),
                    ("QTY", "Per Unit Quantity")
                ]

                match = True
                for model_field, ref_field in fields:
                    model_val = entry.get(model_field)
                    ref_val = ref_entry.get(ref_field)

                    model_val = model_val.strip() if isinstance(model_val, str) else model_val
                    ref_val = ref_val.strip() if isinstance(ref_val, str) else ref_val

                    if isinstance(model_val, (int, float)) and isinstance(ref_val, (int, float)):
                        same = float(model_val) == float(ref_val)
                    else:
                        model_val = "" if model_val is None else model_val
                        ref_val = "" if ref_val is None else ref_val
                        same = str(model_val).strip() == str(ref_val).strip()

                    if not same:
                        match = False

                    field_comparison[model_field] = {
                        "Model BOM": model_val,
                        "Ref BOM": ref_val,
                        "Match": same
                    }

                field_comparison["DESCRIPTION"] = {
                    "Model BOM": entry.get("DESCRIPTION"),
                    "Ref BOM": ref_entry.get("Item Description"),
                    "Match": None
                }

                matched.append({
                    "KEYWORDS": keyword,
                    "Comparison Status": "Match" if match else "Mismatch",
                    "Comparison Details": field_comparison
                })
            else:
                missing.append({
                    "KEYWORDS": keyword,
                    "Comparison Status": "Missing in Ref BOM",
                    "Comparison Details": {
                        "KEYWORDS": {"Model BOM": keyword, "Ref BOM": None, "Match": None},
                        "REVISION NUMBER": {"Model BOM": entry.get("REVISION NUMBER"), "Ref BOM": None, "Match": None},
                        "DRG. NO. / DIMENSION": {"Model BOM": entry.get("DRG. NO. / DIMENSION"), "Ref BOM": None, "Match": None},
                        "QTY": {"Model BOM": entry.get("QTY"), "Ref BOM": None, "Match": None},
                        "DESCRIPTION": {"Model BOM": entry.get("DESCRIPTION"), "Ref BOM": None, "Match": None}
                    }
                })

        unmatched_ref_keywords = ref_keywords - model_keywords
        for keyword in unmatched_ref_keywords:
            ref_entry = ref_lookup[keyword]
            newly_added.append({
                "KEYWORDS": keyword,
                "Comparison Status": "Newly Added in Ref BOM",
                "Comparison Details": {
                    "KEYWORDS": {"Model BOM": None, "Ref BOM": keyword, "Match": None},
                    "REVISION NUMBER": {"Model BOM": None, "Ref BOM": ref_entry.get("Revision Number"), "Match": None},
                    "DRG. NO. / DIMENSION": {"Model BOM": None, "Ref BOM": ref_entry.get("Drawing Number"), "Match": None},
                    "QTY": {"Model BOM": None, "Ref BOM": ref_entry.get("Per Unit Quantity"), "Match": None},
                    "DESCRIPTION": {"Model BOM": None, "Ref BOM": ref_entry.get("Item Description"), "Match": None}
                }
            })

        # Replacement check logic same as before
        potential_replacements, remaining_missing = [], []
        updated_newly_added = newly_added.copy()

        for miss in missing:
            miss_keyword = str(miss["KEYWORDS"])[:4].upper()
            miss_qty = miss["Comparison Details"]["QTY"]["Model BOM"]

            found_replacement = False
            for new in updated_newly_added:
                new_keyword = str(new["KEYWORDS"])[:4].upper()
                new_qty = new["Comparison Details"]["QTY"]["Ref BOM"]

                if miss_keyword == new_keyword and miss_qty == new_qty:
                    potential_replacements.append({
                        "KEYWORDS": miss["KEYWORDS"],
                        "Comparison Status": "Potential Replacement",
                        "Comparison Details": {
                            "KEYWORDS": {"Model BOM": miss["KEYWORDS"], "Ref BOM": new["KEYWORDS"], "Match": None},
                            "REVISION NUMBER": {"Model BOM": miss["Comparison Details"]["REVISION NUMBER"]["Model BOM"], "Ref BOM": new["Comparison Details"]["REVISION NUMBER"]["Ref BOM"], "Match": None},
                            "DRG. NO. / DIMENSION": {"Model BOM": miss["Comparison Details"]["DRG. NO. / DIMENSION"]["Model BOM"], "Ref BOM": new["Comparison Details"]["DRG. NO. / DIMENSION"]["Ref BOM"], "Match": None},
                            "QTY": {"Model BOM": miss["Comparison Details"]["QTY"]["Model BOM"], "Ref BOM": new["Comparison Details"]["QTY"]["Ref BOM"], "Match": None},
                            "DESCRIPTION": {"Model BOM": miss["Comparison Details"]["DESCRIPTION"]["Model BOM"], "Ref BOM": new["Comparison Details"]["DESCRIPTION"]["Ref BOM"], "Match": None}
                        }
                    })
                    updated_newly_added.remove(new)
                    found_replacement = True
                    break

            if not found_replacement:
                remaining_missing.append(miss)

        final_result = {
            "TO CREATE NEW": to_create_new,
            "MATCHED": matched,
            "POTENTIAL REPLACEMENTS": potential_replacements,
            "UNMATCHED / MISSING": remaining_missing,
            "NEWLY ADDED": newly_added,
            "EMPTY OR DASHED": empty_or_dash
        }

        return final_result
