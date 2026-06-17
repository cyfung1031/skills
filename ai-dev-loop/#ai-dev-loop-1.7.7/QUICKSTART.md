# AI Development Loop Quickstart

## 1. Validate the package

From the extracted package root:

```bash
python3 scripts/validate-ai-dev-loop-package.py
```

Expected output:

```text
AI Development Loop standalone package validation passed.
```

## 2. Install into a project

```bash
python3 scripts/install-ai-dev-loop-template.py /path/to/project
```

This creates `/path/to/project/.ai-dev-loop/` with `SKILL.md`, `modules/LOOP-HARNESS.md`, `status.md`, and the `reviews/`, `responses/`, `context/`, and `decisions/` directories.

## 3. Start the loop

Give the repository-editing assistant this instruction:

```text
Use .ai-dev-loop/SKILL.md. Treat .ai-dev-loop/status.md and the latest R/K records as the source of truth. Preserve role separation. Continue same-session handoff until blocked or R gives terminal approval.
```

## 4. First R turn

R reads project evidence and writes `.ai-dev-loop/reviews/0001-r-*.md`. If no durable project requirements exist, R records the missing requirements as a blocker instead of inventing product scope.

## 5. First K turn

K addresses every open required finding, performs a whole-change impact scan, validates, and writes `.ai-dev-loop/responses/0001-k-*.md`. The whole-change impact scan is not a complete task-list generator, but it prevents narrow edits by requiring K to inspect affected artifacts beyond literal R file mentions.

## 6. Status sync

After every R or K role turn, update `.ai-dev-loop/status.md` with current status values, open findings, latest records, blockers, completed items, and one next expected role action.

## 7. Common stop conditions

Stop and record a blocker when safe authority, source evidence, file access, commands, credentials, or validation capability is missing. Do not claim skipped checks passed.

## 8. Terminal acceptance

R gives terminal approval only when required findings are closed or accepted risk, K questions and objections are resolved, validation evidence or blocking limitations are recorded, directly affected artifacts agree, status uses canonical values, and residual risk is explicit.
## Choose the smallest safe mode
Use minimal mode for small known-file changes, review mode for review-only work, degraded mode when tools are unavailable, and release mode for package, benchmark, challenged-score, or release-candidate work. Minimal mode is not a bypass for evidence or validation-tier honesty.

