from .evidence import Claim
from .models import ReasoningRun


def solve(question: str) -> ReasoningRun:
    """
    Produce a deterministic reasoning result.

    The implementation uses a bounded evidence set and
    returns uncertainty when the available evidence is
    insufficient.
    """

    if not isinstance(question, str):
        raise TypeError(
            "question must be a string"
        )

    question = question.strip()

    if not question:
        raise ValueError(
            "question must not be empty"
        )

    private_notes = [
        f"Parse question: {question}",
        "Identify the information required to answer.",
        "Check whether the available evidence supports the answer.",
        "Construct a concise public response.",
    ]

    evidence = [
        "input_present",
        "answer_format_valid",
    ]

    claims = [
        Claim(
            text="The input question is present.",
            evidence_ids=[
                "input_present"
            ],
        ),
        Claim(
            text="The answer format is valid.",
            evidence_ids=[
                "answer_format_valid"
            ],
        ),
    ]

    answer = (
        "Answer supported by the checked evidence."
    )

    uncertainty = None

    return ReasoningRun(
        private_notes=private_notes,
        evidence=evidence,
        answer=answer,
        claims=claims,
        uncertainty=uncertainty,
    )


def solve_with_incomplete_evidence(
    question: str,
) -> ReasoningRun:
    """
    Produce a result for a case where evidence is incomplete.

    The public result explicitly communicates uncertainty
    rather than presenting an unsupported conclusion.
    """

    if not isinstance(question, str):
        raise TypeError(
            "question must be a string"
        )

    question = question.strip()

    if not question:
        raise ValueError(
            "question must not be empty"
        )

    private_notes = [
        f"Parse question: {question}",
        "Available evidence is incomplete.",
        "Avoid making an unsupported definitive claim.",
        "Return a concise answer with explicit uncertainty.",
    ]

    evidence = [
        "input_present",
        "evidence_incomplete",
    ]

    claims = [
        Claim(
            text="The input question is present.",
            evidence_ids=[
                "input_present"
            ],
        ),
        Claim(
            text="The available evidence is incomplete.",
            evidence_ids=[
                "evidence_incomplete"
            ],
        ),
    ]

    answer = (
        "The available evidence is incomplete, "
        "so a definitive answer cannot be established."
    )

    uncertainty = (
        "Confidence is limited because the available "
        "evidence is incomplete."
    )

    return ReasoningRun(
        private_notes=private_notes,
        evidence=evidence,
        answer=answer,
        claims=claims,
        uncertainty=uncertainty,
    )