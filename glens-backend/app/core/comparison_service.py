import asyncio
import json,os
from app.utils.ofn_vs_ga_utils.file_utils import sanitize_filename
from typing import Dict
from app.services.ofn_vs_ga_services.ofn_question_generator_service import generate_comparison_questions_with_keys,generate_nozzle_questions
from fastapi import HTTPException
import random,time
from app.services.ofn_vs_ga_services.ollama_rag import Check
from app.core.ws_manager import send_ws_message

class ComparisonService: #------- real One
    def __init__(self):
        self.checker = Check()
        self.collection_name = None

    # def process_comparison(self, ga_data: dict, ofn_data: dict) -> Dict:
    #     try:
    #         print("🔍 DEBUG -> Type GA:", type(ga_data), "Length:", len(ga_data))
    #         print("🔍 DEBUG -> Type OFN:", type(ofn_data), "Length:", len(ofn_data))
    #         print("🔍 GA content (first 200 chars):", str(ga_data)[:200])
    #         print("🔍 OFN content (first 200 chars):", str(ofn_data)[:200])

    #         # Ensure folder exists
    #         os.makedirs(r"data\flattened_files", exist_ok=True)

    #         # Save GA raw JSON
    #         with open(r"data\flattened_files\ga_raw_data.json", "w", encoding="utf-8") as f:
    #             json.dump(ga_data, f, indent=2)

    #         # Flatten GA
    #         ga_documents = self.checker.flatten_json_new(ga_data)
    #         doc_list = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in ga_documents]

    #         with open(r"data\flattened_files\flattened_ga_documents.json", "w", encoding="utf-8") as f:
    #             json.dump(doc_list, f, indent=2, ensure_ascii=False)


    #         self.collection_name = sanitize_filename(list(ga_data.keys())[0])
    #         vectorstore = self.checker.create_vectorstore_using_data(ga_documents, collection_name=self.collection_name)

    #         KEY_SECTION_MAPPING = {
    #             "Capacity": "design_data",
    #             # "Glass": "lining_and_notes",
    #             # "Jacket Type":"part_list",
    #             # "Design Pressure -> Inner Vessel": "design_data",
    #             # "Design Pressure -> Jacket": "design_data",
    #             # "Design Temperature -> Inner Vessel": "design_data",
    #             # "Design Temperature -> Jacket": "design_data",
    #             # "NDT -> Inner Vessel": "lining_and_notes",
    #             # "NDT -> Jacket": "lining_and_notes",
    #             # "Paint" : "lining_and_notes",
    #             # "Corrosion Allowance -> Glassed Surface":"key_value_pairs",
    #             # "Corrosion Allowance -> Wetted With Jacket Fluid":"key_value_pairs",
    #             # "Corrosion Allowance -> Non Wetted Surface":"key_value_pairs",
    #             # "Material of Construction -> Shell, Head":"material_of_construction",
    #             # "Material of Construction -> Nozzle Necks & Body Flange":"material_of_construction",
    #             # "Material of Construction -> Split Flanges":"material_of_construction",
    #             # "Material of Construction -> Body Flange C-Clamps":"part_list",
    #             # "Material of Construction -> Hand/Manhole C-Clamps":"part_list",
    #             # "Material of Construction -> Fasteners -> Pressure Part":"material_of_construction", 
    #             # "Material of Construction -> Fasteners -> Non-Pressure Part":"material_of_construction",
    #             # "Material of Construction -> Gasket":"material_of_construction",
    #             # "Material of Construction -> Hand/Manhole Cover":"part_list",
    #             # "Material of Construction -> Hand/Manhole Protection Ring":"nozzle_data",
    #             # "Material of Construction -> Spring Balance Assembly":"part_list",
    #             # "Material of Construction -> Sight/Light Glass Flanges":"part_list",
    #             # "Material of Construction -> Earthing":"part_list",
    #             # "Material of Construction -> Lantern Support":"part_list",
    #             # "Material of Construction -> Lantern Guard":"part_list",
    #             # "Material of Construction -> Drive Base Ring":"part_list",
    #             # "Material of Construction -> Drive Hood":"material_of_construction",
    #             # "Material of Construction -> Jacket (Shell, Head)":"material_of_construction",
    #             # "Material of Construction -> Jacket Nozzle":"material_of_construction",
    #             # "Material of Construction -> Jacket Coupling+Plug":"material_of_construction",
    #             # "Nozzles -> Bottom Outlet Valve":"part_list",
    #             # "Nozzles -> Jacket Nozzle":"part_list",
    #             # "Support": "part_list",
    #             # "Agitator -> Viscosity":"design_data",
    #             # "Agitator -> Specific Gravity":"design_data",
    #             # "Agitator -> Flight":"part_list",
    #             # "Agitator -> RPM":"key_value_pairs",
    #             # "Agitator -> Shaft Diameter":"part_list",
    #             # "tables -> agitator_details -> agitator_type": "part_list",
    #             # "Baffle": "part_list",
    #             # "Drive -> Gear Box":"drive_data",
    #             # "Drive -> Motor":"drive_data",
    #             # "Drive -> Shaft Closure -> Type":"part_list",
    #             # "Drive -> Thermosyphon System Make":"part_list",
    #             # "Drive -> Thermosyphon System Material":"part_list",
                
    #         }

    #         NOZZLE_KEY_SECTION_MAPPING = {
    #             "tables -> nozzles_details -> nozzle_no": "nozzle_data"
    #         }

    #         questions = generate_comparison_questions_with_keys(ofn_data=ofn_data, key_section_map=KEY_SECTION_MAPPING)
    #         q = generate_nozzle_questions(ofn_data=ofn_data)

    #         questions.extend(q)
    #         random.shuffle(questions)
    #         results = []

    #         start_time = time.perf_counter()

    #         for q in questions:
    #             question = q["question"]
    #             section = q["section"]
    #             # print(f"\n\nQue: {question}\n")
    #             answer = self.checker.report_over_context(question=question, section=section, vectorstore=vectorstore)
    #             print(answer)
    #             answer_str = answer.content if hasattr(answer, "content") else str(answer)

            
    #             results.append({
    #                 "question": question,
    #                 "section": section,
    #                 "expected_value": q["expected_value"],
    #                 "key": q["key"],
    #                 "display_key": q.get("display_key", q["key"]),
    #                 "display_value": q.get("display_value", q["expected_value"]),
    #                 "answer": answer_str
    #             })

    #         end_time = time.perf_counter()
    #         print(f"✅ Total time taken for batch processing: {end_time - start_time:.2f} seconds")

    #         return {"success": True, "comparison_report": results}

    #     except Exception as e:
    #         print(f"❌ Exception in process_comparison: {str(e)}")
    #         raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

    def process_comparison(self, ga_data: dict, ofn_data: dict, progress_callback=None) -> Dict:
        try:
            print("🔍 DEBUG -> Type GA:", type(ga_data), "Length:", len(ga_data))
            print("🔍 DEBUG -> Type OFN:", type(ofn_data), "Length:", len(ofn_data))

            os.makedirs(r"data\flattened_files", exist_ok=True)

            # Step 1: Save GA raw JSON
            with open(r"data\flattened_files\ga_raw_data.json", "w", encoding="utf-8") as f:
                json.dump(ga_data, f, indent=2)

            if progress_callback:
                progress_callback(5, "GA JSON saved and flattening started")

            # Step 2: Flatten GA
            ga_documents = self.checker.flatten_json_new(ga_data)
            doc_list = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in ga_documents]

            with open(r"data\flattened_files\flattened_ga_documents.json", "w", encoding="utf-8") as f:
                json.dump(doc_list, f, indent=2, ensure_ascii=False)

            if progress_callback:
                progress_callback(10, "GA data flattened successfully")

            # Step 3: Create vectorstore
            self.collection_name = sanitize_filename(list(ga_data.keys())[0])
            vectorstore = self.checker.create_vectorstore_using_data(ga_documents, collection_name=self.collection_name)

            if progress_callback:
                progress_callback(15, "Vectorstore created")

            # Step 4: Generate questions
            KEY_SECTION_MAPPING = {"Capacity": "design_data","Glass": "lining_and_notes",
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
            NOZZLE_KEY_SECTION_MAPPING = {"tables -> nozzles_details -> nozzle_no": "nozzle_data"}

            questions = generate_comparison_questions_with_keys(ofn_data=ofn_data, key_section_map=KEY_SECTION_MAPPING)
            q = generate_nozzle_questions(ofn_data=ofn_data)
            questions.extend(q)
            random.shuffle(questions)

            total = len(questions)
            if progress_callback:
                progress_callback(20, f"Generated {total} questions for comparison")

            results = []
            start_time = time.perf_counter()

            # Step 5: Iterate through questions
            for idx, q in enumerate(questions, start=1):
                question = q["question"]
                section = q["section"]

                answer = self.checker.report_over_context(question=question, section=section, vectorstore=vectorstore)
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

                # 🔄 Progress update based on number processed
                if progress_callback:
                    pct = int(20 + (idx / total) * 80)  # map 20→100% dynamically
                    progress_callback(pct, f"Processed {idx}/{total} questions")

            end_time = time.perf_counter()
            print(f"✅ Total time taken: {end_time - start_time:.2f}s")

            if progress_callback:
                progress_callback(100, "Comparison completed successfully")

            return {"success": True, "comparison_report": results}

        except Exception as e:
            print(f"❌ Exception in process_comparison: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")
    
    # async def process_comparison_async(self, ga_data: dict, ofn_data: dict) -> Dict:
    #     try:
    #         print("🔍 DEBUG -> Type GA:", type(ga_data), "Length:", len(ga_data))
    #         print("🔍 DEBUG -> Type OFN:", type(ofn_data), "Length:", len(ofn_data))

    #         os.makedirs(r"data\flattened_files", exist_ok=True)

    #         # Save GA raw JSON
    #         with open(r"data\flattened_files\ga_raw_data.json", "w", encoding="utf-8") as f:
    #             json.dump(ga_data, f, indent=2)

    #         # Flatten GA
    #         ga_documents = self.checker.flatten_json_new(ga_data)
    #         doc_list = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in ga_documents]

    #         with open(r"data\flattened_files\flattened_ga_documents.json", "w", encoding="utf-8") as f:
    #             json.dump(doc_list, f, indent=2, ensure_ascii=False)

    #         self.collection_name = sanitize_filename(list(ga_data.keys())[0])
    #         vectorstore = self.checker.create_vectorstore_using_data(
    #             ga_documents, collection_name=self.collection_name
    #         )

    #         KEY_SECTION_MAPPING = {
    #             "Capacity": "design_data",
    #             # ... keep others as needed ...
    #         }

    #         NOZZLE_KEY_SECTION_MAPPING = {
    #             "tables -> nozzles_details -> nozzle_no": "nozzle_data"
    #         }

    #         # Generate all questions
    #         questions = generate_comparison_questions_with_keys(ofn_data=ofn_data, key_section_map=KEY_SECTION_MAPPING)
    #         questions.extend(generate_nozzle_questions(ofn_data=ofn_data))
    #         random.shuffle(questions)

    #         start_time = time.perf_counter()

    #         # ⚡ Run Ollama comparisons asynchronously
    #         async def process_question(q):
    #             try:
    #                 answer = await self.checker.report_over_context_async(
    #                     question=q["question"],
    #                     section=q["section"],
    #                     vectorstore=vectorstore
    #                 )
    #                 return {
    #                     "question": q["question"],
    #                     "section": q["section"],
    #                     "expected_value": q["expected_value"],
    #                     "key": q["key"],
    #                     "display_key": q.get("display_key", q["key"]),
    #                     "display_value": q.get("display_value", q["expected_value"]),
    #                     "answer": answer,
    #                 }
    #             except Exception as e:
    #                 return {
    #                     "question": q["question"],
    #                     "section": q["section"],
    #                     "error": str(e),
    #                 }

    #         # ✅ Run all async tasks with limited concurrency (so Ollama isn’t overloaded)
    #         semaphore = asyncio.Semaphore(5)  # adjust as needed

    #         async def sem_task(q):
    #             async with semaphore:
    #                 return await process_question(q)

    #         tasks = [sem_task(q) for q in questions]
    #         results = await asyncio.gather(*tasks)

    #         end_time = time.perf_counter()
    #         print(f"✅ Total time taken for batch processing: {end_time - start_time:.2f} seconds")

    #         return {"success": True, "comparison_report": results}

    #     except Exception as e:
    #         print(f"❌ Exception in process_comparison: {str(e)}")
    #         raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}") 


    # async def process_comparison_async(self, ga_data: dict, ofn_data: dict, job_id: str) -> Dict:
    #     """
    #     Process GA vs OFN comparison asynchronously with live WebSocket progress updates.
    #     """
    #     try:
    #         total_questions = 0
    #         start_time = time.perf_counter()

    #         # -------------------------
    #         # Step 1: Save GA raw JSON
    #         # -------------------------
    #         os.makedirs(r"data\flattened_files", exist_ok=True)
    #         with open(r"data\flattened_files\ga_raw_data.json", "w", encoding="utf-8") as f:
    #             json.dump(ga_data, f, indent=2)
    #         await send_ws_message(job_id, {"status": "running", "progress": 5, "message": "GA JSON saved"})

    #         # -------------------------
    #         # Step 2: Flatten GA JSON
    #         # -------------------------
    #         ga_documents = self.checker.flatten_json_new(ga_data)
    #         doc_list = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in ga_documents]
    #         with open(r"data\flattened_files\flattened_ga_documents.json", "w", encoding="utf-8") as f:
    #             json.dump(doc_list, f, indent=2, ensure_ascii=False)
    #         await send_ws_message(job_id, {"status": "running", "progress": 10, "message": "GA data flattened"})

    #         # -------------------------
    #         # Step 3: Create Vectorstore
    #         # -------------------------
    #         self.collection_name = sanitize_filename(list(ga_data.keys())[0])
    #         vectorstore = self.checker.create_vectorstore_using_data(
    #             ga_documents, collection_name=self.collection_name
    #         )
    #         await send_ws_message(job_id, {"status": "running", "progress": 20, "message": "Vectorstore created"})

    #         # -------------------------
    #         # Step 4: Generate Questions
    #         # -------------------------
    #         KEY_SECTION_MAPPING = {"Capacity": "design_data"}  # extend as needed
    #         NOZZLE_KEY_SECTION_MAPPING = {"tables -> nozzles_details -> nozzle_no": "nozzle_data"}  # extend as needed

    #         questions = generate_comparison_questions_with_keys(ofn_data=ofn_data, key_section_map=KEY_SECTION_MAPPING)
    #         questions.extend(generate_nozzle_questions(ofn_data=ofn_data))
    #         random.shuffle(questions)
    #         total_questions = len(questions)
    #         await send_ws_message(job_id, {"status": "running", "progress": 25, "message": f"Generated {total_questions} comparison questions"})

    #         # -------------------------
    #         # Step 5: Process Questions Async
    #         # -------------------------
    #         semaphore = asyncio.Semaphore(5)  # limit concurrency

    #         async def process_question(idx, q):
    #             try:
    #                 answer = await self.checker.report_over_context_async(
    #                     question=q["question"],
    #                     section=q["section"],
    #                     vectorstore=vectorstore,
    #                     semaphore=semaphore
    #                 )
    #                 progress = 25 + int((idx + 1) / total_questions * 70)  # map to 25%-95% range
    #                 await send_ws_message(job_id, {
    #                     "status": "running",
    #                     "progress": progress,
    #                     "message": f"Processed {idx + 1}/{total_questions} questions"
    #                 })
    #                 return {
    #                     "question": q["question"],
    #                     "section": q["section"],
    #                     "expected_value": q["expected_value"],
    #                     "key": q["key"],
    #                     "display_key": q.get("display_key", q["key"]),
    #                     "display_value": q.get("display_value", q["expected_value"]),
    #                     "answer": answer,
    #                 }
    #             except Exception as e:
    #                 return {"question": q["question"], "section": q["section"], "error": str(e)}

    #         async def sem_task(idx, q):
    #             async with semaphore:
    #                 return await process_question(idx, q)

    #         tasks = [sem_task(idx, q) for idx, q in enumerate(questions)]
    #         results = await asyncio.gather(*tasks)

    #         # -------------------------
    #         # Step 6: Completion
    #         # -------------------------
    #         end_time = time.perf_counter()
    #         await send_ws_message(job_id, {
    #             "status": "completed",
    #             "progress": 100,
    #             "message": f"Comparison completed in {end_time - start_time:.2f}s",
    #             "result": {"success": True, "comparison_report": results}
    #         })

    #         print(f"✅ Total time taken for comparison: {end_time - start_time:.2f} seconds")
    #         return {"success": True, "comparison_report": results}

    #     except Exception as e:
    #         await send_ws_message(job_id, {"status": "error", "error_msg": str(e)})
    #         print(f"❌ Exception in process_comparison_async: {str(e)}")
    #         raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

    async def process_comparison_async(self, ga_data: dict, ofn_data: dict, job_id: str) -> Dict:
        """
        Process GA vs OFN comparison asynchronously with live WebSocket progress updates.
        """
        try:
            total_questions = 0
            start_time = time.perf_counter()

            # -------------------------
            # Step 1: Save GA raw JSON
            # -------------------------
            os.makedirs(r"data\flattened_files", exist_ok=True)
            with open(r"data\flattened_files\ga_raw_data.json", "w", encoding="utf-8") as f:
                json.dump(ga_data, f, indent=2)
            await send_ws_message(job_id, {"status": "running", "progress": 5, "message": "GA JSON saved"})

            # -------------------------
            # Step 2: Flatten GA JSON
            # -------------------------
            ga_documents = self.checker.flatten_json_new(ga_data)
            doc_list = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in ga_documents]
            with open(r"data\flattened_files\flattened_ga_documents.json", "w", encoding="utf-8") as f:
                json.dump(doc_list, f, indent=2, ensure_ascii=False)
            await send_ws_message(job_id, {"status": "running", "progress": 10, "message": "GA data flattened"})

            # -------------------------
            # Step 3: Create Vectorstore
            # -------------------------
            self.collection_name = sanitize_filename(list(ga_data.keys())[0])
            vectorstore = self.checker.create_vectorstore_using_data(
                ga_documents, collection_name=self.collection_name
            )
            await send_ws_message(job_id, {"status": "running", "progress": 20, "message": "Vectorstore created"})

            # -------------------------
            # Step 4: Generate Questions
            # -------------------------
            KEY_SECTION_MAPPING = {"Capacity": "design_data","Glass": "lining_and_notes",
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
            NOZZLE_KEY_SECTION_MAPPING = {"tables -> nozzles_details -> nozzle_no": "nozzle_data"}

            questions = generate_comparison_questions_with_keys(ofn_data=ofn_data, key_section_map=KEY_SECTION_MAPPING)
            questions.extend(generate_nozzle_questions(ofn_data=ofn_data))
            random.shuffle(questions)
            total_questions = len(questions)
            await send_ws_message(job_id, {"status": "running", "progress": 25, "message": f"Generated {total_questions} questions"})

            # -------------------------
            # Step 5: Process Questions Async (Batch-based)
            # -------------------------
            results = []
            batch_size = 5  # tune depending on Ollama’s load tolerance

            async def process_question(idx, q):
                try:
                    answer = await self.checker.report_over_context_async(
                        question=q["question"],
                        section=q["section"],
                        vectorstore=vectorstore,
                        job_id=job_id
                    )
                    progress = 25 + int((idx + 1) / total_questions * 70)
                    await send_ws_message(job_id, {
                        "status": "running",
                        "progress": progress,
                        "message": f"Processed {idx + 1}/{total_questions} questions"
                    })
                    return {
                        "question": q["question"],
                        "section": q["section"],
                        "expected_value": q["expected_value"],
                        "key": q["key"],
                        "display_key": q.get("display_key", q["key"]),
                        "display_value": q.get("display_value", q["expected_value"]),
                        "answer": answer,
                    }
                except Exception as e:
                    return {"question": q["question"], "section": q["section"], "error": str(e)}

            # Run in controlled batches to avoid overload
            for i in range(0, total_questions, batch_size):
                batch = questions[i:i + batch_size]
                batch_results = await asyncio.gather(*[process_question(i + j, q) for j, q in enumerate(batch)])
                results.extend(batch_results)
                await asyncio.sleep(0.5)  # short gap to reduce load

            # -------------------------
            # Step 6: Completion
            # -------------------------
            end_time = time.perf_counter()
            await send_ws_message(job_id, {
                "status": "completed",
                "progress": 100,
                "message": f"Comparison completed in {end_time - start_time:.2f}s",
                "result": {"success": True, "comparison_report": results}
            })

            print(f"✅ Total time taken for comparison: {end_time - start_time:.2f} seconds")
            return {"success": True, "comparison_report": results}

        except Exception as e:
            await send_ws_message(job_id, {"status": "error", "error_msg": str(e)})
            print(f"❌ Exception in process_comparison_async: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")
