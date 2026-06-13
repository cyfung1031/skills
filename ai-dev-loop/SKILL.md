---
name: ai-dev-loop
description: Dual-role autonomous software development loop. Run two cooperating roles — R (Reviewer/Auditor) reviews specs, plans, and implementation for risks, gaps, and contradictions; K (Implementer/Keeper) responds, updates specs, implements code, and tests. All handoff happens through durable markdown in .ai-dev-loop/ plus local git commits, not chat memory. Use when a workspace has specs/plans/roadmaps/tickets and the user wants the agent to drive review→response→implementation→review cycles autonomously with an audit trail.
---

# Skill: Dual-Role Software Development Review and Implementation Loop

## Purpose

Use this skill when a software development workspace already contains specifications, implementation plans, roadmaps, tickets, or design notes, and the AI agent must autonomously drive development through two cooperating roles:

- **R — Reviewer/Auditor**: reviews specifications, plans, and implementation work; identifies risks, gaps, contradictions, unclear requirements, and quality issues.
- **K — Implementer/Keeper**: updates specifications, resolves reviewer feedback, implements code, tests changes, and records responses.

The process is designed to work without requiring human decisions for normal review, clarification, implementation, and follow-up cycles. Human involvement is only required for blocked decisions explicitly outside the available specifications or project authority.

## Core Principles

1. **Single working branch**
   - R and K must work on the same current local branch.
   - Do not switch branches unless the user explicitly requests it.
   - Every meaningful change by either role must be committed locally.
   - Use local commits as the shared history, audit trail, and rollback mechanism.

2. **Markdown-based handoff**
   - R records every review, audit, concern, clarification request, and final approval in markdown.
   - K records every response, decision, spec update, implementation update, and test result in markdown.
   - **Both R and K must write markdown in every round.** A round is incomplete until the R record and the corresponding K record both exist, except when R creates a final approval with no required K follow-up.
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
   - K may then proceed to the next implementation step according to the existing implementation plan, roadmap, or specification priority.
   - The AI should not ask the human to choose between ordinary engineering options when the workspace gives enough context to make a reasonable decision.

6. **Spec-first discipline**
   - Before implementation, R audits the relevant specifications and implementation plan.
   - K resolves spec gaps before writing code when possible.
   - If implementation reveals a spec issue, K updates the spec and records the reason.
   - R then reviews both the spec and implementation changes.

7. **Small, reversible steps**
   - Prefer small commits with focused scope.
   - Each commit should represent one review note, one response, one spec update, one implementation step, or one test/fix step.
   - Avoid large mixed commits that combine unrelated review, spec, and code changes.

8. **Direct repository asset modification after approval**
   - After R approves the relevant specification, plan, or roadmap item, K must modify the actual project source files in the repository workspace directly.
   - K must not implement in a detached artifact staging area, copied sandbox, generated patch-only file, or parallel shadow tree unless the user or repository instructions explicitly require that workflow.
   - The real repository working tree is the source of truth. K validates and commits the actual modified source, tests, specs, and coordination markdown on the same local branch.
   - Temporary files may be used only as scratch space and must not replace direct repository edits or local commits.

## Workspace Conventions

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

If the repository already has a project-specific location for agent notes, ADRs, review logs, or implementation records, use that instead and document the chosen location in `.ai-dev-loop/README.md` or the existing equivalent.

## Integrated Context Compressor

Apply these rules whenever this skill is active. The goal is to reduce token usage in both thinking and writing without weakening the audit trail.

### Operating mode

- Use short, direct progress updates and markdown records.
- State only current action, durable evidence, decisions, changed files, validation result, and next action.
- Avoid restating stable instructions, accepted decisions, full logs, or old alternatives.
- Prefer exact paths, sequence numbers, commit hashes, command names, and finding IDs.
- Ask at most one human clarification question when blocked; otherwise make a safe autonomous assumption and document it.

### Context pruning

Keep:

- Current goal and latest user correction.
- Constraints affecting safety, permissions, git, output format, specs, tests, or project scope.
- Current approval state, blockers, and active findings.
- Files changed, commands run, test status, and remaining work.
- Non-obvious facts discovered from code, tools, specs, or prior durable records.

Drop or compress:

- Rejected alternatives after recording the decision.
- Full command logs after summarizing result and retaining the command.
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

Omit empty fields.

### Compression boundary

Compression must never remove:

- Open findings or blocker rationale.
- Test failures, skipped validations, or environment limitations.
- Commit hashes and changed file paths.
- Human decisions or user-provided constraints.
- Approval status and required next role action.

## Required Git Behavior

Before starting work:

```bash
git status --short
git branch --show-current
```

Rules:

- Do not discard user changes.
- Do not overwrite uncommitted changes unless they were created by the current role in the current loop and the change is intentionally being amended.
- If unrelated uncommitted changes exist, work around them when possible and record the constraint.
- Every R markdown update must be committed locally.
- Every K markdown update must be committed locally.
- Every spec update, implementation change, and test update must be committed locally.

Suggested commit prefixes:

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

## Findings

### Finding R-NNNN-01: <title>

- Severity: Blocker | High | Medium | Low | Nit
- Type: Spec gap | Implementation issue | Test gap | Design risk | Clarification | Process issue
- Location: <file/path or commit reference>
- Details: <clear explanation>
- Required action: <specific requested action>

## Clarifications Needed

List questions only when the workspace does not contain enough information to make a safe autonomous decision.

## Approval Status

One of:

- Blocked: K must respond before implementation continues.
- Changes requested: K must update specs, code, tests, or documentation.
- Approved with notes: K may proceed, but should consider notes.
- Approved: No further follow-up.

## Next Expected K Action

State what K should do next.
```

### R decision rules

R should not block on minor style issues unless they affect correctness, maintainability, or project conventions.

R may approve when:

- The relevant specification is clear enough.
- The implementation matches the specification.
- Tests or validation are adequate for the change size and risk.
- No unresolved blocker, high, or medium findings remain.

R must continue the loop when:

- Requirements are contradictory.
- Acceptance criteria are missing for a material behavior.
- Implementation diverges from the plan.
- Tests do not cover important behavior.
- Security, data loss, migration, or compatibility risks are unresolved.

## Role K: Implementer/Keeper

K is responsible for responding to R, updating specs, implementing code, and validating changes.

### K must do

- Read R's latest markdown review.
- Address every finding explicitly.
- Update specifications when the issue is a spec gap.
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

## Finding Responses

### Response to R-NNNN-01

- Status: Resolved | Partially resolved | Deferred | Rejected
- Action taken: <what changed>
- Files changed: <paths>
- Commit: <local commit hash>
- Notes: <reasoning, tradeoffs, or follow-up>

## Spec Updates

List specification or plan updates, if any.

## Implementation Updates

List implementation updates, if any.

## Tests and Validation

List commands run and results.

## Remaining Questions

Only include questions that cannot be resolved from the workspace context.

## Compact Context

Use the integrated Context Compressor handoff format. Include only durable state that R needs for the next review.

## Next Expected R Action

Ask R to review the response, updated specs, implementation, and tests.
```

### K decision rules

K should autonomously choose the next action when the existing roadmap, implementation plan, or specifications imply priority.

K may update specifications without human confirmation when:

- The update resolves ambiguity using existing project conventions.
- The update aligns with the implementation plan or roadmap.
- The update narrows behavior rather than introducing unrelated scope.
- The update is documented in the K response and committed.

K must avoid proceeding silently when:

- The change would materially alter product direction.
- The change introduces a new external dependency with unclear approval.
- The change may delete or migrate user data.
- The change has security, legal, compliance, or cost implications not addressed by existing specs.

In those cases, K records the blocker in markdown and stops at a safe boundary.

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

## Autonomous Workflow

### Phase 1: Specification and Plan Review

1. Inspect repository status and current branch.
2. Locate specifications, implementation plans, roadmap files, tickets, or design documents.
3. R reviews the relevant spec and implementation plan.
4. R writes a review markdown file.
5. Commit R's review.
6. K reads R's review.
7. K updates specs, plans, or clarification notes as needed.
8. K writes a response markdown file.
9. Commit K's response and any spec changes.
10. Repeat until R records `Approved` or `Approved with notes` with no required follow-up.

### Phase 2: Implementation

1. K selects the next implementation item from the approved plan or roadmap.
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
3. Commit R's review.
4. K addresses every finding.
5. K records responses and validation in markdown.
6. Commit K's response and changes.
7. Repeat until R has no further follow-up.

### Phase 4: Next Roadmap Item

After R approves the completed implementation item:

1. K marks the item complete in the status file or project tracker if available.
2. Commit the status update.
3. K selects the next implementation item according to the roadmap or plan.
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

## Approval State

Spec review: Pending | Approved | Changes requested | Blocked
Implementation review: Pending | Approved | Changes requested | Blocked

## Completed Items

- <item> — <commit>

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

Prefer appending dated/numbered status bullets over rewriting history. When compacting status, preserve active blockers, approval state, latest R/K paths, and commit hashes.

## Loop Termination Criteria

A review-response loop ends only when R records one of the following:

```text
Approval Status: Approved
```

or

```text
Approval Status: Approved with notes
```

and the notes do not require K follow-up before continuing.

If R records `Blocked` or `Changes requested`, K must respond before moving forward.

## Circuit Breaker for Loop Divergence

The loop must not continue indefinitely. Trigger a circuit breaker and write `.ai-dev-loop/decisions/NNNN-blocker.md` when any of these occur:

- The same finding is rejected or re-opened after **three K resolution attempts**.
- R and K disagree twice about whether a finding is resolved and the disagreement depends on product intent, risk tolerance, or external constraints absent from the workspace.
- Two consecutive rounds make no material change to specs, code, tests, or decision evidence.
- The loop exceeds **six R/K rounds** for one roadmap item without approval.

When the circuit breaker trips, K writes the blocker file first, records the safe stopping point, commits it, and stops for human input.

## Handling Clarifications Without Human Involvement

When R asks for clarification, K should first try to answer using:

1. Existing specifications
2. Implementation plans
3. Roadmap files
4. Existing code behavior
5. Tests
6. README or developer documentation
7. Prior R/K markdown records
8. Project conventions visible in the repository

K should update the relevant markdown and, when appropriate, the specification itself.

Only escalate to the human when the decision cannot be made safely from repository context.

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

## Quality Gates

Before R approval, ensure:

- Specs and implementation agree.
- All R findings are addressed or explicitly approved as deferred.
- Tests are added or updated for changed behavior where practical.
- Validation commands and results are recorded.
- Local commits exist for R and K changes.
- Implementation changes, when present, were applied directly to the repository working tree rather than only to staged artifacts or detached copies.
- The status file is current.
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
3. Fix issues caused by K's changes when possible.
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

Proceed autonomously through review, response, implementation, and follow-up loops until one of these occurs:

- The current roadmap item is approved and the next item can begin.
- The roadmap is complete.
- A human escalation criterion is met.
- A technical limitation prevents safe continuation.

Always leave the repository in a traceable state with committed local history for every completed R or K action.
