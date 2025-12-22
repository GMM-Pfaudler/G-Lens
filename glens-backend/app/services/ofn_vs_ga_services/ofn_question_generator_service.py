from dataclasses import dataclass
from collections import defaultdict
import sys,os
from typing import Any
# from app.utils.ofn_vs_ga_utils.data_utils import get_all_nested_values,get_nested_value
def get_all_nested_values(data: any, key_path: str, separator: str = " -> "):
    keys = key_path.split(separator)

    def recursive_extract(current, remaining_keys):
        if not remaining_keys:
            return [current]

        key = remaining_keys[0].strip()
        next_keys = remaining_keys[1:]
        results = []

        if isinstance(current, dict):
            if key in current:
                results.extend(recursive_extract(current[key], next_keys))
        elif isinstance(current, list):
            for item in current:
                results.extend(recursive_extract(item, remaining_keys))

        return results

    return recursive_extract(data, keys)


def get_nested_value(data: dict, key_path: str, separator: str = " -> "):
    keys = [key.strip() for key in key_path.split(separator)]
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data

@dataclass(frozen=True)
class KSD_MAP:
    section : str
    display_name : str | None = None
    question_template : str | None = None

@dataclass(frozen=True)
class ListSD_MAP:
    display_name_template : str
    question_template : str | None = None

KEY_PATH_SEPARATOR = " -> "
NO_VALUE = "No Value"
NA_VALUE = "N/A"
DEFAULT_SCALAR_QUESTION = "Is '{value}' for '{key}' provided in the context?"
SECTIONS = ["design_data", "material_of_construction","part_list","drive_data","key_value_pairs","lining_and_notes","nozzle_data","agitator_data","insulation_data","accessories_data","nq"]

# (keypath -> (section, Display Name, Question))
KEY_SECTION_DISPLAY_MAPPING = {
    # "header -> reactor_header -> quote_no":KSD_MAP("nq","Quote No."),
    "header -> reactor_header -> name":KSD_MAP("key_value_pairs","Client"),
    # "header -> reactor_header -> attention":KSD_MAP("nq","Attention"),
    "header -> reactor_header -> date":KSD_MAP("nq","Date","Was the Order Dated '{value}'?"),
    "header -> reactor_header -> model":KSD_MAP("key_value_pairs","Model","Is the name of the model the same as '{value}'?"),
    "header -> reactor_header -> tag_no":KSD_MAP("key_value_pairs","Tag No."),
    "header -> reactor_header -> capacity":KSD_MAP("design_data","Capacity","Is the Volumn (nominal) for Inner Vessel equal to or similar to {value}?"),
    "header -> reactor_header -> glass":KSD_MAP("lining_and_notes","Glass","Is the glass type same as or similar to '{value}'?"),
    "header -> reactor_header -> code":KSD_MAP("key_value_pairs","Design Code","Is the Design Code the same as or similar to '{value}'?"),
    # "header -> reactor_header -> dimension":KSD_MAP("nq","Dimensions"),
    # "header -> reactor_header -> hydraulic_test_pressure":KSD_MAP("nq","Hydraulic Test Pressure"),
    "header -> reactor_header -> paint":KSD_MAP("lining_and_notes","Paint","Does the paint description match or closely relate to '{value}'?"),
    # "header -> reactor_header -> stress_relief":KSD_MAP("nq","Strss Relief"),
    # "header -> reactor_header -> drilling_standard":KSD_MAP("nq", "Drilling Standard"),
    "header -> reactor_header -> accessories":KSD_MAP("accessories_data","part_list","Do the accessories in the context match with '{value}'?"),
    # "blocks -> dimension -> summary":KSD_MAP("nq","Dimension Summary"),
    "blocks -> dimension -> nominal_volume":KSD_MAP("design_data","Nominal Volume","Is the nominal volume of inner vessel equal to '{value}'?"),
    "blocks -> dimension -> total_volume":KSD_MAP("design_data","Total Volume","Is the total volume of inner vessel equal to '{value}'?"),
    # "blocks -> dimension -> shell_thickness":KSD_MAP("design_data","Shell Thickness"),
    # "blocks -> dimension -> top_dished_end_thickness":KSD_MAP("design_data","Top End Thickness"),
    # "blocks -> dimension -> bottom_dished_end_thickeness":KSD_MAP("design_data","Bottom End Thickness"),
    "blocks -> jacket -> type":KSD_MAP("part_list", "Jacket Type","Is the Jacket Type equal to {value}?"),
    "blocks -> jacket -> volume":KSD_MAP("design_data","Jacket Volume","Is the Jacket volume equal to {value}?"),
    # "blocks -> jacket -> shell_thickness":KSD_MAP("design_data","Jacket Shell Thickness"),
    # "blocks -> jacket -> dish_thickness":KSD_MAP("design_data","Jacket Dish Thickness"),
    "blocks -> jacket -> heat_transfer_area":KSD_MAP("key_value_pairs","Jacket Heat Transfer Area","Is the heat transfer area equal to '{value}'"),
    "blocks -> joint_efficiency -> inner_vessel":KSD_MAP("key_value_pairs","Joint Efficiency (Inner Vessel)","Is the joint efficiency of inner vessel equal to '{value}'?"),
    "blocks -> joint_efficiency -> jacket":KSD_MAP("key_value_pairs","Joint Efficieny (Jacket)","Is the joint efficiency of inner vessel equal to '{value}'?"),
    "blocks -> design_pressure -> inner_vessel":KSD_MAP("design_data","Design Pressure (Inner Vessel)","Is the Design Pressure for the Inner Vessel equal to {value}?"),
    "blocks -> design_pressure -> jacket":KSD_MAP("design_data", "Design Pressure (Jacket)","Is the Design Pressure for the Jacket equal to {value}?"),
    "blocks -> design_temperature -> inner_vessel":KSD_MAP("design_data", "Design Temperature (Inner Vessel)","Is the Design Temperature for the Inner Vessel equal to {value}?"),
    "blocks -> design_temperature -> jacket":KSD_MAP("design_data","Design Temperature (Jacket)","Is the Design Temperature for the Jacket equal to {value}?"),
    "blocks -> ndt -> inner_vessel":KSD_MAP("lining_and_notes", "NDT (Inner Vessel)","Is the Inner Vessel's NDT equal to {value}?"),
    "blocks -> ndt -> jacket":KSD_MAP("lining_and_notes", "NDT (Jacket)","Is the Jacket's NDT equal to {value}?"),
    "blocks -> corrosion_allowance -> glassed_surface":KSD_MAP("key_value_pairs","Corrosion Allowance (Glassed Surface)","Is the Corrosion Allowance for the Glassed Surface equal to {value}?"),
    "blocks -> corrosion_allowance -> wetted_with_jacket_fluid":KSD_MAP("key_value_pairs", "Corrosion Allowance (Wetted with Jacket Fluid)","Is the Corrosion Allowance for the Wetted With Jacket Fluid equal to {value}?"),
    "blocks -> corrosion_allowance -> non_wetted_surface":KSD_MAP("key_value_pairs","Corrosion Allowance (Non Wetted Surface)","Is the Corrosion Allowance for the Non Wetted Surface equal to {value}?"),
    "moc -> reactor_moc_data -> material_of_construction -> shell_head":KSD_MAP("material_of_construction", "Shell, Head", "Does the Material of Construction for the Shell and Head match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> nozzle_neck_&_body_flange":KSD_MAP("material_of_construction","Nozzles Necks & Body Flange","Does the Material of Construction for the Nozzle Necks & Body Flange match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> split_flanges":KSD_MAP("material_of_construction", "Split Flanges","Does the Material of Construction for the Split Flanges match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> manhole_c_clamps":KSD_MAP("part_list","Hand/Manhole C-Clamps","Does the part description for Hand/Manhole C-Clamps match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> fasteners -> pressure_part":KSD_MAP("material_of_construction","Fasteners (Pressure Part)","Does the Material of Construction for the Fasteners Pressure Part match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> fasteners -> non_pressure_part":KSD_MAP("material_of_construction","Fasteners (Non-Pressure Part)","Does the Material of Construction for the Fasteners Non-Pressure Part match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> gasket":KSD_MAP("material_of_construction", "Gasket","Does the Material of Construction for the Gasket match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> manhole_cover":KSD_MAP("part_list","Hand/Manhole Cover","Does the part description for the Hand/Manhole Cover match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> manhole_protection_ring":KSD_MAP("nozzle_data","Hand/Manhole Protection Ring","Is the Hand/Manhole Protection Ring described as '{value}' or something similar?"),
    "moc -> reactor_moc_data -> material_of_construction -> spring_balance_assembly":KSD_MAP("part_list", "Spring Balance Assembly","Does the part description for the Spring Balance Assembly match or closely relate to '{value}' or 'Spring Balance Assembly'?"),
    "moc -> reactor_moc_data -> material_of_construction -> sight_light_glass_flanges":KSD_MAP("part_list","Sight/Light Glass Flanges","Does the part description for the Sight/Light Glass Flanges match or closely relate to '{value}' or 'Sight/Light Glass Flanges'?"),
    "moc -> reactor_moc_data -> material_of_construction -> earthing":KSD_MAP("part_list","Earthing","Does the part description for Earthing match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> lantern_support":KSD_MAP("part_list","Lantern Support","Does the part description for the Lantern Support match or closely relate to '{value}' or 'Lantern Support'?"),
    "moc -> reactor_moc_data -> material_of_construction -> lantern_guard":KSD_MAP("part_list","Lantern Guard","Does the part description for 'Lantern Guard' match or closely relate to '{value}' in the context?"),
    "moc -> reactor_moc_data -> material_of_construction -> drive_base_ring":KSD_MAP("part_list", "Drive Base Ring","Does the part description for the Drive Base Ring match or closely relate to '{value}' or 'Drive Base Ring'?"),
    "moc -> reactor_moc_data -> material_of_construction -> drive_hood":KSD_MAP("material_of_construction", "Drive Hood","Does the Drive Hood match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> jacket_shell_head":KSD_MAP("material_of_construction", "Jacket (Shell, Head)","Does the Material of Construction for the Jacket (Shell, Head) match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> jacket_nozzle":KSD_MAP("material_of_construction","Jacket Nozzle","Does the Material of Construction for the Jacket Nozzle match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> jacket_coupling+plug":KSD_MAP("material_of_construction","Jacket Coupling+Plug","Does the Material of Construction for the Jacket Coupling+Plug match or closely relate to '{value}'?"),
    "moc -> reactor_moc_data -> material_of_construction -> spillage_collection_tray":KSD_MAP("material_of_construction","Is the spillage collection tray present?"),
    "drive_baffle -> baffle -> type":KSD_MAP("part_list","Baffle","Is the Baffle value equals to '{value}'?"),
    # "drive_baffle -> baffle -> sensing_volume":KSD_MAP("nq",),
    "drive_baffle -> drive -> gear_box":KSD_MAP("drive_data","Gear Box (Drive)","Is Drive Gear Box match or closesly relate to '{value}' or is there an exact match to '{value}'?"),
    "drive_baffle -> drive -> motor":KSD_MAP("drive_data","Motor (Drive)","Is Drive for Motor match or closesly relate to '{value}'?"),
    "drive_baffle -> drive -> shaft_closure -> type":KSD_MAP("part_list","Shaft Closure Type (Drive)", "Is the Shaft Closure Type in context, a match or closely related to '{value}' or is there an exact or very close match to 'Shaft CLosure Type'?"),
    # "drive_baffle -> drive -> shaft_closure -> inboard_face":KSD_MAP("nq",),
    # "drive_baffle -> drive -> shaft_closure -> sealing":KSD_MAP("nq",),
    # "drive_baffle -> drive -> shaft_closure -> housing":KSD_MAP("nq",),
    # "drive_baffle -> drive -> shaft_closure -> other":KSD_MAP("nq",),
    # "drive_baffle -> drive -> shaft_closure -> alternate_seal":KSD_MAP("nq",),
    "agitator -> agitator -> flight":KSD_MAP("part_list","Flight","Is Agitator Flight value is match or closerly realted to {value}?"),
    "agitator -> agitator -> shaft_diameter":KSD_MAP("part_list", "Shaft Diameter","Does the part Description for the Agitator's Shaft Diameter match or closesly relate to '{value}'?"),
    "agitator -> agitator -> rpm":KSD_MAP("key_value_pairs", "RPM","Is RPM equals to {value}?"),
    "agitator -> agitator -> specific_gravity":KSD_MAP("design_data","Specific Gravity","Is Inner Vessel Specific Gravity value match or closely realte to {value}?"),
    "agitator -> agitator -> viscosity":KSD_MAP("design_data","Viscosity","Is the Viscosity equal or closely relate to {value}?"),
    # "agitator -> agitator -> level_marking":KSD_MAP("nq",),
    # "agitator -> agitator -> stirring_volume":KSD_MAP("nq",),
    "nozzle -> reactor_nozzle_schema -> nozzle_section -> jacket_nozzle -> description":KSD_MAP("part_list", "Jacket Nozzle","Does the part description for the Jacket Nozzle match or closely relate to '{value}'?"),
    "nozzle -> reactor_nozzle_schema -> nozzle_section -> bottom_outlet_valve -> type":KSD_MAP("part_list","Bottom Outlet Valve","Does the part description for the Bottom Outlet Valve match or similar to '{value}'?"),
    "nozzle -> reactor_nozzle_schema -> nozzle_section -> nozzles":KSD_MAP("nozzle_data",),
    "agitator -> agitator -> agitator_types":KSD_MAP("agitator_data",),
    "insulation -> insulation -> sections":KSD_MAP("insulation_data",),
}
NOZZLE_DISPLAY_MAPPING={
    "nozzle_no": ListSD_MAP("Nozzle ","Is Nozzle '{nozzle_no}' present?"),
    "size_dn": ListSD_MAP("Size of Nozzle '{nozzle_no}'","Is the size(DN) of nozzle '{nozzle_no}' equal or to similar to {size_dn}?"),
    "service": ListSD_MAP("Nozzle {nozzle_no} Service","Is the service associated with nozzle '{nozzle_no}' same as or close to '{service}'?"),
    # "location": ListSD_MAP("Nozzle {nozzle_no} Location", "Is Nozzle '{nozzle_no}' located at '{location}'?"),
    # "description": ListSD_MAP("Nozzle {nozzle_no} description","Is the description of nozzle '{nozzle_no}' same as or similar to '{description}'?")
}
AGITATOR_DISPLAY_MAPPING={
    "type" : ListSD_MAP("Agitator Type", "Is '{type}' the agitator type?"),
    # "position" : ListSD_MAP("Agitator {type} position","Is the position of {type} same as or similar to '{position}'?"),
    "sweep_diameter_mm" : ListSD_MAP("Agitator {type} Diameter", "Is the diameter of '{type}' equivalent to '{sweep_diameter}'?")
}
INSULATION_DISPLAY_MAPPING={
    "section": ListSD_MAP("Insulation Section", "Is '{section}' insulated?"),
    "material": ListSD_MAP("{section} Insulation Material","Is insulation material for '{section}' same as or similar to '{material}'?"),
    "thk": ListSD_MAP("{section} Insulation Thickness", "Is the thickness of insulation for '{section}' same as or similar to '{thk}'?")
}
LIST_DATA = {
    "nozzle_data" : (NOZZLE_DISPLAY_MAPPING,"nozzle_data"),
    "agitator_data" : (AGITATOR_DISPLAY_MAPPING,"part_list"),
    "insulation_data" : (INSULATION_DISPLAY_MAPPING,"material_of_construction")
}
INVALID_VALUES = {"", "N/A", "NA", "NONE", "NULL", "-", "NOT APPLICABLE"}



def gen_comparison_questions(ofn_data: dict[str, Any],key_section_map: dict[str, KSD_MAP] = KEY_SECTION_DISPLAY_MAPPING) -> list[dict[str, Any]]:
    """
    Generate structured comparison questions from OFN data.

    Returns:
        List of dicts with keys:
        - question
        - section
        - key
        - expected_value
        - display_key
        - display_value
    """
    questions = []
    
    for key_path, ksd in key_section_map.items():
        ofn_value = get_nested_value(ofn_data, key_path)
        values = (
            [ofn_value]
            if ofn_value is not None
            else get_all_nested_values(ofn_data, key_path)
        )
        cleaned_values = []
        for val in values:
            if isinstance(val,str):
                val_stripped = val.strip().upper()
                if val_stripped in INVALID_VALUES:
                    cleaned_values.append(NO_VALUE)
                else:
                    cleaned_values.append(val.strip())
            elif val is None:
                cleaned_values.append(NO_VALUE)
            elif isinstance(val, dict):
                cleaned_values.append(val)
            elif isinstance(val,list):
                cleaned_values.extend(val)
            else:
                cleaned_values.append(str(val))
        for value in cleaned_values:
            if isinstance(value, dict): #and ksd.section in LIST_DATA:
                section_format = LIST_DATA.get(ksd.section)[0]
                for field, field_cfg in section_format.items():
                    if not field_cfg.question_template:
                        continue
                    safe_value = defaultdict(lambda: "N/A", value)
                    display_key = field_cfg.display_name_template.format_map(safe_value)
                    question = field_cfg.question_template.format_map(safe_value)
                    if question is not None:
                        questions.append({
                            "question" : question,
                            "section" : LIST_DATA[ksd.section][1],
                            "key" : KEY_PATH_SEPARATOR.join([key_path,display_key]),
                            "expected_value":value.get(field, NA_VALUE),
                            "display_key" : display_key,
                            "display_value": value.get(field, NA_VALUE)
                        })
            elif not isinstance(value,dict):
                if value == NO_VALUE: continue
                context = defaultdict(lambda: NA_VALUE)
                context["value"] = value
                context[key_path.split(KEY_PATH_SEPARATOR)[-1]] = value

                # Use specific template if provided, else fallback
                if ksd.question_template:
                    question = ksd.question_template.format_map(context)
                else:
                    question = DEFAULT_SCALAR_QUESTION.format_map({
                        "value": value,
                        "key": key_path
                    })
                questions.append({
                    "question": question,
                    "section": ksd.section,
                    "key": key_path,
                    "expected_value": value,
                    "display_key": ksd.display_name or key_path,
                    "display_value": value,
                })
    print(f"No. of questions generated:{len(questions)}") 
    return questions


if __name__ == "__main__":
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'core')))
# from ofn_extractor_new import OFNPDFExtractor
    # OFNExtractor = OFNPDFExtractor(".",".")
    # results = OFNExtractor.extract_single_pdf("glens-backend\\app\\core\\088837_AE_250L_section_2.pdf")
    # print(results)
    # raw_text = results
    raw_text={'header': {'reactor_header': {'quote_no': '088837', 'name': 'Saurav Chemicals Ltd', 'attention': 'Mr. Ramakant Pathak', 'date': '04/12/2025', 'model': 'MSGL Reactor with Insulation (Non-GMP Model)', 'tag_no': 'API-3 Project', 'capacity': 'AE_250L', 'glass': 'Pfaudler World Wide 9100 (Dark Blue), Plug Free', 'code': 'ASME SECTION VIII, DIV.I. (LATEST) - Unstamped', 'dimension': '680 ID And Overall Height 1030 mm mm, Other Dimension as per Our Bulletin DIN Reactors _ AE.', 'weight': '', 'hydraulic_test_pressure': 'Pressure tested in accordance with Code.', 'paint': 'Pre-Treatment Removal by blasting. 2 Coats of RAL 5015 (Sky Blue)', 'stress_relief': 'All heating cycles will be as required for glassing process.', 'drilling_standard': 'GMM fItting PN - 10 DIN 2673 & Spare ASME 150#', 'support': '', 'accessories': ['3 mm thickness SS 304 cladding', '220 Grit polishing for insulated area only', 'Insulation only on jacket and not on top dishend']}}, 'blocks': {'dimension': {'summary': '680 ID And Overall Height 1030 mm mm, Other Dimension as per Our Bulletin DIN Reactors _ AE', 'nominal_volume': '250 Ltr', 'total_volume': '335 Ltr', 'shell_thickness': '10 mm', 'top_dished_end_thickness': '', 'bottom_dished_end_thickness': ''}, 'jacket': {'type': 'Plain Jacket with 800 OD', 'volume': '90 Ltr', 'shell_thickness': '', 'dish_thickness': '', 'heat_transfer_area': '1.66 SQ.M'}, 'joint_efficiency': {'inner_vessel': '', 'jacket': ''}, 'design_pressure': {'inner_vessel': 'F. V. / 6 bar(g)', 'jacket': 'F. V. / 6 bar(g)'}, 'design_temperature': {'inner_vessel': '-28.8°C to 200°C', 'jacket': '-28.8°C to 200°C'}, 'ndt': {'inner_vessel': 'Full Radiography- All Main Weld Seams Of Inner Vessel Including \'T\' Joints And Nozzle Size DN250 (10"Nb) And Above Or Nozzle Neck Thickness 29 mm And Above Shall Be Examined By Full Radiography.', 'jacket': 'Nil'}, 'corrosion_allowance': {'glassed_surface': '0.0', 'wetted_with_jacket_fluid': '1.0', 'non_wetted_surface': '0.5'}}, 'moc': {'reactor_moc_data': {'material_of_construction': {'shell_head': 'SA 516 Gr.60(EQ)', 'nozzle_neck_&_body_flange': 'SA 181 Gr. 60 / SA 836', 'split_flanges': 'SA 516 Gr. 70 (CS)', 'manhole_c_clamps': 'SA 182 F 304', 'fasteners': {'pressure_part': 'IS : 1363 / 1367 CL. 4.6 / 4 - Zinc Electro Plated (20µ) & Yellow Passivation', 'non_pressure_part': 'IS : 1363 / 1367 CL. 4.6 / 4 - Zinc Electro Plated (20µ) & Yellow Passivation'}, 'gasket': 'PTFE Enveloped NON ASBESTOS', 'manhole_cover': 'MSGL', 'manhole_protection_ring': 'MSGL', 'spring_balance_assembly': '', 'sight_light_glass_flanges': 'MS', 'earthing': '01 No.- Earthing Cleat (MS)', 'lantern_support': 'MS', 'lantern_guard': 'MS', 'drive_base_ring': 'MS', 'drive_hood': 'SS304', 'jacket_shell_head': 'SA 516 Gr. 60 / 70', 'jacket_nozzle': 'SS304', 'jacket_coupling+plug': 'SS304', 'spillage_collection_tray': 'Yes'}}}, 'drive_baffle': {'baffle': {'type': 'Beavertail type Baffle with FlangeDesign & M12 tantalum tip - Extra Long', 'sensing_volume': 'As low as possible'}, 'drive': {'gear_box': 'Bonfiglioli Make In-Line Helical Gear Box', 'motor': 'BBL Make 3 (2.2 KW) HP IE3 Flameproof Motor', 'shaft_closure': {'type': 'Rolon Make Single Mechanical Seal', 'inboard_face': 'Carbon vs SIC', 'sealing': 'FFKM O-Ring', 'housing': 'MS', 'other': '', 'alternate_seal': 'No'}}}, 'agitator': {'agitator': {'flight': 'Double', 'agitator_types': [{'type': 'CBRT - Bottom', 'sweep_diameter_mm': 3}, {'type': 'PBT - Top', 'sweep_diameter_mm': 4}], 'shaft_diameter': 50, 'rpm': 93, 'specific_gravity': '≤ 1.6', 'viscosity': '100 CPS', 'level_marking': 'Yes', 'stirring_volume': 'As low as possible'}}, 'insulation': {'insulation': [{'section': 'Top Head', 'material': 'Not Applicable', 'thk': 'Not Applicable'}, {'section': 'Jacket', 'material': 'Mineral wool + Puff', 'thk': '50+50 MM'}, {'section': 'Cladding', 'material': 'SS304', 'thk': '2.5 MM'}]}, 'nozzle': {'reactor_nozzle_schema': {'nozzle_section': {'nozzles': [{'nozzle_no': 'N1', 'size_dn': 150, 'service': 'Hand hole', 'location': 'Top Head', 'description': 'MSGL Hand hole Cover With 50NB Sight Glass Assembly'}, {'nozzle_no': 'N2', 'size_dn': 50, 'service': 'Spare', 'location': 'Top Head', 'description': 'CS PTFE Lined dip pipe + Wooden Blind Flange'}, {'nozzle_no': 'N4', 'size_dn': 80, 'service': 'Spare', 'location': 'Top Head', 'description': 'GL Blind Flange'}, {'nozzle_no': 'N6', 'size_dn': 80, 'service': 'Spare', 'location': 'Top Head', 'description': 'GL Blind Flange'}, {'nozzle_no': 'N8', 'size_dn': 80, 'service': 'Baffle / Thermowell', 'location': 'Top Head', 'description': 'With M12 tantalum tip + PT-100 RTD sensor'}, {'nozzle_no': 'N10', 'size_dn': 50, 'service': 'Light Glass', 'location': 'Top Head', 'description': 'Light Glass assembly'}, {'nozzle_no': 'M', 'size_dn': 80, 'service': 'Agitator Entry', 'location': 'Top Head', 'description': 'Mechanical seal'}, {'nozzle_no': 'L', 'size_dn': 80, 'service': 'Outlet', 'location': 'Btm head', 'description': '80/50NB MSGL Glasslined bottom outlet valve'}], 'bottom_outlet_valve': {'type': 'Gland', 'name': 'MSGL Gland Type Down To Open BOV 80x50 + T/Tip + RTD Sensor (GPF 802)'}, 'jacket_nozzle': {'description': '02 Nos. DN40 Jacket Nozzle'}}}}}


    questions = gen_comparison_questions(raw_text)
    for que in questions:
        print(que.get("question"))
