---
name: ai-dev-loop
description: Token-efficient auditable R/K repository loop with module-on-demand runtime details.
version: 1.7.7
last_updated: 2026-06-19
scripts:
  - scripts/install-ai-dev-loop-template.py
  - scripts/validate-ai-dev-loop-package.py
  - scripts/check-ai-dev-loop-state.py
  - scripts/check-ai-dev-loop-flow.py
  - scripts/estimate-ai-dev-loop-token-cost.py
modules:
  - modules/LOOP-HARNESS.md
  - modules/MODE-HARNESS.md
  - modules/RESTRICTION-HARNESS.md
  - modules/VALIDATION.md
  - modules/BENCHMARK-HARNESS.md
---

# Skill: AI Development Loop

## Activation
Use for repository work that needs an auditable reviewer/implementer loop. R reviews requirements, diffs, tests, docs, risks, and evidence. K answers R findings, edits related source/docs/tests/scripts, validates, and records evidence. Do not use for brainstorming, hidden chain-of-thought capture, unsupported rankings, live secrets, or work outside repository authority.

## Core invariant
`status.md scope -> R finding ledger -> K response/evidence -> whole-change scan -> validation -> R terminal review`. **Written-record authority:** `.ai-dev-loop/` files, repository files, command output, tests, logs, diffs, commits, and explicit limitations are evidence; chat memory, filenames, recency, summaries, and assumptions are not.

## Token and loading budget
Always-load is this compact `SKILL.md`. Default order: `SKILL.md -> scripts/check-ai-dev-loop-state.py/check-ai-dev-loop-flow.py output when available -> status/latest records -> affected files -> targeted module only when needed`. Use scripts to target reads, not to replace evidence. Compress prose, not obligations. Token savings may compress wording and move detail into `modules/`, but must not remove required gates, evidence, safety, quality, local commits, degraded fallback, or push/destructive-git authority.

## Role separation and record paths
R owns findings, required outcomes, accepted-risk closure, contradiction decisions, and terminal approval. K owns implementation, finding responses, objections, validation evidence, and handoff. R/K may run in one session, but records stay separate. Update `.ai-dev-loop/status.md` every role turn. Write R records in `reviews/`, K records in `responses/`, handoffs in `context/`, durable choices in `decisions/`. When creating the first R/K/status record, or when record shape is uncertain, load `modules/LOOP-HARNESS.md` templates before writing.

## Status vocabulary and restrictions
Overall Status: Blocked, Changes requested, Pending implementation, Approved with notes, Approved. Spec/Plan/Implementation Status: Not started, Changes requested, Approved for implementation/Pending implementation, Approved with notes, Approved, Not applicable. Most restrictive wins. Missing safe input or authority => Blocked; unresolved required finding, K question/objection, failed validation, or missing evidence => Changes requested; notes only => Approved with notes; final approval is R-owned.

## Operational command pattern
1. Load status, branch, latest R/K, context/decisions, specs/docs/tests/diffs, affected files, and repo policy.
2. Run state/flow scripts when installed; use summaries to target reads.
3. R writes scope, summary, evidence, findings, severity/status/outcomes, clarification/objection responses, approval, and next K action.
4. K addresses every open required finding before new work, updates affected artifacts, validates, records evidence/limits/skipped checks/questions/objections, and hands back to R.
5. Before handoff, commit locally for every meaningful R/K/status transition when git is usable; if unavailable, record degraded mode with exact limitation and uncommitted paths.
6. Continue same-session handoff to the next expected role unless blocked, no safe action exists, authority is missing for non-local/destructive action, or R gives terminal approval. Writing `Next Expected Role Action` is not performing it.

## Inline record contracts
Status names branch, focus, latest R/K/context, decisions, approval, open findings, completed items, next expected role action, next item, blockers, validation/git trace, and residual risk. R records include scope, summary, evidence, findings, clarification needs, K clarification/objection responses, approval, next K action. K records include review addressed, summary, evidence, finding responses, updates, tests/validation, clarifications/objections, compact context, next R action.

## Hard gates
**Current-issue lock:** no cleanup or next items while R-required findings, K questions/objections, failed validation, or missing evidence remain open. **No silent softening:** MUST/required/never/hard-gate language cannot weaken for speed, token budget, convenience, or incomplete context. **Documentation drift prevention:** behavior/API/CLI/config/data/workflow/validation/packaging/user-visible changes require affected docs/specs/examples/tests/validators/scripts/package guidance updates or a no-doc rationale. **Whole-change impact scan:** R task lists are not exhaustive; K owns affected artifacts R did not name. Terminal approval requires closed/accepted findings, validation evidence/limits, resolved objections/questions, artifact agreement, and most restrictive status.

## Git authority and degraded mode
Local git commits are the default audit and rollback mechanism; every meaningful R/K/status transition must be committed locally when git is available and usable. Before commit, inspect status/diffs, stage only intended loop records plus related files, and record commit/hash/status evidence. Degraded mode is a fallback, not a convenience bypass; use only when git/repo/identity/permission/environment prevents commits. Never push, force-push, configure remotes, rebase, reset hard, clean untracked files, delete branches, amend history, rewrite shared history, switch branches, wrapper push, or do destructive git operations without explicit approval.

## Scoring, evidence, validation
For review/change/benchmark/version comparison, score target fit separately from feature richness. State objective, weights, estimator, formula, fixture count/checksum, and claim cap. Use `SCORING-EVIDENCE-SCHEMA.json` unless a stricter rubric exists. Do not score from filenames, recency, polish, length, prior summaries, or assumed intent. Do not invent commands, outputs, commits, tests, file reads, user approvals, or external evidence. Every material claim must cite a file, diff, command, test, log, commit, status record, review/response record, or explicit limitation. Tag claims as observed, measured, inferred, assumed, external-cited, external-unverified, or not-evaluated. Validation tiers: T0 source inspection, T1 deterministic/static checks, T2 live commands/API/model runs, T3 qualified independent review. Never present T0/T1 as live behavior.

## Module loading map
Load `modules/LOOP-HARNESS.md` for templates, first records, local-commit authority, degraded environments, K objections, terminal acceptance, scoring details, and whole-change uncertainty. Load `modules/MODE-HARNESS.md` only for ambiguous minimal/standard/release/degraded mode decisions. Load `modules/RESTRICTION-HARNESS.md` for regression review of hard restrictions. Load `modules/VALIDATION.md` for release validation. Load `modules/BENCHMARK-HARNESS.md` for benchmark fixtures and anti-leakage checks. Release work must check package structure, docs, examples, scripts, validators, installers, schemas, manifest checksums, version refs, forbidden artifacts, archive contents, and module references; rebuild `PACKAGE-MANIFEST.json` and validate from package root.
