import json
from typing import Any

from .models import ReasoningRun
from .redaction import redact_mapping


PUBLIC_FIELDS = {
    "answer",
    "claims",
    "evidence",
    "uncertainty",
}


def to_public_dict(
    result: ReasoningRun,
) -> dict[str, Any]:
    """
    Convert a ReasoningRun into a safe public dictionary.

    Private reasoning fields are never copied into the
    public representation.
    """

    if not isinstance(result, ReasoningRun):
        raise TypeError(
            "result must be a ReasoningRun"
        )

    claims = [
        {
            "text": claim.text,
            "evidence_ids": list(
                claim.evidence_ids
            ),
        }
        for claim in result.claims
    ]

    public_data: dict[str, Any] = {
        "answer": result.answer,
        "claims": claims,
        "evidence": list(result.evidence),
        "uncertainty": result.uncertainty,
    }

    public_data = redact_mapping(
        public_data
    )

    return {
        key: value
        for key, value in public_data.items()
        if key in PUBLIC_FIELDS
    }


def to_public_json(
    result: ReasoningRun,
) -> str:
    """
    Serialize only the safe public representation.
    """

    return json.dumps(
        to_public_dict(result),
        indent=2,
        sort_keys=True,
    )