---
name: variant-best-version-builder
description: Generate 16 strategically different variants of a source artifact, then iteratively synthesize, measure, and retest successors until no further measured improvement remains.
version: 1.0.0
last_updated: 2026-06-17
---

# Variant Best-Version Builder

## Contract

When active, this skill MUST keep **variant generation**, **analysis**, **synthesis**, and **measurement** as separate gates. It MUST NOT call any version “best” until candidates and successors have been measured with the same rubric, fixtures, cost metrics, and scoring formula.

The required workflow is:

1. Generate 16 meaningfully different variants across the requested perspectives.
2. Score all variants and source candidates.
3. Synthesize a successor from measured evidence.
4. Retest the successor against the candidate pool.
5. Repeat synthesis and retest until no non-regressive measured improvement remains.
6. Recommend the best measured version, not automatically the newest or shortest version.

## Inputs

Required:

- `source_artifact` or candidate set to improve.
- `comparison_unit`: skill, prompt, spec, document section, code file, folder, or named draft.

Optional:

- target name/version;
- workspace path;
- variant count, default `16`;
- perspectives/rubric;
- category weights;
- fixtures or test cases;
- cost metric: estimated tokens, words, bytes, runtime, file size, maintenance burden, or output length;
- output format and artifact paths;
- maximum iterations or stop threshold.

If the source artifact is missing, ask for it unless the user explicitly asks to create from scratch. If creating from scratch, state that there is no source candidate and treat the initial draft as `S0`.

## Activate Only When

Use when the user asks to:

- make many variants and choose/improve the best;
- combine variant generation with best-version-building;
- score, compare, synthesize, or measure prompts, skills, specs, docs, or code variants;
- repeatedly improve until no further measurable gain remains.

## Do Not Use For

- Simple rewrites that do not need comparative measurement.
- Pure brainstorming where no best measured successor is requested.
- Tasks where safety or policy requires refusal.
- Claims of live performance unless live tests were actually run.

## Priority Ladder

1. Safety, legality, and protected-content constraints.
2. Preserve originals and exact protected tokens/paths.
3. Analyze before synthesis; synthesize before measurement; measure before recommendation.
4. Use the user’s categories and weights exactly; otherwise use the default rubric.
5. Cover all requested perspectives across the 16 variants.
6. Keep metrics stable across candidates and iterations.
7. Improve token efficiency only after correctness, scope, guardrails, evidence, and audit survive.
8. Report uncertainty, limits, validation status, and failed improvement attempts.

## Default Rubric

Score each category `0–10`. Use equal weights unless the user provides weights or the artifact clearly requires a justified weighting.

1. **Clarity / executability**: ordered, direct, unambiguous, easy to run.
2. **Intent / scope**: purpose, triggers, non-goals, outputs, coverage.
3. **Guardrails**: safety, refusal/fallback, protected content, precedence, ambiguity.
4. **Evidence / validation**: claims tied to source, tests, fixtures, citations, checks, or behavior.
5. **Handoff / audit**: preserves paths, assumptions, decisions, rejected risks, status, next action, validation run/not run.
6. **Scripts / harnesses**: repeatable commands, smoke tests, fixtures, matrices, CSV/log outputs.
7. **Maintainability**: modular, low-duplication, easy to update, regression-resistant.
8. **Token efficiency**: minimum words/tokens after correctness, safety, scope, and audit are preserved.
9. **Language**: tone, personality, conciseness, precision, comprehensiveness, accessibility, and language matching.

Default formula:

`weighted_mean = sum(category_score * category_weight) / sum(category_weight)`

Optional combined formula when cost matters:

`combined = weighted_mean - cost_penalty + coverage_bonus - regression_penalty`

Define cost, coverage, and regression terms before applying them. Do not change the formula mid-loop.

## Gate 1 — Intake / Workspace

1. Create or use a clean workspace.
2. Preserve originals unchanged.
3. Keep generated variants, successors, reports, and harnesses separate from source files.
4. Inventory each source candidate: name, version, path, type, size, token/word estimate, declared purpose, and comparison unit.
5. Ignore metadata/noise: `.DS_Store`, `__MACOSX`, caches, temp files, build outputs, duplicate generated files, and resource forks.
6. Read the complete relevant content, not just filenames or summaries.
7. Extract intent, mechanisms, constraints, output shape, validation behavior, assumptions, exact protected tokens, and known risks.

## Gate 2 — Sixteen-Variant Builder

Generate exactly 16 variants unless the user requests another count. Variants MUST differ in operating logic, emphasis, or structure, not only wording.

Use this default 16-variant matrix unless the user supplies a different matrix:

| Variant | Primary focus | Secondary focus | Required distinguishing feature |
|---:|---|---|---|
| V01 | Clarity / executability | token efficiency | direct run-order procedure |
| V02 | Intent / scope | clarity | activation, stop conditions, outputs |
| V03 | Guardrails | ambiguity | refusal/fallback and precedence ladder |
| V04 | Evidence / validation | claims | source, citation, or check requirements |
| V05 | Handoff / audit | assumptions | status, decisions, rejected risks, next action |
| V06 | Scripts / harnesses | validation | repeatable commands, fixtures, CSV/log outputs |
| V07 | Maintainability | modularity | low-duplication sections and update points |
| V08 | Token efficiency | scope | shortest safe complete version |
| V09 | Language | tone | precise, concise, audience-aware wording rules |
| V10 | Guardrails | high-stakes fallback | professional/safety-critical boundary handling |
| V11 | Ambiguity triage | executability | when to ask, assume, continue, or stop |
| V12 | Output schema | audit | reusable output shapes and required fields |
| V13 | Language matching | accessibility | multilingual and plain-language behavior |
| V14 | Protected tokens | precedence | exact preservation and conflict resolution |
| V15 | Regression pack | harnesses | fixture matrix and pass/fail checks |
| V16 | Balanced full | all categories | best broad-coverage pre-synthesis candidate |

For every variant, include:

- metadata: name, version/variant id, purpose;
- activation and stop conditions;
- priority ladder or operating order;
- procedure;
- guardrails/fallbacks;
- evidence or validation behavior;
- output shape;
- audit or handoff behavior;
- maintenance/token notes when relevant.

## Gate 3 — Analysis and Scoring

For every source candidate and generated variant:

1. Score every rubric category with evidence.
2. Estimate cost: words, tokens, bytes, runtime, or maintenance burden as applicable.
3. Record strengths, weaknesses, best use case, likely failure mode, and protected-token behavior.
4. Penalize hidden ambiguity, unsupported claims, duplicated/conflicting rules, stale text, untestable guidance, missing safety behavior, excessive length, weak handoff, and unverifiable superiority claims.
5. Reward executable sequencing, exact-token preservation, validation hooks, compactness without loss, auditability, maintainability, and compatibility with proven behavior.
6. Produce or internally maintain a score matrix before synthesis begins.

## Gate 4 — Synthesis Loop

Start with the best measured existing candidate from Gate 3.

For each iteration:

1. Identify the best measured candidate and its decisive weaknesses.
2. Synthesize one successor designed to improve those weaknesses while preserving best proven behavior from all candidates.
3. Remove decorative, stale, duplicate, contradictory, or example-only material unless needed for execution.
4. Convert explanations into compact operational rules.
5. Prefer one priority ladder over repeated warnings.
6. Add guardrails only when they improve execution, validation, safety, or audit.
7. Include validation hooks and measurable pass/fail criteria.
8. Re-score the successor using the same rubric, fixtures, weights, formula, and cost metric.
9. Add the successor to the pool and rerank.
10. Continue only if the successor creates a measured non-regressive improvement.

## Stop Rule

Stop when one full synthesis attempt produces no acceptable improvement.

An acceptable improvement must satisfy at least one of these:

- higher weighted mean by the declared threshold, default `+0.05`;
- higher combined score under the frozen formula;
- lower cost with no category regression greater than `0.1` and no failed required fixture;
- higher validation pass rate with no loss in safety, scope, evidence, or audit.

Reject and report a candidate when it improves one metric but causes material regression elsewhere. Use Pareto logic: a successor is not better merely because it is shorter, newer, longer, or more polished.

If multiple successors tie, choose the one with:

1. no safety or scope regressions;
2. higher validation pass rate;
3. lower token/cost burden;
4. clearer audit trail;
5. simpler maintainability.

## Gate 5 — Measurement Harness

Build fixtures before final recommendation. Use user-provided fixtures when available; otherwise create a compact set covering all rubric categories.

For prompts, skills, and documents, include scenario fixtures for:

- normal request;
- edge/ambiguous request;
- adversarial or unsafe request;
- protected-token/path preservation;
- fixed output format;
- sourced factual claim;
- multilingual or tone-sensitive input;
- audit/handoff request;
- regression against legacy behavior;
- token/cost stress.

For code or configuration, include executable tests when possible.

Measurement outputs SHOULD include:

- `score_matrix.csv` and/or `.json`;
- `fixtures.json`;
- `iteration_log.json`;
- optional `measurement_harness.py` or equivalent;
- successor files;
- final best measured file.

If scores are heuristic or expert-estimated rather than live model/API tests, label them clearly.

## Output Shapes

### Variant File Header

```markdown
---
name: {target-name}
variant: V{NN}-{focus}
version: {version}
purpose: {one-line purpose}
---
```

### Iteration Log Row

```markdown
| round | pool | best_before | successor | weighted_mean | cost | decision | reason |
|---|---|---|---|---:|---:|---|---|
```

### Final Response

Return in this order:

1. workspace / files inspected;
2. generated 16-variant set;
3. score matrix;
4. per-version analysis summary;
5. best existing version before synthesis;
6. synthesis iteration history;
7. best measured successor;
8. validation run/not run and limits;
9. saved file links.

## Handoff / Audit Requirements

For every final recommendation or saved successor, preserve:

- workspace path;
- files inspected;
- ignored metadata/noise;
- candidate list and comparison unit;
- category weights and formula;
- fixture list and coverage;
- measurement method and whether live tests ran;
- best existing candidate before synthesis;
- successor versions and paths;
- rejected improvements and why;
- final measured ranking;
- known limits;
- next action only if concrete and actionable.

## Quality Gate

Before final output, verify:

- 16 variants were generated or the user-requested count was honored;
- variants differ by behavior, not only wording;
- every candidate was scored in every category;
- analysis happened before synthesis;
- synthesis happened before best-version recommendation;
- same rubric, fixtures, weights, and formula were used across measurements;
- cost and effectiveness were both tracked;
- no unsupported “best” claim remains;
- failed or rejected successors are reported honestly;
- final file paths and validation status are present;
- token efficiency did not erase correctness, safety, scope, evidence, or audit.
