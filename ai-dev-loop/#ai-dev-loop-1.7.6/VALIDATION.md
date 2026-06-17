# AI Development Loop Validation Contract

Run package validation from the package root:

```bash
python3 scripts/validate-ai-dev-loop-package.py
```

The validator must pass before distribution. It checks:

- required files and example directories;
- absence of root `.ai-dev-loop/`, `__MACOSX`, `.DS_Store`, AppleDouble `._*`, caches, editor metadata, compiled Python, and temporary files;
- `SKILL.md` version and compact-size budget;
- required activation, role separation, evidence, validation, same-session handoff, git/degraded-mode, scoring, and package/release phrases;
- canonical status values in status templates and example records;
- R review record template and K response record template headings;
- whole-change impact guidance in major docs, including that R findings are not exhaustive task lists and affected artifacts may matter even when R did not explicitly mention them;
- installer smoke behavior in a temporary project;
- state checker smoke behavior and token estimator smoke behavior;
- `PACKAGE-MANIFEST.json` file inventory, byte sizes, and SHA-256 checksums;
- `SCORING-EVIDENCE-SCHEMA.json`, benchmark harness, and mode harness presence;
- version consistency across top-level markdown, schema, manifest, and validator constants;
- user-facing process-leakage guardrails.

Installed project validation requires these paths:

```text
.ai-dev-loop/SKILL.md
.ai-dev-loop/LOOP-HARNESS.md
.ai-dev-loop/status.md
.ai-dev-loop/reviews/
.ai-dev-loop/responses/
.ai-dev-loop/context/
.ai-dev-loop/decisions/
.ai-dev-loop/scripts/check-ai-dev-loop-state.py
```

Validation evidence must record command, working directory, exit status, output summary, failures, skipped checks, limitations, and claim cap.

## Mode-gated validation

Minimal mode may run smaller checks, but release mode requires full package validation, manifest checksum agreement, zip hygiene, version consistency, and saved validation results.

## Schema and fixture validation

Release validation must include schema presence, exact version consistency, artifact cleanup, installer smoke behavior, and, when benchmark fixtures exist, dry-load/schema/oracle-leakage preflight before live scoring. Benchmark tests must pass dry-load parsing, schema validation, oracle sealing, answer-leakage checks, duplicate checks, and runner/evaluator entrypoint checks before they are treated as valid measurement evidence.

## Delivered files

Validation must fail when user-facing package files include audit-only tool names, generated-by metadata, comparison history, or internal labels that the user did not request.

## v1.7.6 refinement checks

- `SKILL.md` is materially shorter than the previous mature version while preserving required phrases.
- Expanded glossary, mode detail, claim caps, templates, contradiction handling, and terminal acceptance live in `LOOP-HARNESS.md`.
- `MODE-HARNESS.md` clearly separates minimal, standard, degraded, blocker, review-only, and release modes.
- Package validator rejects AppleDouble `._*` metadata and enforces a lower compact-size budget.
- User-facing package files avoid unrelated internal process history.
