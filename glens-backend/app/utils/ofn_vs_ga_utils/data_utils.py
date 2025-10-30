# utils/data_utils.py

import json
import re
from typing import Any

def get_all_nested_values(data: Any, key_path: str, separator: str = " -> "):
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


def get_nested_value(data: dict, key_path: str, separator: str = " -> "):
    keys = [key.strip() for key in key_path.split(separator)]
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data


def get_ga_nested_value(data: dict, key_path: str, separator: str = "->"):
    keys = [key.strip() for key in key_path.split(separator)]

    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data
 
def parse_json_content(content):
    # If it's bytes (normal uploaded file)
    if isinstance(content, (bytes, bytearray)):
        return json.loads(content.decode("utf-8"))
    # If it's already string (text)
    elif isinstance(content, str):
        return json.loads(content)
    # If it's already dict (FastAPI auto-parsed JSON blob)
    elif isinstance(content, dict):
        return content
    else:
        raise ValueError(f"Unsupported content type: {type(content)}")