---
name: ai-dev-loop
version: 1.3.1
description: Compact dual-role reviewer/implementer workflow for durable AI-assisted software development.
scripts:
  - scripts/install-ai-dev-loop-template.py
  - scripts/validate-ai-dev-loop-package.py
references:
  - README.md
  - COMPLETE-PACKAGE-GUIDE.md
  - INSTALLATION.md
  - QUICKSTART.md
  - REFERENCE.md
---

# Skill: AI Development Loop

## Purpose

Run an auditable two-role development loop:

- **R — Reviewer/Auditor**: reviews requirements, plans, diffs, tests, risks, and evidence.
- **K — Implementer/Keeper**: responds to findings, updates files, validates, and records evidence.

The loop is tool-agnostic and stores durable records under `.ai-dev-loop/`. This compact `SKILL.md` is enough for normal turns. `REFERENCE.md` is an optional expansion file; consult it only for edge cases, R/K conflict, degraded mode, release work, compression, roadmap continuation, escalation, or record-format uncertainty. Do not load `REFERENCE.md` by default for simple role turns.

## Canonical status vocabulary

Allowed `Overall Status`:

- `Blocked`
- `Changes requested`
- `Pending implementation`
- `Approved with notes`
- `Approved`

Allowed `Spec/Plan Status`:

- `Not started`
- `Changes requested`
- `Approved for implementation`
- `Approved with notes`
- `Approved`
- `Not applicable`

Allowed `Implementation Status`:

- `Not started`
- `Changes requested`
- `Pending implementation`
- `Approved with notes`
- `Approved`
- `Not applicable`

`Overall Status` is most restrictive: unresolved fixes mean `Changes requested`; missing human/project input means `Blocked`; approved implementation with non-blocking notes means `Approved with notes`.

## Core principles

- Treat durable files, not chat memory, as the source of truth.
- Keep R and K separate; a single agent may switch roles only after completing one role turn, writing records, and reloading state.
- Do not invent evidence. Record exact files, commands, outputs, commits, and limitations.
- Respect `status.md` scope. Do not start the next roadmap item unless the user, repo instructions, or status explicitly authorize it.
- Prefer small, reviewable changes and clear status transitions.
- R must inspect actual diffs, changed files, tests, and status. K’s response alone does not prove resolution.
- If `SKILL.md`, `REFERENCE.md`, examples, and status records conflict, follow: user instruction, repo instructions, `SKILL.md`, current status, decisions, `REFERENCE.md`, examples.

## Token Efficiency & Context Compression (v1.3.1)

Keep durable records compact:
- Target <350 words per R/K record; table multiple findings.
- Summarize logs with commands such as `git diff --stat` or `command | head -30`; do not paste long output.
- Reload prompts: R reads `SKILL.md`, status, latest K response, git status/diff, changed files. K reads `SKILL.md`, status, latest R review, relevant specs/code/tests.
- Every 4-5 turns, move resolved status history into `context/` or `decisions/`.

## Workspace bootstrap

1. Locate the project root with `git rev-parse --show-toplevel` when possible.
2. If git root lookup fails, confirm the current directory is the project root, not `/`, `/mnt`, `/mnt/data`, `/tmp`, home, or another broad parent.
3. Initialize git only in a confirmed project root; otherwise enter degraded mode and record the limitation.
4. For zips, extract into a new empty staging directory first, then copy intended files into the project root. Avoid broad or dirty workspaces.
5. Ensure `.ai-dev-loop/` exists with these paths:
   - `.ai-dev-loop/status.md`
   - `.ai-dev-loop/reviews/`
   - `.ai-dev-loop/responses/`
   - `.ai-dev-loop/context/`
   - `.ai-dev-loop/decisions/`
6. If git is unavailable, continue in degraded mode: write records, include snapshots/diffs where practical, and state that commit hashes are unavailable.

Never initialize git in a broad parent. Never rewrite history unless explicitly asked.

## Required git behavior

When git is available:

- Check `git status --short` before changing files.
- Distinguish pre-existing changes from your own.
- Commit meaningful completed role turns or implementation changes when repository policy allows.
- Record commit hashes only after the commit exists.
- Do not stage or commit unrelated user changes.

## Durable records

Use four-digit increasing IDs, preserving existing numbering:

- Reviews: `.ai-dev-loop/reviews/0001-r-review.md`
- Responses: `.ai-dev-loop/responses/0001-k-response.md`
- Context notes: `.ai-dev-loop/context/0001-context.md`
- Decisions: `.ai-dev-loop/decisions/0001-decision.md`

Every role turn updates `status.md`, latest record pointers, and next expected action.

## Required status template

```md
# AI Development Loop Status

## Current Branch

<branch or degraded-mode note>

## Current Focus

<task, roadmap item, or blocker>

## Latest R Review

<path or None>

## Latest K Response

<path or None>

## Latest Context Note

<path or None>

## Decisions

<paths or None>

## Approval State

- Spec/Plan Status: <canonical value>
- Implementation Status: <canonical value>
- Overall Status: <canonical value>

## Completed Items

<done items or None>

## Next Expected Role Action

<R action, K action, human action, or Stop>

## Next Item

<next authorized item or None>

## Blockers

<blockers or None>
```

## R role requirements

R reviews requirements, plans, diffs, tests, prior K responses, durable records, and repo state. Verify claims with direct evidence.

R writes `.ai-dev-loop/reviews/NNNN-r-review.md` using this structure:

```md
# R Review NNNN: <topic>

## Scope

## Summary

## Evidence

## Findings

### Finding R-NNNN-01: <title>
- Severity: Critical|High|Medium|Low|Note
- Status: Open | Closed | Accepted risk
- Details:
- Required action:

## Clarifications Needed

## Approval Status

- Spec/Plan Status: <canonical value>
- Implementation Status: <canonical value>
- Overall Status: <canonical value>

## Next Expected K Action
```

R may approve only when required issues are resolved or accepted as risk. Separate verified facts from unverified K claims.

## K role requirements

K reads latest R review, status, context/decisions, repo state, and changed files. K responds to every finding, updates files, validates, and records evidence.

K writes `.ai-dev-loop/responses/NNNN-k-response.md` using this structure:

```md
# K Response NNNN: <topic>

## Review Addressed

## Summary

## Evidence

## Finding Responses

### Response to R-NNNN-01
- Status: Addressed | Partially addressed | Not addressed | Accepted risk
- Changes made:
- Evidence:

## Spec Updates

## Implementation Updates

## Tests and Validation

## Remaining Questions

## Compact Context

## Next Expected R Action
```

K must not mark a finding resolved without evidence. If K cannot safely proceed, K records a blocker and updates status to `Blocked`.

## Context compression

Use `.ai-dev-loop/context/NNNN-context.md` when context is long, stale, near handoff, or may exceed working memory. Preserve only:

- current focus and authorized scope,
- latest status and approval state,
- open findings and blockers,
- durable decisions,
- changed paths, commit hashes, and validation evidence,
- next expected action.

Summarize command output as command + pass/fail/limited + key excerpt/diff. Paste full logs only to reproduce failure. Periodically move stale `Completed Items` detail to `context/` or `decisions/`.

Discard repeated rationale, superseded proposals, irrelevant logs, and resolved discussion. Never remove open findings, blockers, validation limits, human constraints, changed paths, commit hashes, or approval status.

## Decisions and blockers

Create `.ai-dev-loop/decisions/NNNN-decision.md` for durable architectural/product decisions. Include status, context, decision, consequences, and evidence.

Record a blocker when autonomous action is unsafe due to missing requirements, secrets, destructive operations, compliance, production impact, ambiguous intent, or repeated divergence.

## Autonomous workflow

1. **Spec/plan review**: R reviews requirements and plan. If the spec/plan authorizes K work, set `Spec/Plan Status: Approved for implementation`, `Implementation Status: Not started`, and `Overall Status: Pending implementation`.
2. **Implementation**: K implements only within authorized scope, validates, records evidence, and asks for R review.
3. **Implementation review**: R reviews actual diffs/tests/status. R either requests changes, approves with notes, approves, or blocks.
4. **Continuation**: Continue only within explicitly authorized scope. Otherwise stop with status updated and next action recorded.

Stop when the current authorized item is approved, a blocker requires human input, the user asks to stop, or continuing would exceed scope.

## Quality gates

Before any role turn is complete:

- Required record headings are present.
- Evidence is specific and reproducible.
- Every R finding has a K response or remains open.
- `status.md` is synchronized with latest files and approval state.
- Git state is checked and commit hashes are recorded only when real.
- Degraded mode limitations are explicit.

## Failure handling

If commands fail, record the command, failure, and impact. Try safe alternatives if available. Do not hide failures behind generic success language.

If the loop diverges after repeated R/K turns on the same issue, summarize the dispute, record the safe stopping point, mark status `Blocked`, and ask for human decision.

## Operating instruction

At start, read this file and status. Determine the next role, perform only that role, write the record, update status, validate, and summarize paths/evidence.
