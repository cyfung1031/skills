---
name: ai-dev-loop
version: 1.3.3
scripts: [scripts/install-ai-dev-loop-template.py, scripts/validate-ai-dev-loop-package.py]
references: [README.md, REFERENCE.md]
---

# Skill: AI Development Loop

## Goal
Run an auditable R/K loop. R reviews requirements, plans, diffs, tests, documentation, risks, and evidence. K responds, updates files including docs, validates, and records evidence.

Store durable records under `.ai-dev-loop/`. `REFERENCE.md` is an optional expansion file for edge cases, conflict, degraded mode, release work, compression, roadmap continuation, escalation, or record uncertainty. Do not load `REFERENCE.md` by default for simple role turns.

## Status vocabulary
`Overall Status`: `Blocked`, `Changes requested`, `Pending implementation`, `Approved with notes`, `Approved`.
`Spec/Plan Status`: `Not started`, `Changes requested`, `Approved for implementation`, `Approved with notes`, `Approved`, `Not applicable`.
`Implementation Status`: `Not started`, `Changes requested`, `Pending implementation`, `Approved with notes`, `Approved`, `Not applicable`.
Most restrictive wins: unresolved required fixes => `Changes requested`; missing safe input => `Blocked`; approved with non-blocking notes => `Approved with notes`.

## Core principles
- Durable files, not chat memory, are source of truth. Do not rely on hidden chain-of-thought, stale context, or assumptions; copy relevant chat facts into `.ai-dev-loop/`.
- Keep R/K separate; switch roles only after writing records, committing when git is available, and reloading state. Use the same local branch unless user requests a switch.
- Every role turn writes durable markdown. R records reviews/concerns/approvals; K records responses/decisions/spec/code/test updates. Do not invent evidence; record files, commands, outputs, commits, limits.
- Respect `status.md` scope. Continue the current loop until R has no required follow-up. Current-issue lock: K must finish, block, or obtain written R/human risk acceptance for every current R-required finding before starting any next item, refactor, cleanup, or opportunistic implementation.
- Do not ask humans to choose ordinary engineering options when repo context is enough; decide, record evidence, continue. Escalate only under blocker rule.
- Open required findings ledger: `status.md` carries all unresolved required findings until R closes them or records accepted risk. R must carry forward unresolved findings; K must address all open required findings listed in status, not only the latest review.
- R must inspect diffs, files, docs, tests, and status; K's response alone does not prove resolution. K must not mark findings resolved without evidence.
- Documentation consistency is a hard gate: whenever K changes behavior, API, CLI, config, data model, workflow, validation, packaging, or user-visible semantics, K must update affected docs/specs/examples/install/quickstart/reference records or explicitly record why no docs change is needed. R must check documentation discrepancy and request fixes. R must verify code-doc-test consistency using direct file/diff evidence.
- K resolves spec/doc gaps before code when possible. After R approval, K edits actual repo source directly, not detached artifacts, copied sandboxes, patch-only files, or shadow trees unless required. K must address current R-required issues before any new implementation. Scope-change freeze: while fixing an R finding, K must not introduce unrelated behavior, broad refactors, dependency changes, formatting churn, or cleanup; record newly discovered issues as future findings/decisions.
- Prefer small focused commits; avoid mixed commits combining unrelated review, spec, and code changes.
- If `SKILL.md`, `REFERENCE.md`, examples, and status records conflict: user instruction, repo instructions, `SKILL.md`, current status, decisions, `REFERENCE.md`, examples.

## Token Efficiency
Keep records compact: target <350 words per R/K record; table findings; summarize logs; reload durable state. Every 4-5 turns, move resolved status history into `context/` or `decisions/`.

## Workspace bootstrap
1. Locate project root with `git rev-parse --show-toplevel` when possible.
2. If git root lookup fails, confirm current directory is project root, not `/`, `/mnt`, `/mnt/data`, `/tmp`, home, or another broad parent.
3. Initialize git only in a confirmed project root; otherwise record degraded mode.
4. For zips, extract into a new empty staging directory first, then copy intended files into project root. Avoid broad/dirty workspaces.
5. Ensure `.ai-dev-loop/` exists with `status.md`, `reviews/`, `responses/`, `context/`, and `decisions/`.
6. If git is unavailable, degraded mode: write records, include snapshots/diffs where practical, and state commit hashes are unavailable.

Never initialize git in a broad parent. Never rewrite history unless explicitly asked.

## Git behavior
When git is available:
- Check `git status --short` and branch before changes; distinguish pre-existing from own changes.
- Never discard, overwrite, stage, commit, reset, clean, amend, or rebase user changes unless asked; work around unrelated dirty files and record the constraint.
- Every completed R turn must commit its R review and `status.md` update.
- Every completed K turn must commit K response, `status.md`, and spec/code/test changes.
- Use exact commit-subject prefixes: `R: <review action>` for R, `K: <implementation/response action>` for K.
- Do not treat a role turn as complete, approved, or ready for handoff until its required commit succeeds or degraded-mode evidence explicitly explains why no commit can exist.
- Record commit hashes only after commit exists. If commit fails, write `Commit: not committed: <reason>` and list uncommitted paths in role record and `status.md`.

## Records
Use four-digit increasing IDs, preserving numbering: `reviews/0001-r-review.md`, `responses/0001-k-response.md`, `context/0001-context.md`, `decisions/0001-decision.md`. Every role turn updates `status.md`, latest pointers, approval state, and next action.

Role-local state sources are mandatory: each role reads git status/log/diff, `status.md`, latest R/K records, context/decisions, relevant specs, docs, code, tests, and validation evidence before acting. Chat is not evidence unless copied into a durable record.

## Status template
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
- Spec/Plan Status: <value>
- Implementation Status: <value>
- Overall Status: <value>
## Open Required Findings
<finding IDs, required actions, owner, evidence needed, or None>
## Completed Items
<done items or None>
## Next Expected Role Action
<R action, K action, human action, or Stop>
## Next Item
<next authorized item or None>
## Blockers
<blockers or None>
```

## R role
R reviews requirements, plans, diffs, docs/specs, examples, tests, prior K responses, open-finding ledger, records, and repo state. Verify claims with direct evidence. Before approval, R must match changed behavior against docs/specs/examples/tests and inspect for unintended scope changes.

R writes `.ai-dev-loop/reviews/NNNN-r-review.md`:
```md
# R Review NNNN: <topic>
## Scope
## Summary
## Evidence
- Commit: <hash and `R: ...` subject, or `not committed: <reason>`>
- Coverage: <open findings reviewed, docs/specs/examples/tests checked, changed paths inspected>
## Findings
### Finding R-NNNN-01: <title>
- Severity: Critical|High|Medium|Low|Note
- Status: Open | Closed | Accepted risk
- Details:
- Required action:
## Clarifications Needed
## Approval Status
- Spec/Plan Status: <value>
- Implementation Status: <value>
- Overall Status: <value>
## Next Expected K Action
```
R approves only when required issues are resolved or explicitly accepted as risk with evidence. Required follow-up means `Changes requested`; non-blocking notes may be `Approved with notes`. R must not approve merely because K claims completion; R verifies files, diffs, docs/specs, examples, tests, status, and open-finding ledger. R must treat documentation discrepancy, missing tests for changed behavior, stale examples, or unintended scope change as review findings.

## K role
K reads latest R review, status open-finding ledger, context/decisions, repo state, docs/specs/examples, and changed files. K responds to every open required finding, updates code and documentation together, validates, records evidence, and keeps scope limited to the active findings.

K writes `.ai-dev-loop/responses/NNNN-k-response.md`:
```md
# K Response NNNN: <topic>
## Review Addressed
## Summary
## Evidence
- Commit: <hash and `K: ...` subject, or `not committed: <reason>`>
- Finding coverage: <all open required finding IDs and status>
- Drift scan: <docs/specs/examples/tests searched or updated, or no-doc rationale>
## Finding Responses
### Response to R-NNNN-01
- Status: Addressed | Partially addressed | Not addressed | Accepted risk
- Changes made:
- Evidence:
## Spec Updates
## Documentation Updates
## Implementation Updates
## Tests and Validation
## Remaining Questions
## Compact Context
## Next Expected R Action
```
K must not mark a finding resolved without evidence. K must answer every open R-required finding from the latest review and `status.md` before touching a next roadmap item, refactor, cleanup, or unrelated implementation. K must update docs/specs/examples/install/quickstart/reference for any changed behavior or record `Documentation Updates: Not needed because <evidence>`. K must run a drift scan by inspecting changed behavior against relevant docs/specs/examples/tests. K shall not move to the next implementation while any current issue advised by R is unresolved, unvalidated, or missing evidence. If any finding is partially addressed, not addressed, unvalidated, or lacks evidence, set `Overall Status: Changes requested` or `Blocked` and keep `Next Item: None` unless R explicitly accepted the risk. If unsafe to proceed, K records blocker and sets status `Blocked`.

## Context compression
Use `.ai-dev-loop/context/NNNN-context.md` when context is long, stale, near handoff, or may exceed memory. Preserve focus/scope, status, findings, blockers, decisions, changed paths, commits, validation, next action. Never remove open findings, blockers, validation limits, human constraints, changed paths, commits, approval status.

## Decisions and blockers
Create `.ai-dev-loop/decisions/NNNN-decision.md` for durable architecture/product decisions or blockers: missing requirements, secrets, destructive operations, compliance, production impact, ambiguous intent, divergence, unsafe autonomous choice.

## Clarification and conflict handling
R/K resolve ordinary ambiguity from repo evidence first. K may update specs without human input only when consistent with durable requirements and low risk. Escalate and stop only for missing authority, destructive or irreversible action, secrets, external systems, production/user-data/security/compliance/cost risk, or repeated R/K disagreement.

## Production hardening gates
- Latest R review is a hard gate; latest R review plus `status.md` open-finding ledger is a hard gate. `Open`, `Changes requested`, `Blocked`, or unresolved required action freezes all new implementation scope.
- K cannot skip, reorder, batch around, defer, or partially bypass current R-required issues; fix them with evidence, including documentation/test/example updates when relevant, prove them impossible/unsafe, or record written R/human risk acceptance.
- Current-issue lock survives roadmap priority: K shall not move to the next implementation while the current issue advised by R is unresolved, unvalidated, or missing evidence.
- No silent softening: do not reinterpret MUST/required/never rules as advisory to fit token limits, tool limits, speed, or convenience. Compress wording, not obligations.
- Documentation drift prevention: code-only fixes are incomplete when docs/specs/examples/tests/user guidance become inaccurate; R must block approval and K must fix the drift before moving on.
- Package maintenance must keep non-negotiable rules in always-loaded `SKILL.md`; `REFERENCE.md` may expand but must not weaken them.

## Practical failure prevention
- Open-finding carry-forward: every R review and K response must reconcile the `status.md` open required findings list; removed items require R closure or accepted-risk evidence.
- Scope-change control: K fixes only the active findings unless R explicitly authorizes added scope; discovered adjacent work becomes a new finding, decision, or next item after approval.
- Code-doc-test matrix: K records changed behavior, changed files, docs/spec/examples touched or no-doc rationale, tests/validation, and remaining risk; R verifies that matrix before approval.
- Evidence granularity: generic claims like "updated docs" or "tests pass" are insufficient without paths, commands, results, and finding IDs.

## Autonomous workflow
1. **Spec review**: R reviews requirements/plan. If authorized, set `Spec/Plan Status: Approved for implementation`, `Implementation Status: Not started`, and `Overall Status: Pending implementation`.
2. **Implementation**: K implements only within authorized scope, validates, records evidence, and asks for R review.
3. **Impl review**: R reviews diffs/tests/status. R requests changes, approves with notes, approves, or blocks.
4. **Continuation**: Continue only within explicitly authorized scope.

Loop ends only when R records `Approved`, or `Approved with notes` with no required K follow-up. If R records `Blocked` or `Changes requested`, K must resolve or block those findings before any next implementation; do not proceed based on roadmap order, convenience, or partial fixes. Trigger blocker when same finding fails after 3 K attempts, R/K disagree twice on missing intent/risk/external context, 2 rounds make no material change, or item exceeds 6 R/K rounds; write/commit blocker, mark `Blocked`, stop.

## Gates
Before any role turn is complete:
- Required record headings are present.
- Evidence is specific and reproducible.
- Every R finding has a K response or remains in `status.md` Open Required Findings; open required findings block next implementation.
- Specs, documentation, examples, tests, and implementation agree; required findings are resolved with evidence, blocked, or accepted as risk by R/human.
- Tests are added/updated for changed behavior where practical; validation commands/results are recorded; documentation updates or no-doc rationale are recorded.
- Implementation edits are in the real repository working tree, not only detached artifacts/copies.
- `status.md` is synchronized with latest files and approval state.
- Required commits exist when git is available; hashes are recorded only when real.
- No unrelated user changes were overwritten, staged, or committed.
- Degraded mode limitations are explicit.

## Recommended command pattern
Read status/open findings -> inspect branch/status -> inspect latest R/K/context -> inspect relevant docs/specs/examples/files/diffs -> run targeted validation and doc-drift scan -> write role record/status -> review own diff -> commit with `R:` or `K:` subject -> record real hash or degraded reason.

## Failure handling
If commands fail, record exact command, failure, impact, likely cause, alternatives. Fix K-caused issues when possible and commit. For pre-existing/flaky/environment failures, record baseline evidence and why unrelated. R may approve with notes only with adequate alternative validation; block if failure prevents validation, hides regression risk, or creates security/data-loss risk. Human escalation requires blocked safe progress, missing workspace evidence, and material product/data/security/compliance/cost/user risk; write/commit blocker first.

## Operating instruction
At start, read this file and status. Determine next role, perform only that role, write record, update status, validate, commit when required, summarize paths/evidence.
