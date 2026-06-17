# AI Development Loop

AI Development Loop is a standalone repository workflow for AI-assisted development. It separates review and implementation into durable roles so another agent, teammate, or future session can continue from files instead of chat memory.

- **R** is the reviewer. R inspects source evidence, writes findings, answers K objections, accepts risk, resolves contradictions, and gives terminal approval.
- **K** is the implementer. K addresses each open required finding, edits directly related source/docs/tests/examples/scripts, validates, records evidence, and hands back to R.

The loop stores state in `.ai-dev-loop/` inside the target project. The package itself is a template; it intentionally does not ship a live root `.ai-dev-loop/` directory.

## Contents

```text
ai-dev-loop/
├── SKILL.md
├── modules/
│   ├── LOOP-HARNESS.md
│   ├── MODE-HARNESS.md
│   ├── RESTRICTION-HARNESS.md
│   ├── VALIDATION.md
│   └── BENCHMARK-HARNESS.md
├── scripts/
├── SCORING-EVIDENCE-SCHEMA.json
├── PACKAGE-MANIFEST.json
└── examples/.ai-dev-loop/
```

## Install

```bash
python3 scripts/install-ai-dev-loop-template.py /path/to/project
```

The installer refuses broad targets and existing `.ai-dev-loop/` directories unless explicit force flags are used.

## Operate

```text
Use .ai-dev-loop/SKILL.md. Treat .ai-dev-loop/status.md and the latest R/K records as the source of truth. Preserve role separation. Continue same-session handoff until blocked or R gives terminal approval.
```

Use minimal mode for small safe tasks; use release mode for package, version, manifest, validator, installer, scoring, benchmark, archive, or cross-file consistency work.

## Core loop

1. Load status, latest records, decisions, context, specs/docs/tests/diffs, and directly affected files.
2. R writes source-grounded findings, status, required outcomes, and next K action.
3. K addresses every open required finding or records a supported objection/blocker.
4. K performs a whole-change impact scan. R findings are not exhaustive task lists, and K remains responsible for affected artifacts even when R did not name those files explicitly.
5. K validates and records command evidence, limits, skipped checks, and next R action.
6. R closes findings, accepts risk, or requests further work.

## Token-efficient operation

Start normal turns with `SKILL.md`, then run the installed checker when available:

```bash
python3 .ai-dev-loop/scripts/check-ai-dev-loop-state.py /path/to/project
```

Use the concise output to target reads. Verify material claims against source files and records before approval. Load `modules/LOOP-HARNESS.md` only for templates, uncertain record shape, release work, degraded environments, blockers, K objections, terminal acceptance, scoring details, or whole-change uncertainty.

## Validation

```bash
python3 scripts/validate-ai-dev-loop-package.py
```

Validation covers required files, canonical status values, record templates, whole-change guidance, installer smoke behavior, manifest checksums, version consistency, forbidden artifacts, process-leakage guardrails, and compact SKILL.md budget.

## Safety and evidence rules

Do not claim file reads, commands, tests, commits, approvals, or external evidence that did not happen. Every material claim in review or implementation records must cite a file, diff, command, test, log, commit, status record, or explicit limitation. When package files disagree, prefer the stricter safety/evidence rule until an R decision resolves the contradiction.

## When to load `modules/LOOP-HARNESS.md`

Use `SKILL.md` for normal turns. Load `modules/LOOP-HARNESS.md` for templates, release/package work, degraded environments, blockers, K objections, context compression, status conflicts, terminal acceptance, scoring details, or whole-change scope uncertainty.

## Scoring and release evidence

For comparison, benchmark, release-candidate, or release work, use `SCORING-EVIDENCE-SCHEMA.json` and `VALIDATION-RESULTS.md` to keep evidence tags, category scores, validation tier, skipped checks, and checksums recomputable for version 1.7.7.

## Benchmark fixture readiness

`modules/BENCHMARK-HARNESS.md` defines first-shot-ready fixture fields, oracle sealing, format contracts, and anti-leakage checks for version 1.7.7.

## Release hygiene

Generated packages and user-facing docs should describe behavior, usage, constraints, validation, and maintenance only. Keep audit-only process notes outside the delivered package unless the user explicitly asks for a separate audit report.

## Module loading

`SKILL.md` is the always-loaded operating core. Runtime detail lives in `modules/` and is loaded only for first-record templates, release validation, benchmark fixture work, restriction regression review, or ambiguous mode decisions. This preserves whole-change impact guidance, not exhaustive task lists, and did not name those files explicitly as a complete implementation checklist.
