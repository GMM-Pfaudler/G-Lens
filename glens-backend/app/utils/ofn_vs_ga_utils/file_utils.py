# utils/file_utils.py

import re

def sanitize_filename(filename: str) -> str:
    filename = filename.strip()
    filename = filename.replace(" ", "_")
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)

    if not filename[0].isalnum():
        filename = filename.lstrip("._-")
    if not filename[-1].isalnum():
        filename = filename.rstrip("._-")

    if len(filename) < 3:
        raise ValueError("Filename is too short after sanitization")

    return filename[:512]
