"""Chain-of-Thought in Code assessment package."""

from .evidence import Claim, Evidence
from .models import ReasoningRun
from .service import (
    solve,
    solve_with_incomplete_evidence,
)

__all__ = [
    "Claim",
    "Evidence",
    "ReasoningRun",
    "solve",
    "solve_with_incomplete_evidence",
]