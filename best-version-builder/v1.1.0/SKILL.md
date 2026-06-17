---
name: best-version-builder
description: Compare candidate versions, synthesize an evidence-backed successor, then measure it against the candidates to validate the best measured version before making a recommendation.
version: v1.1.0
---

# Candidate Version Analysis + Measured Synthesis

Use when the user provides candidate versions, drafts, prompts, skills, specs, code variants, documents, or archives and asks to compare, score, choose, improve, or synthesize a better version.

Core rule: **analysis, synthesis, and measurement are separate gates**. First evaluate existing candidates. Then synthesize from evidence. Then measure the successor against the candidates before calling it best. Do not rewrite first and justify afterward.

## 1. Intake / Workspace

1. Put files in the requested workspace; otherwise use the active project workspace.
2. Unpack archives safely into a clean directory. Preserve originals. Ignore metadata/noise: `__MACOSX`, `.DS_Store`, resource forks, temp files, caches, build products, duplicate generated outputs.
3. Inventory candidates: version/name, path, type, size/token estimate, declared metadata, purpose, and comparison unit.
4. Identify comparison unit: folder, `SKILL.md`, prompt/spec, implementation, named draft, or document section.
5. Use user-specified categories exactly. Otherwise use the default rubric.
6. Keep generated artifacts separate from source candidates.

## 2. Default Rubric

Score 0–10. Equal weights unless the user gives priorities or the artifact’s purpose clearly requires weighting; state any weighting.

- **Clarity / executability**: ordered, direct, unambiguous, easy to run.
- **Intent / scope**: purpose, triggers, non-goals, outputs, coverage.
- **Guardrails**: safety, refusal/fallback, protected content, precedence, ambiguity.
- **Evidence / validation**: claims tied to source, tests, fixtures, citations, checks, or behavior.
- **Handoff / audit**: preserves paths, assumptions, decisions, rejected risks, status, next action, validation run/not run.
- **Scripts / harnesses**: repeatable commands, smoke tests, fixtures, matrices, CSV/log outputs.
- **Maintainability**: modular, low-duplication, easy to update, regression-resistant.
- **Token efficiency**: minimum words/tokens after correctness, safety, scope, and audit are preserved.

## 3. Analysis Gate

For each candidate:

1. Read the complete relevant content, not just filenames or summaries.
2. Extract intent, mechanism, constraints, output shape, validation behavior, assumptions, and exact protected tokens.
3. Score every rubric category with concrete evidence: path + heading/function/line/short quote when available.
4. Record strengths, weaknesses, best use case, likely failure mode, and token/size cost.
5. Penalize hidden ambiguity, unsupported claims, duplicated/conflicting rules, stale text, untestable guidance, missing safety behavior, excessive length, weak handoff, and unverifiable superiority claims.
6. Reward executable sequencing, precedence ladders, exact-token preservation, validation hooks, compactness without loss, auditability, and compatibility with proven legacy behavior.

Do not bias toward newer, longer, shorter, or more polished versions. Higher score requires more reliable required behavior.

## 4. Comparative Output Gate

Before synthesis, produce or internally maintain:

- scoring scale and weights;
- score matrix with category + overall scores;
- per-candidate rationale;
- cross-version ranking;
- decisive tradeoffs;
- best existing version.

Overall score is the weighted mean unless a measured combined score is defined.

## 5. Synthesis Gate

Synthesize one successor designed to beat the best existing candidate.

Rules:

1. Preserve best proven behavior from all candidates.
2. Remove decorative, stale, duplicate, contradictory, and example-only material unless needed for execution.
3. Convert explanations into compact operational rules.
4. Add guardrails only when they improve execution, validation, safety, or audit.
5. Keep valuable legacy behavior unless unsafe, unclear, or conflicting.
6. Prefer one priority ladder over repeated warnings.
7. Prefer reusable output shapes over prose.
8. Include validation hooks and measurable pass/fail criteria.
9. Optimize tokens only after correctness, safety, scope, evidence, and audit survive.
10. State uncertainty; never claim superiority until measured or logically demonstrated.

## 6. Measured-Version Gate

Use this gate whenever the user asks for the “best,” “best measured,” “test again,” “token consumption,” “effectiveness,” “score all,” or when synthesis claims should be validated.

1. Build fixtures covering normal, edge, and adversarial cases. For text/prompt/skill artifacts, include scenario fixtures; for code/config, include executable tests where possible.
2. Fixture minimums: use the user’s requested count. If none is given, use a compact but diverse set sufficient to test every rubric category.
3. Include stress cases: risk/safety, exact code/error/log, fixed format, multilingual, domain terms, audit/file handoff, sourced claims, rewrite, summary, decision, procedure, ambiguity, and protected tokens.
4. Measure each candidate and successor using the same harness, inputs, weights, and scoring formula.
5. Track both **effectiveness** and **cost**. Cost may include prompt tokens, skill tokens, output tokens, runtime, file size, or maintenance burden.
6. If using estimates or deterministic heuristics instead of live model/API calls, label them clearly and do not imply live-call accuracy.
7. Store detailed per-entry results when requested or when needed for audit: candidate, fixture id/category, input size, expected preservation, scores, token estimates, failures, notes.
8. Save CSV/JSON artifacts for large evaluations; include direct paths/links.
9. Re-rank after adding the successor. The final recommendation is the **best measured version**, not automatically the synthesized one.
10. If the successor fails to beat the best existing candidate, report that honestly and revise once if the failure is fixable without violating constraints.

Suggested combined score when token efficiency matters:

`combined = effectiveness_score - cost_penalty + coverage_bonus - regression_penalty`

Define each component before applying it. Keep formula stable across candidates.

## 7. Successor Structure

Use unless the target artifact requires another format:

1. metadata: name, version, purpose;
2. activation/applicability and stop conditions;
3. priority ladder;
4. operating procedure;
5. guardrails/protected tokens/fallbacks;
6. evidence and validation;
7. output shapes;
8. handoff/audit fields;
9. measurement harness;
10. maintenance and quality gate.

## 8. Handoff / Audit

For every final recommendation or saved successor, preserve:

- workspace and files inspected;
- ignored metadata/noise;
- candidate list and comparison unit;
- categories, weights, formula;
- best existing version;
- synthesized successor path/version;
- measured rank after synthesis;
- validation run/not run;
- known limits, especially estimated tokens or non-live tests;
- next action only if actionable.

Saved/modified files must report exact path and validation status.

## 9. Final Quality Gate

Before responding or saving:

- analysis finished before synthesis;
- every candidate scored in every category;
- major claims have evidence;
- successor preserves best unique capabilities;
- no duplicated/conflicting rules;
- no unsupported “best” claim;
- measurement is apples-to-apples;
- token efficiency improved or tradeoff is justified;
- paths, citations, validation status, and download links are present when relevant.

## 10. Final Response Contract

Return in this order:

1. workspace / files inspected;
2. score matrix;
3. per-version analysis;
4. best existing version;
5. synthesized successor;
6. measured retest result, if run;
7. validation notes and limits;
8. saved file links.

Be direct. No alternative designs unless asked. Give the best measured answer with enough evidence to audit it and enough compression to stay usable.
