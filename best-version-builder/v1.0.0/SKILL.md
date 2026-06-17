---
name: best-version-builder
description: Unpack and compare candidate versions, independently score each one, then build a stronger best-version successor using evidence-backed best practices.
version: v1.0.0
---

# Candidate Version Analysis + Best-of-All Synthesis

Use this skill when the user provides multiple versions, drafts, prompts, skills, specs, code variants, documents, or archives and asks to compare, score, choose, or synthesize a better version.

Core rule: **analysis and synthesis are independent tasks**. First evaluate what exists. Only after the analysis is complete, synthesize the best successor from evidence. Do not rewrite first and justify afterward.

## 1. Intake and Workspace

1. Put all provided files in the requested workspace. If none is specified, use the active project workspace.
2. Unpack archives safely into a clean directory. Preserve original files. Ignore generated metadata such as `__MACOSX`, `.DS_Store`, temporary files, caches, build products, and duplicate resource forks unless the user explicitly asks about them.
3. Build an inventory: version name, path, file type, size, apparent purpose, and any declared version metadata.
4. Identify the comparison unit. Usually this is each version folder, each `SKILL.md`, each prompt/spec, each implementation, or each named draft.
5. If categories are user-specified, use them exactly. Otherwise use the default rubric below.

## 2. Default Rubric

Score each category from **0 to 10**.

- **Clarity / executability**: instructions are direct, ordered, unambiguous, and easy for an agent or human to execute.
- **Intent / scope**: purpose, activation conditions, covered cases, non-goals, and expected outputs are clear.
- **Guardrails**: safety, refusal conditions, protected content, precedence rules, and ambiguity handling are explicit.
- **Evidence / validation**: claims are grounded in source text, tests, examples, checks, citations, or observable behavior.
- **Handoff / audit**: outputs preserve decisions, assumptions, paths, status, next actions, verification, and review trail.
- **Scripts / harnesses**: includes or enables repeatable checks, smoke tests, fixtures, scripts, commands, or validation matrices.
- **Maintainability**: structure is modular, low-duplication, easy to update, and resilient to future changes.
- **Token efficiency**: achieves the goal with minimal necessary words while preserving correctness, safety, and usability.

Default weighting is equal. Change weights only if the user provides priority or if the artifact’s stated purpose makes one category dominant; state that change explicitly.

## 3. Analysis Method

For each version:

1. Read the complete relevant file set, not only filenames or summaries.
2. Extract the version’s intent, mechanism, constraints, output shape, validation behavior, and obvious assumptions.
3. Compare against the rubric with concrete evidence. Use short source references: path, heading, function name, line number if available, or concise quoted fragment.
4. Record strengths, weaknesses, best use case, failure mode, and score per category.
5. Penalize hidden ambiguity, unsupported claims, missing safety behavior, untestable guidance, duplicated/conflicting instructions, excessive length, and weak handoff.
6. Reward executable sequencing, explicit precedence, exact-token preservation, validation hooks, clear outputs, compactness without loss, and compatibility with prior useful behavior.

Do not let newer version numbers bias scores. Do not assume “longer” means safer or “shorter” means better. A version scores higher only when it preserves required behavior more reliably.

## 4. Comparative Output

Produce a score matrix with all versions and categories. Include:

- scoring scale definition;
- category scores and overall score;
- short rationale for each version;
- cross-version ranking;
- decisive tradeoffs;
- final recommendation for the best existing version.

Overall score should usually be the mean of category scores. If weights differ, show the formula.

## 5. Synthesis Method

After analysis is complete, synthesize a successor that aims to beat every input version in every category.

Synthesis rules:

1. Preserve the best proven behavior from all versions.
2. Remove duplicate, decorative, stale, contradictory, or example-only material unless examples are necessary for execution.
3. Convert long explanations into compact operational rules.
4. Add missing guardrails only when they improve real execution, validation, or safety.
5. Keep compatibility with valuable legacy behaviors unless they conflict with the improved design.
6. Prefer one clear precedence ladder over repeated warnings.
7. Prefer reusable output shapes over prose instructions.
8. Include a lightweight validation harness so the new version is testable.
9. Optimize for minimum tokens after correctness, safety, scope, and auditability are preserved.
10. Do not claim superiority unless the synthesized version demonstrably addresses the weaknesses found in analysis.

## 6. Best-Practice Structure for Synthesized Skill

Use this structure unless the target artifact requires another format:

1. Metadata: name, version, one-sentence purpose.
2. Activation / applicability: when to use, when not to use.
3. Priority ladder: what wins when constraints conflict.
4. Operating procedure: ordered steps that can be executed.
5. Guardrails: safety, ambiguity, protected tokens, refusal or fallback behavior.
6. Evidence and validation: how to prove claims and test outputs.
7. Output shapes: compact templates for common tasks.
8. Handoff / audit: what status, assumptions, paths, and next actions to preserve.
9. Maintenance rule: how future edits should avoid duplication and regressions.
10. Quality gate: final checklist before responding or saving.

## 7. Validation Harness

Run or define a small harness appropriate to the artifact:

- inventory check: all candidate versions included, metadata ignored;
- coverage check: every rubric category scored for every version;
- evidence check: each major criticism or praise has source support;
- regression check: synthesized version retains best unique capabilities from prior versions;
- conflict check: no duplicated or contradictory rules;
- token check: synthesized version is no longer than necessary and ideally shorter than bloated predecessors;
- execution check: a fresh reader can apply it without asking for hidden context.

When code, configs, or scripts are involved, add commands that can be run repeatedly. When text or prompts are involved, use scenario fixtures instead of pretending there is executable test coverage.

## 8. Final Response Contract

Keep analysis and synthesis visibly separate.

Return, in this order:

1. workspace / files inspected;
2. score matrix;
3. per-version analysis;
4. best existing version;
5. synthesized successor;
6. validation notes;
7. saved file links, if files were created.

Be direct. Do not include alternative designs unless the user asks. Give the best answer, with enough evidence to audit it and enough compression to stay usable.
