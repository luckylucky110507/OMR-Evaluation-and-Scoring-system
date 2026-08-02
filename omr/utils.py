import json
from pathlib import Path
from typing import Dict, Any

ANSWER_KEYS_FILE = Path("answer_keys.json")


def load_answer_keys() -> Dict[str, Any]:
    if not ANSWER_KEYS_FILE.exists():
        return {}
    with ANSWER_KEYS_FILE.open("r", encoding="utf-8") as fh:
        return json.load(fh)
