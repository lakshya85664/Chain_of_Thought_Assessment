import argparse
import json
from pathlib import Path
from typing import Any

from .serialization import to_public_dict
from .service import (
    solve,
    solve_with_incomplete_evidence,
)


def load_question(
    input_path: Path,
) -> str:
    """Load and validate a question from JSON."""

    if not input_path.exists():
        raise ValueError(
            f"input file does not exist: {input_path}"
        )

    try:
        data: dict[str, Any] = json.loads(
            input_path.read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON: {exc.msg}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(
            "input must be a JSON object"
        )

    question = data.get("question")

    if not isinstance(question, str):
        raise ValueError(
            "input must contain a string question"
        )

    if not question.strip():
        raise ValueError(
            "question must not be empty"
        )

    return question


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the Chain-of-Thought reasoning "
            "summary service."
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    answer_parser = subparsers.add_parser(
        "answer",
        help="Generate a safe public answer.",
    )

    answer_parser.add_argument(
        "--input",
        required=True,
        help="Input question JSON file.",
    )

    answer_parser.add_argument(
        "--output",
        required=True,
        help="Output answer JSON file.",
    )

    args = parser.parse_args()

    if args.command != "answer":
        parser.error(
            "unsupported command"
        )

    try:
        question = load_question(
            Path(args.input)
        )

        result = solve(question)

        output = to_public_dict(result)

        output_path = Path(args.output)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            json.dumps(
                output,
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

    except (
        OSError,
        TypeError,
        ValueError,
    ) as exc:
        parser.error(str(exc))

    print(
        f"Answer written to {args.output}"
    )
    print(
        f"Answer: {result.answer}"
    )

    if result.uncertainty is not None:
        print(
            f"Uncertainty: {result.uncertainty}"
        )

    print(
        f"Evidence IDs: {', '.join(result.evidence)}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())