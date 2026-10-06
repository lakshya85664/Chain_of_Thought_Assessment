from typing import Any


SENSITIVE_KEYS = {
    "api_key",
    "access_token",
    "authorization",
    "password",
    "secret",
    "private_notes",
    "internal_notes",
    "chain_of_thought",
    "raw_reasoning",
}


def redact_mapping(
    data: dict[str, Any],
) -> dict[str, Any]:
    """
    Remove sensitive and internal-only fields from a mapping.

    Nested dictionaries and lists are processed recursively.
    """

    if not isinstance(data, dict):
        raise TypeError(
            "data must be a dictionary"
        )

    result: dict[str, Any] = {}

    for key, value in data.items():
        normalized_key = str(key).lower()

        if normalized_key in SENSITIVE_KEYS:
            continue

        if isinstance(value, dict):
            result[key] = redact_mapping(value)

        elif isinstance(value, list):
            result[key] = [
                redact_value(item)
                for item in value
            ]

        else:
            result[key] = value

    return result


def redact_value(value: Any) -> Any:
    """Recursively redact sensitive mapping fields."""

    if isinstance(value, dict):
        return redact_mapping(value)

    if isinstance(value, list):
        return [
            redact_value(item)
            for item in value
        ]

    return value