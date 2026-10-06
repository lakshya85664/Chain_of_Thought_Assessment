import json

import pytest

from reasoning_summary.serialization import (
    to_public_dict,
    to_public_json,
)
from reasoning_summary.service import (
    solve,
    solve_with_incomplete_evidence,
)


def test_private_notes_are_not_in_public_dict():
    result = solve(
        "What should be verified first?"
    )

    public_data = to_public_dict(result)

    assert "private_notes" not in public_data
    assert "internal_notes" not in public_data
    assert "chain_of_thought" not in public_data
    assert "raw_reasoning" not in public_data


def test_private_notes_are_not_in_public_json():
    result = solve(
        "What should be verified first?"
    )

    serialized = to_public_json(result)

    assert "private_notes" not in serialized
    assert "internal reasoning" not in serialized
    assert "chain_of_thought" not in serialized
    assert "raw_reasoning" not in serialized


def test_public_json_is_valid_json():
    result = solve(
        "What should be verified first?"
    )

    serialized = to_public_json(result)

    parsed = json.loads(serialized)

    assert isinstance(parsed, dict)
    assert parsed["answer"] == (
        "Answer supported by the checked evidence."
    )


def test_public_output_contains_evidence_links():
    result = solve(
        "What should be verified first?"
    )

    public_data = to_public_dict(result)

    assert public_data["evidence"]

    for claim in public_data["claims"]:
        assert claim["evidence_ids"]


def test_uncertainty_survives_public_serialization():
    result = solve_with_incomplete_evidence(
        "What should be verified first?"
    )

    public_data = to_public_dict(result)

    assert public_data["uncertainty"] is not None
    assert "incomplete" in (
        public_data["uncertainty"].lower()
    )


def test_serializer_rejects_invalid_input():
    with pytest.raises(TypeError):
        to_public_dict(
            {"private_notes": ["secret"]}
        )