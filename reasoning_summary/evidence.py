from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    """A single traceable piece of evidence."""

    evidence_id: str
    description: str

    def __post_init__(self) -> None:
        if not isinstance(self.evidence_id, str):
            raise TypeError(
                "evidence_id must be a string"
            )

        if not self.evidence_id.strip():
            raise ValueError(
                "evidence_id must not be empty"
            )

        if not isinstance(self.description, str):
            raise TypeError(
                "description must be a string"
            )

        if not self.description.strip():
            raise ValueError(
                "description must not be empty"
            )


@dataclass(frozen=True)
class Claim:
    """A public claim linked to evidence IDs."""

    text: str
    evidence_ids: list[str]

    def __post_init__(self) -> None:
        if not isinstance(self.text, str):
            raise TypeError(
                "claim text must be a string"
            )

        if not self.text.strip():
            raise ValueError(
                "claim text must not be empty"
            )

        if not isinstance(self.evidence_ids, list):
            raise TypeError(
                "evidence_ids must be a list"
            )

        if not all(
            isinstance(item, str)
            for item in self.evidence_ids
        ):
            raise TypeError(
                "evidence_ids must contain strings"
            )

        if not self.evidence_ids:
            raise ValueError(
                "claim must reference at least one evidence ID"
            )