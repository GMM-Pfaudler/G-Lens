# pdf_core.py
import os
import re
from PyPDF2 import PdfReader, PdfWriter

KEYWORDS = ["Model", "Tag No", "Tag No.", "Capacity"]


# ---------------------------------------
# Extract base page
# ---------------------------------------
def extract_base_page(pdf_path, base_page_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    page = reader.pages[0]

    # ⭐ clone page properly to avoid referencing closed stream
    writer.add_page(page)

    with open(base_page_path, "wb") as out:
        writer.write(out)

# ---------------------------------------
# Extract Quote Number
# ---------------------------------------
def extract_quote_number(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        first_page_text = reader.pages[0].extract_text() or ""

    for line in first_page_text.splitlines():
        if "Quote No" in line and ":" in line:
            value = line.split(":", 1)[1].strip()
            m = re.search(r"(\d+)", value)
            return m.group(1) if m else ""

    return ""


# ---------------------------------------
# Capacity extraction (placeholder)
# ---------------------------------------
def extract_capacity_from_page(page):
    text = page.extract_text() or ""
    m = re.search(r"Capacity\s+([A-Z]{2,3}_\d+L)", text, re.IGNORECASE)
    return m.group(1) if m else None


# ---------------------------------------
# Helper: first 10 lines
# ---------------------------------------
def extract_first_10_lines(text):
    return text.splitlines()[:10] if text else []


# ---------------------------------------
# Check if page starts a new section
# ---------------------------------------
def page_starts_section(text):
    joined = " ".join(extract_first_10_lines(text))
    return any(key in joined for key in KEYWORDS)


# ---------------------------------------
# Build sections
# ---------------------------------------
def build_sections(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        total_pages = len(reader.pages)

        sections = []
        current = []

        for i in range(1, total_pages):
            page = reader.pages[i]
            text = page.extract_text() or ""

            if page_starts_section(text):
                if current:
                    sections.append(current)
                    current = []
                current.append(i)
            else:
                current.append(i)

        if current:
            sections.append(current)

        return sections


# ---------------------------------------
# Generate section PDFs
# ---------------------------------------
def generate_section_pdfs(base_page_path, source_pdf_path, sections, quote_number, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    created_files = []

    with open(base_page_path, "rb") as base_f, open(source_pdf_path, "rb") as src_f:
        base_page = PdfReader(base_f).pages[0]
        source_reader = PdfReader(src_f)

        for idx, pages in enumerate(sections, start=1):
            first_page = source_reader.pages[pages[0]]
            capacity = extract_capacity_from_page(first_page) or f"section_{idx}"

            writer = PdfWriter()
            writer.add_page(base_page)

            for p in pages:
                writer.add_page(source_reader.pages[p])

            filename = f"{quote_number}_{capacity}.pdf"
            output_path = os.path.join(output_folder, filename)

            with open(output_path, "wb") as f:
                writer.write(f)

            created_files.append(output_path)

    return created_files
