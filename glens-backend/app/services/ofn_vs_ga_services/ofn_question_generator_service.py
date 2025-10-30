import json
import re
from app.utils.ofn_vs_ga_utils.data_utils import get_all_nested_values,get_nested_value

def generate_comparison_questions_with_keys(ofn_data: dict, key_section_map: dict) -> list[dict]:
    questions = []

    INVALID_VALUES = {"", "N/A", "NA", "NONE", "NULL", "-", "NOT APPLICABLE"}

    for key_path, section in key_section_map.items():
        ofn_value = get_nested_value(ofn_data, key_path)

        if ofn_value is None:
            all_values = get_all_nested_values(ofn_data, key_path)
        else:
            all_values = [ofn_value]

        # Normalize and clean the values
        cleaned_values = []
        for val in all_values:
            if isinstance(val, str):
                val_stripped = val.strip().upper()
                if val_stripped in INVALID_VALUES:
                    cleaned_values.append("No Value")
                else:
                    cleaned_values.append(val.strip())
            elif val is None:
                cleaned_values.append("No Value")
            elif isinstance(val, dict):
                cleaned_values.append(json.dumps(val, separators=(", ", ": ")))
            else:
                cleaned_values.append(str(val))

        for value in cleaned_values:
            # Default display_key and display_value
            display_key = key_path
            display_value = value

            # Check for the special cases, adjust display_key and display_value accordingly
            if key_path == "Capacity":
                match = re.search(r'(\d+[A-Za-z]+)', value)
                if match:
                    capacity = match.group(1)
                    question_display_value = f"{capacity}(Liter)"
                    question = f"Is the Volume (nominal) for Inner Vessel equals or simillar to {question_display_value}?"
                    display_key = "Capacity"
                    display_value = question_display_value

            elif key_path == "Glass":
                question = f"Is the Glass type {value} or something similar?"
                display_key = "Glass"
                display_value = value
            
            elif key_path == "Jacket Type":
                question = f"Is the Jacket Type equal to {value}?"
                display_key = "Jacket Type"
                display_value = value
            
            elif key_path == "Design Pressure -> Inner Vessel":
                question = f"Is the Design Pressure for the Inner Vessel equal to {value}?"
                display_key = "Design Pressure (Inner Vessel)"
                display_value = value
            
            elif key_path == "Design Pressure -> Jacket":
                question = f"Is the Design Pressure for the Jacket equal to {value}?"
                display_key = "Design Pressure (Jacket)"
                display_value = value
            
            elif key_path == "Design Temperature -> Inner Vessel":
                question = f"Is the Inner Vessel's Design Temperature in the range {value}?"
                display_key = "Design Temperature (Inner Vessel)"
                display_value = value
            
            elif key_path == "Design Temperature -> Jacket":
                question = f"Is the Jacket's Design Temperature in the range {value}?"
                display_key = "Design Temperature (Jacket)"
                display_value = value
            
            elif key_path == "NDT -> Inner Vessel":
                question_display_value = "Ultrasonically Tested" if value.upper() == "UT" else value
                question = f"Is the Inner Vessel's NDT equal to {question_display_value}?"
                display_key = "NDT (Inner Vessel)"
                display_value = value

            elif key_path == "NDT -> Jacket":
                question_display_value = "Ultrasonically Tested" if value.upper() == "UT" else value
                question = f"Is the NDT equal to {question_display_value}?"
                display_key = "NDT (Jacket)"
                display_value = value

            elif key_path == "Paint":
                question = f"Does the Paint description match or closely relate to '{value}'?"
                display_key = "Paint"
                display_value = value
            
            elif key_path == "Corrosion Allowance -> Glassed Surface":
                question = f"Is the Corrosion Allowance for the Glassed Surface equal to {value}?"
                display_key = "Corrosion Allowance (Glassed Surface)"
                display_value = value

            elif key_path == "Corrosion Allowance -> Wetted With Jacket Fluid":
                question = f"Is the Corrosion Allowance for the Wetted With Jacket Fluid equal to {value}?"
                display_key = "Corrosion Allowance (Wetted With Jacket Fluid)"
                display_value = value

            elif key_path == "Corrosion Allowance -> Non Wetted Surface":
                question = f"Is the Corrosion Allowance for the Non Wetted Surface equal to {value}?"
                display_key = "Corrosion Allowance (Non Wetted Surface)"
                display_value = value

            elif key_path == "Material of Construction -> Shell, Head":
                question = f"Does the Material of Construction for the Shell and Head match or closely relate to '{value}'?"
                display_key = "Shell, Head"
                display_value = value

            elif key_path == "Material of Construction -> Nozzle Necks & Body Flange":
                question = f"Does the Material of Construction for the Nozzle Necks & Body Flange match or closely relate to '{value}'?"
                display_key = "Nozzle Necks & Body Flange"
                display_value = value
            
            elif key_path == "Material of Construction -> Split Flanges":
                question = f"Does the Material of Construction for the Split Flanges match or closely relate to '{value}'?"
                display_key = "Split Flanges"
                display_value = value
            
            elif key_path == "Material of Construction -> Body Flange C-Clamps":
                question = f"Does the part description for Body Flange C-Clamps match or closely relate to '{value}'?"
                display_key = "Body Flange C-Clamps"
                display_value = value
            
            elif key_path == "Material of Construction -> Hand/Manhole C-Clamps":
                question = f"Does the part description for Hand/Manhole C-Clamps match or closely relate to '{value}'?"
                display_key = "Hand/Manhole C-Clamps"
                display_value = value
            
            elif key_path == "Material of Construction -> Fasteners -> Pressure Part":
                question = f"Does the Material of Construction for the Fasteners Pressure Part match or closely relate to '{value}'?"
                display_key = "Fasteners (Pressure Part)"
                display_value = value
            
            elif key_path == "Material of Construction -> Fasteners -> Non-Pressure Part":
                question = f"Does the Material of Construction for the Fasteners Non-Pressure Part match or closely relate to '{value}'?"
                display_key = "Fasteners (Non-Pressure Part)"
                display_value = value

            elif key_path == "Material of Construction -> Gasket":
                question = f"Does the Material of Construction for the Gasket match or closely relate to '{value}'?"
                display_key = "Gasket"
                display_value = value
            
            elif key_path == "Material of Construction -> Hand/Manhole Cover":
                question = f"Does the part description for the Hand/Manhole Cover match or closely relate to '{value}'?"
                display_key = "Hand/Manhole Cover"
                display_value = value

            elif key_path == "Material of Construction -> Hand/Manhole Protection Ring":
                question = f"Is the Hand/Manhole Protection Ring described as '{value}' or something similar?"
                display_key = "Hand/Manhole Protection Ring"
                display_value = value

            elif key_path == "Material of Construction -> Spring Balance Assembly":
                question = f"Does the part description for the Spring Balance Assembly match or closely relate to '{value}'?"
                display_key = "Spring Balance Assembly"
                display_value = value
            
            elif key_path == "Material of Construction -> Sight/Light Glass Flanges":
                question = f"Does the part description for the Sight/Light Glass Flanges match or closely relate to '{value}'?"
                display_key = "Sight/Light Glass Flanges"
                display_value = value
            
            elif key_path == "Material of Construction -> Earthing":
                question = f"Does the part description for Earthing match or closely relate to '{value}'?"
                display_key = "Earthing"
                display_value = value
            
            elif key_path == "Material of Construction -> Lantern Support":
                question = f"Does the part description for the Lantern Support match or closely relate to '{value}'?"
                display_key = "Lantern Support"
                display_value = value
            
            elif key_path == "Material of Construction -> Lantern Guard":
                # question = f"Does the part description for the Lantern Guard match or closely relate to '{value}'?"
                question = f"Does the part description for 'Lantern Guard' match or closely relate to '{value}' in the context?"
                display_key = "Lantern Guard"
                display_value = value
            
            elif key_path == "Material of Construction -> Drive Base Ring":
                question = f"Does the part description for the Drive Base Ring match or closely relate to '{value}'?"
                display_key = "Drive Base Ring"
                display_value = value
            
            elif key_path == "Material of Construction -> Drive Hood":
                question = f"Does the Drive Hood match or closely relate to '{value}'?"
                display_key = "Drive Hood"
                display_value = value
            
            elif key_path == "Material of Construction -> Jacket (Shell, Head)":
                question = f"Does the Material of Construction for the Jacket (Shell, Head) match or closely relate to '{value}'?"
                display_key = "Jacket (Shell, Head)"
                display_value = value
            
            elif key_path == "Material of Construction -> Jacket Nozzle":
                question = f"Does the Material of Construction for the Jacket Nozzle match or closely relate to '{value}'?"
                display_key = "Jacket Nozzle"
                display_value = value
            
            elif key_path == "Material of Construction -> Jacket Coupling+Plug":
                question = f"Does the Material of Construction for the Jacket Coupling+Plug match or closely relate to '{value}'?"
                display_key = "Jacket Coupling+Plug"
                display_value = value
            
            elif key_path == "Nozzles -> Bottom Outlet Valve":
                question = f"Does the part description for the Bottom Outlet Valve match or similar to '{value}'?"
                display_key = "Bottom Outlet Valve"
                display_value = value
            
            elif key_path == "Nozzles -> Jacket Nozzle":
                question = f"Does the part description for the Jacket Nozzle match or closely relate to '{value}'?"
                display_key = "Jacket Nozzle"
                display_value = value
            
            elif key_path == "Support":
                question = f"Does the part description for the Support match or closely relate to '{value}'?"
                display_key = "Support"
                display_value = value
            
            elif key_path == "Agitator -> Viscosity":
                question = f"Is the Viscosity equal or closely relate to {value}?"
                display_key = "Viscosity"
                display_value = value
            
            elif key_path == "Agitator -> Specific Gravity":
                question = f"Is Inner Vessel Specific Gravity value match or closely realte to {value}?"
                display_key = "Specific Gravity"
                display_value = value
            
            elif key_path == "Agitator -> Flight":
                question = f"Is Agitator Flight value is match or closerly realted to {value}?"
                display_key = "Flight"
                display_value = value
            
            elif key_path == "Agitator -> RPM":
                question =f"Is RPM equals to {value}?"
                display_key = "RPM"
                display_value = value
            
            elif key_path == "Agitator -> Shaft Diameter":
                question = f"Does the part Description for the Agitator's Shaft Diameter match or closesly relate to '{value}'?"
                display_key = "Shaft Diameter"
                display_value = value
            
            elif key_path == "Baffle":
                question = f"Is the Baffle value equals to '{value}'?"
                display_key = "Baffle"
                display_value = value

            elif key_path == "Drive -> Gear Box":
                question = f"Is Drive for Gear Box match or closesly relate to '{value}'?"
                display_key = "Gear Box (Drive)"
                display_value = value
            
            elif key_path == "Drive -> Motor":
                question = f"Is Drive for Motor match or closesly relate to '{value}'?"
                display_key = "Motor (Drive)"
                display_value = value
            
            elif key_path == "Drive -> Shaft Closure -> Type":
                question = f"Is Drive Shaft Closure Type a match or closely related to '{value}'?"
                display_key = "Shaft Closure Type (Drive)"
                display_value = value
            
            elif key_path == "Drive -> Thermosyphon System Make":
                question = f"Is Drive Thermosyphon System Make is a match or closely relate to '{value}'?"
                display_key = "Thermosyphon System Make (Drive)"
                display_value = value
            
            elif key_path == "Drive -> Thermosyphon System Material":
                question = f"Is Drive Thermosyphon System Material is a match or closely relate to '{value}'?"
                display_key = "Thermosyphon System Material (Drive)"
                display_value = value
            
            elif key_path == "tables -> agitator_details -> agitator_type" and value.upper().strip() == "RCI":
                question_display_value = "Impeller"
                question = f"Is Agitatory Type's value is a match or closely relate to '{question_display_value}'?"
                display_key = "Agitator Type"
                display_value = value
            
            else:
                question = f"is {value} for {key_path} is provided in the context?"
                display_key = key_path
                display_value = value

            questions.append({
                "question": question,
                "section": section,
                "key": key_path,
                "expected_value": value,
                "display_key": display_key,
                "display_value": display_value
            })

    return questions

# Nozzle Question Generator
def generate_nozzle_questions(ofn_data: dict) -> list[dict]:
    questions = []
    tables = ofn_data.get("tables", [])
    nozzles = []

    for table in tables:
        nozzles = table.get("nozzles_details", [])
        if nozzles:
            break

    if nozzles:
        for nozzle in nozzles:
            nozzle_no = nozzle.get("No.")
            if not nozzle_no:
                continue

            # Size question
            if "Size" in nozzle:
                field = "Size"
                value = nozzle["Size"]
                if value:  # Check if value exists
                    question = f"In the 'Nozzles' section, does nozzle '{nozzle_no}' have {field} equal to or similar to '{value}'?"
                    key_path = f"Nozzles -> {nozzle_no} -> {field}"
                    questions.append({
                        "question": question,
                        "section": "nozzle_data",
                        "key": key_path,
                        "expected_value": value
                    })
                else:
                    # If the size value is missing, add a question with "N/A" as expected value
                    question = f"In the 'Nozzles' section, does nozzle '{nozzle_no}' have {field}?"
                    key_path = f"Nozzles -> {nozzle_no} -> {field}"
                    questions.append({
                        "question": question,
                        "section": "nozzle_data",
                        "key": key_path,
                        "expected_value": "N/A"
                    })

            # Service question
            if "Service" in nozzle:
                field = "Service"
                value = nozzle["Service"]
                if value:  # Check if value exists
                    question = f"In the 'Nozzles' section, does nozzle '{nozzle_no}' have {field} equal to or similar to '{value}'?"
                    key_path = f"Nozzles -> {nozzle_no} -> {field}"
                    questions.append({
                        "question": question,
                        "section": "nozzle_data",
                        "key": key_path,
                        "expected_value": value
                    })
                else:
                    # If the service value is missing, add a question with "N/A" as expected value
                    question = f"In the 'Nozzles' section, does nozzle '{nozzle_no}' have {field}?"
                    key_path = f"Nozzles -> {nozzle_no} -> {field}"
                    questions.append({
                        "question": question,
                        "section": "nozzle_data",
                        "key": key_path,
                        "expected_value": "N/A"
                    })
    else:
        print("No nozzle details found.")

    return questions