import ollama,httpx
from ollama import Client
import os,sqlite3
import json,re,time
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_ollama import ChatOllama, OllamaEmbeddings
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain.embeddings.base import Embeddings
from app.utils.ofn_vs_ga_utils.file_utils import sanitize_filename
from app.utils.prompt import build_section_prompt,build_payload
import aiohttp
import asyncio
from langchain.schema import Document
from app.core.ws_manager import send_ws_message

OLLAMA_BASE_URL = "http://192.168.157.82:11434"
# MODEL_NAME = "gemma3n:latest"
MODEL_NAME = "llama3.2:latest"
# MODEL_NAME = "gpt-oss:120b-cloud"

class OllamaEmbeddingWrapper(Embeddings):
    def __init__(self, model="nomic-embed-text:latest"):
        self.model = model

    def embed_documents(self, texts):
        return [get_ollama_embedding(text, model=self.model) or [0.0]*768 for text in texts]

    def embed_query(self, text):
        return get_ollama_embedding(text, model=self.model) or [0.0]*768
    

def get_ollama_embedding(text, model="nomic-embed-text:latest"):
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/embeddings",
            json={"model": model, "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

class Check:
    def __init__(self):
        self.vectorstore = None
    
    def load_vectorstore(self, persist_directory="./chroma_store", collection_name=None):
        embeddings = OllamaEmbeddingWrapper(model="nomic-embed-text:latest")
        collection_name = sanitize_filename(collection_name)
        vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        self.vectorstore = vectorstore
        return self.vectorstore

    def chat_over_context(self, question, section, vectorstore=None):
       
        all_docs = vectorstore._collection.get(
            where={"section": section},
            include=["documents"]
        )["documents"]

        # Reconstruct Document objects
        docs = [Document(page_content=doc) for doc in all_docs]
        context = "\n".join([doc.page_content for doc in docs])
        prompt_chat = (
            f"You are a helpful assistant analyzing technical data from the section '{section}'.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            f"Answer:"
        )

        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt_chat,
            "stream": False
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["response"]
    
    def report_over_context(self, question, section, vectorstore=None):
        
        embeddings = OllamaEmbeddingWrapper(model="nomic-embed-text:latest")
        collection = vectorstore._collection

        nozzle_no = self.extract_nozzle_number_from_question(question)
        query_embedding = embeddings.embed_query(question)

        # Set document filter if nozzle number exists
        if nozzle_no not in ("", "N/A"):
            where_document = {"$contains": f"Nozzle: Ref.: {nozzle_no},"}
        else:
            where_document = None

        # print(f"This is Where Document Contains: {where_document}")
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            where={"section": section},
            where_document=where_document,
            include=["documents", "metadatas"]
        )

        docs = [Document(page_content=doc, metadata=meta) for doc, meta in zip(results["documents"][0], results["metadatas"][0])]
        print(f"Length of Doc is {len(docs)}")
        context = "\n".join([doc.page_content for doc in docs])

        prompt_report = build_section_prompt(section=section,question=question,context=context)

        url = f"{OLLAMA_BASE_URL}/api/generate"
        # print(prompt_report)
        print("----------------------------------------\n")
        # payload = {
        #     "model": MODEL_NAME,
        #     "prompt": prompt_report,
        #     "stream": False,
        #     "temperature": 0.0,
        #     "format": {
        #     "type": "object",
        #     "properties": {
        #         "matched": {"type": "string"},
        #         "section": {"type": "string"},
        #         "matched_value": {"type": "string"},
        #         "closest_match": {"type": "string"},
        #     },
        #     "required": ["matched", "section"]
        #     }
        # }

        payload = build_payload(model_name=MODEL_NAME,prompt=prompt_report)
        

        try:
            response = requests.post(url, json=payload)
            # print(f"Response 1: {response}")
            response.raise_for_status()
            result = response.json()
            # print(f"Result: {result}")
            content = result.get("response", "")
            # print(f"content: {content}")

            final_result = json.loads(content)
            # print(f"Final Result: {final_result}")
            # Ensure valid JSON from model output
            return content

        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"❌ Ollama Error: {e}")
            return {
                "matched": "Error",
                "section": section,
                "error": str(e),
                "response": content if 'content' in locals() else ""
            }
        
    def run_batch_report(self, question_dicts, vectorstore=None, max_workers=5):
        print(f"Thread vectorstore type: {type(vectorstore)}")
        results = [None] * len(question_dicts)

        def process_question(idx, qd):
            try:
                result = self.report_over_context(qd["question"], qd["section"], vectorstore)
            except Exception as e:
                result = {
                    "matched": "Error",
                    "section": qd["section"],
                    "error": str(e),
                }
            return idx, result

        start_time = time.time()  # Start timing

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(process_question, idx, qd)
                for idx, qd in enumerate(question_dicts)
            ]
            for future in as_completed(futures):
                idx, result = future.result()
                results[idx] = result

        end_time = time.time()  # End timing
        print(f"Total time taken for batch report: {end_time - start_time:.2f} seconds")

        return results

    def extract_key_value_from_question(self,question: str) -> tuple[str, str]:
        question = question.strip()

        # 🔹 Handle nozzle-type structured question
        nozzle_match = re.search(r"nozzle '([^']+)' have (\w+) equal to '([^']+)'", question.lower())
        if nozzle_match:
            nozzle_no = nozzle_match.group(1).strip().upper()
            field = nozzle_match.group(2).strip().capitalize()
            value = nozzle_match.group(3).strip()
            ofn_key = f"Nozzles -> {nozzle_no} -> {field}"
            ofn_value = value
            return ofn_key, ofn_value

        # 🔹 Handle flat format: "... -> Field is 'Value' in the provided context?"
        flat_match = re.search(r"is\s+'([^']+)'", question)
        if flat_match:
            ofn_value = flat_match.group(1).strip()
            ofn_key = question.split(' is ')[0].strip()
            return ofn_key, ofn_value

        # ❌ Fallback if parsing fails
        return "N/A", "N/A"
    
    def extract_nozzle_number_from_question(self,question: str) -> str:
        question = question.strip().lower()

        match = re.search(r"nozzle\s+'([^']+)'", question)
        if match:
            return match.group(1).strip().upper()
        
        return "N/A"
    
    def extract_keywords_from_question(self, question: str) -> list[str]:
        match = re.match(r"(.*?)\s+is\s+'(.*?)'\s+in the provided context\?", question)
        if not match:
            return []
        
        key_path = match.group(1)
        value = match.group(2)

        if len(value.strip()) > 2 and value.strip().upper() not in {"YES", "NO", "N/A", "NONE", "NA"}:
            value_tokens = re.findall(r'\b\w+\b', value.upper())
        else:
            value_tokens = []

        parts = re.split(r"->|:|,", key_path)
        key_tokens = [p.strip().upper() for p in parts if len(p.strip()) > 1]
        key_tokens_cleaned = [w for phrase in key_tokens for w in phrase.split() if w not in {"OF", "THE", "AND"}]

        keyword_list = list(set(value_tokens + key_tokens_cleaned))
        return keyword_list

    def flatten_json_new(self, json_data):
        documents = []

        if len(json_data) != 1:
            raise ValueError("Expected JSON to have exactly one top-level key representing the document name.")

        document_name, content = next(iter(json_data.items()))

        # -----------------------------
        # Lining and Notes
        # -----------------------------
        lining_notes = content.get("Lining and Notes", {})

        if "LINING SPECIFICATION" in lining_notes:
            documents.append(Document(
                page_content=lining_notes["LINING SPECIFICATION"],
                metadata={"doc_name": document_name, "section": "lining_and_notes", "field": "LINING SPECIFICATION"}
            ))

        for note in lining_notes.get("GENERAL NOTES", []):
            documents.append(Document(
                page_content=note,
                metadata={"doc_name": document_name, "section": "lining_and_notes", "field": "GENERAL NOTES"}
            ))

        # -----------------------------
        # Part List
        # -----------------------------
        for part in content.get("Part List", []):
            content_str = ", ".join(f"{k}: {v}" for k, v in part.items())
            documents.append(Document(
                page_content=f"Part: {content_str}",
                metadata={"doc_name": document_name, "section": "part_list", "part_no": part.get("part_no")}
            ))

        # -----------------------------
        # Design Data
        # -----------------------------
        for entry in content.get("Design Data", []):
            for key, value in entry.items():
                if key != "Parameter":
                    documents.append(Document(
                        page_content=f"{entry['Parameter']} - {key}: {value}",
                        metadata={"doc_name": document_name, "section": "design_data", "parameter": entry["Parameter"], "field": key}
                    ))

        # -----------------------------
        # Nozzle Data
        # -----------------------------
        for nozzle in content.get("Nozzle Data", []):
            content_str = ", ".join(f"{k}: {v}" for k, v in nozzle.items())
            documents.append(Document(
                page_content=f"Nozzle: {content_str}",
                metadata={"doc_name": document_name, "section": "nozzle_data", "ref": nozzle.get("Ref.")}
            ))

        # -----------------------------
        # Material of Construction
        # -----------------------------
        material_data = content.get("Material of Construction", {})
        for component, fields in material_data.items():
            for part, material in fields.items():
                documents.append(Document(
                    page_content=f"{component} - {part}: {material}",
                    metadata={"doc_name": document_name, "section": "material_of_construction", "component": component, "part": part}
                ))

        kv_pairs = content.get("Key-Value Pairs", {}).get("KEY-VALUE PAIRS", {})

        # Iterate over the key-value pairs
        for key, value in kv_pairs.items():
            if isinstance(value, dict):  # If value is a dictionary (like CORROSION ALLOWANCE)
                for sub_key, sub_value in value.items():
                    documents.append(Document(
                        page_content=f"{key.strip()} - {sub_key.strip()}: {sub_value}",
                        metadata={"doc_name": document_name, "section": "key_value_pairs", "key": f"{key.strip()} - {sub_key.strip()}"}
                    ))
            else:
                documents.append(Document(
                    page_content=f"{key.strip()}: {value}",
                    metadata={"doc_name": document_name, "section": "key_value_pairs", "key": key.strip()}
                ))
        
        drive_data = content.get("Drive Data", {})

        for key, value in drive_data.items():
            documents.append(Document(
                page_content=f"{key}: {value}",
                metadata={
                    "doc_name": document_name,
                    "section": "drive_data",
                    "type": key
                }
            ))

        return documents
    
    def collection_exists_in_chroma(self,collection_name, persist_directory="./chroma_store"):
        sqlite_path = os.path.join(persist_directory, "chroma.sqlite3")
        if not os.path.exists(sqlite_path):
            return False

        try:
            with sqlite3.connect(sqlite_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM collections WHERE name = ?", (collection_name,))
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        
    #----------------------------Test Version for create_vectorstore --------------------------------------------
    def create_vectorstore_using_data(self, flattened_json_data, collection_name):
        persist_dir = "./chroma_store"

        # Use SQLite to check if collection exists
        if self.collection_exists_in_chroma(collection_name, persist_directory=persist_dir):
            print(f"Collection '{collection_name}' already exists. Loading the existing vectorstore.")
            self.vectorstore = self.load_vectorstore(collection_name=collection_name)
            return self.vectorstore

        if not flattened_json_data:
            raise ValueError(f"Flattened JSON data is empty. Cannot create vector store for collection '{collection_name}'.")

        try:
            embeddings = OllamaEmbeddingWrapper(model="nomic-embed-text:latest")
            self.vectorstore = Chroma.from_documents(
                documents=flattened_json_data,
                embedding=embeddings,
                collection_name=collection_name,
                persist_directory=persist_dir
            )
            self.vectorstore.persist()
            print(f"Collection '{collection_name}' created successfully.")
            return self.vectorstore
        except Exception as e:
            print(f"Error creating vectorstore: {str(e)}")
            raise

    def format_history(self, msg: str, history: list[list[str, str]], system_prompt: str = None):
        chat_history = [{"role": "system", "content":system_prompt}]
        for query, response in history:
            chat_history.append({"role": "user", "content": query})
            chat_history.append({"role": "assistant", "content": response})  
        chat_history.append({"role": "user", "content": msg})
        return chat_history

    def chat(self, message):
        if "Design Data".lower() in message.lower():
            return "Now you can ask question about Design Data!"
        else:
            return None

    def generate_response(self, msg: str, history: list[list[str, str]], system_prompt: str=None):
        section_description = self.chat(msg)
        if section_description:
            yield section_description
        else:

            self.checker.chat_over_context
            chat_history = self.format_history(msg, history, system_prompt)
            res = self.chat_over_context(msg, chat_history[0], vectorstore=self.vectorstore)
            print(res)
            response = ollama.chat(model='llama3.2:latest', stream=True, messages=chat_history)
            message = ""
            for partial_resp in response:
                token = partial_resp["message"]["content"]
                message += token
                yield message
    
    def report_over_context_ga_to_ga(self, question, section, vectorstore=None):
    
        embeddings = OllamaEmbeddingWrapper(model="nomic-embed-text:latest")
        collection = vectorstore._collection

        nozzle_no = self.extract_nozzle_number_from_question(question)
        query_embedding = embeddings.embed_query(question)

        # Set document filter if nozzle number exists
        if nozzle_no not in ("", "N/A"):
            where_document = {"$contains": f"Nozzle: Ref.: {nozzle_no},"}
        else:
            where_document = None

        print(f"This is Where Document Contains: {where_document}")
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            where={"section": section},
            where_document=where_document,
            include=["documents", "metadatas"]
        )

        docs = [Document(page_content=doc, metadata=meta) for doc, meta in zip(results["documents"][0], results["metadatas"][0])]
        print(f"Length of Doc is {len(docs)}")
        context = "\n".join([doc.page_content for doc in docs])

        # Prompt instructs the model to return JSON with double quotes — essential for JSON parsing
        if section == "design_data":
            prompt_report = (
                f"You are a detail-oriented assistant helping verify if a specific value is present in the '{section}' section of the following structured technical data.\n\n"
                f"Each entry includes a parameter name, and values for INNER VESSEL and/or JACKET.\n"
                f"You must locate the parameter in the context, then check its corresponding value under the specified section (e.g., INNER VESSEL or JACKET).\n"
                f"Context:\n{context}\n\n"
                f"Question:\n{question}\n\n"
                f"Rules for Answering:\n"
                f"1. Match the exact parameter name.\n"
                f"2. Match the correct sub-section (INNER VESSEL or JACKET) only.\n"
                f"3. If the value in the question is *identical or logically equivalent* to the value in the context (e.g., formatting differences, spacing, case, symbols like °C), return a match.\n"
                f"4. If the value is not present or significantly different in meaning, return the closest value found (if any).\n"
                f"5. Only return a valid JSON. No explanations, comments, or extra text.\n\n"
                f"⚠️ DO NOT infer or hallucinate values.\n"
                f"⚠️ DO NOT copy values from the question unless they appear in the context.\n"
                f"⚠️ DO NOT compare unrelated sections (e.g., INNER VESSEL vs. JACKET).\n"
                f"⚠️ Return full value strings as written in the context.\n\n"
                f"Match format:\n"
                f'{{"matched": "Yes", "section": "{section}", "matched_value": "<copy exact or logically matching value from context>"}}\n\n'
                f"No-match format:\n"
                f'{{"matched": "No", "section": "{section}", "closest_match": "<copy closest value from context>"}}\n\n'
                f"✅ Think carefully and check formatting, spacing, symbols, and number values.\n"
            )
        elif section == "lining_and_notes":
                prompt_report = (
                f"You are a precise assistant helping to compare two technical instructions from the '{section}' section.\n\n"
                f"Your task is to decide whether the *candidate instruction* means the same as the *original instruction*.\n"
                f"Use ONLY the candidate instruction to decide. Do not assume or invent anything.\n\n"
                f"Original Instruction:\n{context}\n\n"
                f"Candidate Instruction:\n{question}\n\n"
                f"Return ONLY a JSON object in this exact format:\n"
                f'{{\n  "matched": "Yes" | "No",\n  "reason": "<short reason explaining the decision>"\n}}\n\n'
                f"Guidelines:\n"
                f"- Say 'Yes' if the candidate clearly means the same, even with slightly different wording.\n"
                f"- Say 'No' if any important part is missing, changed, or unclear.\n"
                f"- Keep the reason short and specific.\n"
                f"- Do NOT hallucinate or assume missing information.\n"
                f"- Return only the JSON — nothing else.\n"
            )
                
        else:
            prompt_report = (
                f"You are a smart assistant helping to check if a value exists in the following context from the '{section}' section:\n\n"
                f"Your job is to decide if the value in the question is already written in the context.\n"
                f"- Only use values from the context. Do not copy from the question unless it also appears in the context.\n"
                f"{context}\n\n"
                f"Here is the question:\n"
                f"{question}\n\n"
                f"- You can say YES if the value in the context means the same thing, even if the words are a little different and some symbols are missing.\n"
                f"- You can say NO if the value is missing or very different, but try to find the closest line in the context.\n\n"
                f"- Take your time, Think Carefully and check whole context before answering."
                f"- **Try to return full values or more detailed in both cases match or closest to reduce the confusion and choose only from context.**"
                f"If it’s a match, reply like this:\n"
                f'{{"matched": "Yes", "section": "{section}", "matched_value": "<copy the logically matching value from the context>"}}\n\n'
                f"If not a match, reply like this:\n"
                f'{{"matched": "No", "section": "{section}", "closest_match": "<copy the closest value from the context>"}}\n\n'
                f"⚠️ Rules:\n"
                f"- Only return a valid JSON. No extra explanation, no comments."
            )


        url = f"{OLLAMA_BASE_URL}/api/generate"
        print(prompt_report)
        print("----------------------------------------\n")
        if section == "lining_and_notes":
            format_schema = {
                "type": "object",
                "properties": {
                    "matched": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": ["matched", "reason"]
            }
        else:
            format_schema = {
                "type": "object",
                "properties": {
                    "matched": {"type": "string"},
                    "section": {"type": "string"},
                    "matched_value": {"type": "string"},
                    "closest_match": {"type": "string"}
                },
                "required": ["matched", "section"]
            }
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt_report,
            "stream": False,
            "temperature": 0.0,
            "format": format_schema
        }

        try:
            response = requests.post(url, json=payload)
            # print(f"Response 1: {response}")
            response.raise_for_status()
            result = response.json()
            # print(f"Result: {result}")
            content = result.get("response", "")
            print(f"content: {content}")

            final_result = json.loads(content)
            print(f"Final Result: {final_result}")
            # Ensure valid JSON from model output
            return content

        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"❌ Ollama Error: {e}")
            return {
                "matched": "Error",
                "section": section,
                "error": str(e),
                "response": content if 'content' in locals() else ""
            }
        
    # async def report_over_context_async(self, question, section, vectorstore=None, semaphore=None):
    #     embeddings = OllamaEmbeddingWrapper(model="nomic-embed-text:latest")
    #     collection = vectorstore._collection

    #     nozzle_no = self.extract_nozzle_number_from_question(question)
    #     query_embedding = embeddings.embed_query(question)

    #     # Build filter
    #     where_document = {"$contains": f"Nozzle: Ref.: {nozzle_no},"} if nozzle_no not in ("", "N/A") else None
    #     print(f"🔍 Document filter applied: {where_document}")

    #     # Query Chroma in a thread to avoid blocking
    #     results = await asyncio.to_thread(
    #         collection.query,
    #         query_embeddings=[query_embedding],
    #         n_results=5,
    #         where={"section": section},
    #         where_document=where_document,
    #         include=["documents", "metadatas"]
    #     )

    #     docs = [Document(page_content=doc, metadata=meta)
    #             for doc, meta in zip(results["documents"][0], results["metadatas"][0])]
    #     print(f"📄 Retrieved {len(docs)} relevant documents.")

    #     context = "\n".join([doc.page_content for doc in docs])
    #     prompt_report = build_section_prompt(section=section, question=question, context=context)
    #     payload = build_payload(model_name=MODEL_NAME, prompt=prompt_report)

    #     url = f"{OLLAMA_BASE_URL}/api/generate"

    #     try:
    #         # ⚡ Limit concurrent Ollama requests
    #         if semaphore is None:
    #             semaphore = asyncio.Semaphore(1)  # match OLLAMA_NUM_PARALLEL

    #         async with semaphore:
    #             async with aiohttp.ClientSession() as session:
    #                 async with session.post(url, json=payload, timeout=180) as response:
    #                     if response.status != 200:
    #                         text = await response.text()
    #                         raise Exception(f"HTTP {response.status}: {text}")
    #                     result = await response.json()

    #         content = result.get("response", "")
    #         print(f"🧾 Raw model output: {repr(content)}")

    #         # Clean and parse JSON
    #         try:
    #             final_result = json.loads(content)
    #         except json.JSONDecodeError:
    #             import re
    #             match = re.search(r"\{.*\}", content, re.DOTALL)
    #             final_result = json.loads(match.group(0)) if match else {
    #                 "matched": "Error", "section": section, "error": "Invalid JSON", "raw_response": content
    #             }

    #         return final_result

    #     except Exception as e:
    #         print(f"❌ Ollama Error: {e}")
    #         return {
    #             "matched": "Error",
    #             "section": section,
    #             "error": str(e),
    #             "raw_response": content if 'content' in locals() else ""
    #         }


async def report_over_context_async(self, question, section, vectorstore=None, semaphore=None, job_id=None):
    import aiohttp
    import asyncio

    embeddings = OllamaEmbeddingWrapper(model="nomic-embed-text:latest")
    collection = vectorstore._collection

    nozzle_no = self.extract_nozzle_number_from_question(question)
    query_embedding = embeddings.embed_query(question)

    # Build filter
    where_document = {"$contains": f"Nozzle: Ref.: {nozzle_no},"} if nozzle_no not in ("", "N/A") else None
    print(f"🔍 Document filter applied: {where_document}")

    # ---------------------------
    # 1️⃣ Query Chroma in a thread with timeout
    # ---------------------------
    try:
        results = await asyncio.wait_for(
            asyncio.to_thread(
                collection.query,
                query_embeddings=[query_embedding],
                n_results=5,
                where={"section": section},
                where_document=where_document,
                include=["documents", "metadatas"]
            ),
            timeout=10  # seconds per query
        )
    except asyncio.TimeoutError:
        print(f"⚠️ Chroma query timed out for section {section}")
        return {"matched": "Error", "section": section, "error": "Chroma query timed out"}

    docs = [Document(page_content=doc, metadata=meta)
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])]
    print(f"📄 Retrieved {len(docs)} relevant documents.")

    context = "\n".join([doc.page_content for doc in docs])
    prompt_report = build_section_prompt(section=section, question=question, context=context)
    payload = build_payload(model_name=MODEL_NAME, prompt=prompt_report)

    url = f"{OLLAMA_BASE_URL}/api/generate"

    # ---------------------------
    # 2️⃣ Set semaphore if missing
    # ---------------------------
    if semaphore is None:
        semaphore = asyncio.Semaphore(1)  # adjust as needed

    # ---------------------------
    # 3️⃣ Run Ollama request with timeout
    # ---------------------------
    try:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async def fetch():
                    async with session.post(url, json=payload, timeout=180) as response:
                        if response.status != 200:
                            text = await response.text()
                            raise Exception(f"HTTP {response.status}: {text}")
                        return await response.json()

                print(f"🚀 Sending question to Ollama: {question}")
                result = await asyncio.wait_for(fetch(), timeout=30)  # 30s per question
                print(f"✅ Received answer from Ollama")

        content = result.get("response", "")

        # ---------------------------
        # 4️⃣ Send WS message (if job_id provided)
        # ---------------------------
        if job_id:
            try:
                await send_ws_message(job_id, {
                    "status": "running",
                    "progress": None,  # can calculate later in batch
                    "message": f"Processed question: {question}",
                    "question": question
                })
            except Exception as e:
                print(f"⚠️ Failed to send WS message: {e}")

        # ---------------------------
        # 5️⃣ Parse JSON safely
        # ---------------------------
        try:
            final_result = json.loads(content)
        except json.JSONDecodeError:
            import re
            match = re.search(r"\{.*\}", content, re.DOTALL)
            final_result = json.loads(match.group(0)) if match else {
                "matched": "Error",
                "section": section,
                "error": "Invalid JSON",
                "raw_response": content
            }

        return final_result

    except asyncio.TimeoutError:
        print(f"⚠️ Ollama request timed out for section {section}")
        return {"matched": "Error", "section": section, "error": "Ollama request timed out"}
    except Exception as e:
        print(f"❌ Ollama Error: {e}")
        return {
            "matched": "Error",
            "section": section,
            "error": str(e),
            "raw_response": content if 'content' in locals() else ""
        }

 