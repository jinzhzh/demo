"""Utilities for validating and formatting JSON strings."""

import json
from typing import Any


def pretty_json(value: str | dict[str, Any] | list[Any], indent: int = 2) -> str:
    """Validate a JSON string or serialize a JSON-compatible value consistently."""
    data = json.loads(value) if isinstance(value, str) else value
    return json.dumps(data, ensure_ascii=False, indent=indent, sort_keys=True)
