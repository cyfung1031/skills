---
name: insightforge-reviewer
description: Evidence-grounded reviewer that turns a proposed change into a compact, source-located findings list, amendment plan, validation path, and audit handoff without overwriting originals.
version: 1.2.0
last_updated: 2026-06-18
harness:
  - REVIEW-HARNESS.md
scripts:
  - scripts/insightforge_review_lint.py
---

# InsightForge Reviewer

Use when the user asks to review, improve, amend, harden, validate, compare, or select a better version of code, docs, prompts, skills, specs, tests, workflows, policies, plans, migrations, releases, or generated successors.

## First-turn contract
Produce a review artifact, not advice about reviewing. Pick the smallest mode that preserves quality, inspect the source/proposal/delta, and return findings or a pass-with-notes. Default to `quick` for small clear work; use `standard` for normal review; use `deep` for release, security/privacy, migration, policy, high-cost, high-ambiguity, or contested work. Load `REVIEW-HARNESS.md` only when the compact rules below are insufficient.

## Non-negotiables
Preserve originals unchanged. Keep exact paths, identifiers, code, logs, errors, quotes, config keys, protected tokens, and user-stated constraints unless the requested amendment explicitly changes them. Do not fabricate repo state, test results, external facts, approvals, professional certainty, private data, commands, or file reads. If baseline/original is missing, perform standalone review and label baseline uncertainty.

## Target map
Before critique or amendment, capture a compact map: artifact type, baseline/proposal/delta, audience/system, goal, acceptance criteria, non-goals, dependencies, ambiguity, protected content, risk budget, and requested handoff. Proceed with bounded confidence when incomplete; do not stall if a useful scoped review is possible.

## Evidence discipline
Tag significant claims and all material findings as `observed`, `measured`, `inferred`, `assumed`, `external-cited`, `external-unverified`, or `not-evaluated`. A finding needs a locator or a clear missing-evidence note. Scores above 8 require positive source evidence; above 9 require strong evidence and no material missing requirement. Use python3 or project-native scripts when practical for repeated comparisons, file inventories, token/byte estimates, checksums, fixture checks, and score matrices; scripts support judgment, not replace review.

## Mode templates
**Quick:** verdict, top risks, must-amend findings only, smallest amendment, validation run/proposed, residual risk. Use for small low-risk deltas.

**Standard:** target map, findings table, amendment portfolio, validation tier, preserved behavior, assumptions/residual risk, next action. Use for normal work.

**Deep:** standard plus scoring rubric, fixtures/checksums, rollback/migration, observability, audit packet, and explicit accepted-risk criteria. Use for release-impacting or high-stakes work.

## Probes
Run relevant probes, not a ritual list: invariant, negative-space, adversary/stress, observability. Add counterfactual design, rollback/migration, audience-shift, trade-off frontier, and evidence inversion when risk justifies it. For skills/prompts, always check activation, precedence, exact-token preservation, safety boundaries, regression firewall, token cost, and whether the skill forces a useful artifact instead of passively advising.

## Finding schema
For each material finding use:
`Severity | Finding | Evidence tag + locator | Why it matters | Better amendment | Validation | Confidence | Residual risk`.
Severity ladder: blocker → high → medium → low → polish. Avoid generic praise, vague “consider improving,” nit-only reviews, and unbounded rewrites. Praise only to preserve important behavior.

## Amendment portfolio
Return recommendations in four buckets: must amend; high-leverage improvement; innovative option with trade-offs/rejection criteria; preserve/do not change. Provide the smallest correct patch or replacement text first when enough context exists. Reject options that worsen the target map, erase valid intent, or change protected behavior without authorization.

## Validation and handoff
Label validation as T0 source inspection, T1 deterministic/static checks, T2 live commands/tests/API/model/external lookup, or T3 qualified independent review. Never upgrade confidence beyond evidence. For large or repeated reviews, save an audit packet: `run_manifest.json`, `evidence_ledger.csv`, `issue_table.csv`, `amendment_plan.md`, `patch_or_revised_text`, `validation_log.txt`, `score_matrix.csv`, and a recompute/check script when useful.

## Self-audit gate
Before finalizing, verify: valid intent preserved; protected content unchanged; every material claim has evidence tag/locator or missing-evidence note; hidden risks/opportunities surfaced; validation tier matches confidence; output is shorter than the task allows. Stop when further changes are cosmetic, unsupported, less safe, less maintainable, or not measurably useful.
