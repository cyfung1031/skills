---
name: best-version-builder
description: Compare candidate versions, synthesize evidence-backed successors, and measure them with identity checks, rubric calibration, anti-compression safeguards, challenge handling, and auditable re-benchmarking before recommending the best measured version.
version: v1.2.0
last_updated: 2026-06-17
---

# Candidate Version Analysis + Measured Synthesis

Use when the user provides candidate versions, drafts, prompts, skills, specs, code variants, documents, archives, or benchmark reports and asks to compare, score, choose, improve, synthesize, retest, or validate a best version.

Core rule: **identity, analysis, synthesis, measurement, and recommendation are separate gates**. Verify what each candidate is before scoring. Evaluate existing candidates before synthesis. Synthesize only from evidence. Measure every candidate and successor under the same harness before calling anything best.

## 1. Intake / Workspace

1. Put files in the requested workspace; otherwise use the active project workspace.
2. Unpack archives safely into a clean source directory. Preserve originals unchanged.
3. Keep generated artifacts separate from source candidates.
4. Ignore metadata/noise: `__MACOSX`, `.DS_Store`, resource forks, temp files, caches, build products, and duplicate generated outputs.
5. Inventory every candidate:
   - name/version/path;
   - declared artifact type and purpose;
   - comparison unit: folder, `SKILL.md`, prompt/spec, implementation, named draft, or section;
   - source checksum or stable size marker;
   - token estimate method and estimate;
   - known constraints, protected tokens, and declared output contract.
6. Check candidate identity before measurement. If a filename/version label conflicts with frontmatter, title, purpose, or content, report the conflict and use the content-grounded identity in the matrix.
7. Check comparability. If a candidate is for a different task or scope, either exclude it with reason or include it as an out-of-scope comparator only if the user explicitly requested it. Mark scope mismatch in the matrix.

## 2. Candidate Identity Gate

Before scoring or comparing:

1. Verify that the candidate name, version, frontmatter, title, and content describe the same artifact.
2. Verify that the candidate's purpose matches the benchmark goal.
3. Verify that the comparison unit is the same for all candidates, or mark the mismatch explicitly.
4. Do not treat an attached file as the intended candidate solely because its filename is `SKILL.md`; identify it from content.
5. If the user asks to add a candidate with a different scope, include it only with a scope-mismatch note and prevent it from silently winning a production recommendation for another task.

## 3. Rubric Calibration Gate

Before scoring, define and save:

- artifact purpose and benchmark goal;
- candidate set and comparison unit;
- scoring categories and category meanings;
- weights;
- pass/fail criteria;
- token/cost estimator;
- combined-score formula;
- deterministic proxy vs live-model/API status;
- dataset/fixture identity and checksum when reused.

Default categories, 0-10:

- **Clarity / executability**: ordered, direct, unambiguous, easy to run; preserves enough steps to prevent skipped gates.
- **Intent / scope**: purpose, applicability, stop conditions, candidate boundaries, outputs, and non-goals.
- **Guardrails**: safety, refusal/fallback, protected content, precedence, ambiguity, unverifiable-superiority prevention, and source/generated separation.
- **Evidence / validation**: claims tied to source, exact text, tests, fixtures, citations, checks, or behavior; validation status stated.
- **Handoff / audit**: paths, assumptions, ignored noise, decisions, rejected risks, score rationale, artifacts, validation run/not run, and known limits.
- **Scripts / harnesses**: repeatable commands, smoke tests, fixtures, matrices, CSV/JSON logs, and rerun instructions.
- **Maintainability**: modular, low-duplication, easy to update, regression-resistant, and not over-coupled by compression.
- **Token efficiency**: minimum tokens only after correctness, safety, scope, evidence, validation, audit, and localization survive.
- **Language / tone / localization** when relevant: same-language handling, script integrity, localized headings/audit fields, and tone fit.

Default weighting: equal weights across required effectiveness categories. Token efficiency may be included, but must not dominate unless the user explicitly prioritizes compression.

Recommended combined score:

`combined = effectiveness_score - cost_penalty + coverage_bonus - regression_penalty`

Define each component once before measuring. Keep the formula stable across candidates in the same run.

## 4. Anti-Compression Bias Rules

1. Do not reward a shorter candidate for removing required operational detail.
2. Token efficiency is subordinate to correctness, safety, scope, evidence, validation, auditability, and required localization.
3. A compressed candidate that loses clear sequencing, explicit gates, evidence capture, or handoff requirements must lose points in the relevant categories, not just gain token-efficiency points.
4. If a candidate wins only because of token efficiency while losing most core effectiveness categories, flag it as **best compressed**, not **best production**, unless the user requested compression as the primary objective.
5. Report both:
   - effectiveness without token efficiency; and
   - overall/combined score with token cost.
6. Use a transparent token estimator. If using a proxy, name it and apply it consistently. Do not mix character-count, word-count, and tokenizer estimates in the same matrix unless separately labeled.

## 5. Analysis Gate

For each candidate:

1. Read the complete relevant content, not just filenames, prior summaries, or generated matrices.
2. Extract intent, mechanism, constraints, output shape, validation behavior, assumptions, exact protected tokens, and source-vs-generated boundaries.
3. Score every rubric category with concrete evidence: path + heading/function/line/short quote when available.
4. Record strengths, weaknesses, best use case, likely failure mode, token/size cost, and comparability status.
5. Penalize hidden ambiguity, unsupported claims, duplicated/conflicting rules, stale text, untestable guidance, missing safety behavior, weak handoff, over-compression, and unverifiable superiority claims.
6. Reward executable sequencing, priority ladders, exact-token preservation, validation hooks, source-grounded scoring, auditability, compactness without loss, and compatibility with proven legacy behavior.
7. Do not bias toward newer, longer, shorter, or more polished versions. Higher score requires more reliable required behavior.

## 6. Score Sanity Gate

Before publishing or using scores for synthesis:

1. Verify candidate identities and versions against source content.
2. Recompute category means and combined scores from raw rows.
3. Check that all candidates used the same inputs, weights, formula, token estimator, and pass/fail rules.
4. Compare ranking against category evidence. If a lower-effectiveness candidate outranks a higher-effectiveness candidate, explain exactly which cost or coverage term caused it.
5. Run dominance checks:
   - If Candidate A beats Candidate B in most core categories but loses overall, explain or adjust the weighting if it contradicts stated priorities.
   - If token efficiency is the only decisive win, label the result as compression-favored.
   - If a candidate has a scope mismatch, prevent it from silently winning a production recommendation.
6. Spot-check at least the top two, bottom two, and any newly added candidate against source text.
7. When prior results, user-provided critiques, or external reports conflict with the matrix, perform a re-benchmark from source artifacts rather than defending the old score.

## 7. Comparative Output Gate

Before synthesis, produce or internally maintain:

- scoring scale and weights;
- score matrix with category + overall/combined scores;
- per-candidate rationale;
- cross-version ranking;
- decisive tradeoffs;
- best existing version;
- best compressed version, if different;
- best production/effectiveness version, if different.

Overall score is the weighted mean unless a measured combined score is defined.

## 8. Synthesis Gate

Synthesize one successor designed to beat the best measured production candidate, not merely the shortest candidate.

Rules:

1. Preserve best proven behavior from all candidates.
2. Remove decorative, stale, duplicate, contradictory, and example-only material unless needed for execution.
3. Convert explanations into compact operational rules without deleting required gates.
4. Add guardrails only when they improve execution, validation, safety, audit, identity checks, or challenge handling.
5. Keep valuable legacy behavior unless unsafe, unclear, conflicting, or demonstrably redundant.
6. Prefer one priority ladder over repeated warnings.
7. Prefer reusable output shapes over prose.
8. Include validation hooks, pass/fail criteria, and rerun instructions.
9. Optimize tokens only after correctness, safety, scope, evidence, audit, and maintainability survive.
10. State uncertainty; never claim superiority until measured or logically demonstrated.

## 9. Measured-Version Gate

Use this gate whenever the user asks for the “best,” “best measured,” “test again,” “token consumption,” “effectiveness,” “score all,” “same mixture,” “complete matrix,” or when synthesis claims should be validated.

1. Reuse the exact prior dataset/fixtures when the user asks for the same mixture. Verify and report dataset checksum.
2. Build fixtures covering normal, edge, and adversarial cases when no reusable dataset exists.
3. Fixture minimums: use the user’s requested count. If none is given, use a compact but diverse set sufficient to test every rubric category.
4. Include stress cases: risk/safety, exact code/error/log, fixed format, multilingual, domain terms, audit/file handoff, sourced claims, rewrite, summary, decision, procedure, ambiguity, protected tokens, and regression-from-legacy behavior.
5. Measure each candidate and successor using the same harness, inputs, weights, formula, token estimator, and pass/fail criteria.
6. Track both **effectiveness** and **cost**. Cost may include prompt tokens, skill tokens, output tokens, runtime, file size, or maintenance burden.
7. If using estimates or deterministic heuristics instead of live model/API calls, label them clearly and do not imply live-call accuracy.
8. Store detailed per-entry results when requested or needed for audit: candidate, fixture id/category, input size, expected behavior, scores, token estimates, cost terms, failures, notes, and source-evidence markers.
9. Save CSV/JSON artifacts for large evaluations and include direct paths/links.
10. Re-rank after adding any candidate or successor. The final recommendation is the **best measured version under the declared objective**, not automatically the newest or shortest version.
11. If the successor fails to beat the best existing candidate, report that honestly and revise once if the failure is fixable without violating constraints.

## 10. Challenge / Re-Benchmark Gate

Use when the user says the scoring is wrong, provides a conflicting report, asks to verify, or identifies a likely mistake.

1. Acknowledge the challenge without defensiveness.
2. Re-open source candidate files and benchmark config. Do not rely only on prior generated summaries.
3. Verify candidate identity, scope, token estimator, formula, weights, and dataset checksum.
4. Compare the user-provided category scores or critique against source evidence.
5. If the critique is plausible, rerun the benchmark with corrected assumptions while preserving the same dataset when requested.
6. Publish a delta table showing old score, corrected score, and reason for each material change.
7. Save corrected artifacts with a new prefix; do not overwrite prior results unless explicitly requested.
8. State which conclusion changed and which prior claim should be disregarded.

## 11. Successor Structure

Use unless the target artifact requires another format:

1. metadata: name, version, purpose, last_updated;
2. activation/applicability and stop conditions;
3. priority ladder;
4. operating procedure;
5. guardrails, protected tokens, source/generated separation, and fallbacks;
6. evidence and validation;
7. output shapes;
8. handoff/audit fields;
9. measurement harness and challenge/rerun behavior;
10. maintenance and quality gate.

## 12. Handoff / Audit

For every final recommendation or saved successor, preserve:

- workspace and files inspected;
- ignored metadata/noise;
- candidate list and comparison unit;
- candidate identity conflicts or scope mismatches;
- dataset/fixture checksum when applicable;
- categories, weights, formula, and token estimator;
- best existing version;
- best compressed version, if different;
- best production/effectiveness version, if different;
- synthesized successor path/version;
- measured rank after synthesis;
- validation run/not run;
- deterministic vs live benchmark status;
- known limits, especially estimated tokens and non-live tests;
- corrected/obsolete prior conclusions, if a re-benchmark changed results;
- next action only if actionable.

Saved/modified files must report exact path and validation status.

## 13. Final Quality Gate

Before responding or saving:

- source identities verified;
- rubric and formula defined before scoring;
- analysis finished before synthesis;
- every candidate scored in every category;
- major claims have evidence;
- scores pass sanity checks;
- token efficiency did not override required behavior unless explicitly prioritized;
- successor preserves best unique capabilities;
- no duplicated/conflicting rules;
- no unsupported “best” claim;
- measurement is apples-to-apples;
- challenged results were rechecked from source;
- paths, citations, validation status, and download links are present when relevant.

## 14. Final Response Contract

Return in this order:

1. workspace / files inspected;
2. rubric, weights, formula, and token estimator;
3. score matrix;
4. per-version analysis;
5. best existing version;
6. best compressed vs best production, if different;
7. synthesized successor;
8. measured retest result, if run;
9. corrections from any prior mistaken result;
10. validation notes and limits;
11. saved file links.

Be direct. No alternative designs unless asked. Give the best measured answer with enough evidence to audit it and enough compression to stay usable.
