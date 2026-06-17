---
name: best-version-builder
description: Compare candidate versions and synthesize a best measured successor with source-grounded identity, target-behavior mapping, calibrated objectives, validation-tier claim caps, evidence ledgers, reproducible score packets, contradiction checks, correction audits, and plateau-based iteration without rewarding wrong-target or compression-only wins.
version: 1.3.0
last_updated: 2026-06-17
---

# Candidate Version Analysis + Measured Synthesis

Use when the user provides candidate versions, prompts, skills, specs, code variants, documents, archives, benchmark reports, prior score matrices, or generated successors and asks to compare, score, choose, improve, synthesize, retest, correct, or validate a best version.

Core rule: **source identity → target behavior → objective → rubric → evidence → measurement → sanity/provenance → synthesis → correction → recommendation** are separate gates. Do not score from filenames, prior summaries, age, polish, length, or assumed intent. Do not rewrite first and justify afterward.

## 1. Intake and Identity

1. Use the requested workspace; otherwise use the active project workspace. Unpack archives into a clean source directory, preserve originals unchanged, and save generated artifacts separately.
2. Ignore noise: `__MACOSX`, `.DS_Store`, resource forks, temp files, caches, build products, and duplicate generated outputs.
3. Inventory each candidate: name/version/path, checksum or stable size marker, artifact type, declared purpose, comparison unit, output contract, protected tokens, constraints, token estimator/estimate, and scope notes.
4. Identify candidates from source content, not filename alone. If filename/frontmatter/title/body conflict, report the conflict and use content-grounded identity.
5. Mark comparability: `in-scope`, `comparator-only`, or `out-of-scope`. Comparator-only artifacts may inform scoring but cannot silently win a production recommendation for another task.

## 2. Target Behavior Map

Before scoring, create a compact target map:

- intended user task, artifact purpose, and comparison unit;
- activation, stop, and non-goal conditions;
- required outputs, saved artifacts, handoff shape, protected tokens, and exact-preservation needs;
- critical behaviors that must survive synthesis;
- safety/professional, evidence, validation, localization, and audit requirements;
- optional helpful behaviors;
- irrelevant or comparator-only features that must not be rewarded or penalized unless explicitly required.

Rules: no target map means max production recommendation 8.0. Unresolved target mismatch means max production recommendation 6.5. A prior matrix using another target map is critique evidence only. Score objective fit separately from feature richness. Mark every category and feature as required, optional, out-of-scope, or comparator-only.

## 3. Objective Profiles, Categories, Weights

Default objective: **best production version**.

Profiles:

- **production**: maximize reliable target-task performance, evidence, auditability, and maintainability; token cost is secondary.
- **compressed**: minimize cost only after required production behavior remains acceptable.
- **research/exploratory**: maximize diagnostic coverage, alternatives, and explanation; cost tolerance is higher.
- **live-model**: use repeated model/API calls with variance notes.
- **deterministic proxy**: use static or heuristic checks only; never imply live behavior.

Default categories when the user gives none:

| Category | Meaning | Weight |
|---|---|---:|
| Clarity / executability | Can an operator follow it without guessing? | 1.15 |
| Intent / scope / target fit | Does it activate for the right task and exclude wrong targets? | 1.20 |
| Guardrails | Does it prevent unsafe, unsupported, wrong-format, or wrong-target behavior? | 1.15 |
| Evidence / validation | Are scores and claims source-grounded and testable? | 1.20 |
| Handoff / audit | Are outputs, paths, checksums, limits, and reproducibility clear? | 1.05 |
| Scripts / harnesses | Does it support fixtures, tests, reruns, and raw rows when relevant? | 0.85 |
| Maintainability | Is it compact, non-duplicative, stable, and easy to revise? | 1.00 |
| Token efficiency | Does it avoid unnecessary words without deleting required behavior? | 0.50 |
| Language / localization, when relevant | Does it preserve user language, script, locale, and localized output contracts? | 1.00 |

Use user categories exactly when provided. State category relevance, weights, anchors, pass/fail criteria, estimator, formula, fixture checksum, validation tier, and limits before scoring. Prefer a tokenizer; otherwise use a stable word-count proxy and label it as an estimate. Do not switch estimators mid-run. For compressed objective, raise token weight only after all production-critical categories are at least 7.5.

Default combined formula when no better user formula exists:

`combined = production_effectiveness - cost_penalty + coverage_bonus - regression_penalty`

Define every term once and keep it stable across candidates.

## 4. Validation Tier and Claim Caps

Classify before scoring:

| Tier | Evidence | Allowed claim | Default cap |
|---|---|---|---:|
| T0 | source inspection only | best structural/proxy candidate | 9.2 |
| T1 | fixed fixtures + deterministic/heuristic scoring | best deterministic-proxy measured candidate | 9.4 |
| T2 | repeated live model/API calls + variance notes | best live-measured candidate for this setup | 9.7 |
| T3 | qualified independent human review | best validated candidate under review protocol | none |

Separate production effectiveness, overall including cost, and confidence/tier. Never imply live behavior from T0/T1. If the winner changes under another tier, estimator, objective, weight setting, or target map, report sensitivity. A challenged result must show old claim, corrected claim, and obsolete conclusion.

## 5. Rubric Anchors, Caps, and Evidence Ledger Gate

Score 0-10. For each active category, define 10/8/6/4 anchors using the target map. A score above 8 requires positive source evidence. A score above 9 requires strong evidence and no material missing requirement. If a category cannot be evaluated from available artifacts, score conservatively and label the limit.

Evidence ledger gate: recommendation-grade, repeated, close-margin, challenged, or synthesized work needs candidate/category evidence. No high score may rest only on vibe, age, filename, or prior summary. Inferred evidence lowers confidence. Close or disputed candidates require ledger comparison.

Caps unless stronger source evidence justifies override:

- full comparison unit not read: max overall 6.0;
- unresolved identity/scope mismatch: max production 6.5;
- missing/wrong target map: max production 8.0;
- category relevance undefined in a disputed score: max affected category 7.5;
- no evidence ledger for recommendation-grade work: max evidence 6.5 and audit 7.0;
- no manifest for large/repeated benchmarks: max handoff/audit 7.0;
- different inputs, formulas, estimators, weights, target maps, or relevance labels: no best-measured claim;
- token efficiency is the only winning production category: label best compressed, not best production;
- deterministic proxy presented as live behavior: invalidate until corrected.

## 6. Score Packet and Manifest

For recommendation-grade, repeated, challenged, or large benchmark work, save enough data to recompute the rank:

- `run_manifest.json`: run id, timestamp, source paths, ignored noise, candidate checksums/sizes, generated paths, objective, target map, category relevance, anchors, weights, formula, estimator, caps, validation tier/status, fixture checksum/sample count, random seed if any, model/API settings if any, validation commands, exclusion reasons, overwrite policy, and old-vs-corrected references.
- `candidate_inventory.csv`: candidate identity, path, checksum, purpose, comparison unit, token estimate, target-fit status.
- `evidence_ledger.csv`: candidate, category, relevance, score, source locator, positive evidence, missing evidence, confidence, evidence type, validation tier.
- `score_matrix.csv`: category scores, production effectiveness, cost terms, overall/combined, pass rate, failure count, rank.
- `row_results.csv/jsonl` when fixtures exist: candidate, fixture id/category, input size, target behavior, expected behavior, scores, cost, failures, notes, evidence marker, validation tier.
- `correction_audit.csv/json` for re-benchmarks or disputed scores.

Do not overwrite source candidates or silently replace earlier generated results.

## 7. Analysis Gate

For each candidate, read the complete comparison unit and report: intent, mechanism, constraints, output shape, validation behavior, assumptions, protected tokens, source-vs-generated boundaries, target-map fit, strengths, weaknesses, best use case, likely failure mode, cost, comparability, objective fit, uncertainty, and score rationale.

Penalize wrong-target scoring, hidden ambiguity, unsupported claims, duplicated/conflicting rules, stale text, untestable guidance, missing safety behavior, weak handoff, over-compression, unverifiable superiority claims, and localization loss. Reward executable sequencing, target-fit clarity, priority ladders, exact code/error/log/token preservation, domain-term preservation, validation hooks, source-grounded scoring, auditability, compactness without loss, and proven legacy compatibility. Do not bias toward newer, longer, shorter, or more polished versions.

Prior reports, user challenges, and old matrices are critique evidence, not ground truth.

## 8. Measurement Gate

Use when the user asks for best, best measured, test again, same mixture, complete matrix, effectiveness, token consumption, repeated improvement, or synthesis validation.

1. Reuse exact prior fixtures when requested; verify and report checksum.
2. Otherwise build fixtures from the target map. Use the user-requested count; if none is given, use a compact but diverse set sufficient to test every active category.
3. Include normal, edge, adversarial, multilingual, fixed-format, exact code/error/log, domain terms, risk/safety, ambiguity, protected tokens, sourced claims, audit/file handoff, rewrite, summary, decision, procedure, localization, and legacy-regression cases as relevant.
4. Measure all candidates and successors with identical inputs, target map, relevance labels, weights, formula, estimator, pass/fail criteria, validation tier, and failure taxonomy.
5. Track effectiveness and cost separately: skill tokens, prompt tokens, output tokens, runtime, file size, and maintenance burden as relevant.
6. Label deterministic proxy, heuristic, live-model/API, or human-review status clearly.
7. Re-rank after adding any candidate or successor. Recommend the best measured version under the declared objective and target map, not the newest or shortest.

## 9. Anti-Compression and Dominance

Do not reward shorter text for deleting required behavior. If compression removes sequencing, scope control, target-fit clarity, evidence capture, validation, correction, or handoff, subtract in those categories. Report production effectiveness without token efficiency and overall including cost. If a candidate wins only through token efficiency while losing core production categories, label best compressed. If one candidate wins most production categories but loses overall, explain cost/coverage terms or revise weights if they contradict the objective. Flag compression-favored, target-mismatch, scope-mismatch, estimator-sensitive, low-evidence, close-margin, and validation-tier-sensitive wins.

## 10. Sanity, Sensitivity, and Contradiction Checks

Before publishing or synthesizing:

1. Recompute means, weighted scores, costs, bonuses, penalties, pass rates, and combined scores from raw rows.
2. Confirm identical inputs, weights, formula, estimator, pass/fail rules, fixture set, target map, relevance labels, candidate inclusion rules, and validation tier.
3. Spot-check evidence for top two, bottom two, newly added candidates, close-margin winners, and material rank changes.
4. Compare rank with dominance rules and target map; resolve wrong-target or compression-only winners.
5. Run sensitivity checks for close margins by varying token-cost and subjective weights within a declared range; report margin-sensitive rather than decisive when ranks change.
6. Check contradiction triad: prose claims, matrix rows, and evidence ledger must agree with objective, target map, estimator, and validation tier.
7. Do not mix token counts, word proxies, and file sizes as equivalent.

## 11. Synthesis Structure and Rules

Synthesize only after analysis/measurement evidence exists. Preserve best proven behavior and valuable legacy behavior unless unsafe, unclear, obsolete, contradictory, or wrong-target. Convert explanations into compact operational rules. Prefer one priority ladder, reusable output shapes, and concise gates over repeated advice.

Default successor structure for skill/prompt artifacts:

1. metadata/frontmatter;
2. purpose and activation scope;
3. priority ladder or core rule;
4. intake/identity;
5. target/objective/rubric;
6. evidence/measurement protocol;
7. synthesis/change rules;
8. correction/audit rules;
9. output/handoff contract;
10. quality gate.

Add rules only when they improve execution, safety, target fit, evidence, validation, audit, reproducibility, correction quality, maintainability, or measured performance. Optimize tokens only after correctness, safety, scope, evidence, audit, localization, and validation-tier honesty survive. Record why material additions are worth their token cost.

If a successor fails to beat the best existing candidate, report it honestly. Revise once if the failure is specific and fixable; otherwise keep the incumbent as winner.

## 12. Iteration and Plateau Control

For repeated successor building, define the revision target before editing, create one successor at a time, retest with the same objective/fixtures/estimator/formula/weights/target map/relevance labels/tier, and accept only if:

- production effectiveness improves by at least 0.05; or
- a high-severity failure is fixed without reducing production effectiveness and without lowering overall beyond a declared small threshold.

Do not accept a revision that improves only token efficiency while lowering required behavior. Preserve an iteration log: old score, new score, delta, changed sections, expected benefit, regression notes, reason accepted/rejected, rollback path, rejected/no-improvement probe, and stop reason. Stop when the next change is cosmetic, duplicative, token-expanding, estimator-sensitive, wrong-target, or not measurably useful. Recommend the best measured accepted version, not the newest candidate.

## 13. Challenge and Correction Audit

When the user challenges scoring, provides a conflicting report, asks to check again, or highlights a mistake, acknowledge non-defensively and treat the challenge as evidence requiring review, not proof.

Reopen source files and verify identity, target map, objective, rubric, weights, estimator, formula, raw rows, validation tier, and manifest. Compare the challenge against source evidence, anchors, caps, dominance rules, target map, and raw matrix. Recompute from raw data; if unavailable, rerun or say the prior result cannot be verified.

Publish: old score, corrected score, delta, mistaken assumption, failed safeguard, affected candidates/categories/target fields, obsolete conclusion, corrected recommendation, validation tier before/after, live-validation status, remaining uncertainty, and corrected artifact paths/checksums. Save corrected outputs with a new prefix/path/checksum; do not silently replace earlier outputs.

## 14. Final Handoff

Be direct. Do not offer alternatives unless asked or required by uncertainty. Return, as relevant:

1. workspace/files inspected and ignored noise;
2. objective, target-map summary, validation tier, rubric/anchors, weights, formula, estimator;
3. score matrix;
4. per-version analysis;
5. best existing version;
6. best compressed vs best production, if different;
7. synthesized successor path/version;
8. measured retest result;
9. corrections from prior mistaken results;
10. validation notes, manifest summary, limits, and claim-strength caps;
11. saved file links.

Saved/modified files must report exact path, checksum, validation status, live-vs-proxy status, and claim-strength limits. Use the user's language unless they ask otherwise, while preserving exact code, logs, paths, identifiers, and protected tokens.

## 15. Final Adversarial Review

Before final recommendation, ask:

- What evidence would make the winner lose?
- Is the result sensitive to estimator, weights, objective, target map, fixture coverage, or validation tier?
- Did any score come from old summaries instead of source files?
- Did a shorter version win by deleting required behavior?
- Did synthesis remove valuable legacy behavior?
- Would “your scoring seems incorrect” be plausible?
- Do prose, score matrix, evidence ledger, objective, target map, estimator, and validation tier agree?
- Are best-production and best-compressed different and clearly labeled?

If material risk remains, recheck affected files or rerun the matrix before publishing.
