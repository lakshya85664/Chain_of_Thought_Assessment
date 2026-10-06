import pytest

from reasoning_summary.models import ReasoningRun
from reasoning_summary.service import solve


def test_reasoning_run_stores_private_notes_separately():
    result = solve(
        "What should be verified first?"
    )

    assert isinstance(result, ReasoningRun)
    assert result.private_notes
    assert result.evidence
    assert result.answer


def test_private_notes_are_separate_from_answer():
    result = solve(
        "What should be verified first?"
    )

    assert result.private_notes != [
        result.answer
    ]

    for note in result.private_notes:
        assert note not in result.answer


def test_answer_is_concise():
    result = solve(
        "What should be verified first?"
    )

    assert result.answer == (
        "Answer supported by the checked evidence."
    )


def test_empty_question_is_rejected():
    with pytest.raises(ValueError):
        solve("")


def test_non_string_question_is_rejected():
    with pytest.raises(TypeError):
        solve(123)


def test_reasoning_run_rejects_invalid_private_notes():
    with pytest.raises(TypeError):
        ReasoningRun(
            private_notes="not-a-list",
            evidence=[],
            answer="answer",
        )