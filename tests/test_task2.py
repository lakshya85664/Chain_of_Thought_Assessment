import pytest

from reasoning_summary.evidence import Claim, Evidence
from reasoning_summary.service import solve


def test_claim_contains_evidence_ids():
    result = solve(
        "What should be verified first?"
    )

    assert result.claims

    for claim in result.claims:
        assert claim.evidence_ids


def test_claim_evidence_ids_exist_in_evidence():
    result = solve(
        "What should be verified first?"
    )

    evidence_ids = set(result.evidence)

    for claim in result.claims:
        assert set(
            claim.evidence_ids
        ).issubset(evidence_ids)


def test_claim_text_is_public_and_concise():
    result = solve(
        "What should be verified first?"
    )

    for claim in result.claims:
        assert claim.text
        assert len(claim.text) < 120


def test_evidence_rejects_empty_id():
    with pytest.raises(ValueError):
        Evidence(
            evidence_id="",
            description="Input is present.",
        )


def test_claim_requires_evidence():
    with pytest.raises(ValueError):
        Claim(
            text="Unsupported claim",
            evidence_ids=[],
        )


def test_claim_rejects_invalid_evidence_ids():
    with pytest.raises(TypeError):
        Claim(
            text="Invalid claim",
            evidence_ids="E1",
        )