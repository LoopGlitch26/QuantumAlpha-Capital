"""Prompt serialization helpers shared across agent entry points."""

from datetime import datetime
from typing import Iterable, Any, Optional, List, Union


def json_default(obj: Any) -> Any:
    """Serialize datetime and set objects for JSON dumps."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, set):
        return list(obj)
    return str(obj)


def safe_float(value: Any) -> Optional[float]:
    """Cast ``value`` to float when possible, otherwise return ``None``."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def round_or_none(value: Any, decimals: int = 2) -> Optional[float]:
    """Round numeric values to ``decimals`` places, preserving ``None``."""
    numeric = safe_float(value)
    if numeric is None:
        return None
    return round(numeric, decimals)


def round_series(series: Optional[Iterable[Any]], decimals: int = 2) -> List[Optional[float]]:
    """Round each entry in ``series`` to ``decimals`` places when numeric."""
    if not series:
        return []
    rounded: List[Optional[float]] = []
    for val in series:
        numeric = safe_float(val)
        rounded.append(round(numeric, decimals) if numeric is not None else None)
    return rounded
