# Benchmark Fixture Contract

Version: 1.7.7

Use this contract when creating benchmark, scoring, or release-candidate test cases. The goal is first-shot readiness: a fixture must be parseable, valid, and evaluable before any live run.

## Fixture fields
Each fixture row or JSON object must include:

- `fixture_id`: stable unique identifier.
- `language`: user-facing language of the stimulus.
- `category`: broad category or coverage lens.
- `target_behavior`: what the candidate must do.
- `stimulus`: the exact input shown to the candidate. Do not include hidden oracle hints.
- `expected_behavior`: evaluator-facing behavior summary.
- `oracle`: sealed expected result, rubric, or adjudication rule hidden from the stimulus.
- `format_contract`: exact output shape, schema, delimiter, or path expectations.
- `evidence_required`: file, command, citation, checksum, or limitation evidence expected.
- `safety_boundary`: refusal, privacy, protected-token, or professional-risk constraint when relevant.
- `validation_tier`: T0, T1, T2, or T3.
- `pass_fail_rule`: deterministic rule or human-review instruction.
- `failure_taxonomy`: allowed failure labels.

## Preflight gates
A fixture is not ready to test until it passes dry-load parsing, schema validation, oracle sealing, answer-leakage check, duplicate/near-duplicate check, and evaluator-entrypoint check.

## First-shot readiness
Testing may be possible only once. Do not rely on trial-and-error discovery of hidden format. If the target system requires a strict schema, validate fixture format before execution and fail the fixture build rather than running malformed tests.

## Anti-leakage rule
Never place expected pass/fail hints, hidden oracle fields, or evaluator-only scoring rules in the user-visible stimulus.
