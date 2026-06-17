---
name: ai-dev-loop
description: Token-efficient auditable R/K repository loop.
version: 1.7.6
last_updated: 2026-06-18
scripts:
  - scripts/install-ai-dev-loop-template.py
  - scripts/validate-ai-dev-loop-package.py
  - scripts/check-ai-dev-loop-state.py
  - scripts/check-ai-dev-loop-flow.py
  - scripts/estimate-ai-dev-loop-token-cost.py
harness:
  - LOOP-HARNESS.md
  - RESTRICTION-HARNESS.md
  - MODE-HARNESS.md
---

# Skill: AI Development Loop

## Activation and modes
Use for repo work needing R/K audit loop. R reviews requirements/diffs/tests/docs/risk/evidence. K answers findings, edits related source/docs/tests/scripts, validates, records evidence. Do not use for brainstorming, CoT, unsupported rankings, live secrets, or outside repo authority. Use smallest mode preserving source identity, role split, evidence, validation-tier honesty, auditability. Release mode covers package/benchmark/version/manifest/validator/installer/schema/example/archive consistency. Degraded mode means local commit/tool/file/network/credential/authority unavailable; record limit and safe partial path; never claim skipped checks passed.

## Core invariant
`status.md scope -> R finding ledger -> K response/evidence -> whole-change scan -> validation -> R terminal review`. Operational review order: `source identity -> target map -> evidence boundaries -> risk/opportunity model -> amendment portfolio -> validation -> audit handoff`. **Written-record authority:** `.ai-dev-loop/` files are source of truth; chat memory, filenames, recency, summaries, assumptions are not evidence.

## Token and loading budget
Default load order: `SKILL.md -> scripts/check-ai-dev-loop-state.py/check-ai-dev-loop-flow.py output when available -> status/latest records -> affected files -> LOOP-HARNESS.md only when needed`. Use script summaries and targeted files, not packages/logs/history. Prefer paths/lines; put long evidence in context/audit files. Compress prose, not obligations. Token controls may shorten wording and script mechanical checks, but must not weaken gates, evidence, safety, quality, local commits, degraded fallback, or push/destructive-git authority.

## Source identity and target map
Before critique/implementation/scoring/change, identify artifact type, baseline/proposal/delta, audience/system, goal, criteria, non-goals, dependencies, ambiguity, protected content, validation tier, handoff. Preserve originals, locators, code, commands, errors, logs, paths, identifiers. Missing baseline => standalone review; unseen-regression claims are assumptions.

## Role separation and records
R/K may run in one session; records stay separate. R owns findings, outcomes, accepted-risk closure, contradiction decisions, terminal approval. K owns edits, evidence, objections, handoff. K may request clarification or object when a finding is unclear, unsafe, unsupported, contradictory, already satisfied, or beyond authority; K records safe partial path; asks R to resolve. Update `.ai-dev-loop/status.md` every role turn. Write R in `reviews/`, K in `responses/`, handoffs in `context/`, decisions in `decisions/`. When creating the first R/K/status record, or when record shape is uncertain, load `LOOP-HARNESS.md` templates before writing.

## Status vocabulary
Overall Status: Blocked, Changes requested, Pending implementation, Approved with notes, Approved. Spec/Plan/Implementation Status: Not started, Changes requested, Approved for implementation/Pending implementation, Approved with notes, Approved, Not applicable. Most restrictive wins: missing safe input/authority => Blocked; unresolved required finding/K question/objection/failed validation => Changes requested; notes only => Approved with notes; final approval is R-owned.

## Operational command pattern
1. Load status, branch, latest R/K, context/decisions, relevant specs/docs/tests/diffs, affected files, repo policy.
2. Run state/flow scripts when installed; target reads, do not replace evidence.
3. R writes scope, summary, evidence, findings, severity, status, outcomes, clarification/objection responses, approval, next K action.
4. K addresses every open required finding before new work; updates related artifacts; validates; records evidence, limits, skipped checks, questions, objections, next R action.
5. Before handoff, commit locally for every meaningful R/K/status transition when git is usable; if unavailable, record degraded mode with exact limitation and uncommitted paths.
6. Continue same-session handoff to next expected role unless blocked, no safe action exists, authority is missing for non-local/destructive action, or R gives terminal approval. Writing `Next Expected Role Action` is not performing it.

## Inline record contracts
Status names branch, focus, latest R/K/context, decisions, approval, open findings, completed items, next expected role action, next item, blockers, validation/git trace, residual risk. R records include scope, summary, evidence, findings, clarification needs, K clarification/objection responses, approval, next K action. K records include review addressed, summary, evidence, finding responses, updates, tests/validation, clarifications/objections, context, next R action. Use tables, paths, command summaries; move long evidence to context/audit.

## Hard gates
**Current-issue lock:** no cleanup or next items while R-required findings, K questions/objections, failed validation, or missing evidence remain open. **No silent softening:** MUST/required/never/hard-gate language cannot weaken for speed, token budget, convenience, or incomplete context. **Documentation drift prevention:** behavior/API/CLI/config/data/workflow/validation/packaging/user-visible changes require affected docs/specs/examples/tests/validators/scripts/package guidance updates or no-doc rationale. **Whole-change impact scan:** R task lists are not exhaustive; K owns affected artifacts R did not name. Terminal approval requires closed/accepted findings, validation evidence/limits, resolved objections/questions, artifact agreement, most restrictive status. Prefer stricter safety/evidence rule on conflict.

## Git authority and degraded-mode defaults
Local git commits are the default audit and rollback mechanism. In normal git mode, every meaningful R/K/status transition must be committed locally when git is available and usable. Before commit, inspect `git status --short` and diffs, stage only intended loop records plus related files, avoid broad staging unless written scope proves every path belongs, verify commit/hash/status evidence. Degraded mode is a fallback, not a convenience bypass. Use only when local commits cannot be created because git, repo access, identity, permissions, or environment support is unavailable. Continue with durable records, exact limitation, uncommitted paths, git trace unavailable; never claim a commit exists. Never push, force-push, configure remotes, rebase, reset hard, clean untracked files, delete branches, amend history, rewrite shared history, switch branches, wrapper push, or destructive git operations without explicit approval/written instruction. Work on current branch unless branch creation/checkout is authorized.

## Scoring, evidence, validation
For review/change/benchmark/version comparison, score target fit separately from feature richness. State objective, weights, estimator, formula, fixture count/checksum, claim cap. Do not score from filenames, recency, polish, length, prior summaries, or assumed intent. Use `SCORING-EVIDENCE-SCHEMA.json` unless stricter rubric exists. Do not invent commands, outputs, commits, tests, file reads, user approvals, or external evidence. Every claim must cite a file, diff, command, test, log, commit, status record, review/response record, or explicit limitation. Tag material claims as observed, measured, inferred, assumed, external-cited, external-unverified, not-evaluated. Validation tiers: T0 source inspection, T1 deterministic/static checks, T2 live commands/API/model runs, T3 qualified independent review. Never present T0/T1 as live behavior.

## Handoff, release, escalation
Every handoff names role, branch, focus, changed files, evidence, validation status, skipped checks, open findings, questions/objections, next role, residual risk, token exceptions. Verify saved paths, bytes, sha256, overwrite policy. Keep delivered files focused on behavior, usage, constraints, validation, maintenance; keep audit-only notes outside package files unless requested. Use validator, installer, state/flow checkers, token estimator. Release work must check package structure, docs, examples, scripts, validators, installers, schemas, manifest checksums, version refs, forbidden artifacts, archive contents. Rebuild `PACKAGE-MANIFEST.json`; validate from package root. Use `LOOP-HARNESS.md` for templates, local-commit authority, degraded environments, K objections, terminal acceptance, scoring. Use `MODE-HARNESS.md` only for ambiguous modes; `RESTRICTION-HARNESS.md` only for regression review; `VALIDATION.md` only for release validation. A compact `SKILL.md` lowers activation cost but does not delete requirements.
