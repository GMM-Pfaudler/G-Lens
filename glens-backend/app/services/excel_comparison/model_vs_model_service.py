import pandas as pd
import io


def compare_records(model_a_bytes,model_b_bytes):
    try:
        fields_to_compare = ['PART NO.', 'QTY', 'DESCRIPTION', 'DRG. NO. / DIMENSION','REVISION NUMBER', 'KEYWORDS', 'MATERIAL']
        model_a = extract_excel_to_json(model_a_bytes, fields_to_compare)
        model_b = extract_excel_to_json(model_b_bytes,fields_to_compare)

        to_create_new = []
        empty_or_dash = []
        model_a_lookup = {}
        
        for entry in model_a:
            keyword = str(entry.get("KEYWORDS","")).strip()
            description = str(entry.get("DESCRIPTION","")).strip()
            # if not keyword: keyword = str(entry.get("ITEM CODE", "")).strip()
            if keyword == "TO CREATE NEW": to_create_new.append(entry)
            elif keyword == "" or keyword =="-": empty_or_dash.append(entry)
            else:
                entry["KEYWORDS"] = keyword
                entry["DESCRIPTION"] = description
                model_a_lookup[(keyword,description)]=entry
        
        model_b_lookup = {}
        for entry in model_b:
            keyword = str(entry.get("KEYWORDS","")).strip()
            description = str(entry.get("DESCRIPTION","")).strip()
            # if not keyword: keyword = str(entry.get("ITEM CODE", "")).strip()
            if keyword == "TO CREATE NEW": to_create_new.append(entry)
            elif keyword == "" or keyword =="-": empty_or_dash.append(entry)
            else:
                entry["KEYWORDS"] = keyword
                entry["DESCRIPTION"] = description
                model_b_lookup[(keyword,description)]=entry

        comparable_kwd = set((entry["KEYWORDS"].strip(),entry["DESCRIPTION"].strip()) for lookup in [model_a_lookup, model_b_lookup] for entry in lookup.values())
        matched, missing, newly_added = [], [], []

        for keyword,description in comparable_kwd:
            model_a_entry = model_a_lookup.get((keyword,description))
            model_b_entry = model_b_lookup.get((keyword,description))

            if model_a_entry and model_b_entry:
                field_comparison={}
                
                match=True
                for field in fields_to_compare:
                    val_ma = model_a_entry[field]
                    val_mb = model_b_entry[field]

                    val_ma = val_ma.strip() if isinstance(val_ma,str) else val_ma
                    val_mb = val_mb.strip() if isinstance(val_mb,str) else val_mb

                    if isinstance(val_ma,(int,float)) and isinstance(val_mb,(int,float)): same = float(val_ma) == float(val_mb)
                    else:
                        val_ma = "" if val_ma is None else val_ma
                        val_mb = "" if val_mb is None else val_mb
                        same = str(val_ma).strip() == str(val_mb).strip()
                    
                    if not same:
                        match = False

                    field_comparison[field]={
                        "Model A BOM" : val_ma,
                        "Model B BOM" : val_mb,
                        "Match" : same 
                    }
                mismatched_fields = [
                    field for field, values in field_comparison.items() if values.get("Match") is False
                ]

                matched.append({
                    "KEYWORDS": keyword,
                    "Comparison Status" : "Match" if match else "Mismatch",
                    "Comparison Details" : field_comparison,
                    "Mismatched Fields" : mismatched_fields
                })

            elif model_a_entry: # REVIEW
                fields_comparison={}
                for field in fields_to_compare:
                    field_comparison[field]={"Model A BOM": model_a_entry.get(field),"Model B BOM": None, "Match": None}
                missing.append({
                    "KEYWORDS": keyword,
                    "Comparison Status": "Missing in Model B BOM",
                    "Comparison Details": field_comparison
                })
            elif model_b_entry: # REVIEW
                fields_comparison={}
                for field in fields_to_compare:
                    field_comparison[field]={"Model A BOM": None,"Model B BOM": model_b_entry.get(field), "Match": None}
                newly_added.append({
                "KEYWORDS": keyword,
                "Comparison Status": "Newly Added in Model B BOM",
                "Comparison Details": field_comparison
            })

        potential_replacements, remaining_missing = [],[]
        updated_newly_added = newly_added.copy()

        for miss in missing:
            miss_keyword = str(miss["KEYWORDS"])[:4].upper()
            miss_qty = miss["Comparison Details"]["QTY"]["Model A BOM"]

            found_replacement = False
            for new in updated_newly_added:
                new_keyword = str(new["KEYWORDS"])[:4].upper()
                new_qty = new["Comparison Details"]["QTY"]["Model B BOM"]

                if miss_keyword == new_keyword and miss_qty == new_qty:
                    potential_replacements.append({
                        "KEYWORDS" : miss["KEYWORDS"],
                        "Comparison Status" : "Potential Replacement",
                        "Comparison Details" : {
                            "KEYWORDS" : {"Model A BOM": miss['KEYWORDS'], "Model B BOM" : new['KEYWORDS'], "Match" : None},
                            "REVISION NUMBER": {"Model A BOM": miss["Comparison Details"]["REVISION NUMBER"]["Model A BOM"], "Model B BOM": new["Comparison Details"]["REVISION NUMBER"]["Model B BOM"], "Match": None},
                            "DRG. NO. / DIMENSION": {"Model A BOM": miss["Comparison Details"]["DRG. NO. / DIMENSION"]["Model A BOM"], "Model B BOM": new["Comparison Details"]["DRG. NO. / DIMENSION"]["Model B BOM"], "Match": None},
                            "QTY": {"Model A BOM": miss["Comparison Details"]["QTY"]["Model A BOM"], "Model B BOM": new["Comparison Details"]["QTY"]["Model B BOM"], "Match": None},
                            "DESCRIPTION": {"Model A BOM": miss["Comparison Details"]["DESCRIPTION"]["Model A BOM"], "Model B BOM": new["Comparison Details"]["DESCRIPTION"]["Model B BOM"], "Match": None}
                        }
                    })
                    updated_newly_added.remove(new)
                    found_replacement=True
                    break
            if not found_replacement:
                remaining_missing.append(miss)

        final_result = {
            "TO CREATE NEW": to_create_new,
            "MATCHED" : matched,
            "POTENTIAL REPLACEMENTS" : potential_replacements,
            "UNMATCHED / MISSING" : missing,
            "NEWLY ADDED" : newly_added,
            "EMPTY OR DASHED" : empty_or_dash
        }
    except Exception as e:
        print(e)
    return final_result

def extract_excel_to_json(excel_bytes,fields, sheet="UNIT PART LIST"):
    raw_df = pd.read_excel(io.BytesIO(excel_bytes),header=0,sheet_name=sheet)[fields]
    
    raw_df.dropna(how = "all",inplace=True)
    df=raw_df
    # df = raw_df.replace(to_replace=['TO CREATE NEW','' ,'','-'],value=pd.NA)
    # df.dropna(subset=["KEYWORDS"], inplace=True) # To filter out records with missing keyword.
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
    
    df = df.where(pd.notnull(df),None)
    orc = len(df)
    records = df.to_dict(orient='records')
    records = [{k:("" if v is None else v) for k,v in record.items()} for record in records]
    jrc = len(records)

    if orc!=jrc:
        print("⚠️ Warning: Row count mismatch!")
        print(f"Excel data rows: {orc}")
        print(f"JSON records generated: {jrc}")

    return records