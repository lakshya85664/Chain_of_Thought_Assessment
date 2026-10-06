from dataclasses import dataclass, field

from .evidence import Claim


@dataclass(frozen=True)
class ReasoningRun:
    """
    Internal reasoning result.

    private_notes are internal-only intermediate records.

    claims are public-facing claims that must reference
    evidence IDs.

    evidence contains the available evidence records.

    answer is the concise public-facing response.

    uncertainty describes limitations in the available
    evidence without exposing private reasoning.
    """

    private_notes: list[str] = field(
        default_factory=list
    )

    evidence: list[str] = field(
        default_factory=list
    )

    answer: str = ""

    claims: list[Claim] = field(
        default_factory=list
    )

    uncertainty: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.private_notes, list):
            raise TypeError(
                "private_notes must be a list"
            )

        if not all(
            isinstance(note, str)
            for note in self.private_notes
        ):
            raise TypeError(
                "private_notes must contain strings"
            )

        if not isinstance(self.evidence, list):
            raise TypeError(
                "evidence must be a list"
            )

        if not all(
            isinstance(item, str)
            for item in self.evidence
        ):
            raise TypeError(
                "evidence must contain strings"
            )

        if not isinstance(self.answer, str):
            raise TypeError(
                "answer must be a string"
            )

        if not isinstance(self.claims, list):
            raise TypeError(
                "claims must be a list"
            )

        if not all(
            isinstance(claim, Claim)
            for claim in self.claims
        ):
            raise TypeError(
                "claims must contain Claim objects"
            )

        if (
            self.uncertainty is not None
            and not isinstance(
                self.uncertainty,
                str,
            )
        ):
            raise TypeError(
                "uncertainty must be a string or None"
            )