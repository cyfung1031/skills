# RealityBench CaseForge v0.9.0

Generates source-grounded, format-fit, first-shot-ready benchmark test cases that approximate non-synthesized real-world testing and produce globally differentiated, objectively scoreable evaluation suites.

## Why this name

`RealityBench` signals that benchmark cases must preserve real workload reality rather than synthetic surface patterns. `CaseForge` signals that cases are shaped into the evaluator's required schema, runner contract, oracle, scoring format, and first-shot execution bundle before the benchmark is run.

## Package contents

- `SKILL.md` — the production skill.
- `README.md` — package overview.
- `CHANGELOG.md` — changes from v0.8.0 to v0.9.0.
- `manifest.json` — generated file sizes and SHA-256 checksums.

## Core validity formula

```text
non-synthesized closeness + source grounding + format validity + first-shot readiness + global differentiability + objective scoring + decision relevance
```

A case is invalid if it is realistic but unparseable, format-correct but unrealistic, globally redundant, answer-leaking, or not ready for the first permitted test attempt.
