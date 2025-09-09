from __future__ import annotations
from dataclasses import is_dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Any


def serialize_for_storage(value: Any) -> Any:
    """
    Recursively serialize a value into JSON/storage friendly primitives.

    Rules:
    - dataclass -> dict (recursively serialized)
    - Enum -> its value
    - datetime -> ISO 8601 string
    - list/tuple/set -> list of serialized items
    - dict -> dict with string keys preserved, values serialized
    - other primitives returned as-is
    """
    # Dataclass (but avoid treating plain strings etc.)
    if is_dataclass(value):
        return {k: serialize_for_storage(v) for k, v in asdict(value).items()}

    # Enum
    if isinstance(value, Enum):
        return value.value

    # datetime
    if isinstance(value, datetime):
        return value.isoformat()

    # Collections
    if isinstance(value, (list, tuple, set)):
        return [serialize_for_storage(v) for v in value]

    if isinstance(value, dict):
        return {k: serialize_for_storage(v) for k, v in value.items()}

    # Primitive (str, int, float, bool, None)
    return value


def entity_to_storage_dict(entity: Any, include_none: bool = False) -> dict[str, Any]:
    """
    Convert a domain entity (possibly dataclass) into a dict for persistence.

    Args:
        entity: The domain entity instance.
        include_none: Whether to include keys whose serialized value is None.
    """
    
    data = serialize_for_storage(entity)

    if not isinstance(data, dict):  # Fallback: wrap non-dict dataclass (rare)
        return {"value": data}

    if not include_none:
        return {k: v for k, v in data.items() if v is not None}

    return data
