import os
import uuid
import shutil
from app.core.pdf_splitter import (
    extract_base_page,
    extract_quote_number,
    build_sections,
    generate_section_pdfs
)

def process_uploaded_pdf(uploaded_pdf_path, output_folder):
    """
    Process the uploaded PDF:
    - Use a temporary internal folder for processing
    - Extract base page, quote number, and sections
    - Generate individual section PDFs inside output_folder
    - Cleanup temp folder automatically
    """

    # --- Internal temp folder for processing ---
    session_id = str(uuid.uuid4())
    temp_dir = os.path.join(output_folder, f"temp_session_{session_id}")
    os.makedirs(temp_dir, exist_ok=True)

    # Move uploaded PDF into temp folder
    local_pdf = os.path.join(temp_dir, "input.pdf")
    os.rename(uploaded_pdf_path, local_pdf)

    # Extract base page (first page)
    base_page_path = os.path.join(temp_dir, "base_page.pdf")
    extract_base_page(local_pdf, base_page_path)

    # Extract quote number
    quote_number = extract_quote_number(local_pdf)

    # Build sections
    sections = build_sections(local_pdf)

    # Generate final PDFs directly in output_folder
    final_files = generate_section_pdfs(
        base_page_path,
        local_pdf,
        sections,
        quote_number,
        output_folder
    )

    # Cleanup temp folder entirely
    shutil.rmtree(temp_dir, ignore_errors=True)

    return {
        "quote_number": quote_number,
        "sections": sections,
        "generated_files": final_files
    }
