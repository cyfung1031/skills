---
name: best-version-builder
description: Compare, score, synthesize, retest, and plateau-stop candidate versions with source-grounded identity, target maps, calibrated objectives, validation-tier claim caps, evidence ledgers, recomputable score packets, artifact checksums, correction audits, and anti-compression safeguards.
version: 1.3.1
last_updated: 2026-06-17
---

# Candidate Version Analysis + Plateau Synthesis

Use when the user provides candidate versions, prompts, skills, specs, code variants, documents, archives, benchmark reports, prior matrices, or generated successors and asks to compare, score, choose, improve, synthesize, retest, correct, or validate a best version.

Core invariant: **identity → target map → objective → rubric → evidence → measurement → recomputation → synthesis → correction → handoff**. Keep these gates separate. Do not score from filenames, recency, polish, length, prior summaries, or assumed intent. Do not rewrite first and rationalize afterward.

## 1. Intake, Identity, and Workspace

1. Use the requested workspace; otherwise use the active project workspace. Unpack archives into a clean source directory. Preserve originals unchanged; write generated successors and results to separate output paths.
2. Ignore noise: `__MACOSX`, `.DS_Store`, resource forks, temp files, caches, build products, duplicate outputs, and prior generated artifacts unless explicitly in scope.
3. Inventory every candidate: name/version/path, checksum or stable size marker, artifact type, declared purpose, comparison unit, output contract, protected tokens, constraints, estimator/estimate, scope notes, and source-vs-generated boundary.
4. Identify candidates from source content, not filename alone. If filename, frontmatter, title, and body disagree, report the conflict and use content-grounded identity.
5. Mark each artifact `in-scope`, `comparator-only`, or `out-of-scope`. Comparator-only artifacts may inform analysis but cannot silently win for another target.
6. Before final handoff, verify every saved path exists and report checksum/status. Never invent sandbox links or silently overwrite source or prior generated files.

## 2. Target Behavior Map

Before scoring, write a compact target map:

- intended user task, artifact purpose, comparison unit, activation/stop conditions, and non-goals;
- required outputs, saved artifacts, handoff shape, protected tokens, exact-preservation needs, and localization expectations;
- safety/professional, evidence, validation, audit, reproducibility, and correction requirements;
- critical legacy behaviors that must survive synthesis;
- optional helpful behaviors;
- irrelevant, comparator-only, and wrong-target features that must not be rewarded or penalized unless explicitly required.

Rules: no target map caps production recommendation at 8.0. Unresolved target mismatch caps production at 6.5. A prior matrix using another target map is critique evidence only. Score target fit separately from feature richness. Mark every category and material feature as required, optional, out-of-scope, or comparator-only.

## 3. Objective, Rubric, Weights, Formula

Default objective: **best production version**.

Profiles:

- **production**: reliable target-task performance, evidence, auditability, maintainability, correction quality; cost is secondary.
- **compressed**: cost minimization only after required production behavior remains acceptable.
- **research/exploratory**: diagnostic coverage and alternatives; higher cost tolerance.
- **live-model**: repeated model/API calls with variance notes.
- **deterministic proxy**: static/heuristic checks only; never imply live behavior.

Default categories when the user gives none:

| Category | Weight |
|---|---:|
| Clarity / executability | 1.15 |
| Intent / scope / target fit | 1.20 |
| Guardrails | 1.15 |
| Evidence / validation | 1.20 |
| Handoff / audit | 1.05 |
| Scripts / harnesses | 0.85 |
| Maintainability | 1.00 |
| Token efficiency | 0.50 |
| Language / localization, when relevant | 1.00 |

Use user categories exactly when provided. Before scoring, state relevance, weights, 10/8/6/4 anchors, pass/fail criteria, estimator, formula, fixture checksum, validation tier, and limits. Prefer tokenizer counts; otherwise use a stable word-count proxy and label it. Do not change estimator mid-run. For compressed objectives, increase token weight only after all production-critical categories are at least 7.5.

Default formula when no better user formula exists:

`combined = production_effectiveness - cost_penalty + coverage_bonus - regression_penalty`

Define each term once. Store raw data so another run can recompute the rank.

## 4. Validation Tier and Claim Caps

Classify before scoring:

| Tier | Evidence | Allowed claim | Cap |
|---|---|---|---:|
| T0 | source inspection only | best structural/proxy candidate | 9.2 |
| T1 | fixed fixtures + deterministic/heuristic scoring | best deterministic-proxy measured candidate | 9.4 |
| T2 | repeated live model/API calls + variance notes | best live-measured candidate for this setup | 9.7 |
| T3 | qualified independent human review | best validated under review protocol | none |

Separate production effectiveness, overall including cost, confidence, and tier. Never imply live behavior from T0/T1. If the winner changes under another tier, estimator, objective, weights, target map, or fixture coverage, report sensitivity. A challenged result must show old claim, corrected claim, and obsolete conclusion.

## 5. Evidence, Caps, and Score Packet

Score 0-10. Scores above 8 require positive source evidence; above 9 require strong evidence and no material missing requirement. If a category cannot be evaluated, score conservatively and label the limit.

Caps unless stronger source evidence justifies override:

- full comparison unit not read: max overall 6.0;
- unresolved identity/scope mismatch: max production 6.5;
- no/wrong target map: max production 8.0;
- undefined category relevance in a disputed score: max affected category 7.5;
- no evidence ledger for recommendation-grade work: max evidence 6.5 and audit 7.0;
- no manifest for large/repeated work: max handoff/audit 7.0;
- different inputs, formulas, estimators, weights, target maps, or relevance labels: no best-measured claim;
- token efficiency is the only winning production category: label best compressed, not best production;
- deterministic proxy presented as live behavior: invalidate until corrected.

For recommendation-grade, repeated, challenged, synthesized, or large benchmark work, save enough to audit and recompute:

- `run_manifest.json`: run id, timestamp, source/generated paths, ignored noise, checksums/sizes, objective, target map, category relevance, anchors, weights, formula, estimator, caps, validation tier, fixture checksum/count, seed, model/API settings if any, validation commands, exclusions, overwrite policy, old-vs-corrected references.
- `candidate_inventory.csv`: identity, path, checksum, purpose, comparison unit, token estimate, target-fit status.
- `evidence_ledger.csv`: candidate, category, relevance, score, source locator, positive evidence, missing evidence, confidence, evidence type, validation tier.
- `score_matrix.csv`: category scores, production effectiveness, cost terms, overall/combined, pass rate, failure count, rank.
- `row_results.csv/jsonl` when fixtures exist: candidate, fixture id/category, input size, target behavior, expected behavior, score, cost, failures, notes, evidence marker, validation tier.
- `iteration_log.csv/json`: revision target, old/new scores, deltas, changed sections, expected benefit, regressions, accept/reject reason, rollback path, probe, stop reason.
- `correction_audit.csv/json` for challenged scores.

When feasible, include a small rank-recompute script or command. Run it once. Prose, matrix, ledger, manifest, and recomputed rank must agree.

## 6. Analysis Gate

For each candidate, read the complete comparison unit and report: intent, mechanism, constraints, output shape, validation behavior, assumptions, protected tokens, source-vs-generated boundary, target-map fit, strengths, weaknesses, best use case, likely failure mode, cost, comparability, objective fit, uncertainty, and score rationale.

Penalize wrong-target scoring, hidden ambiguity, unsupported claims, duplicated/conflicting rules, stale text, untestable guidance, missing safety behavior, weak handoff, over-compression, unverifiable superiority claims, localization loss, source/result overwrite risk, unrecomputable rank, and challenge-handling gaps. Reward executable sequencing, target-fit clarity, priority ladders, exact code/error/log/token preservation, domain-term preservation, validation hooks, evidence-grounded scoring, auditability, compactness without loss, recomputable packets, and legacy compatibility. Do not bias toward newer, longer, shorter, or more polished versions.

Prior reports, user challenges, and old matrices are critique evidence, not ground truth.

## 7. Measurement Gate

Use when the user asks for best, best measured, test again, same mixture, complete matrix, effectiveness, token consumption, repeated improvement, synthesis validation, or a successor.

1. Reuse exact prior fixtures when requested; verify checksum.
2. Otherwise build fixtures from the target map. Use the requested count; if none is given, use a compact diverse set sufficient for every active category.
3. Include normal, edge, adversarial, multilingual, fixed-format, exact code/error/log, domain terms, risk/safety, ambiguity, protected tokens, sourced claims, audit/file handoff, rewrite, summary, decision, procedure, localization, and legacy-regression cases as relevant.
4. Measure candidates and successors with identical inputs, target map, relevance labels, weights, formula, estimator, pass/fail criteria, validation tier, and failure taxonomy.
5. Track effectiveness and cost separately: skill tokens, prompt/output tokens, runtime, file size, maintenance burden, artifact count, and rerun complexity as relevant.
6. Label deterministic proxy, heuristic, live-model/API, or human-review status clearly.
7. Re-rank after adding any candidate or successor. Recommend the best measured version under the declared objective and target map, not the newest or shortest.

## 8. Sanity, Sensitivity, and Dominance

Before publishing or synthesizing:

1. Recompute means, weighted scores, costs, bonuses, penalties, pass rates, and combined scores from raw rows.
2. Confirm identical inputs, weights, formula, estimator, pass/fail rules, fixtures, target map, relevance labels, candidate inclusion rules, and validation tier.
3. Spot-check evidence for top two, bottom two, newly added candidates, close-margin winners, and material rank changes.
4. Compare rank with target map and dominance rules. Resolve wrong-target, compression-only, estimator-sensitive, low-evidence, and validation-tier-sensitive wins.
5. Run sensitivity checks for close margins by varying token-cost and subjective weights within a declared range; call the result margin-sensitive when ranks change.
6. Check contradiction triad: prose claims, matrix rows, and evidence ledger must agree with objective, target map, estimator, and validation tier.
7. Do not mix token counts, word proxies, and file sizes as equivalent.

## 9. Synthesis and Regression Firewall

Synthesize only after analysis/measurement evidence exists. Preserve best proven behavior and valuable legacy behavior unless unsafe, unclear, obsolete, contradictory, or wrong-target. Convert explanations into compact operational rules. Prefer one priority ladder, reusable output shapes, and concise gates over repeated advice.

For skill/prompt successors, use: metadata, activation scope, core invariant, intake/identity, target/objective/rubric, evidence/measurement, synthesis/change rules, correction/audit, output/handoff, quality gate.

Add rules only when they improve execution, safety, target fit, evidence, validation, audit, reproducibility, correction quality, maintainability, measured performance, or localization. Optimize tokens only after correctness, safety, scope, evidence, audit, validation-tier honesty, and localization survive.

Before accepting a successor, run a regression firewall:

- list valuable legacy behaviors;
- verify each is preserved or explicitly deprecated;
- identify behavior removed for token savings;
- reject if required behavior regresses;
- record why material additions are worth their cost.

If a successor fails to beat the incumbent, report it honestly. Revise once only when the failure is specific and fixable; otherwise keep the incumbent.

## 10. Iteration and Plateau Control

For repeated successor building, define the revision target, create one successor at a time, retest with the same objective, fixtures, estimator, formula, weights, target map, relevance labels, and tier, and accept only if:

- production effectiveness improves by at least 0.05; or
- a high-severity failure is fixed without reducing production effectiveness and without lowering overall beyond a declared small threshold.

Do not accept a revision that improves only token efficiency while lowering required behavior. Preserve an iteration log: old score, new score, delta, changed sections, expected benefit, regression notes, accept/reject reason, rollback path, rejected/no-improvement probe, and stop reason. Stop when the next change is cosmetic, duplicative, token-expanding, estimator-sensitive, wrong-target, already capped, or not measurably useful. Recommend the best measured accepted version, not the newest candidate.

## 11. Challenge and Correction Audit

When the user challenges scoring, provides a conflicting report, asks to check again, or highlights a mistake, acknowledge non-defensively and treat the challenge as evidence requiring review, not proof.

Reopen source files and verify identity, target map, objective, rubric, weights, estimator, formula, raw rows, validation tier, and manifest. Compare the challenge against source evidence, anchors, caps, dominance rules, target map, and raw matrix. Recompute from raw data; if unavailable, rerun or state that the prior result cannot be verified.

Publish: old score, corrected score, delta, mistaken assumption, failed safeguard, affected candidates/categories/target fields, obsolete conclusion, corrected recommendation, validation tier before/after, live-validation status, remaining uncertainty, and corrected artifact paths/checksums. Save corrected outputs with a new prefix/path/checksum; do not silently replace earlier outputs.

## 12. Final Handoff and Adversarial Review

Return, as relevant: workspace/files inspected and ignored noise; objective, target map summary, validation tier, rubric/anchors, weights, formula, estimator; score matrix; per-version analysis; best existing version; best compressed vs best production; synthesized successor path/version; measured retest result; corrections; manifest summary; validation notes, limits, claim caps, and saved file links.

Saved/modified files must include exact path, checksum, validation status, live-vs-proxy status, and claim-strength limit. Use the user's language unless asked otherwise, while preserving exact code, logs, paths, identifiers, and protected tokens.

Before final recommendation, ask: What evidence would make the winner lose? Is the result sensitive to estimator, weights, objective, target map, fixture coverage, or validation tier? Did any score come from old summaries instead of source files? Did a shorter version win by deleting required behavior? Did synthesis remove valuable legacy behavior? Would “your scoring seems incorrect” be plausible? Do prose, matrix, ledger, manifest, and tier agree? Are best-production and best-compressed clearly labeled?

If material risk remains, recheck affected files or rerun the matrix before publishing.
