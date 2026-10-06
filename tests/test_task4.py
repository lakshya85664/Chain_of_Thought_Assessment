import pytest

from reasoning_summary.service import (
    solve,
    solve_with_incomplete_evidence,
)


def test_complete_evidence_has_no_uncertainty():
    result = solve(
        "What should be verified first?"
    )

    assert result.uncertainty is None


def test_incomplete_evidence_reports_uncertainty():
    result = solve_with_incomplete_evidence(
        "What should be verified first?"
    )

    assert result.uncertainty is not None
    assert "incomplete" in (
        result.uncertainty.lower()
    )


def test_incomplete_evidence_answer_is_concise():
    result = solve_with_incomplete_evidence(
        "What should be verified first?"
    )

    assert len(result.answer) < 160


def test_incomplete_evidence_does_not_claim_certainty():
    result = solve_with_incomplete_evidence(
        "What should be verified first?"
    )

    assert "definitive" in result.answer.lower()


def test_incomplete_evidence_has_traceable_claims():
    result = solve_with_incomplete_evidence(
        "What should be verified first?"
    )

    evidence_ids = set(result.evidence)

    assert "evidence_incomplete" in evidence_ids

    for claim in result.claims:
        assert set(
            claim.evidence_ids
        ).issubset(evidence_ids)


def test_invalid_question_is_rejected():
    with pytest.raises(ValueError):
        solve_with_incomplete_evidence("")