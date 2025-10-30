import json
import re
from app.utils.camelot_extractor import extract_table_data

def extract_lining_spec_and_notes(file_path):
    
    raw_data = extract_table_data(file_path=file_path)

    lining_spec_keyword = "LINING SPECIFICATION"
    general_notes_keyword = "GENERAL NOTES : -"

    def normalize(text):
        return " ".join(re.sub(r'\s+', ' ', text.strip().replace("\xa0", " ")).split())

    lining_spec = None
    general_notes = []
    general_notes_started = False
    target_col = None

    for row_idx, row in enumerate(raw_data):
        for col_idx, cell in row.items():
            text = cell.strip()

            if not lining_spec and normalize(text).startswith(lining_spec_keyword):
                lining_spec = text.replace(lining_spec_keyword, "", 1).strip()

            if not general_notes_started and general_notes_keyword in normalize(text):
                general_notes_started = True
                target_col = col_idx
                general_notes.append(text)

        if general_notes_started:
            for next_row in raw_data[row_idx + 1:]:
                note = next_row.get(str(target_col), "").strip()
                if note:
                    if any(section in normalize(note) for section in ["LINING SPECIFICATION", "NOTES", "SCOPE"]):
                        break
                    general_notes.append(note)
            break

    cleaned_notes = []
    header_removed = False
    for note in general_notes:
        if not header_removed and general_notes_keyword in note:
            cleaned_notes.append(note.replace(general_notes_keyword, "", 1).strip())
            header_removed = True
        else:
            cleaned_notes.append(note)

    seen = set()
    final_notes = []
    for note in cleaned_notes:
        if note and note not in seen:
            final_notes.append(note)
            seen.add(note)

    output_data = {
        "LINING SPECIFICATION": lining_spec if lining_spec else "Not found",
        "GENERAL NOTES": final_notes if final_notes else ["Not found"]
    }

    return output_data