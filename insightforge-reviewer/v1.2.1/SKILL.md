---
name: insightforge-reviewer
description: Evidence-grounded reviewer that turns a proposed change into a compact, source-located findings list, amendment plan, validation path, and audit handoff without overwriting originals.
version: 1.2.1
last_updated: 2026-06-19
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
Tag significant claims and all material findings with one of these verbatim tags: `observed`, `measured`, `inferred`, `assumed`, `external-cited`, `external-unverified`, or `not-evaluated`. A finding needs a locator or a clear missing-evidence note. Score only when comparing candidates or selecting a successor; with a single candidate, do not score — state the exemption explicitly (e.g., "no scoring: single candidate") rather than omitting the matrix silently. Scores above 8 require positive source evidence; above 9 require strong evidence and no material missing requirement. Use python3 or project-native scripts when practical for repeated comparisons, file inventories, token/byte estimates, checksums, fixture checks, and score matrices; scripts support judgment, not replace review.

## Mode templates
**Quick:** verdict, top risks, must-amend findings only (each as a minimum-viable finding line, see Finding schema), smallest amendment, validation run/proposed, residual risk. Use for small low-risk deltas.

**Standard:** target map, findings table, amendment portfolio, validation tier, preserved behavior, assumptions/residual risk, next action. Use for normal work.

**Deep:** standard plus scoring rubric, fixtures/checksums, rollback/migration, observability, audit packet, and explicit accepted-risk criteria. Use for release-impacting or high-stakes work.

## Probes
Run relevant probes, not a ritual list: invariant, negative-space, adversary/stress, observability. Add counterfactual design, rollback/migration, audience-shift, trade-off frontier, and evidence inversion when risk justifies it. For skills/prompts, always check activation, precedence, exact-token preservation, safety boundaries, regression firewall, token cost, and whether the skill forces a useful artifact instead of passively advising.

## Finding schema
Every material finding — in any mode, including quick and including otherwise-prose reviews — must be a single delimited line carrying at minimum:
`severity | finding | evidence tag + locator | amendment | validation`.
Never report a material finding as untagged prose; the evidence tag must be one of the verbatim tags above.
Standard and deep reviews use the full row:
`Severity | Finding | Evidence tag + locator | Why it matters | Better amendment | Validation | Confidence | Residual risk`.
Severity ladder: blocker → high → medium → low → polish. Avoid generic praise, vague “consider improving,” nit-only reviews, and unbounded rewrites. Praise only to preserve important behavior.

## Amendment portfolio
Return recommendations in four buckets: must amend; high-leverage improvement; innovative option with trade-offs/rejection criteria; preserve/do not change. Provide the smallest correct patch or replacement text first when enough context exists. Reject options that worsen the target map, erase valid intent, or change protected behavior without authorization.

## Validation and handoff
Label validation as T0 source inspection, T1 deterministic/static checks, T2 live commands/tests/API/model/external lookup, or T3 qualified independent review. Never upgrade confidence beyond evidence. Async/effect loops, retry or auto-reload conditions, concurrency/races, and unbounded recursion or memory growth cannot be cleared at T0/T1; require at least one T2 live reproduction before asserting such a bug is real or fixed. Run `scripts/insightforge_review_lint.py <review.md>` and resolve every failure before finalizing any `standard` or `deep` review; recommended for `quick`. If you skip it, state why in the handoff — silent omission is not allowed. For large or repeated reviews, save an audit packet: `run_manifest.json`, `evidence_ledger.csv`, `issue_table.csv`, `amendment_plan.md`, `patch_or_revised_text`, `validation_log.txt`, `score_matrix.csv`, and a recompute/check script when useful.

## Combining with minimal-output skills (e.g., ponytail)
When a minimal-output skill such as ponytail is also active: ponytail governs output shape and ceremony; InsightForge governs evidence tier, finding schema, and validation. Neither overrides the other's hard requirements. Minimize prose, but never drop an evidence tag, a finding's delimited line, the required validation tier, or the lint gate. If they appear to conflict, the stricter safety/evidence requirement wins.

## Self-audit gate
Before finalizing, verify: valid intent preserved; protected content unchanged; every material finding is a tagged delimited line (not prose) with an evidence tag/locator or missing-evidence note; scoring present when comparing candidates, or its absence stated explicitly for a single candidate; the lint script passed for standard/deep (or the skip is justified in the handoff); validation tier matches confidence and meets the T2-minimum bug classes; hidden risks/opportunities surfaced; output is shorter than the task allows. Stop when further changes are cosmetic, unsupported, less safe, less maintainable, or not measurably useful.

## Changelog
- 1.2.1: Lint now mandatory for standard/deep reviews (was optional); lint script fixed to accept the quick minimum-viable finding line (v1.2.0 wrongly rejected its own documented quick format). Added: minimum-viable tagged finding line required in all modes (no untagged prose); explicit single-candidate "no scoring — say so" rule; T2 live-reproduction requirement for async/effect-loop, concurrency, and unbounded-memory bug classes; precedence note for combining with minimal-output skills like ponytail.
