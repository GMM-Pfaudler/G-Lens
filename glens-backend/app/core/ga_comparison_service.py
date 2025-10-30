import asyncio
import json,random
import time,pprint
from typing import Dict
import aiofiles
from fastapi import HTTPException
from app.services.ofn_vs_ga_services.ollama_rag import Check
from app.services.ga_vs_ga_services.rag_comparision_service import get_all_nested_values,sanitize_filename, get_ga_nested_value
from app.services.ga_vs_ga_services.ga_to_ga_helper.general_notes_ga_to_ga import generate_general_notes_questions
from app.services.ga_vs_ga_services.ga_to_ga_helper.nozzle_cmpr_ga_to_ga_helper import compare_nozzle_data
from app.services.ga_vs_ga_services.ga_to_ga_helper.part_list_cmpr_ga_to_ga_helper import compare_part_list
from app.utils.ofn_vs_ga_utils.data_utils import parse_json_content

def build_design_data_key_section_map(design_data: list, section: str = "design_data") -> dict:
    key_map = {}
    for entry in design_data:
        param = entry.get("Parameter", "").strip().replace("\n", " ").strip()
        if not param:
            continue

        for field in ["INNER VESSEL", "JACKET"]:
            value = entry.get(field, "").strip()
            if value:  # only map if value exists
                key = f"Design Data -> {param} -> {field}"
                key_map[key] = section
    return key_map

def generate_design_data_questions(design_data: list, section: str = "design_data") -> list[dict]:
    questions = []
    INVALID_VALUES = {"", "----", "-----", "N/A", "NA", "-", "NONE", "NULL", "NOT APPLICABLE"}

    for entry in design_data:
        param = entry.get("Parameter", "").strip().replace("\n", " ").strip()

        if not param:
            continue

        for field in ["INNER VESSEL", "JACKET"]:
            value = entry.get(field, "").strip().replace("\n", " ")
            if value.upper() in INVALID_VALUES:
                continue
    
            key_path = f"Design Data -> {param} -> {field}"
            param_upper = param.upper()
            if param_upper == "FLUID" and field == "INNER VESSEL":
                question = f"What is the fluid used inside the inner vessel? Is it '{value}'?"
                display_key = "Fluid (Inner Vessel)"
                display_value = value
            
            elif param_upper == "FLUID" and field == "JACKET":
                question = f"Is FLUID value in JACKET is equal or ralate to '{value}'?"
                display_key = "Fluid (Jacket)"
                display_value = value

            elif param_upper == "VOLUME (NOMINAL)" and field == "INNER VESSEL":
                question = f"Is value for VOLUME (NOMINAL) in INNER VESSEL is equal to '{value}'?"
                display_key = "Volume NOMINAL (Inner Vessel)"
                display_value = value

            elif param_upper == "VOLUME (NOMINAL)" and field == "JACKET":
                question = f"Is value for VOLUME (NOMINAL) in Jacket is equal to '{value}'?"
                display_key = "Volume NOMINAL (Jacket)"
                display_value = value
            
            elif param_upper == "VOLUME (FULL)" and field == "INNER VESSEL":
                question = f"Is value for VOLUME (FULL) in INNER VESSEL is equal to '{value}'?"
                display_key = "Volume FULL (Inner Vessel)"
                display_value = value

            elif param_upper == "VOLUME (FULL)" and field == "JACKET":
                question = f"Is value for VOLUME (FULL) in Jacket is equal to '{value}'?"
                display_key = "Volume FULL (Jacket)"
                display_value = value
            
            elif param_upper == "OPERATING TEMPERATURE" and field == "INNER VESSEL":
                question = f"Is the operating temperature of the Inner Vessel '{value}'?"
                display_key = "Operating Temperature (Inner Vessel)"
                display_value = value

            elif param_upper == "OPERATING TEMPERATURE" and field == "JACKET":
                question = f"Is the oeprating Temperature of Jacket '{value}'?"
                display_key = "Operating Temperature (Jacket)"
                display_value = value
            
            elif param_upper == "MAX. DESIGN TEMPERATURE" and field == "INNER VESSEL":
                question = f"Is value for MAX. DESIGN TEMPERATURE in INNER VESSEL is eqaul to '{value}'?"
                display_key = "Max Design Temperature (Inner Vessel)"
                display_value = value

            elif param_upper == "MAX. DESIGN TEMPERATURE" and field == "JACKET":
                question = f"Is value for MAX. DESIGN TEMPERATURE in Jacket is eqaul to '{value}'?"
                display_key = "Max Design Temperature (Jacket)"
                display_value = value
            
            elif param_upper == "MIN. DESIGN TEMPERATURE" and field == "INNER VESSEL":
                question = f"Is value for MIN. DESIGN TEMPERATURE in INNER VESSEL is eqaul to '{value}'?"
                display_key = "Min Design Temperature (Inner Vessel)"
                display_value = value

            elif param_upper == "MIN. DESIGN TEMPERATURE" and field == "JACKET":
                question = f"Is value for MIN. DESIGN TEMPERATURE in Jacket is eqaul to '{value}'?"
                display_key = "Min Design Temperature (Jacket)"
                display_value = value

            elif param_upper == "MAX. ALLOWABLE WORKING PRESSURE\n(DESIGN PRESSURE)" and field == "INNER VESSEL":
                question = f"Is value for MAX. ALLOWABLE WORKING PRESSURE (DESIGN PRESSURE) in INNER VESSEL is equal to '{value}'?"
                display_key = "Max. Allowable Working Pressure / Design Pressure (INNER VESSEL)"
                display_value = value

            elif param_upper == "MAX. ALLOWABLE WORKING PRESSURE\n(DESIGN PRESSURE)" and field == "JACKET":
                question = f"Is value for MAX. ALLOWABLE WORKING PRESSURE (DESIGN PRESSURE) in JACKET is equal to '{value}'?"
                display_key = "Max. Allowable Working Pressure / Design Pressure (Jacket)"
                display_value = value

            elif param_upper == "PRESSURE\nHYDROSTATIC TEST (AFTER\nLINING)\nDURATION" and field == "INNER VESSEL":
                question = f"Is value of PRESSURE HYDROSTATIC TEST DURATION in INNER VESSEL equal to '{value}'?"
                display_key = "Pressure Hydrostatic Test After Lining and Duration (INNER VESSEL)"
                display_value = value

            elif param_upper == "PRESSURE\nHYDROSTATIC TEST (AFTER\nLINING)\nDURATION" and field == "JACKET":
                question = f"Is value of PRESSURE HYDROSTATIC TEST DURATION in JACKET equal to '{value}'?"
                display_key = "Pressure Hydrostatic Test After Lining and Duration (Jacket)"
                display_value = value
            
            else:
                question = f"Is {key_path} has value equals to '{value}'?"
                display_key = param
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

def generate_comparison_questions_ga(standard_ga_data: dict, key_section_map: dict) -> list[dict]:
    print("🔍 Starting question generation...")

    questions = []
    INVALID_VALUES = {"", "N/A", "NA", "NONE", "NULL", "-", "NOT APPLICABLE", "----", "-----"}

    # Separate design data keys and others
    design_data_keys = [k for k in key_section_map if k.startswith("Design Data")]
    other_keys = [k for k in key_section_map if not k.startswith("Design Data")]

    # Generate questions for design data ONCE
    if design_data_keys:
        design_data_list = standard_ga_data.get("Design Data", [])
        section = key_section_map[design_data_keys[0]]  # All design data keys have same section usually
        questions.extend(generate_design_data_questions(design_data_list, section))

    # Generate questions for other keys normally
    for key_path in other_keys:
        section = key_section_map[key_path]
        standard_value = get_ga_nested_value(standard_ga_data, key_path)

        if standard_value is None:
            all_values = get_all_nested_values(standard_ga_data, key_path)
        else:
            all_values = [standard_value]

        cleaned_values = []
        for val in all_values:
            if isinstance(val, str):
                val_stripped = val.strip().upper()
                cleaned_values.append("No Value" if val_stripped in INVALID_VALUES else val.strip())
            elif val is None:
                cleaned_values.append("No Value")
            elif isinstance(val, dict):
                cleaned_values.append(json.dumps(val, separators=(", ", ": ")))
            else:
                cleaned_values.append(str(val))

        for value in cleaned_values:
            question = f"{key_path} is '{value}' in the provided context?"
            questions.append({
                "question": question,
                "section": section,
                "key": key_path,
                "expected_value": value,
                "display_key": key_path.split("->")[-1].strip(),
                "display_value": value
            })

    print(f"\n✅ Total questions generated: {len(questions)}")
    return questions

class GAtoGAComparisonService:
    def __init__(self):
        self.checker = Check()

    async def process_comparison_ga(self, ga1_content,ga2_content) -> Dict:
        try:
            # STEP 1: Parse input JSONs
            ga1_data = parse_json_content(ga1_content)
            ga2_data = parse_json_content(ga2_content)
            # ga1_data = json.loads(ga1_content)  # Standard GA (used for questions)
            # ga2_data = json.loads(ga2_content)  # Target GA (used for answers)

            # Save GA1 raw data
            with open("data/flattened_files/ga1_raw_data.json", "w", encoding="utf-8") as f:
                json.dump(ga1_data, f, indent=2)

            # STEP 2: Flatten GA2 data (context source)
            ga2_documents = self.checker.flatten_json_new(ga2_data)

            # Dump for examination
            doc_list = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in ga2_documents]
            with open("data/flattened_files/flattened_ga2_documents.json", "w", encoding="utf-8") as f:
                json.dump(doc_list, f, indent=2, ensure_ascii=False)

            # STEP 3: Create vectorstore
            collection_name = sanitize_filename(list(ga2_data.keys())[0])
            vectorstore = self.checker.create_vectorstore_using_data(ga2_documents, collection_name=collection_name)

            root_key = list(ga1_data.keys())[0]
            nested_ga1 = ga1_data[root_key]

            root_key_2 = list(ga2_data.keys())[0]
            nested_ga2 = ga2_data[root_key_2]

            # STEP 4: Define KEY_SECTION_MAPPING (you can later move this to a config)
            KEY_SECTION_MAPPING = {
                "Material of Construction ->INNERVESSEL ->SHELL, HEADS AND BLIND COVER": "material_of_construction",
                "Material of Construction ->INNERVESSEL ->WELDING NECKS FOR BODY FLANGE & NOZZLES": "material_of_construction",
                "Material of Construction ->INNERVESSEL ->SPLIT FLANGES": "material_of_construction",
                "Material of Construction ->INNERVESSEL ->GASKET FOR BODY FLANGE & NOZZLES": "material_of_construction",
                "Material of Construction ->INNERVESSEL ->FASTENERS": "material_of_construction",
                "Material of Construction ->JACKET ->SHELL, HEAD": "material_of_construction",
                "Material of Construction ->JACKET ->NOZZLE NECKS": "material_of_construction",
                "Material of Construction ->JACKET ->SORF FLANGES": "material_of_construction",
                "Material of Construction ->JACKET ->COUPLINGS & PLUGS": "material_of_construction",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> WIND LOAD": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> SEISMIC LOADING": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> HEAT TRANSFER AREA": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> TARE WEIGHT ": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> WEIGHT FULL OF WATER ": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> FASTENERS": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> QNTY": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> CLIENT": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> PO NO. ": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> ADDRESS": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> TITLE ": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> DRG. NO.": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> CALCULATED RPM": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> CORROSION ALLOWANCE -> GLASSED SURFACE": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> CORROSION ALLOWANCE -> WETTED WITH JKT FLUID": "key_value_pairs",
                "Key-Value Pairs -> KEY-VALUE PAIRS -> CORROSION ALLOWANCE -> NON WETTED SURFACE": "key_value_pairs",
            }

            design_data = nested_ga1.get("Design Data", [])
            print(design_data)
            KEY_SECTION_MAPPING.update(build_design_data_key_section_map(design_data))

            top_key = list(ga1_data.keys())[0]
            
            questions = generate_comparison_questions_ga(nested_ga1, KEY_SECTION_MAPPING)

            comparison_report = []

            start_time = time.perf_counter()
            random.shuffle(questions)
            for q in questions:
                question = q["question"]
                section = q["section"]
                answer = await asyncio.to_thread(
                    self.checker.report_over_context_ga_to_ga,
                    question,
                    section,
                    vectorstore
                )
                answer_str = answer.content if hasattr(answer, "content") else str(answer)

                comparison_report.append({
                    "question": question,
                    "section": section,
                    "expected_value": q["expected_value"],
                    "key": q["key"],
                    "answer": answer_str,
                    "display_key": q.get("display_key", q["key"]),
                    "display_value": q.get("display_value", q["expected_value"])
                })

            #----------------- Nozzle Comparison section------------------
            nozzle_comparison_result = []
            try:
                standard_nozzle = nested_ga1.get("Nozzle Data",[])
                target_nozzle = nested_ga2.get("Nozzle Data", [])

                if isinstance(standard_nozzle,list) and isinstance(target_nozzle,list):
                    nozzle_comparison_result = compare_nozzle_data(standard_nozzle,target_nozzle)
            except Exception as e:
                print(f"Nozzle Comparison Failed: {str(e)}")
            
            #--------------- Part List Comparison section ----------------
            part_list_comparison_result = []
            try:
                standard_parts = nested_ga1.get("Part List", [])
                target_parts = nested_ga2.get("Part List", [])

                if isinstance(standard_parts, list) and isinstance(target_parts, list):
                    part_list_comparison_result = compare_part_list(standard_parts, target_parts)
            except Exception as e:
                print(f"Part List Comparison Failed: {str(e)}")

            #------------- General Notes Comparison Section ---------------
            general_notes_comparison_result = []
            try:
                standard_notes = nested_ga1.get("Lining and Notes", {}).get("GENERAL NOTES", [])
                target_notes = nested_ga2.get("Lining and Notes", {}).get("GENERAL NOTES", [])

                standard_notes_str = "\n".join(standard_notes) if isinstance(standard_notes, list) else standard_notes
                
                general_notes_questions = generate_general_notes_questions(standard_notes_str)

                # for general_question in general_notes_questions:
                #     result_json = self.checker.report_over_context_ga_to_ga(
                #         question=general_question,
                #         section="lining_and_notes",
                #         vectorstore=vectorstore
                #     )
                #     general_notes_comparison_result.append(result_json)
            except Exception as e:
                print(f"Error Processing General Notes comparison: {e}")

            end_time = time.perf_counter()
            print(f"✅ Total time taken for batch processing: {end_time - start_time:.2f} seconds")

            return {
                "success": True,
                "comparison_report": comparison_report,
                "nozzle_comparison_result":nozzle_comparison_result,
                "part_list_comparison_result":part_list_comparison_result,
                "general_notes_comparison_result":general_notes_comparison_result,
                "standard_notes":standard_notes
            }

        except Exception as e:
            print(f"❌ GA-to-GA Comparison Exception: {str(e)}")
            raise HTTPException(status_code=500, detail=f"GA-to-GA comparison failed: {str(e)}")