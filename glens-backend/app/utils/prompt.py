def build_section_prompt(section:str,question:str,context:str) -> str:
    if section == "part_list":
            return(
                f"You are a smart assistant helping to verify if a component or its type is present in the following Bill of Materials (BoM) section:\n\n"
                f"Your job is to decide if the item or design described in the question is already written in the context.\n"
                f"- Only use component names and descriptions from the context. Do not copy from the question unless it also appears in the context.\n"
                f"{context}\n\n"
                f"Here is the question:\n"
                f"{question}\n\n"
                f"- You can say YES if the **primary component type or design** in the question is clearly present in the context (e.g., 'Spring Balance Assembly' matches 'SPRING BALANCE ASSEMBLY').\n"
                f"- Do NOT say YES if only a generic material (like 'MS') matches — the full part or function must match.\n"
                f"- Look for matches in structure, type, and function — even if phrasing or order of words differs.\n"
                f"- If it’s not an exact match, try to return the closest functional or naming equivalent.\n\n"
                f"- Only return the **description** from the context as your matched or closest value. Do not include part numbers, quantities, or drawing numbers.\n"
                f"- Ignore drawing numbers, even if they're on the same line. Match only the component description exactly.\n"
                f"- Think carefully through the whole context before deciding.\n\n"
                f"If it's a match, reply like this:\n"
                f'{{"matched": "Yes", "section": "{section}", "matched_value": "<copy full matching part description from the context>"}}\n\n'
                f"If not a match, reply like this:\n"
                f'{{"matched": "No", "section": "{section}", "closest_match": "<copy the closest part description from the context>"}}\n\n'
                f"⚠️ Rules:\n"
                f"- Only return a valid JSON. No comments, no explanations, no markdown."
            )

    elif section == "lining_and_notes":
         return(
            f"You are a smart assistant tasked with checking whether a value from the question exists in the provided context from the '{section}' section.\n\n"
            f"Rules:\n"
            f"- Use only information explicitly present in the context. Do NOT copy or infer anything from the question unless the exact value appears in the context.\n"
            f"- A match can still be valid if there's a minor variation in wording, symbols, or formatting.\n"
            f"- For abbreviations or codes in the question (e.g., 'UT'), match them to their full form in the context (e.g., 'Ultrasonically Tested'). Return the form from the context.\n"
            f"- Take your time, think carefully, and check the entire context before answering.\n"
            f"- If no exact match is found, return the closest relevant value or phrase.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{question}\n\n"
            f"Output Format:\n"
            f'If matched, respond ONLY with JSON:\n'
            f'{{"matched": "Yes", "section": "{section}", "matched_value": "<exact value from context>"}}\n\n'
            f'If no match, respond ONLY with JSON:\n'
            f'{{"matched": "No", "section": "{section}", "closest_match": "<closest value from context>"}}\n\n'
            f"⚠️ Important: Return ONLY valid JSON without any additional text or comments."
        )

    elif section == "design_data":
        return(
            f"You are a smart assistant tasked with checking whether a specific value mentioned in a question exists in the following context from the '{section}' section.\n\n"
            f"--- CONTEXT ---\n{context}\n\n"
            f"--- QUESTION ---\n{question}\n\n"
            f"Instructions:\n"
            f"1. Carefully read the context.\n"
            f"2. Check if the value from the question is explicitly or logically present in the context.\n"
            f"   - Logical match means same meaning using different words, units, symbols, or abbreviations (e.g., 'F.V.', '≤', etc.)\n"
            f"3. ✅ If a match is found, return the **entire matching value exactly as it appears in the context** — including full phrases, numbers, symbols, and units.\n"
            f"   - Do not return a partial value (e.g., just '6 bar') if the context has more (e.g., 'F. V. 6 bar(g)')\n"
            f"   - Do not use or copy the value from the question — always extract directly from the context\n"
            f"4. ❌ If there's no match, find and return the **closest related value or phrase** from the context.\n\n"
            f"⚠️ Output Format:\n"
            f"- Return strictly valid JSON. No other text.\n"
            f"If matched:\n"
            f'{{"matched": "Yes", "section": "{section}", "matched_value": "<copy the full matching value exactly as written in the context>"}}\n\n'
            f"If not matched:\n"
            f'{{"matched": "No", "section": "{section}", "closest_match": "<copy the closest related value or phrase from the context>"}}\n\n'
            f"💡 Think carefully. Be precise. Never return partial or rephrased answers — only extract complete values from the context."
        )
    
    elif section == "material_of_construction":
        return(
            f"You are a smart assistant helping to verify if a specific material or standard appears in the 'Materials of Construction' section below:\n\n"
            f"Your job is to check if the material or standard in the question is already present in the context.\n"
            f"- Only match based on the actual context. Do not copy from the question unless it also appears in the context.\n"
            f"{context}\n\n"
            f"Here is the question:\n"
            f"{question}\n\n"
            f"- You can say YES if the material or standard in the context logically matches or closely relates to the one in the question (e.g., same grade, standard, or acceptable variant).\n"
            f"- Minor formatting differences (e.g., 'SA 105' vs 'ASTM A105') are acceptable as long as the meaning is the same.\n"
            f"- If it does not match, try to find and return the closest relevant material or part name from the context.\n\n"
            f"- **Always return the full matching or closest value as it appears in the context — prioritize detail and completeness.**\n"
            f"- Take your time, think carefully, and examine the entire context before answering.\n\n"
            f"If it’s a match, reply in this exact JSON format:\n"
            f'{{"matched": "Yes", "section": "{section}", "matched_value": "<copy the logically matching value from the context>"}}\n\n'
            f"If it’s not a match, reply in this format:\n"
            f'{{"matched": "No", "section": "{section}", "closest_match": "<copy the closest value from the context>"}}\n\n'
            f"⚠️ Rules:\n"
            f"- Only return a valid JSON. No extra explanation, no comments, no markdown."
        )

    else:
        return(
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

def build_payload(model_name: str,prompt: str) -> dict:
    """
    Build a standardized payload for the Ollama API.
    Keeps all formatting consistent across calls.
    """
    return {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.0,
        "format": {
            "type": "object",
            "properties": {
                "matched": {"type": "string"},
                "section": {"type": "string"},
                "matched_value": {"type": "string"},
                "closest_match": {"type": "string"},
            },
            "required": ["matched", "section"]
        }
    }