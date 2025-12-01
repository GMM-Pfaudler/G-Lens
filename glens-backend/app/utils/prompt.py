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
    }
  
def build_section_prompt(section: str, question: str, context: str) -> str:
    COMMON_EQUIVALENCE_RULES = """
EQUIVALENCE RULES (APPLY STRICTLY):
1. Literal Equivalence — exact word/symbol matches.
2. Semantic Equivalence — same meaning with different wording. also Fabricated is the same as/equivalent to Plain.
3. Numeric Equivalence:
   - Extract all numbers from question and context.
   - Normalize formats (05 → 5, 1.0 → 1, 12.50 → 12.5).
   - Compare numbers numerically, not textually.
4. Unit Equivalence — equivalent units match (10 mm == 1 cm). also treat CPS same as CP
5. Abbreviation / Full Form Equivalence — UT == Ultrasonically Tested, SA 105 == ASTM A105,etc. also a few reference abbreviations are [ULGL is Ultra Glass, WGL is White Glass, ARGL is ARG Glass, SSGL is Blue Glass, PPGL is Pharma Glass]
6. Case / Punctuation / Whitespace Equivalence — ignore differences (SA-105 == sa 105).
7. Word Order Equivalence — Flow Control Valve == Valve for Flow Control.
8. Material / Standard Equivalence — SA 105 == ASTM A105; SS316 == Stainless Steel 316, etc. also MSGL is the same as/equivalent to [GL ,UGL,9100 Glass, Pharma Glass, Ultra Glass, White Glass, Nano Glass, ARG Glass, PPGL] only. Also note that Ultra Glass 6500 (Dark Blue) is equivalent to Ultra Glass 6500. Also Pfaudler World Wide is equivalent to Pfaudler.
9. Range / Tolerance Equivalence — numbers close within tolerance may match (5.0 bar == 5.05 bar).
10. Implicit/Optional Information Equivalence — known abbreviations or contextual meanings match (CR == Corrosion Resistant).
11. Singular/Plural Equivalence — Valve == Valves.
12. Partial Phrase Equivalence — partial numeric/descriptor matches must return the full context phrase.
13. Symbol/Notation Equivalence — ≤ == <= ; °C == Celsius.
14. Functional/Contextual Equivalence — match components performing the same function.
CLOSEST MATCH RULE:
- If no match, return the closest semantic/functional value from the context.
OUTPUT RULES:
- Return STRICT JSON ONLY.
- No comments, no markdown, no explanations.
THINKING RULES:
- Carefully compare entire context before deciding.
- Use only values that appear exactly in the context.
- Return full phrases from context for all matches.
"""

    if section == "part_list":
        return f"""
You are a smart assistant verifying whether a component or its type from the question is present in the Bill of Materials (BoM) section.

Your task:
- Determine if the primary component type or design in the question is already present in the context.
- Use only component names/descriptions from the context.
- Do NOT copy anything from the question unless it also appears in the context.

Context:
{context}

Question:
{question}

Matching rules:
- YES if the component type/design clearly appears (even if word order or phrasing differs).
- Do NOT match based only on generic materials unless that is the only value specified in the question.
- If matched, return the full description exactly as written in the context.
- Ignore drawing numbers, quantities, page numbers and part numbers.
- If no exact or equivalent match, return the closest functional/naming equivalent.

{COMMON_EQUIVALENCE_RULES}

Return formats:
If matched:
{{"matched": "Yes", "section": "part_list", "matched_value": "<copy full matching description from context>"}}
If not matched:
{{"matched": "No", "section": "part_list", "closest_match": "<copy closest description from context>"}}
""".strip()

    elif section == "lining_and_notes":
        return f"""
You are a smart assistant determining whether a value from the question exists in the 'lining_and_notes' context.

Rules:
- Only use values explicitly present in the context.
- Abbreviations in question must match their full forms in context and vice versa.
- Minor formatting or symbol variations still count as matches.
- If matched, return the full value as written in the context.
- If unmatched, return the closest value in the context.

Context:
{context}

Question:
{question}

{COMMON_EQUIVALENCE_RULES}

Return formats:
If matched:
{{"matched": "Yes", "section": "lining_and_notes", "matched_value": "<exact value from context>"}}
If not:
{{"matched": "No", "section": "lining_and_notes", "closest_match": "<closest value from context>"}}
""".strip()

    elif section == "design_data":
        return f"""
You are a smart assistant verifying whether a specific value from the question exists in the 'design_data' context.

Context:
{context}

Question:
{question}

Rules:
- Identify whether the value (numeric, symbolic, descriptive) exists explicitly or logically.
- Logical = semantic wording, numeric equivalence, unit conversion, symbol equivalence.
- If matched, return the entire matching phrase exactly as in the context. if essential, concatenate upto two phrases, only and only if deemed necessary.
- Never return partial values.
- If unmatched, return the closest related value.

{COMMON_EQUIVALENCE_RULES}

Return formats:
If matched:
{{"matched": "Yes", "section": "design_data", "matched_value": "<full phrase exactly from context>"}}
If not:
{{"matched": "No", "section": "design_data", "closest_match": "<closest phrase from context>"}}
""".strip()

    elif section == "material_of_construction":
        return f"""
You are a smart assistant verifying whether a material or standard from the question appears in the 'material_of_construction' context.

Context:
{context}

Question:
{question}

Rules:
- Match based on equivalent grades, standards, materials, or acceptable variants.
- Accept minor formatting differences (e.g., SA-105 vs ASTM A105).
- Always return the full context phrase.
- If unmatched, return the closest relevant material/standard.

{COMMON_EQUIVALENCE_RULES}

Return formats:
If matched:
{{"matched": "Yes", "section": "material_of_construction", "matched_value": "<value from context>"}}
If not:
{{"matched": "No", "section": "material_of_construction", "closest_match": "<closest value from context>"}}
""".strip()

    else:
        return f"""
You are a smart assistant checking whether a value from the question exists in the '{section}' context.

Context:
{context}

Question:
{question}

Rules:
- Match logically equivalent meanings, symbols, numbers, or descriptions.
- Always return full context phrases.
- If unmatched, provide the closest meaningful value.

{COMMON_EQUIVALENCE_RULES}

Return formats:
If matched:
{{"matched": "Yes", "section": "{section}", "matched_value": "<value from context>"}}
If not:
{{"matched": "No", "section": "{section}", "closest_match": "<closest value from context>"}}
""".strip()
