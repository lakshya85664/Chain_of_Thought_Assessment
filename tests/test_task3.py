from reasoning_summary.redaction import (
    redact_mapping,
    redact_value,
)


def test_redacts_api_key():
    data = {
        "answer": "safe",
        "api_key": "secret-key-value",
    }

    result = redact_mapping(data)

    assert result == {
        "answer": "safe",
    }


def test_redacts_private_notes():
    data = {
        "answer": "safe",
        "private_notes": [
            "internal reasoning",
            "another internal note",
        ],
    }

    result = redact_mapping(data)

    assert "private_notes" not in result
    assert result["answer"] == "safe"


def test_redacts_internal_reasoning_fields():
    data = {
        "answer": "safe",
        "chain_of_thought": "internal content",
        "raw_reasoning": "internal content",
        "internal_notes": "internal content",
    }

    result = redact_mapping(data)

    assert "chain_of_thought" not in result
    assert "raw_reasoning" not in result
    assert "internal_notes" not in result


def test_redacts_nested_sensitive_fields():
    data = {
        "result": {
            "answer": "safe",
            "credentials": {
                "password": "secret",
                "access_token": "token",
            },
        }
    }

    result = redact_mapping(data)

    assert result == {
        "result": {
            "answer": "safe",
            "credentials": {},
        }
    }


def test_redacts_sensitive_fields_inside_lists():
    data = {
        "items": [
            {
                "name": "safe",
                "secret": "hidden",
            },
            {
                "name": "visible",
                "api_key": "hidden",
            },
        ]
    }

    result = redact_mapping(data)

    assert result == {
        "items": [
            {
                "name": "safe",
            },
            {
                "name": "visible",
            },
        ]
    }


def test_redact_value_handles_non_mapping_values():
    assert redact_value("safe") == "safe"
    assert redact_value(42) == 42
    assert redact_value(["safe", 42]) == [
        "safe",
        42,
    ]