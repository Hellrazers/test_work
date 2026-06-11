from typing import Any


def not_none_or_empty(value: Any, message: str = "Value should not be null or empty"):
    if not value:
        raise ValueError(message)
    return value


def not_none(value: Any, message: str = "Value should not be null"):
    if value is None:
        raise ValueError(message)
    return value
