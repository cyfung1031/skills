---
name: best-version-builder
description: Compare, score, improve, retest, and stop candidate-version work with source-grounded identity, target maps, calibrated objectives, broad category buckets with explicit coverage lenses, validation-tier claim caps, evidence ledgers, recomputable score packets, observability markers, artifact checksums, correction audits, release-content hygiene, behavioral-invariance checks, and anti-compression safeguards.
version: 1.3.4
last_updated: 2026-06-18
---

# Candidate Version Analysis + Release Selection

Use when the user provides candidate versions, prompts, skills, specs, code variants, documents, archives, benchmark reports, prior matrices, or generated candidates and asks to compare, score, choose, improve, retest, correct, or validate a best version.

Core invariant: **identity → target map → objective → broad rubric → coverage lenses → evidence → measurement → observability → recomputation → improvement → correction → handoff**. Keep these gates separate. Do not score from filenames, recency, polish, length, prior summaries, or assumed intent. Do not rewrite first and rationalize afterward.

## 1. Intake, Identity, and Workspace

1. Use the requested workspace; otherwise use the active project workspace. Unpack archives into a clean source directory. Preserve originals unchanged; write generated candidates and results to separate output paths.
2. Ignore noise: `__MACOSX`, `.DS_Store`, resource forks, temp files, caches, build products, duplicate outputs, and prior generated artifacts unless explicitly in scope.
3. Inventory every candidate: name/version/path, checksum or stable size marker, artifact type, declared purpose, comparison unit, output contract, protected tokens, constraints, estimator/estimate, scope notes, category-lens coverage notes, observability hooks, and source-vs-generated boundary.
4. Identify candidates from source content, not filename alone. If filename, frontmatter, title, and body disagree, report the conflict and use content-grounded identity.
5. Mark each artifact `in-scope`, `comparator-only`, or `out-of-scope`. Comparator-only artifacts may inform analysis but cannot silently win for another target.
6. Before final handoff, verify every saved path exists and report checksum/status. Never invent sandbox links or silently overwrite source or prior generated files.
7. Separate **working notes** from **release contents**. Internal review terms, benchmark provenance, iteration history, tool names, evaluator names, generated-by text, or build-process wording must not appear inside a delivered candidate/package unless the user explicitly requests an audit artifact or provenance appendix.

## 2. Target Behavior Map

Before scoring, write a compact target map:

- intended user task, artifact purpose, comparison unit, activation/stop conditions, and non-goals;
- required outputs, saved artifacts, handoff shape, protected tokens, exact-preservation needs, release-content hygiene, and localization expectations;
- safety/professional, correctness, evidence, validation, observability, audit, reproducibility, compatibility, behavioral-invariance, and correction requirements;
- critical legacy behaviors that must survive improvement;
- optional helpful behaviors;
- irrelevant, comparator-only, provenance-only, and wrong-target features that must not be rewarded or penalized unless explicitly required.

Rules: no target map caps production recommendation at 8.0. Unresolved target mismatch caps production at 6.5. A prior matrix using another target map is critique evidence only. Score target fit separately from feature richness. Mark every category and material feature as required, optional, conditional, out-of-scope, or comparator-only.

## 3. Objective, Broad Rubric, Coverage Lenses, Weights, Formula

Default objective: **best production version**.

Profiles:

- **production**: reliable target-task performance, correctness, evidence, observability, auditability, maintainability, compatibility, behavioral-invariance, correction quality; cost is secondary.
- **compressed**: cost minimization only after required production behavior remains acceptable.
- **research/exploratory**: diagnostic coverage and alternatives; higher cost tolerance.
- **live-model**: repeated model/API calls with variance notes.
- **deterministic proxy**: static/heuristic checks only; never imply live behavior.

Default broad categories when the user gives none. Keep the top-level rubric broad enough to transfer across benchmark styles, artifacts, and domains; use coverage lenses to prevent blind spots instead of multiplying narrow mandatory categories.

| Category | Weight | Production-critical | Coverage lenses to inspect |
|---|---:|---|---|
| Correctness / target behavior | 1.25 | Yes | Executability, semantic preservation, required outputs, exact content, constraints, edge cases, stop conditions, contradiction checks. |
| Scope / user value / fit | 1.15 | Yes | Target-map fit, comparison-unit fit, non-goals, comparator-only handling, user value, wrong-target expansion. |
| Safety / guardrails / risk control | 1.15 | Yes | Safety, privacy, professional-risk boundaries, protected tokens, overwrite risk, false certainty, abuse resistance, release-content hygiene. |
| Evidence / validation / reproducibility | 1.20 | Yes | Source grounding, validation tier, fixtures, pass/fail criteria, estimator stability, formulas, seeds, versions, checksums, recompute ability. |
| Observability / audit / handoff | 1.05 | Yes | Failure localization, logs, metrics, evidence rows, artifact paths, manifests, score packets, checksums, correction notes, claim limits, publication boundary. |
| Maintainability / evolvability | 1.00 | Yes | Modularity, readability, low duplication, update safety, cognitive load, anti-overfitting, reusable gates. |
| Compatibility / regression safety | 1.00 | Yes | Legacy behavior, output contracts, localization, exact-preservation rules, migration/rollback, regression firewall. |
| Behavioral invariance / change discipline | 1.10 | Yes | Intended behavior preservation, no semantic drift, no hidden policy/output-shape changes, stable activation and stop behavior, unchanged protected-token handling, explicit deprecation only when requested or justified. |
| Cost / complexity / token efficiency | 0.65 | No unless compressed objective | Token use, runtime, artifact burden, maintenance burden, harness complexity, simplicity after required behavior is safe. |
| Language / audience, when relevant | 1.00 | Conditional | Requested language, terminology, domain terms, reader level, localization, code/path/identifier preservation. |

Coverage-lens rule: do not create a new top-level category just because a lens matters. First decide whether the lens is required, optional, conditional, out-of-scope, or comparator-only under the target map; then score it inside the broad category where it best affects the outcome. Add a narrow category only when the user asks for it, the target map requires separate reporting, or merging it would materially hide a winner-changing defect.

Category-map rule: before scoring, mark each broad category and material lens `required`, `optional`, `conditional`, `out-of-scope`, or `comparator-only`; define category/lens-specific evidence requirements and caps. If old and new matrices use different categories, weights, anchors, relevance labels, or pass/fail criteria, either backfill old candidates under the new rubric or label the comparison non-equivalent. Do not let token efficiency, polish, or feature richness compensate for a production-critical category below the declared pass threshold.

Default 10/8/6/4 anchors unless the user provides better anchors:

- **10**: complete target fit; strong positive source or measured evidence; no material missing requirement; observable, reproducible, auditable, and regression-safe.
- **8**: production-usable with minor gaps; evidence supports the main claim; limitations are disclosed and do not threaten required behavior.
- **6**: partially useful but missing a material requirement, validation, observability, reproducibility, compatibility, or behavioral-invariance evidence; safe only with caveats.
- **4**: weak, ambiguous, wrong-target, hard to execute, or mostly unsupported; likely to fail important cases.

Use user categories exactly when provided, but warn when they omit production-critical lenses such as correctness, observability, reproducibility, compatibility, or behavioral-invariance. When user categories are narrow, keep them for reporting and add a separate broad-category rollup if it improves comparability. Before scoring, state relevance, weights, anchors, pass/fail criteria, estimator, formula, fixture checksum, validation tier, and limits. Prefer tokenizer counts; otherwise use a stable word-count proxy and label it. Do not change estimator mid-run. For compressed objectives, increase token weight only after all production-critical categories are at least 7.5.

Default formula when no better user formula exists:

`combined = production_effectiveness - cost_penalty + coverage_bonus - regression_penalty`

Define each term once. Store raw data so another run can recompute the rank. Production effectiveness should be the weighted mean of required and conditional production-critical categories, not a raw feature count.

## 4. Validation Tier and Claim Caps

Classify before scoring:

| Tier | Evidence | Allowed claim | Cap |
|---|---|---|---:|
| T0 | source inspection only | best structural/proxy candidate | 9.2 |
| T1 | fixed fixtures + deterministic/heuristic scoring | best deterministic-proxy measured candidate | 9.4 |
| T2 | repeated live model/API calls + variance notes | best live-measured candidate for this setup | 9.7 |
| T3 | qualified independent human review | best validated under review protocol | none |

Separate production effectiveness, overall including cost, confidence, and tier. Never imply live behavior from T0/T1. If the winner changes under another tier, estimator, objective, weights, target map, category/lens map, or fixture coverage, report sensitivity. A challenged result must show old claim, corrected claim, and obsolete conclusion.

## 5. Evidence, Caps, and Score Packet

Score 0-10. Scores above 8 require positive source evidence; above 9 require strong evidence and no material missing requirement. If a category cannot be evaluated, score conservatively and label the limit.

Caps unless stronger source evidence justifies override:

- full comparison unit not read: max overall 6.0;
- unresolved identity/scope mismatch: max production 6.5;
- no/wrong target map: max production 8.0;
- undefined category relevance in a disputed score: max affected category 7.5;
- missing correctness evidence for a production recommendation: max correctness 7.0 and max production 8.0;
- no observability path for failures in recommendation-grade work: max observability 6.5 and max production 8.5;
- no evidence ledger for recommendation-grade work: max evidence 6.5 and audit 7.0;
- no manifest for large/repeated work: max handoff/audit 7.0;
- unverified behavioral-invariance for a next-version recommendation: max behavioral-invariance 7.0 and max production 8.5;
- unrequested semantic, activation, output-contract, refusal, validation-tier, or protected-token behavior changes: max behavioral-invariance 6.0 until corrected;
- different inputs, formulas, estimators, weights, category/lens maps, target maps, or relevance labels: no best-measured claim;
- token efficiency is the only winning production category: label best compressed, not best production;
- deterministic proxy presented as live behavior: invalidate until corrected;
- user-facing package includes irrelevant process provenance, tool/evaluator names, or revision-history wording not requested by the user: max release-content hygiene 6.0 and require a sanitization pass before handoff.

For recommendation-grade, repeated, challenged, synthesized, or large benchmark work, save enough to audit and recompute:

- `run_manifest.json`: run id, timestamp, source/generated paths, ignored noise, checksums/sizes, objective, target map, category relevance, anchors, weights, formula, estimator, caps, validation tier, fixture checksum/count, seed, model/API settings if any, validation commands, observability markers, failure taxonomy, exclusions, overwrite policy, publication-boundary policy, old-vs-corrected references.
- `candidate_inventory.csv`: identity, path, checksum, purpose, comparison unit, token estimate, target-fit status, category/lens coverage status, observability hooks.
- `category_map.json`: category names, weights, relevance labels, production-critical flags, anchors, pass/fail criteria, evidence requirements, cap rules, and any user overrides.
- `evidence_ledger.csv`: candidate, category, relevance, score, source locator, positive evidence, missing evidence, confidence, evidence type, validation tier.
- `score_matrix.csv`: category scores, production effectiveness, cost terms, overall/combined, pass rate, failure count, rank.
- `row_results.csv/jsonl` when fixtures exist: candidate, fixture id/category, input size, target behavior, expected behavior, score, cost, failures, failure locality, debug evidence, notes, evidence marker, validation tier.
- `iteration_log.csv/json`: working-log-only record of revision target, old/new scores, deltas, changed sections, expected benefit, regressions, accept/reject reason, rollback path, probe, and stop reason. Keep this out of release contents unless the user asks for audit materials.
- `correction_audit.csv/json` for challenged scores.

When feasible, include a small rank-recompute script or command. Run it once. Prose, matrix, ledger, category/lens map, manifest, observability markers, and recomputed rank must agree.

## 6. Analysis Gate

For each candidate, read the complete comparison unit and report: intent, mechanism, constraints, output shape, validation behavior, assumptions, protected tokens, source-vs-generated boundary, target-map fit, category/lens coverage, strengths, weaknesses, best use case, likely failure mode, observability/debug path, cost, comparability, objective fit, uncertainty, and score rationale.

Penalize wrong-target scoring, hidden ambiguity, unsupported claims, duplicated/conflicting rules, stale text, untestable guidance, missing correctness behavior, missing safety behavior, weak observability, weak handoff, over-compression, unintended behavior change, irrelevant process provenance in release contents, unverifiable superiority claims, localization loss, source/result overwrite risk, unrecomputable rank, and challenge-handling gaps. Reward executable sequencing, target-fit clarity, priority ladders, exact code/error/log/token preservation, domain-term preservation, validation hooks, evidence-grounded scoring, auditability, failure traceability, compactness without loss, recomputable packets, behavioral invariance, and legacy compatibility. Do not bias toward newer, longer, shorter, or more polished versions.

Prior reports, user challenges, and old matrices are critique evidence, not ground truth.

## 7. Measurement Gate

Use when the user asks for best, best measured, test again, same mixture, complete matrix, effectiveness, token consumption, repeated improvement, validation of a new candidate, or a next version.

1. Reuse exact prior fixtures when requested; verify checksum.
2. Otherwise build fixtures from the target map and category/lens map. Use the requested count; if none is given, use a compact diverse set sufficient for every active category.
3. Include normal, edge, adversarial, multilingual, fixed-format, exact code/error/log, domain terms, risk/safety, ambiguity, protected tokens, sourced claims, audit/file handoff, rewrite, summary, decision, procedure, localization, observability, reproducibility, compatibility, behavioral invariance, release-content hygiene, and legacy-regression cases as relevant.
4. For generated test cases, define the fixture contract before examples: input shape, expected output shape, pass/fail oracle, validation command, allowed variation, forbidden leakage, and why the case targets an active category. Cases must be ready-to-test without trial-and-error format discovery.
5. Measure candidates and generated candidates with identical inputs, target map, category/lens map, relevance labels, weights, formula, estimator, pass/fail criteria, validation tier, and failure taxonomy.
6. Track effectiveness and cost separately: skill tokens, prompt/output tokens, runtime, file size, maintenance burden, artifact count, and rerun complexity as relevant.
7. Track observability separately: failure taxonomy, error locality, debug evidence, log/row locator, artifact status, and whether another reviewer can reproduce the failure from the packet.
8. Label deterministic proxy, heuristic, live-model/API, or human-review status clearly.
9. Re-rank after adding any candidate or generated candidate. Recommend the best measured version under the declared objective and target map, not the newest or shortest.

## 8. Sanity, Sensitivity, and Dominance

Before publishing or improving:

1. Recompute means, weighted scores, costs, bonuses, penalties, pass rates, and combined scores from raw rows.
2. Confirm identical inputs, categories, weights, formula, estimator, pass/fail rules, fixtures, target map, relevance labels, candidate inclusion rules, observability markers, and validation tier.
3. Spot-check evidence for top two, bottom two, newly added candidates, close-margin winners, and material rank changes.
4. Compare rank with target map and dominance rules. Resolve wrong-target, compression-only, estimator-sensitive, low-evidence, low-observability, behavioral-invariance-sensitive, and validation-tier-sensitive wins.
5. Run sensitivity checks for close margins by varying token-cost and subjective weights within a declared range; call the result margin-sensitive when ranks change.
6. Check contradiction triad: prose claims, matrix rows, category/lens map, manifest, and evidence ledger must agree with objective, target map, estimator, and validation tier.
7. Do not mix token counts, word proxies, and file sizes as equivalent.

## 9. Improvement and Regression Firewall

Create or revise a candidate only after analysis/measurement evidence exists. Preserve best proven behavior and valuable legacy behavior unless unsafe, unclear, obsolete, contradictory, or wrong-target. Convert explanations into compact operational rules. Prefer one priority ladder, reusable output shapes, and concise gates over repeated advice.

For skill/prompt next versions, use: metadata, activation scope, core invariant, intake/identity, target/objective/category/rubric, evidence/measurement/observability, improvement/change rules, correction/audit, output/handoff, quality gate.

Add rules only when they improve execution, correctness, safety, target fit, evidence, validation, observability, audit, reproducibility, compatibility, behavioral-invariance, correction quality, maintainability, measured performance, or localization. Optimize tokens only after correctness, safety, scope, evidence, observability, audit, validation-tier honesty, compatibility, behavioral-invariance, and localization survive.

Before accepting a next version, run a regression firewall, behavioral-invariance firewall, category firewall, and publication firewall:

- list valuable legacy behaviors;
- verify each is preserved or explicitly deprecated;
- identify behavior removed for token savings;
- compare old/new activation, stop conditions, output contract, refusal/fallback behavior, protected-token handling, validation-tier claims, and handoff shape;
- reject if required behavior, correctness, observability, reproducibility, compatibility, behavioral invariance, evidence, audit, or localization regresses;
- record why material additions are worth their cost;
- scan release contents for irrelevant process wording, tool/evaluator names, generation provenance, benchmark-bragging, internal iteration details, and stale version breadcrumbs; remove them unless explicitly requested.

If a next version fails to beat the incumbent, report it honestly. Revise once only when the failure is specific and fixable; otherwise keep the incumbent.

## 10. Iteration and Stop Control

For repeated version improvement, define the revision target, create one candidate at a time, retest with the same objective, fixtures, estimator, formula, weights, category/lens map, target map, relevance labels, and tier, and accept only if:

- production effectiveness improves by at least 0.05; or
- a high-severity failure is fixed without reducing production effectiveness and without lowering overall beyond a declared small threshold.

Do not accept a revision that improves only token efficiency while lowering required behavior or causing unrequested behavioral change. Preserve an iteration log: old score, new score, delta, changed sections, expected benefit, regressions, accept/reject reason, rollback path, rejected/no-improvement probe, and stop reason. Stop when the next change is cosmetic, duplicative, token-expanding, estimator-sensitive, wrong-target, already capped, behaviorally divergent without need, or not measurably useful. Recommend the best measured accepted version, not the newest candidate.

## 11. Challenge and Correction Audit

When the user challenges scoring, provides a conflicting report, asks to check again, or highlights a mistake, acknowledge non-defensively and treat the challenge as evidence requiring review, not proof.

Reopen source files and verify identity, target map, category/lens map, objective, rubric, weights, estimator, formula, raw rows, validation tier, and manifest. Compare the challenge against source evidence, anchors, caps, dominance rules, target map, category/lens map, and raw matrix. Recompute from raw data; if unavailable, rerun or state that the prior result cannot be verified.

Publish: old score, corrected score, delta, mistaken assumption, failed safeguard, affected candidates/categories/target fields, obsolete conclusion, corrected recommendation, validation tier before/after, live-validation status, remaining uncertainty, and corrected artifact paths/checksums. Save corrected outputs with a new prefix/path/checksum; do not silently replace earlier outputs.

## 12. Final Handoff and Adversarial Review

Return, as relevant: workspace/files inspected and ignored noise; objective, target map summary, validation tier, category/lens map/rubric/anchors, weights, formula, estimator; score matrix; per-version analysis; best existing version; best compressed vs best production; new version path/version; measured retest result; corrections; manifest summary; validation notes, observability notes, limits, claim caps, and saved file links.

Saved/modified files must include exact path, checksum, validation status, live-vs-proxy status, and claim-strength limit. Use the user's language unless asked otherwise, while preserving exact code, logs, paths, identifiers, and protected tokens.

Before final recommendation, ask: What evidence would make the winner lose? Is the result sensitive to estimator, weights, objective, target map, category/lens map, fixture coverage, behavioral-invariance checks, or validation tier? Did any score come from old summaries instead of source files? Did a shorter version win by deleting required behavior? Did the improvement remove valuable legacy behavior or change behavior without user need? Would “your scoring seems incorrect” be plausible? Do prose, matrix, ledger, category/lens map, manifest, observability markers, and tier agree? Are best-production and best-compressed clearly labeled?

If material risk remains, recheck affected files or rerun the matrix before publishing.

Release-content hygiene check: before handing off a package or revised artifact, inspect the delivered files separately from audit files. The delivered files should describe only the artifact's intended behavior, usage, constraints, validation, and maintenance contract. Keep comparison history, evaluator names, internal process labels, generated-by metadata, and rejected-option narratives in the audit packet, not in the release package, unless the user asks otherwise.
