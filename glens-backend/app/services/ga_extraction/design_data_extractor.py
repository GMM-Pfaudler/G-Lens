import json,re
from app.utils.camelot_extractor import extract_table_data

#NEW METHOD TO EXTRACT LIMPET COIL AND JACKET WITH SEPARETED CONDITION
def extract_design_parameters(data):
    parameter_key = None
    inner_vessel_key = None
    alt_column_key = None
    alt_column_label = None  # Will hold either "JACKET" or "LIMPET COIL"
    parameters = []

    alt_names = {"JACKET", "LIMPET COIL"}
    end_markers = {
        "PRESSURE\nHYDROSTATIC TEST (AFTER\nLINING)\nDURATION",
        "HYDROSTATIC TEST (AFTER\nPRESSURE\nLINING)\nDURATION",
        "HYDROSTATIC TEST\nPRESSURE\n(AFTER LINING)\nDURATION"
    }

    # Step 1: Find column key for "DESIGN DATA :"
    for row in data:
        for key, value in row.items():
            if value.strip().upper() == "DESIGN DATA :":
                parameter_key = key
                break
        if parameter_key:
            break

    if not parameter_key:
        raise ValueError("Could not find 'DESIGN DATA :' in the data.")

    # Step 2: Detect "INNER VESSEL" and optionally "JACKET" or "LIMPET COIL"
    for row in data:
        if row.get(parameter_key, "").strip().upper() == "PARAMETER DESCRIPTION":
            for key, value in row.items():
                value_clean = value.strip().upper()
                if value_clean == "INNER VESSEL":
                    inner_vessel_key = key
                elif value_clean in alt_names:
                    alt_column_key = key
                    alt_column_label = value_clean
            break

    if not inner_vessel_key:
        raise ValueError("Could not find key for 'INNER VESSEL'.")

    # Step 3: Extract the rows
    for row in data:
        param_name = row.get(parameter_key, "").strip()
        if not param_name or param_name.upper() in ["DESIGN DATA :", "PARAMETER DESCRIPTION"]:
            continue

        inner_value = row.get(inner_vessel_key, "").strip()
        row_data = {
            "Parameter": param_name,
            "INNER VESSEL": inner_value
        }

        if alt_column_key:
            alt_value = row.get(alt_column_key, "").strip()
            row_data[alt_column_label] = alt_value

        parameters.append(row_data)

        if param_name.strip().upper() in (marker.upper() for marker in end_markers):
            break

    return parameters