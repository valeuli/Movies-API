from enum import Enum
from typing import Dict, Any


def serialize_enums(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms Enum to their string representations (value) in a dictionary.
    """
    for key, value in data.items():
        if isinstance(value, Enum):
            data[key] = value.value
    return data
