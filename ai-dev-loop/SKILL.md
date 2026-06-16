---
name: ai-dev-loop
version: 1.4.3
scripts: [scripts/install-ai-dev-loop-template.py, scripts/validate-ai-dev-loop-package.py]
references: [README.md, REFERENCE.md]
---

# Skill: AI Development Loop

## Goal
Run an auditable R/K loop. R reviews requirements, plans, diffs, tests, documentation, risks, and evidence. K responds to every required finding, scans whole-change impact, updates all directly affected files, validates, and records evidence.

Store durable records under `.ai-dev-loop/`. `REFERENCE.md` is an optional expansion file for edge cases, conflict, degraded mode, release work, compression, roadmap continuation, escalation, or record uncertainty. Do not load `REFERENCE.md` by default for simple role turns.

## Status vocabulary
`Overall Status`: `Blocked`, `Changes requested`, `Pending implementation`, `Approved with notes`, `Approved`.
`Spec/Plan Status`: `Not started`, `Changes requested`, `Approved for implementation`, `Approved with notes`, `Approved`, `Not applicable`.
`Implementation Status`: `Not started`, `Changes requested`, `Pending implementation`, `Approved with notes`, `Approved`, `Not applicable`.
Most restrictive wins: unresolved required fixes or unresolved K questions/objections awaiting R => `Changes requested`; missing safe input or authority => `Blocked`; approved with non-blocking notes => `Approved with notes`.

## Core principles
- Durable files, not chat memory, are source of truth. Do not rely on hidden chain-of-thought, stale context, or assumptions; copy relevant chat facts into `.ai-dev-loop/`.
- Keep R/K separate in records; never act as both roles in one record. Role switch is internal: after a completed R or K turn, reload status and continue with the next expected R/K action in the same session unless a stop condition below holds. Use the same local branch unless user requests a switch.
- Every role turn writes durable markdown. R records reviews/concerns/approvals; K records responses/decisions/spec/code/test updates. Do not invent evidence; record files, commands, outputs, commits, limits.
- Respect `status.md` scope. Continue the current loop until R has no required follow-up. Current-issue lock: K must finish, block, or obtain written R/human risk acceptance for every current R-required finding before starting any next item, refactor, cleanup, or opportunistic implementation.
- Do not ask humans for ordinary engineering choices when repo context is enough. K can ask R for clarification or object to a requirement/finding that is unclear, inconsistent, unsupported, unsafe, or likely wrong. K records evidence, risk, proposed safe path, and whether safe partial progress exists.
- Open required findings ledger: `status.md` carries all unresolved required findings until R closes them or records accepted risk. R must carry forward unresolved findings; K must address all open required findings listed in status, not only the latest review.
- R must inspect diffs, files, docs, tests, and status; K's response alone does not prove resolution. K must not mark findings resolved without evidence. Final confirmation is R-owned: a K response can request review but can never be terminal approval.
- Documentation consistency is a hard gate: behavior/API/CLI/config/data/workflow/validation/packaging/user-visible changes require affected docs/specs/examples/install/quickstart/reference updates or no-doc rationale. R findings define required outcomes, not complete K task checklists. K must scan for directly related fallout and fix docs, examples, tests, validators, scripts, packaging notes, and status templates even when R did not name those files. R must verify code-doc-test consistency with file/diff evidence.
- K resolves spec/doc gaps before code when repo evidence supports a safe update. After R approval, K edits actual repo source directly, not detached artifacts/shadow trees unless required. K must address current R-required issues before any new implementation. Scope-change freeze: no unrelated behavior, broad refactors, dependencies, formatting churn, or cleanup; record adjacent work as future findings/decisions.
- Prefer small focused commits; avoid mixed commits combining unrelated review, spec, and code changes.
- If `SKILL.md`, `REFERENCE.md`, examples, and status records conflict: user instruction, repo instructions, `SKILL.md`, current status, decisions, `REFERENCE.md`, examples.

## Token Efficiency
Keep records compact: target <350 words per R/K record; table findings; summarize logs; reload durable state. Every 4-5 turns, move resolved status history into `context/` or `decisions/`. In live `status.md`, omit `## Next Item` and `## Blockers` when value is None.

## Workspace bootstrap
1. Locate project root with `git rev-parse --show-toplevel`; if it fails, use the root-confirmation checks below.
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
- Every completed K turn must commit K response, `status.md`, and spec/code/test changes, then set `Next Expected Role Action` to R review unless K is blocked awaiting R or human input.
- Use exact commit-subject prefixes: `R: <review action>` for R, `K: <implementation/response action>` for K.
- Do not treat a role turn as complete, approved, or ready for handoff until its required commit succeeds or degraded-mode evidence explicitly explains why no commit can exist.
- Record commit hashes only after commit exists. If the current record/status is being committed with the change, `pending current commit` is valid for that closed historical turn; do not treat it later as missing evidence. If commit fails, write `Commit: not committed: <reason>` and list uncommitted paths in role record and `status.md`.

## Records
Use four-digit increasing IDs, preserving numbering: `reviews/0001-r-review.md`, `responses/0001-k-response.md`, `context/0001-context.md`, `decisions/0001-decision.md`. Every role turn updates `status.md`, latest pointers, approval state, and next action.

Role-local state sources are mandatory: read git status/log/diff, `status.md`, latest R/K records, context/decisions, relevant specs/docs/code/tests, and validation before acting. Chat is not evidence unless copied into durable records.

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
<R action, K action, human action, or Stop; Stop only after an R review approves; R/K means continue now>
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
## Clarification and Objection Responses
- Questions answered: <K question IDs or None>
- Objections resolved: <K objection IDs, decision/evidence/risk acceptance, or None>
## Approval Status
- Spec/Plan Status: <value>
- Implementation Status: <value>
- Overall Status: <value>
## Next Expected K Action
```
R approves only when required issues are resolved or accepted risk with evidence. Required follow-up means `Changes requested`; non-blocking notes use `Approved with notes`. Documentation discrepancy, missing tests, or unintended scope change is a finding. R must answer each K clarification/objection in `## Clarification and Objection Responses` before expecting more implementation.

## K role
K reads latest R review, status open-finding ledger, context/decisions, repo state, docs/specs/examples, and changed files. K responds to every open required finding. K then performs a whole-change impact scan and updates all directly affected specs/docs/examples/tests/validators/scripts/package guidance, not only literal R bullet items or requested files. K validates, records evidence, and keeps scope limited to active findings plus necessary related consistency fixes; unrelated adjacent work becomes a new finding/decision/next item.

K writes `.ai-dev-loop/responses/NNNN-k-response.md`:
```md
# K Response NNNN: <topic>
## Review Addressed
## Summary
## Evidence
- Commit: <hash and `K: ...` subject, or `not committed: <reason>`>
- Finding coverage: <all open required finding IDs and status>
- Whole-change impact scan: <docs/specs/examples/tests/validators/scripts/package guidance searched or updated, or no-impact rationale>
## Finding Responses
### Response to R-NNNN-01
- Status: Addressed | Partially addressed | Not addressed | Accepted risk
- Changes made:
- Evidence:
## Spec Updates
## Documentation Updates
## Implementation Updates
## Tests and Validation
## Clarifications or Objections
- Questions for R: <only unresolved spec/requirement questions, or None>
- Objections: <requirement/finding objections with evidence and proposed alternative, or None>
## Compact Context
## Next Expected R Action
```
K responses are never final approval. After K changes, `status.md` and `## Next Expected R Action` must request R review unless K is blocked and records the blocker. K must not mark findings resolved without evidence. Changed behavior requires `Documentation Updates` or `Not needed because <evidence>`. If any item is unresolved, unvalidated, or missing evidence, set `Overall Status: Changes requested` or `Blocked` and keep `Next Item: None`; then ask R, object, or block with disputed requirement, evidence, risk, safe path, and possible partial progress.

## Context compression
Use `.ai-dev-loop/context/NNNN-context.md` when context is long, stale, near handoff, or may exceed memory. Preserve focus/scope, status, findings, blockers, decisions, changed paths, commits, validation, next action. Never remove open findings, blockers, validation limits, human constraints, changed paths, commits, approval status.

## Decisions and blockers
Create `.ai-dev-loop/decisions/NNNN-decision.md` for durable architecture/product decisions or blockers: missing requirements, secrets, destructive operations, compliance, production impact, ambiguous intent, divergence, unsafe autonomous choice.

## Clarification and conflict handling
R/K resolve ordinary ambiguity from repo evidence first. K can update low-risk specs that match durable requirements. K asks R instead of guessing when requirements are unclear, contradictory, or underspecified. K objects when evidence, safety, tests, user intent, or maintainability contradict the request. Record questions/objections with evidence, impact, and safe path; R must answer, revise, uphold, or accept risk next. Escalate beyond R only for missing authority, destructive/irreversible action, secrets, external systems, production/user-data/security/compliance/cost risk, or repeated R/K disagreement.

## Production hardening gates
- Latest R review is a hard gate; latest R review plus `status.md` open-finding ledger is a hard gate. `Open`, `Changes requested`, `Blocked`, unresolved required action, or unresolved K question/objection freezes all new implementation scope.
- K cannot skip, reorder, batch around, defer, or partially bypass current R-required issues; fix with evidence, ask R, object, prove impossible/unsafe, or record written R/human risk acceptance.
- Current-issue lock survives roadmap priority: K shall not move to the next implementation while the current issue advised by R is unresolved, unvalidated, or missing evidence.
- No silent softening: do not reinterpret MUST/required/never rules as advisory to fit token limits, tool limits, speed, or convenience. Compress wording, not obligations.
- Documentation drift prevention: code-only fixes are incomplete when docs/specs/examples/tests/user guidance become inaccurate; R must block approval and K must fix the drift before moving on.
- Package maintenance must keep non-negotiable rules in always-loaded `SKILL.md`; `REFERENCE.md` may expand but must not weaken them.

## Practical failure prevention
- Scope-change control: K fixes only the active findings unless R explicitly authorizes added scope; discovered adjacent work becomes a new finding, decision, or next item after approval.
- Code-doc-test-harness matrix: K records changed behavior, changed files, related docs/spec/examples/tests/validators/scripts/package guidance touched or no-impact rationale, validation, and remaining risk. R verifies that matrix before approval.

## Autonomous workflow
Phases: spec review (R) → implementation (K) → impl review (R) → continuation within authorized scope. A finished role turn hands off to the other role inside the same session, not to the user. Writing `Next Expected Role Action` is not performing it; if it names R or K, execute that role next. Loop ends only when R records `Approved` or `Approved with notes` with no required K follow-up and `Next Expected Role Action: Stop`. K must not set terminal approval state; hand off to R for final review. Trigger blocker when: same finding fails after 3 K attempts; R/K disagree twice on intent/risk/external context; 2 rounds make no material change; or item exceeds 6 R/K rounds. Write/commit blocker, mark `Blocked`, stop.

## Gates
Before any role turn is complete:
- Required record headings are present.
- Evidence is specific and reproducible.
- Every R finding has a K response, recorded K clarification/objection awaiting R, or remains in `status.md` Open Required Findings; open required findings block next implementation, as do unresolved K questions/objections.
- Specs, documentation, examples, tests, and implementation agree; required findings are resolved with evidence, blocked, or accepted as risk by R/human.
- Tests are added/updated for changed behavior where practical; validation commands/results are recorded; documentation updates or no-doc rationale are recorded.
- Implementation edits are in the real repository working tree, not only detached artifacts/copies.
- `status.md` is synchronized with latest files and approval state; terminal `Stop` or final approval appears only after an R review, never directly after a K response.
- Before ending the session or addressing the user, confirm a terminal stop condition holds; if `Next Expected Role Action` names R or K, continue that role now.
- Required commits exist when git is available; hashes are recorded only when real.
- No unrelated user changes were overwritten, staged, or committed.
- Degraded mode limitations are explicit.

## Recommended command pattern
Command order:
1. Read status/open findings.
2. Inspect branch/status, latest R/K/context, relevant docs/specs/examples/files/diffs.
3. Run targeted validation and whole-change impact scan.
4. Write role record/status.
5. Review own diff.
6. Commit with `R:` or `K:` subject.
7. Record real hash or degraded reason.

## Failure handling
If commands fail, record exact command, failure, impact, likely cause, alternatives. Fix K-caused issues and commit. For pre-existing/flaky/environment failures, record baseline evidence and why unrelated. R can approve with notes only with adequate alternative validation. Block if failure prevents validation, hides regression risk, or creates security/data-loss risk. Human escalation requires blocked safe progress, missing workspace evidence, and material product/data/security/compliance/cost/user risk; write/commit blocker first. See `REFERENCE.md` for validator/installer hardening details.

## Operating instruction
At start, read this file and status. Determine the next role and perform that role only; write record, update status, validate, commit when required. Then reload status and continue the next expected R/K role in the same session. Do not stop after a commit, summary, or written handoff. Stop and address the user only when: R approved with no open required findings and `Next Expected Role Action: Stop`; a committed blocker sets `Overall Status: Blocked`; or K needs human-only authority for missing requirements, secrets, or destructive/irreversible/external action. If none holds, execute the next role now; summarize paths/evidence only at a valid stop.
