from __future__ import annotations
from dataclasses import is_dataclass, asdict
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any
import math


def json_serialize(value: Any) -> Any:
    """
    Recursively serialize a value into JSON/storage friendly primitives.

    Rules:
    - dataclass -> dict (recursively serialized)
    - Enum -> its value
    - datetime -> ISO 8601 string
    - float NaN -> None (for DynamoDB compatibility)
    - list/tuple/set -> list of serialized items
    - dict -> dict with string keys preserved, values serialized
    - other primitives returned as-is
    """

    # Handle NaN values (convert to None for DynamoDB)
    if isinstance(value, float) and math.isnan(value):
        return None
    
    # Handle string representations of NaN
    if isinstance(value, str) and value.lower().strip() in ('nan', 'n/a', 'null', ''):
        return None

    # Dataclass (but avoid treating plain strings etc.)
    if is_dataclass(value):
        return {k: json_serialize(v) for k, v in asdict(value).items()}

    # Enum
    if isinstance(value, Enum):
        return value.value

    # datetime
    if isinstance(value, datetime):
        return value.isoformat()

    # Decimal (DynamoDB compatibility)
    if isinstance(value, Decimal):
        # Attempt int if no fractional part else float
        if value % 1 == 0:
            return int(value)
        return float(value)

    # Collections
    if isinstance(value, (list, tuple, set)):
        return [json_serialize(v) for v in value]

    if isinstance(value, dict):
        return {k: json_serialize(v) for k, v in value.items()}

    # Primitive (str, int, float, bool, None)
    return value
