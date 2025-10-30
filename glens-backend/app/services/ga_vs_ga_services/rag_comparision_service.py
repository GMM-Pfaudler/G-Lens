from collections import defaultdict
import random
import ollama
import json,re,time
from typing import List, Dict,Any
from fastapi import HTTPException
from app.services.ofn_vs_ga_services.ollama_rag import Check
from app.services.ga_vs_ga_services.question_generator_helper import generate_comparison_questions_with_keys


def get_all_nested_values(data, key_path: str, separator: str = " -> "): # real one
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

def sanitize_filename(filename: str) -> str: # to sanatize name of collection before saving
    # Remove leading/trailing whitespace
    filename = filename.strip()
    
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")
    
    # Remove any invalid characters (anything not a letter, number, underscore, or hyphen)
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    
    # Ensure the name starts and ends with an alphanumeric character
    if not filename[0].isalnum():
        filename = filename.lstrip("._-")
    if not filename[-1].isalnum():
        filename = filename.rstrip("._-")
    
    # Ensure the filename length is within the acceptable range (3-512 characters)
    if len(filename) < 3:
        raise ValueError("Filename is too short after sanitization")
    
    if len(filename) > 512:
        filename = filename[:512]  # Truncate to 512 characters if necessary
    
    return filename

def get_nested_value(data: dict, key_path: str, separator: str = " -> "): # User in helper in real function
    keys = [key.strip() for key in key_path.split(separator)]  # Clean up spaces
    for key in keys:
        # print(f"Looking for '{key}' in data: {data}")  # Debug print
        if isinstance(data, dict):
            if key in data:
                data = data[key]
            else:
                # print(f"[Missing] Key '{key}' not found in current level.")
                return None
        else:
            # print(f"[Invalid] Expected dict but found {type(data)} at key '{key}'")
            return None
    return data

def get_ga_nested_value(data: dict, key_path: str, separator: str = "->"):
    keys = [key.strip() for key in key_path.split(separator)]

    for i, key in enumerate(keys):
        if isinstance(data, dict):
            # print(f"🔑 Looking for key '{key}' at level {i} in dict keys: {list(data.keys())}")
            if key in data:
                data = data[key]
            else:
                # print(f"❌ Key '{key}' not found at level {i}")
                return None
        else:
            print(f"❌ Expected dict at level {i}, got {type(data)}")
            return None
    # print(f"✅ Final resolved value: {data}")
    return data

def generate_comparison_questions(ofn_data: dict, key_section_map: dict) -> list[dict]:
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
            # Check for the special case of "RCI"
            if key_path == 'Agitator -> Specific Gravity':
                question = f"Fluid -> Specific Gravity is '{value}' in the provided context?"
            elif key_path == "tables -> agitator_details -> agitator_type" and value.upper().strip() == "RCI":
                display_value = "RCI (Impeller)"
                question = f"{key_path} is '{display_value}' in the provided context?"
            elif key_path == "Capacity":
                match = re.search(r'(\d+[A-Za-z]+)', value)
                if match:
                    capacity = match.group(1)
                    display_value = f"{capacity}"
                else:
                    display_value = value
                question = f"{key_path} is '{display_value}' in the provided context?"
            elif key_path == "Material of Construction -> Hand/Manhole Cover" and value.upper().strip() == "MSGL":
                display_value = "GL"
                question = f"{key_path} is '{display_value}' in the provided context?"
            else:
                question = f"{key_path} is '{value}' in the provided context?"

            questions.append({
                "question": question,
                "section": section,
                "key": key_path,
                "expected_value": value
            })

    return questions

def generate_nozzle_questions(ofn_data: dict) -> list[dict]: # ----------------- previoulsy used stable version -------------------------------------------
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

class ComparisonService: #------- real One
    def __init__(self):
        self.checker = Check()
        self.collection_name = None

    def process_comparison(self, ga_content: bytes, ofn_content: bytes) -> Dict:
        try:
            ga_data = json.loads(ga_content.decode("utf-8"))
            with open(r"data\flattened_files\ga_raw_data.json","w",encoding='utf-8') as f:
                json.dump(ga_data,f,indent=2)

            ofn_data = json.loads(ofn_content.decode("utf-8"))
            ga_documents = self.checker.flatten_json_new(ga_data)

            doc_list = [
                {"page_content": doc.page_content, "metadata": doc.metadata}
                for doc in ga_documents
            ]

            with open(r"data\flattened_files\flattened_ga_documents.json", "w", encoding="utf-8") as f:
                json.dump(doc_list, f, indent=2, ensure_ascii=False)

            self.collection_name = sanitize_filename(list(ga_data.keys())[0])
            vectorstore = self.checker.create_vectorstore_using_data(ga_documents, collection_name=self.collection_name)

            KEY_SECTION_MAPPING = {
                "Capacity": "design_data",
                "Glass": "lining_and_notes",
                "Jacket Type":"part_list",
                "Design Pressure -> Inner Vessel": "design_data",
                "Design Pressure -> Jacket": "design_data",
                "Design Temperature -> Inner Vessel": "design_data",
                "Design Temperature -> Jacket": "design_data",
                "NDT -> Inner Vessel": "lining_and_notes",
                "NDT -> Jacket": "lining_and_notes",
                "Paint" : "lining_and_notes",
                "Corrosion Allowance -> Glassed Surface":"key_value_pairs",
                "Corrosion Allowance -> Wetted With Jacket Fluid":"key_value_pairs",
                "Corrosion Allowance -> Non Wetted Surface":"key_value_pairs",
                "Material of Construction -> Shell, Head":"material_of_construction",
                "Material of Construction -> Nozzle Necks & Body Flange":"material_of_construction",
                "Material of Construction -> Split Flanges":"material_of_construction",
                "Material of Construction -> Body Flange C-Clamps":"part_list",
                "Material of Construction -> Hand/Manhole C-Clamps":"part_list",
                "Material of Construction -> Fasteners -> Pressure Part":"material_of_construction", 
                "Material of Construction -> Fasteners -> Non-Pressure Part":"material_of_construction",
                "Material of Construction -> Gasket":"material_of_construction",
                "Material of Construction -> Hand/Manhole Cover":"part_list",
                "Material of Construction -> Hand/Manhole Protection Ring":"nozzle_data",
                "Material of Construction -> Spring Balance Assembly":"part_list",
                "Material of Construction -> Sight/Light Glass Flanges":"part_list",
                "Material of Construction -> Earthing":"part_list",
                "Material of Construction -> Lantern Support":"part_list",
                "Material of Construction -> Lantern Guard":"part_list",
                "Material of Construction -> Drive Base Ring":"part_list",
                "Material of Construction -> Drive Hood":"material_of_construction",
                "Material of Construction -> Jacket (Shell, Head)":"material_of_construction",
                "Material of Construction -> Jacket Nozzle":"material_of_construction",
                "Material of Construction -> Jacket Coupling+Plug":"material_of_construction",
                "Nozzles -> Bottom Outlet Valve":"part_list",
                "Nozzles -> Jacket Nozzle":"part_list",
                "Support": "part_list",
                "Agitator -> Viscosity":"design_data",
                "Agitator -> Specific Gravity":"design_data",
                "Agitator -> Flight":"part_list",
                "Agitator -> RPM":"key_value_pairs",
                "Agitator -> Shaft Diameter":"part_list",
                "tables -> agitator_details -> agitator_type": "part_list",
                "Baffle": "part_list",
                "Drive -> Gear Box":"drive_data",
                "Drive -> Motor":"drive_data",
                "Drive -> Shaft Closure -> Type":"part_list",
                "Drive -> Thermosyphon System Make":"part_list",
                "Drive -> Thermosyphon System Material":"part_list",
                
            }

            NOZZLE_KEY_SECTION_MAPPING = {
                "tables -> nozzles_details -> nozzle_no": "nozzle_data"
            }

            questions = generate_comparison_questions_with_keys(ofn_data=ofn_data, key_section_map=KEY_SECTION_MAPPING)
            q = generate_nozzle_questions(ofn_data=ofn_data)

            questions.extend(q)
            random.shuffle(questions)
            results = []

            start_time = time.perf_counter()

            for q in questions:
                question = q["question"]
                section = q["section"]
                # print(f"\n\nQue: {question}\n")
                answer = self.checker.report_over_context(question=question, section=section, vectorstore=vectorstore)
                print(answer)
                answer_str = answer.content if hasattr(answer, "content") else str(answer)

            
                results.append({
                    "question": question,
                    "section": section,
                    "expected_value": q["expected_value"],
                    "key": q["key"],
                    "display_key": q.get("display_key", q["key"]),
                    "display_value": q.get("display_value", q["expected_value"]),
                    "answer": answer_str
                })

            end_time = time.perf_counter()
            print(f"✅ Total time taken for batch processing: {end_time - start_time:.2f} seconds")

            return {"success": True, "comparison_report": results}

        except Exception as e:
            print(f"❌ Exception in process_comparison: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")
        
    def format_history(self, msg: str, history: list[list[str, str]], system_prompt: str = None):
        chat_history = [{"role": "system", "content":system_prompt}]
        for query, response in history:
            chat_history.append({"role": "user", "content": query})
            chat_history.append({"role": "assistant", "content": response})  
        chat_history.append({"role": "user", "content": msg})
        return chat_history

    def generate_response(self, data):
        msg = data['msg']
        history = data['history']
        # section = f"{history[0][0].lower().split(" ")[0]}_{history[0][0].lower().split(" ")[1]}"
        section = data['section']
        collection_name = data['collection_name']
        # chat_history = self.format_history(msg, history, None)
        vectorstore = self.checker.load_vectorstore(collection_name=collection_name)
        res = self.checker.chat_over_context(msg, section=section, vectorstore=vectorstore)
        # print(res)
        # response = ollama.chat(model='llama3.2:latest', stream=True, messages=chat_history)
        # message = ""
        # for partial_resp in response:
        #     token = partial_resp["message"]["content"]
        #     message += token
        #     return message
        # return res
        return {"text": res}