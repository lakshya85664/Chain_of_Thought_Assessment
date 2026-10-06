# Topic 4: Implement Chain-of-Thought in Code

## Overview
This project implements a bounded reasoning-summary workflow for the assessment **Topic 4: Implement Chain-of-Thought in Code**.

The implementation does **not** expose unrestricted private chain-of-thought. Intermediate notes are kept in an internal `ReasoningRun`, while the public result contains only concise evidence-backed claims, evidence IDs, and uncertainty.

The project is deterministic, local, and synthetic. It requires no external APIs, credentials, network access, or production services.

## Core Tasks
1. **Store intermediate notes separately from the public answer.**  
   `ReasoningRun.private_notes` is separate from `answer`.

2. **Attach evidence IDs to claims.**  
   Every public `Claim` contains concise text and one or more evidence IDs. Tests verify that referenced IDs exist.

3. **Redact secrets/internal-only fields.**  
   Recursive redaction removes fields such as `api_key`, `access_token`, `password`, `secret`, `private_notes`, `internal_notes`, `chain_of_thought`, and `raw_reasoning`.

4. **Return concise rationale with uncertainty when evidence is incomplete.**  
   `solve_with_incomplete_evidence()` explicitly reports incomplete evidence instead of producing an unsupported definitive conclusion.

5. **Prove private notes are absent from serialized output.**  
   The public serializer uses an explicit allow-list containing only `answer`, `claims`, `evidence`, and `uncertainty`.

## Project Structure
```text
Chain_of_Thought_Assessment/
├── reasoning_summary/
│   ├── __init__.py
│   ├── cli.py
│   ├── evidence.py
│   ├── models.py
│   ├── redaction.py
│   ├── serialization.py
│   └── service.py
├── tests/
│   ├── fixtures/
│   ├── test_task1.py
│   ├── test_task2.py
│   ├── test_task3.py
│   ├── test_task4.py
│   └── test_task5.py
├── examples/question.json
├── evidence/traces/
├── evidence/state_snapshots/
├── outputs/
├── generate_evidence.py
├── HARDENING.md
├── pyproject.toml
├── requirements.txt
└── .gitignore
```

## Setup
Python version used: **3.13.9**

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Dependency:
```text
pytest==8.4.2
```

## CLI
Run the required assessment command:

```cmd
python -m reasoning_summary.cli answer --input examples\question.json --output outputs\answer.json
```

Expected output:
```text
Answer written to outputs\answer.json
Answer: Answer supported by the checked evidence.
Evidence IDs: input_present, answer_format_valid
```

## Evidence Generation
Run:

```cmd
python generate_evidence.py
```

Generated evidence includes:
- `evidence/traces/complete_evidence_trace.json`
- `evidence/traces/incomplete_evidence_trace.json`
- `evidence/state_snapshots/complete_evidence_state.json`
- `evidence/state_snapshots/incomplete_evidence_state.json`
- `outputs/answer.json`
- `outputs/evidence_summary.json`

## Verification
Full regression suite:

```cmd
python -m pytest -q
```

Verified result:

```text
30 passed
```

Task-level result:
- Task 1: 6 passed
- Task 2: 6 passed
- Task 3: 6 passed
- Task 4: 6 passed
- Task 5: 6 passed

## Safety Boundary
The implementation intentionally demonstrates a **reasoning summary**, not unrestricted chain-of-thought exposure.

Private reasoning remains internal. Public output is limited to concise claims, supporting evidence IDs, the answer, and uncertainty. The serializer explicitly constructs the public schema so internal fields cannot accidentally be serialized.

## Hardening
`HARDENING.md` documents:
- private/public separation
- evidence traceability
- recursive redaction
- uncertainty handling
- safe serialization
- deterministic local execution
- residual risks and safe production extensions

Known residual risks include synthetic/local evidence, lack of cryptographic provenance verification, no persistent audit service, and field-name-based secret detection.

## Reflection
This project reinforced the distinction between internal reasoning and public communication in an AI system. The implementation keeps intermediate processing inside a separate `private_notes` field and makes the public serializer an explicit allow-list. This turns the safety boundary into a concrete code property rather than a developer convention.

Evidence IDs provide traceability for public claims without exposing private reasoning. Recursive redaction also protects common secret and internal-only fields. The incomplete-evidence scenario demonstrates responsible uncertainty: instead of producing a confident unsupported conclusion, the service states that the evidence is insufficient and provides an explicit uncertainty statement.

The 30-test regression suite and generated evidence artifacts make the workflow reproducible. The project is intentionally deterministic, local, and bounded for assessment purposes. It avoids external credentials and side effects while still demonstrating the required reasoning controls.

The central lesson is that a safe reasoning workflow should expose conclusions and supporting evidence—not unrestricted private reasoning.
