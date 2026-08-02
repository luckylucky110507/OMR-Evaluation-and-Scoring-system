from pathlib import Path
from typing import Dict, Any


def read_image_bytes(filepath: str) -> bytes:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError("File does not exist")
    return path.read_bytes()


def preprocess_image(image_bytes: bytes) -> Dict[str, Any]:
    return {"width": len(image_bytes), "height": 1}


def find_document_contour(image_bytes: bytes) -> Dict[str, Any]:
    return {"found": True}
