# ai-dev-loop Reference Notes

This file holds non-normative guidance. `SKILL.md` remains the source of truth.

Use the loop when a repository benefits from a durable reviewer/implementer split:

1. R reviews specs, plans, code, tests, and prior K responses.
2. K responds to every finding, performs a whole-change impact scan, updates all directly affected specs/docs/examples/code/tests/validators/scripts/package guidance, validates, and records evidence.
3. Both roles update `.ai-dev-loop/status.md` after their turns.
4. Git commits are required audit trail entries when git is available.

Keep role records compact. Preserve evidence, changed paths, commands, validation results, open findings, blockers, and approval state. Compress repeated rationale and stale background.

---

# Extended Operating Reference

The root `SKILL.md` is intentionally compact to reduce always-loaded context. This file is optional expansion material for cases where compact rules need more detail. When this reference and `SKILL.md` conflict, `SKILL.md` is authoritative. Consult this file only when an edge case appears, degraded mode or release/package maintenance requires deeper detail, or a role turn cannot be completed confidently from `SKILL.md` alone.

# Skill: Dual-Role Software Development Review and Implementation Loop

## Purpose

Use this skill when a software development workspace already contains specifications, implementation plans, roadmaps, tickets, or design notes, and the AI agent must autonomously drive development through two cooperating roles:

- **R — Reviewer/Auditor**: reviews specifications, plans, and implementation work; identifies risks, gaps, contradictions, unclear requirements, and quality issues.
- **K — Implementer/Keeper**: updates specifications, resolves reviewer feedback, implements code, tests changes, performs related documentation/harness consistency updates, and records responses.

The process runs normal review, clarification, implementation, and follow-up cycles without human decisions. R and K can exchange explicit clarification questions or evidence-backed objections inside the loop. Human involvement is required only for blocked decisions outside the available specifications or project authority.

## Tool-Agnostic Scope

This skill is not specific to any single coding assistant. It can be used with any comparable repository-editing agent that can read files, edit the workspace, run validation commands, and create local git commits. Vendor-specific integrations, if any, are optional adapters rather than requirements.

When a tool has its own skills, rules, memory, custom instructions, project policy files, or repository instruction mechanism, install or reference this `SKILL.md` there. When it does not, keep `SKILL.md` in the repository, preferably under `.ai-dev-loop/SKILL.md`, and instruct the agent to load it before working.

Tool-specific commands, directories, or UI features are adapters only. The normative workflow is the repository-local process: durable `.ai-dev-loop/` records, real working-tree edits, validation evidence, synchronized `status.md`, and local git commits.


## Canonical Status Model

Use this exact status vocabulary in R reviews, K responses, context notes, decisions, and `status.md`.

**Spec/Plan Status:**

- `Not started`
- `Changes requested`
- `Approved for implementation`
- `Approved with notes`
- `Approved`
- `Not applicable`

**Implementation Status:**

- `Not started`
- `Changes requested`
- `Pending implementation`
- `Approved with notes`
- `Approved`
- `Not applicable`

**Overall Status:**

- `Blocked`
- `Changes requested`
- `Pending implementation`
- `Approved with notes`
- `Approved`

Interpretation rules:

- `Blocked` means a human decision, external access, missing authority, or unsafe product/security/legal/cost choice prevents safe progress.
- `Changes requested` means K must update specs, code, tests, documentation, or coordination records before the reviewed artifact can be approved.
- `Pending implementation` means the spec or plan is approved and K is authorized to implement, but the implementation has not yet been reviewed.
- `Approved with notes` means K must continue only when R records no required corrective action; notes are advisory or future-facing only.
- `Approved` means no further follow-up is required for the reviewed scope.

Do not invent additional approval states. When a review covers both planning and implementation, always write all three fields: `Spec/Plan Status`, `Implementation Status`, and `Overall Status`.

## Core Principles

1. **Single working branch**
   - R and K must work on the same current local branch.
   - Do not switch branches unless the user explicitly requests it.
   - Every meaningful change by either role must be committed locally when git is available. If git is unavailable, git identity is missing, permissions prevent commits, or the repository is in degraded mode, record the limitation and exact uncommitted paths in the role record and status file. Repository policy is not a reason to skip commits unless that policy is explicitly present in durable project instructions or stated by the user.
   - If the repository has an existing commit policy, follow it while preserving durable `.ai-dev-loop/` records and never claiming a commit exists when it does not.
   - Use local commits as the shared history, audit trail, and rollback mechanism.

2. **Markdown-based handoff**
   - R records every review, audit, concern, clarification request, and final approval in markdown.
   - K records every response, decision, spec update, implementation update, and test result in markdown.
   - **Every role turn must write markdown.** An R turn is complete when the R review and synchronized status update are written and committed when git is available. A K turn is complete when the K response, any repository changes, and synchronized status update are written and committed when git is available; K must then request R review unless blocked. A K response is never terminal approval. A full review-response cycle is complete only when required R and K records both exist, except when R records final approval with no required K follow-up.
   - Markdown files are the durable conversation between R and K.

3. **Role-local context, not chat-memory context**
   - R and K must not rely on hidden chain-of-thought, chat memory, stale conversation context, or assumptions from prior turns.
   - Each role must reconstruct current state from durable sources: git history, workspace files, `.ai-dev-loop/` records, specs, plans, code, and test results.
   - Each role must explicitly cite or reference the durable files, commits, commands, and findings it used.
   - If prior chat content matters, copy the relevant facts into `.ai-dev-loop/` markdown before relying on them.

4. **Compressed context by default**
   - Use the integrated Context Compressor rules in this skill to reduce token usage while preserving correctness.
   - Prefer compact records, stable identifiers, summaries of command output, and exact file paths over repeated prose.

5. **Autonomous loop**
   - R and K continue the review-response loop until R has no further follow-up.
   - K may then proceed to the next implementation step only after the latest R review has no unresolved required finding or R/human has accepted the risk in writing.
   - Respect the user's current requested scope. Do not proceed to the next roadmap item unless the user asked for autonomous continuation, the project instructions explicitly authorize it, or `status.md` already records that continuation scope.
   - The AI must not ask the human to choose between ordinary engineering options when workspace evidence is sufficient for a safe decision.

6. **Spec-first discipline**
   - Before implementation, R audits the relevant specifications and implementation plan.
   - K resolves spec gaps before writing code when repo evidence supports a safe update.
   - If implementation reveals a spec issue, K updates the spec and records the reason.
   - R then reviews both the spec and implementation changes.

7. **Small, reversible steps**
   - Prefer small commits with focused scope.
   - Each commit must stay focused: one review note, one response, one spec update, one implementation step, or one test/fix step unless the repo requires an atomic cross-file change.
   - Avoid large mixed commits that combine unrelated review, spec, and code changes.

8. **Direct repository asset modification after approval**
   - After R approves the relevant specification, plan, or roadmap item, K must modify the actual project source files in the repository workspace directly.
   - K must not implement in a detached artifact staging area, copied sandbox, generated patch-only file, or parallel shadow tree unless the user or repository instructions explicitly require that workflow.
   - The real repository working tree is the source of truth. K validates and commits the actual modified source, tests, specs, and coordination markdown on the same local branch.
   - Temporary files may be used only as scratch space and must not replace direct repository edits or local commits.

## Workspace Conventions and Bootstrap Defaults

Create a durable coordination directory if the workspace does not already define one:

```text
.ai-dev-loop/
  README.md
  reviews/
  responses/
  decisions/
  context/
  status.md
```

Recommended file naming:

```text
.ai-dev-loop/reviews/NNNN-r-review.md
.ai-dev-loop/responses/NNNN-k-response.md
.ai-dev-loop/decisions/NNNN-decision.md
.ai-dev-loop/context/NNNN-context.md
```

Where `NNNN` is a zero-padded sequence number such as `0001`, `0002`, `0003`.

If the repository already has a project-specific location for agent notes, ADRs, review logs, or implementation records, use that location. Document the chosen location in `.ai-dev-loop/README.md` or the existing equivalent.

## Integrated Context Compressor

Apply these rules whenever this skill is active. The goal is to reduce token usage in both thinking and writing without weakening the audit trail.

### Operating mode

- Use short, direct progress updates and markdown records.
- State only current action, durable evidence, decisions, changed files, validation result, and next action.
- Avoid restating stable instructions, accepted decisions, full logs, or old alternatives.
- Prefer exact paths, sequence numbers, commit hashes, command names, and finding IDs.
- Use compact records by default: target roughly 200-500 words for ordinary R/K records, shorter for routine approvals, longer only for high-risk evidence.
- Prefer a small focused set of R clarification questions when blocked by unclear requirements; escalate to a human only under the human-escalation criteria. Otherwise make a safe autonomous assumption and document it.

### Context pruning

Keep:

- Current goal and latest user correction.
- Constraints affecting safety, permissions, git, output format, specs, tests, or project scope.
- Current approval state, blockers, and active findings.
- Files changed, commands run, test status, and remaining work.
- Non-obvious facts discovered from code, tools, specs, or prior durable records.

Drop or compress:

- Rejected alternatives after recording the decision.
- Full command logs after summarizing as command + pass/fail/limited + key excerpt, diff, or failure line.
- Repeated process explanations.
- Large pasted content after extracting actionable facts.
- Polite filler and redundant caveats.

### Compact handoff format

Use this format for role-local summaries, continuation notes, or status compression:

```markdown
Goal: <current objective>
State: <approval state and active phase>
Decisions: <durable decisions only>
Changed: <paths and commits>
Verified: <commands and result summary>
Next: <single next action>
Risks: <blockers or none>
```

For brief progress updates, use:

```markdown
Now: <current action>
Found: <new durable fact>
Next: <next action>
```

Omit empty fields. In simple role turns, put the compact handoff in the K `Compact Context` section or in `status.md`; create a separate context note only when the context note creation gate below is met.

### Role-switch reload prompts

Use minimal reload prompts instead of pasting old records:

- R reload: `Read SKILL.md, status.md, latest K response, changed files, git diff/status, then write the next R review.`
- K reload: `Read SKILL.md, status.md, active R review, relevant files, git status, then address each finding and write the next K response.`

Do not load `REFERENCE.md` unless the turn hits an edge case, package maintenance, degraded mode, context compression, human escalation, or uncertainty.

### Compression boundary

Compression must never remove:

- Open findings or blocker rationale.
- Test failures, skipped validations, or environment limitations.
- Commit hashes and changed file paths.
- Human decisions or user-provided constraints.
- Approval status and required next role action.


## Workspace Bootstrap and Degraded Mode

Use these defaults when a workspace is empty, new, or not yet prepared for the loop.

### Initial setup for an empty or new workspace

If `.ai-dev-loop/` is missing, create it at the workspace root before the first R or K role record unless the repository already defines an equivalent coordination directory. Create at least:

```text
.ai-dev-loop/
  README.md
  reviews/
  responses/
  decisions/
  context/
  status.md
```

If no specs, plans, roadmap, tickets, or design notes exist, do not invent product requirements. Create bootstrap coordination records stating that the project lacks reviewable requirements, record the safe stopping point, and ask for or point to project requirements only if no durable source exists.

### Git bootstrap

Before initializing git, detect whether the current directory is already inside an existing repository, worktree, or submodule:

```bash
git rev-parse --show-toplevel
```

If that command succeeds, use the reported repository root for normal operation. Do not run `git init` merely because `.git/` is absent in the current directory; in worktrees and submodules, `.git` can be a file, and nested project folders can inherit a parent repository.

Only run `git init` when all conditions hold:

- `git rev-parse --show-toplevel` fails.
- The current directory is confirmed as the intended project root.
- The directory is not `$HOME`, `/`, `/mnt/data`, or another broad container/workspace parent.

Confirm the current directory only when it contains a project manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`), a root `README.md` plus source directories, or an explicit user statement that this directory is the project root. Otherwise enter degraded mode and ask for the intended project root before initializing git:

```bash
git init
git status --short
git branch --show-current
```

Then create the initial coordination files and commit them when git is available. If git identity or permissions prevent the commit, enter degraded mode and record the limitation. Automatic `git init` is allowed only at a confirmed project root because this skill relies on local commits for auditability and rollback. Do not push or configure remotes unless the user explicitly asks.

### Non-git fallback and degraded mode

If git is unavailable, `git init` fails, git identity is missing, or commits cannot be created, continue only in degraded mode:

- Record the limitation in the current R/K record and `status.md`.
- List the exact changed or uncommitted paths.
- Continue with safe documentation, review, planning, and bootstrap work.
- Do not proceed with implementation changes beyond safe documentation/bootstrap work unless the user explicitly authorizes degraded mode for code changes.
- Never claim a commit exists when it does not. Use `pending current commit`, `not committed: <reason>`, or `not applicable`.

### Single-Agent Alternation Rules

A single AI agent may perform both R and K roles, but each role turn must be treated as a separate durable act:

- R writes only R review records and status updates for the R turn.
- K writes only K response records, implementation/spec/test changes, and status updates for the K turn.
- Do not merge R findings and K responses into one markdown file unless the user explicitly asks for a summary outside the formal loop.
- Commit each role turn separately when git is available.

## Required Git Behavior

Before starting work:

```bash
git status --short
git branch --show-current
```

Rules:

- Do not discard user changes.
- Do not overwrite uncommitted changes unless they were created by the current role in the current loop and the change is intentionally being amended.
- If unrelated uncommitted changes exist, avoid touching them when repo state permits and record the constraint.
- Every completed R turn must be committed locally after the R review and synchronized `status.md` update are written.
- Every completed K turn must be committed locally after the K response, synchronized `status.md`, and any spec/code/test changes are written.
- Every spec update, implementation change, and test update must be included in a K commit unless it is explicitly part of an R-only documentation review turn.
- Commit subjects must keep the role-log format: `R: <review action>` for R commits and `K: <implementation or response action>` for K commits. Do not replace these prefixes with generic subjects such as `update files` or `fix issue`.
- If commits cannot be created because the environment lacks git identity, permissions, or repository access, record `Commit: not committed: <reason>` as a validation limitation. List the exact files that remain uncommitted in the role record and `status.md`.

Required commit prefixes:

```text
R: audit specs for <topic>
R: review implementation for <topic>
R: approve <topic>
K: respond to review for <topic>
K: update specs for <topic>
K: implement <topic>
K: fix review findings for <topic>
K: add tests for <topic>
```

## Role R: Reviewer/Auditor

R is responsible for independent review and audit.

### R must review

- Existing specifications
- Implementation plans or roadmaps
- Acceptance criteria
- Architecture and design assumptions
- Dependencies and integration points
- Security, privacy, reliability, and data risks
- Test coverage expectations
- Implementation changes made by K
- Whether K's response fully resolves prior review comments

### R output format

R writes a markdown review file with this structure:

```markdown
# R Review NNNN: <topic>

## Scope

Describe the files, specs, plans, commits, or implementation areas reviewed.

## Summary

State the overall review result.

## Evidence

- Branch: <branch-name>
- Git status: <clean, dirty, or limited summary>
- Recent commits reviewed: <commit hashes or none>
- Files reviewed: <paths>
- Commands run: <exact commands or none>
- Validation result: <pass, fail, limited, or not applicable>

## Findings

### Finding R-NNNN-01: <title>

- Severity: Critical|High|Medium|Low|Note
- Status: Open | Closed | Accepted risk
- Type: Spec gap | Implementation issue | Test gap | Design risk | Clarification | Process issue
- Location: <file/path or commit reference>
- Details: <clear explanation>
- Required action: <specific requested action>

## Clarifications Needed

List questions only when the workspace does not contain enough information to make a safe autonomous decision.

## Clarification and Objection Responses

When K asked questions or objected, answer each item, revise the finding, uphold it with evidence, or record accepted risk. State `None` only when no K question or objection is pending.

## Approval Status

Use both fields when the review covers both planning/spec status and implementation status:

- Spec/Plan Status: Not started | Changes requested | Approved for implementation | Approved with notes | Approved | Not applicable
- Implementation Status: Not started | Changes requested | Pending implementation | Approved with notes | Approved | Not applicable
- Overall Status: Blocked | Changes requested | Pending implementation | Approved with notes | Approved

Overall status must be one of:

- Blocked: human input, external access, or a durable decision is required before safe progress can continue.
- Changes requested: K must update specs, code, tests, or documentation.
- Pending implementation: the spec/plan is approved and K is authorized to implement, but no implementation has been reviewed yet.
- Approved with notes: K must proceed only when notes require no follow-up before continuing.
- Approved: No further follow-up.

Do not use `Approved with notes` when any Critical, High, or Medium finding has a required K action.
Use `Changes requested` when K must correct the artifact under review before it can proceed.
Use `Pending implementation` when the spec/plan is approved, no correction is required before implementation starts, and R's findings are implementation requirements or documentation follow-up for K to perform next.
For spec audits that authorize implementation but still require K work, use `Spec/Plan Status: Approved for implementation` and `Implementation Status: Not started`. Use overall status `Pending implementation` unless the spec/plan itself needs correction.

## Next Expected K Action

State K's next required action.
```

### R decision rules

R must not block on minor style issues unless they affect correctness, maintainability, or project conventions.

R may approve when:

- The relevant specification is clear enough.
- The implementation matches the specification and documentation.
- Tests or validation are adequate for the change size and risk.
- No unresolved blocker, high, or medium findings remain.

R must continue the loop when:

- Requirements are contradictory.
- Acceptance criteria are missing for a material behavior.
- Implementation diverges from the plan.
- Documentation/specs/examples diverge from implemented behavior or user-visible workflow.
- Tests do not cover important behavior.
- Security, data loss, migration, or compatibility risks are unresolved.

## Role K: Implementer/Keeper

K is responsible for responding to R, updating specs and documentation, implementing code, validating changes, and fixing directly related cross-file/harness discrepancies discovered by the whole-change impact scan. R's findings define required outcomes and evidence, not a complete mechanical task list; K must not stop at the literal files or bullets R mentioned when related artifacts are affected.

### K must do

- Read R's latest markdown review.
- Address every finding explicitly.
- Treat R findings as required outcomes, not an exhaustive checklist; infer and fix all directly related discrepancies, including files R did not name.
- Run a whole-change impact scan across specs, docs, examples, tests, validators, scripts, installer/package guidance, status templates, and release notes when behavior or workflow changes.
- Update specifications when the issue is a spec gap.
- Update documentation, examples, installation notes, quickstart, package guides, or reference docs when behavior, commands, setup, API, config, workflow, validation, packaging, or user-visible semantics change.
- Update implementation when the issue is a code or behavior gap.
- Update tests when validation is insufficient.
- Record responses in markdown.
- Commit every meaningful response and change locally.
- After approved spec/plan review, modify the actual repository source files directly and commit those real workspace changes locally.

### K response format

K writes a markdown response file with this structure:

```markdown
# K Response NNNN: <topic>

## Review Addressed

Reference the R review file and relevant commit.

## Summary

Briefly summarize the response.

## Evidence

- Branch: <branch-name>
- Git status: <clean, dirty, or limited summary>
- Relevant commits: <commit hashes>
- Files changed: <paths or none>
- Whole-change impact scan: <related docs/specs/examples/tests/validators/scripts/package guidance checked or updated>
- Commands run: <exact commands or none>
- Validation result: <pass, fail, limited, or not applicable>
- Known limitations: <limitations or none>

## Finding Responses

### Response to R-NNNN-01

- Status: Addressed | Partially addressed | Not addressed | Accepted risk
- Changes made: <what changed>
- Evidence: <paths, commits, commands, validation, or accepted-risk rationale>
- Notes: <reasoning, tradeoffs, or follow-up>

## Spec Updates

List specification or plan updates, if any.

## Documentation Updates

List documentation/spec/example/install/quickstart/reference updates, or state `Not needed` with evidence.

## Implementation Updates

List implementation updates, if any.

## Tests and Validation

List commands run and results.

## Clarifications or Objections

- Questions for R: <only unresolved spec/requirement questions, or None>
- Objections: <requirement/finding objections with evidence and proposed alternative, or None>

Questions or objections must identify the exact requirement/finding, cite repo/spec/test evidence, explain the risk of implementing as written, and propose a safe default or alternatives when repo evidence supports them.

## Compact Context

Use the integrated Context Compressor handoff format. Include only durable state that R needs for the next review.

## Next Expected R Action

Ask R to review the response, updated specs, implementation, and tests.
```

### K decision rules

K autonomously chooses the next action when the existing roadmap, implementation plan, or specifications imply priority, but unresolved required R findings override roadmap priority and block new implementation. Within an active finding, K must go beyond R's literal bullet list and file mentions when necessary to complete the related change safely. Documentation, example, validator, script, installer, package-guide, or status-template discrepancy is a required finding when changed behavior/workflow and supporting artifacts diverge. Unrelated adjacent improvements are not part of the active fix; record them as future findings, decisions, or next items instead.

K may update specifications without human confirmation when:

- The update resolves ambiguity using existing project conventions.
- The update aligns with the implementation plan or roadmap.
- The update narrows behavior or completes directly related consistency work rather than introducing unrelated scope.
- The update is documented in the K response and committed.

K must avoid proceeding silently when:

- The requirement or finding is materially unclear, contradictory, or underspecified.
- R's requested action appears inconsistent with durable specs, tests, repo behavior, or user intent.
- K believes R is wrong, has missed evidence, or is asking for a change that would create avoidable defects or maintainability risk.
- The change would materially alter product direction.
- The change introduces a new external dependency with unclear approval.
- The change may delete or migrate user data.
- The change has security, legal, compliance, or cost implications not addressed by existing specs.

In those cases, K records a clarification request, objection, or blocker in markdown and stops at a safe boundary when continuing would require guessing.

## Role-Local Context Protocol

R and K must treat each role turn as if it starts with limited, potentially stale chat context. Before writing a role record, each role must reload state from durable artifacts.

### Required state sources

Each R turn reads, as applicable:

1. `git status --short` and recent git log.
2. Latest `.ai-dev-loop/status.md`.
3. Latest K response for the active sequence.
4. Relevant specs, plans, code, tests, and validation output recorded by K.
5. Prior R findings only when still open or referenced by status.

Each K turn reads, as applicable:

1. `git status --short` and recent git log.
2. Latest `.ai-dev-loop/status.md`.
3. The active R review file.
4. Relevant specs, plans, code, tests, and prior decisions.
5. The latest compact context note, if present.

### Context notes

Create or update `.ai-dev-loop/context/NNNN-context.md` when a round contains enough information that future R/K turns may otherwise waste tokens or rely on stale chat context. Context notes use the compact handoff format from the integrated Context Compressor section.

Context notes are summaries, not substitutes for source files. R and K may use them to find relevant durable evidence, but must verify critical facts against files, commits, or commands before approval or implementation.

### Context note creation gate

Create a context note rather than leaving `.ai-dev-loop/context/` empty when any of the following is true:

- A roadmap item, milestone, or stage gate is approved or handed off.
- A loop has reached three or more R/K records for the same item.
- The latest status file has become long enough that a future role would need to reread many old records to find the active state.
- The role is about to switch from spec review to implementation, or from implementation to review.
- The user provides material constraints in chat that are not already captured in repository files.

The context note must be compact and current. It includes only durable handoff facts: goal, state, decisions, changed paths/commits, validation, next action, and risks. It must not replace status, R/K records, specs, or code.

### Decision record gate

Create `.ai-dev-loop/decisions/NNNN-decision.md` only for durable decisions that affect future work and cannot be safely inferred from the approved spec, code, or R/K records. Examples include product-scope choices, security or data-risk tradeoffs, dependency approvals, architecture pivots, accepted deferrals, or human escalations.

Do not create fake decision records just to make the `decisions/` directory non-empty. If there are no durable decisions, leave the directory empty or include only a `README.md` explaining that decision records are created on demand.

Decision records use this compact structure. A blocker file may use `NNNN-blocker.md` with the same evidence fields plus the human-escalation fields below:

```markdown
# Decision NNNN: <topic>

## Status

Proposed | Accepted | Superseded | Blocked

## Context

<why a durable decision is needed>

## Decision

<the decision>

## Consequences

<expected impact, risks, follow-up>

## Evidence

- Related R/K records: <paths>
- Related commits: <hashes or none>
- Human input: <reference or none>
```

## Autonomous Workflow

### Phase 1: Specification and Plan Review

1. Inspect repository status and current branch.
2. Locate specifications, implementation plans, roadmap files, tickets, or design documents.
3. R reviews the relevant spec and implementation plan.
4. R writes a review markdown file.
5. R updates `status.md` and commits the review and status together with an `R: ...` subject.
6. K reads R's review.
7. K updates specs, plans, or clarification notes as needed.
8. K writes a response markdown file.
9. K updates `status.md` and commits the response, status, and any spec changes together with a `K: ...` subject.
10. Repeat until R records `Approved` or `Approved with notes` with no required follow-up.

### Phase 2: Implementation

1. K selects the next implementation item from the approved plan or roadmap only if the user requested autonomous continuation, project instructions authorize it, or `status.md` already records that continuation scope.
2. K modifies the actual project files in the repository workspace directly.
   - Source files, tests, configs, specs, and docs are changed in place.
   - Do not use artifact-only staging, copied source trees, or patch-only outputs as the implementation target unless explicitly required by project instructions.
   - Generated artifacts may be produced only when they are normal repository outputs required by the project workflow.
3. K implements the smallest coherent change.
4. K adds or updates tests and documentation as appropriate.
5. K runs relevant validation commands against the real repository working tree.
6. K records implementation notes and validation results in markdown.
7. Commit code, tests, docs, and K notes locally on the same branch.

### Phase 3: Implementation Review

1. R reviews the implementation against the approved specification and plan.
2. R records findings, clarification needs, or approval in markdown.
3. R updates `status.md` and commits the review and status together with an `R: ...` subject.
4. K addresses every finding.
5. K records responses and validation in markdown.
6. K updates `status.md` and commits the response, status, and changes together with a `K: ...` subject.
7. Repeat until R has no further follow-up.

### Phase 4: Next Roadmap Item

After R approves the completed implementation item:

1. K marks the item complete in the status file or project tracker if available.
2. Commit the status update.
3. K selects the next implementation item according to the roadmap or plan only if the user requested autonomous continuation, project instructions authorize it, or `status.md` already records that continuation scope.
4. Return to Phase 2.

## Status Tracking

Maintain or update `.ai-dev-loop/status.md` unless the project already has an equivalent tracker.

Suggested format:

```markdown
# AI Development Loop Status

## Current Branch

<branch-name>

## Current Focus

<spec, feature, ticket, or roadmap item>

## Latest R Review

<path and commit>

## Latest K Response

<path and commit>

## Latest Context Note

<path and commit, or none>

## Decisions

- <decision path and status, or none>

## Approval State

- Spec/Plan Status: Not started | Changes requested | Approved for implementation | Approved with notes | Approved | Not applicable
- Implementation Status: Not started | Changes requested | Pending implementation | Approved with notes | Approved | Not applicable
- Overall Status: Blocked | Changes requested | Pending implementation | Approved with notes | Approved

## Completed Items

- <item> — <commit>

## Next Expected Role Action

<next R or K action>

## Next Item

<next implementation item from roadmap or plan>

## Blockers

- <blocker or none>
```

### Status file ownership

To avoid role confusion and accidental overwrites, R and K own different sections of `.ai-dev-loop/status.md`:

- **R owns:** `Latest R Review`, R-side `Approval State`, open findings summary, and review blocker references.
- **K owns:** `Latest K Response`, `Completed Items`, `Next Item`, implementation/test summaries, and K-side blocker references.
- **Shared but append-only:** `Blockers`, `Decisions`, and compact context references. Do not delete another role's entry unless a later committed record explicitly resolves it.
- **Both roles may update:** `Current Focus` only when the change follows an approved plan or recorded decision.

Append dated/numbered status bullets only while they remain useful. When `Completed Items` grows beyond the active work, archive resolved history into `context/` or `decisions/`. Keep `status.md` focused on current state, latest R/K paths, approval state, active blockers, next action, and commit hashes.

### Commit-hash timing note

A status file cannot always know the hash of the commit that is about to introduce the status update. In that case, record the path plus `pending current commit`, then commit the files. A later role can replace or supplement it with the actual hash when useful. Do not invent commit hashes. When reviewing historical turns, the literal value `pending current commit` within a committed record is a valid, closed audit entry for that specific turn's commit. It must not be flagged as an uncommitted file, missing evidence, or open finding.


## Loop Termination Criteria

K responses may request review, document blockers, or ask questions but are never terminal approval. A review-response loop ends only when R records:

```text
Overall Status: Approved
```

or

```text
Overall Status: Approved with notes
```

and the notes do not require K follow-up before continuing.

If R records `Changes requested` or `Pending implementation`, K must respond or implement before moving forward. If R records `Blocked`, K must create or update a blocker/decision record and stop at a safe boundary unless the missing information is later found in durable workspace context.

## Circuit Breaker for Loop Divergence

The loop must not continue indefinitely. Trigger a circuit breaker and write `.ai-dev-loop/decisions/NNNN-blocker.md` when any of these occur:

- The same finding is rejected or re-opened after **three K resolution attempts**.
- R and K disagree twice about one of these: whether a finding is resolved, whether K's objection is valid, or whether a clarification can be answered from workspace evidence. This breaker applies only when the disagreement depends on product intent, risk tolerance, or external constraints absent from the workspace.
- Two consecutive rounds make no material change to specs, code, tests, or decision evidence.
- The loop exceeds **six R/K rounds** for one roadmap item without approval.

When the circuit breaker trips, K writes the blocker file first, records the safe stopping point, commits it, and stops for human input.

## Agent-Readable Instruction Style

Package instructions must be easy for agents to execute and validate. Prefer:

- imperative verbs: `must`, `do`, `record`, `verify`, `block`, `commit`;
- explicit triggers and outcomes;
- named fields, headings, files, commands, and status values;
- short sentences or numbered control flow for gates.

Avoid soft guidance for required behavior: `should`, `try to`, `might`, `natural`, `reasonable`, and long compound sentences. Use `can` only for permission, not obligation. Use `when repo evidence supports...` instead of vague `when possible`.

## Handling Clarifications and Objections

Use agent-readable control flow, not conversational advice:

1. K first checks durable repo evidence: specs, plans, roadmap files, code behavior, tests, README/developer docs, prior R/K records, and project conventions.
2. If evidence resolves the ambiguity, K records the decision and implements the safe path.
3. If the material gap remains, K records a question in `## Clarifications or Objections`, sets `Next Item: None`, and returns to R.
4. If R's request conflicts with evidence, creates avoidable risk, or appears to solve the wrong problem, K records an objection instead of implementing blindly.
5. When a clarification or objection changes behavior, K updates the relevant markdown/spec plus related docs, examples, tests, validators, scripts, installer/package guidance, and status templates that would otherwise drift.

Each K question or objection must include: exact unclear or disputed requirement, evidence checked, impact/risk, recommended safe path, and whether safe partial progress exists.

R's next review must answer, revise, uphold with evidence, or accept risk for each K question or objection before expecting further implementation. Until R does so, the open question or objection remains a required follow-up item in `status.md` and blocks new implementation scope. Escalate to the human only when the decision cannot be made safely from repository context or R/K disagreement reaches the circuit breaker criteria.

## Human Escalation Criteria

Stop and ask for human input only when all of the following are true:

- The issue blocks safe progress.
- The workspace does not contain enough information to decide.
- Choosing incorrectly could cause material product, data, security, compliance, cost, or user-facing impact.

When escalating, write a markdown blocker note first and commit it locally.

Use this format:

```markdown
# Blocker NNNN: <topic>

## Decision Needed

<specific decision>

## Why Autonomous Decision Is Unsafe

<reason>

## Options Considered

1. <option, pros, cons>
2. <option, pros, cons>

## Recommended Option

<recommendation if any>

## Current Safe Stopping Point

<what has been completed and committed>
```

## Record Completeness and Status Synchronization

### Mandatory template completeness

Every R review and K response must include all headings in the required template.
If a section has no content, write `None.` rather than omitting the section.
A role record is incomplete if any required heading is missing.

### Evidence block

Every R review and K response must include an Evidence section with durable facts used by the role:

- Branch
- Git status
- Relevant commits
- Files reviewed or changed
- Commands run
- Validation result
- Known limitations when applicable

Do not claim a command passed unless the exact command and summarized result are recorded.

### Status synchronization gate

After writing any R review or K response, update `.ai-dev-loop/status.md` before the role turn is considered complete. Commit the role record and status update together when git is available.
The status file must reference the latest R review and latest K response that exist at the end of the role turn.
The role turn is incomplete if `.ai-dev-loop/status.md` is stale.

The status update must include:

- latest R review path and associated commit when known; use `pending current commit` only inside the commit that first introduces the review
- latest K response path and associated commit when known; use `pending current commit` only inside the commit that first introduces the response
- latest context note path and associated commit when known
- active decision records or `none`
- current approval state
- next expected role action
- active blockers or `none`

### Approval status precision

Use `Approved with notes` only when no K follow-up is required before continuing.
If R identifies any Critical, High, or Medium finding requiring correction to the reviewed artifact, the overall approval status must be `Changes requested` or `Blocked`.
If the spec/plan is approved and the findings are implementation requirements rather than corrections to the plan, use `Pending implementation`.
When a spec or plan is approved but implementation remains to be done, separate the statuses:

```markdown
- Spec/Plan Status: Approved for implementation
- Implementation Status: Not started
- Overall Status: Pending implementation
```

This avoids confusing authorization to implement with final implementation approval.

## Practical R/K failure prevention

Common production failures and mandatory countermeasures:

- **Lost findings:** keep an Open Required Findings ledger in `status.md`; R carries unresolved findings forward, and K cannot work only from memory or only from the newest paragraph.
- **Code-only fixes:** every behavior change needs matching docs/specs/examples/tests or a recorded no-doc rationale with evidence.
- **Rubber-stamp reviews:** R verifies changed paths, diffs, docs/specs/examples/tests, validation output, and status before approval.
- **Scope creep:** K fixes the active R findings only. New adjacent work is recorded as a future finding, decision, or next item after R approval.
- **Weak evidence:** each finding response cites changed paths, commands/results, commits, and whole-change impact-scan outcome.

## Quality Gates

Before R approval, ensure:

- Specs, documentation, examples, and implementation agree.
- All R findings are addressed or explicitly approved as deferred.
- Tests are added or updated for changed behavior unless the record gives a concrete reason they are impractical and alternative validation evidence is recorded.
- Validation commands and results are recorded.
- K response includes documentation updates or a concrete no-doc-change rationale.
- Local commits exist for R and K changes.
- Implementation changes, when present, were applied directly to the repository working tree rather than only to staged artifacts or detached copies.
- The status file is current.
- A context note exists when the context creation gate is triggered.
- A decision record exists when the decision record gate is triggered.
- No unrelated user changes were overwritten.

## Recommended Command Pattern

Use commands appropriate to the project. Common examples:

```bash
git status --short
git log --oneline -n 10
```

For validation, prefer the project's documented commands. Examples may include:

```bash
npm test
npm run lint
npm run typecheck
pytest
cargo test
go test ./...
make test
```

Record exact commands and results in K response markdown.

## Failure Handling

If a command fails:

1. Record the exact command and summarized failure in K's markdown response.
2. Determine whether it is caused by K's changes, pre-existing workspace state, flaky tests, missing dependencies, or environment limitations.
3. Fix issues caused by K's changes when repo state permits.
4. Commit the fix and updated response.
5. If failure is pre-existing, flaky, or environmental, document evidence: baseline command, affected tests, why unrelated, and any safe workaround.
6. R may grant `Approved with notes` only when evidence shows the failure is unrelated to K's changes and the changed behavior has adequate alternative validation.
7. R must block when the failure prevents validation of the changed behavior, hides a possible regression, or creates security/data-loss risk.

## Commit Discipline Examples

Example review commit:

```bash
git add .ai-dev-loop/reviews/0001-r-review.md .ai-dev-loop/status.md
git commit -m "R: audit payment retry implementation plan"
```

Example response/spec commit:

```bash
git add specs/payment-retry.md .ai-dev-loop/responses/0001-k-response.md .ai-dev-loop/status.md
git commit -m "K: respond to payment retry review"
```

Example implementation commit:

```bash
git add src tests .ai-dev-loop/responses/0002-k-response.md .ai-dev-loop/status.md
git commit -m "K: implement payment retry backoff"
```

Example approval commit:

```bash
git add .ai-dev-loop/reviews/0003-r-review.md .ai-dev-loop/status.md
git commit -m "R: approve payment retry implementation"
```

## Operating Instruction for the AI Agent

When this skill is active, operate as both R and K in alternating turns. Maintain role separation in written markdown records even though the same AI agent may perform both roles.

Never skip the R/K record merely because the same agent can infer the state internally. The markdown records and local commits are required outputs of the process.

Use compressed records by default. Preserve durable facts, open findings, decisions, commit hashes, file paths, validation results, and next actions; omit redundant explanation.

Proceed through review, response, implementation, and follow-up loops by resolving ordinary ambiguity from repo evidence and using the R/K clarification-or-objection path when needed, until one of these occurs:

- The current roadmap item is approved and the next item can begin.
- The roadmap is complete.
- A human escalation criterion is met.
- A technical limitation prevents safe continuation.

Always leave the repository in a traceable state with committed local history for every completed R or K action, using `R:` and `K:` commit subjects; otherwise record the commit limitation and exact uncommitted paths.

## v1.4.1 Validator and Installer Hardening

- Parse R finding blocks and K response blocks line-by-line. Do not use full-document `.*?` or `[\s\S]*?` lookahead regexes for Markdown block extraction. This keeps validation linear in input size and avoids ReDoS-style backtracking on malformed headings.
- Normalize status option-list vocabulary before comparison: remove common Markdown decoration, strip label prefixes, split on `|`, trim each item, and compare sets of values. Keep separate canonical status-value validation for actual record state.
- Wrap installer template writes with local `PermissionError` and `OSError` handling. Report permission or file-lock causes with actionable messages instead of raw tracebacks.


## v1.4.1 Terminal R Review Gate

K responses are implementation evidence, not final approval. After any K response that makes changes, K must request R review via `status.md`. R must inspect the implementation and documentation evidence before recording `Approved`, `Approved with notes`, or `Stop`.

## v1.4.1 Token-Efficiency and Packaging Notes

This revision keeps durable R/K separation, open-finding carry-forward, code-doc-test consistency checks, evidence-first reviews, synchronized status, git discipline, degraded-mode honesty, and optional reference material. It also fixes the prior validation/package mismatch:

- `SKILL.md` remains the compact authoritative policy and fits a realistic validator budget with modest maintenance headroom.
- `REFERENCE.md` remains optional and skippable for simple turns.
- R/K templates remain canonical and auditable.
- Context compression summarizes logs without deleting risk evidence.
- Resolved `status.md` history may move into context or decision notes.
- Release zips use the documented clean root layout.
- Validator size checks remain provider-neutral: bytes, lines, and words, not model-specific tokenizers; limits must leave modest headroom for maintenance while still preventing bloat.

## Production hardening addendum
Latest R review is a hard gate. K must address every current R-required issue and all directly related consistency fallout before any next implementation, roadmap item, refactor, or opportunistic cleanup. Partially addressed, unvalidated, or evidence-free responses keep `Overall Status: Changes requested` or `Blocked` and keep `Next Item: None` unless R/human explicitly accepts the risk. Token budgets may justify aggressive editing, not weaker obligations.
