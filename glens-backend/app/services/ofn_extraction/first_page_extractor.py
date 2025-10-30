import re
import json
import PyPDF2  # Import the PyPDF2 library

def extract_page_1_data_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = reader.pages[0].extract_text()
            if text is None:
                text = ""
    except FileNotFoundError:
        return {"error": "PDF file not found."}
    except Exception as e:
        return {"error": f"An error occurred during PDF processing: {str(e)}"}

    splitted_text = text.split("\n")
    res = extract_title_and_metadata(splitted_text)
    res['Document_code'] = splitted_text[0]
    return res

def extract_title_and_metadata(lines):
    title_lines = []
    metadata = {}
    lines = lines[1:]
    for line in lines:
        if ":" in line:
            key, value = map(str.strip, line.split(":", 1))
            metadata[key] = value
        elif line.strip():
            title_lines.append(line.strip())

    title = " ".join(title_lines[:5])
    return {
        "Title": title,
        **metadata
    }
