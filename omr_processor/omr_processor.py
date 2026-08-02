from pathlib import Path
from typing import Tuple, Dict, Any


class OMRProcessor:
    def __init__(self):
        self.config = {}

    def validate_image(self, filepath: str) -> Tuple[bool, str]:
        if not Path(filepath).exists():
            return False, "File does not exist"
        return True, "OK"

    def process(self, filepath: str) -> Dict[str, Any]:
        return {"status": "completed", "score": 0, "answers": {}}
