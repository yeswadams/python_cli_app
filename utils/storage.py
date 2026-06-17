import json
import os
from typing import Any


def ensure_dir_for_file(path: str) -> None:
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def load_json_list(path: str) -> list[Any]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []
    return data if isinstance(data, list) else []


def save_json_list(path: str, records: list[Any]) -> None:
    ensure_dir_for_file(path)
    with open(path, "w") as f:
        json.dump(records, f, indent=4)
