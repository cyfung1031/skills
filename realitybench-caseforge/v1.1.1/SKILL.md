---
name: realitybench-caseforge
description: Generates source-grounded, format-fit, first-shot-ready benchmark cases and evaluation suites with explicit source-ledger, oracle-sealing, global-differentiability, validation-tier, LLM-evaluation, and release-gate controls.
version: 1.1.1
last_updated: 2026-06-18
---

# RealityBench CaseForge

## Identity
RealityBench CaseForge creates benchmark cases that are close enough to real-world evaluation to support a stated decision and exact enough to load, run, and score in the target evaluator on the first permitted attempt.

A released case must be realistic, source-grounded, format-valid, globally differentiable, first-shot-ready, objectively scoreable, and decision-relevant. If any required property is unknown, mark the suite `exploratory_only` and cap the claim.

## Activation and Non-Goals
Use this skill when asked to synthesize, repair, validate, benchmark, score, compare, or package benchmark cases for prompts, agents, models, APIs, apps, workflows, retrieval systems, document pipelines, or other evaluable systems.

Do not use it to create toy examples, marketing demos, schema-invalid samples, answer-leaking prompts, or cases that require trial-and-error against the real evaluator to discover whether they can load.

## Mandatory Operating Order
1. Define the benchmark claim, decision use, and forbidden claims.
2. Identify target population, exclusions, representation debt, and validity risk budget.
3. Discover the evaluator contract: schema, runner entrypoint, parser constraints, fixture paths, scoring inputs, scoring outputs, side effects, and accepted examples.
4. Build the source ledger and admissibility map.
5. Extract real task anatomy and causal skeleton.
6. Write the sampling plan, calibration anchors, and fixture split policy.
7. Select coverage axes and differentiability targets.
8. Construct, sanitize, composite, or mutate cases inside the mutation budget.
9. Seal oracle data away from the stimulus and system under test.
10. Audit leakage, shortcuts, memorization risk, and trivial-baseline passability.
11. Preflight without consuming the real attempt.
12. Score realism, anti-synthetic risk, pairwise distance, coverage debt, oracle quality, diagnostic capture, and release readiness.
13. Package a ready-to-test bundle with manifest, cases, fixtures, scorer or rubric, adapter if needed, checksums, limitations, validation tier, and run status.

## Precedence
Native evaluator schema, runner code, existing accepted fixtures, CI scripts, and scoring outputs outrank prose preference. System/developer safety rules outrank user convenience. Oracle sealing outranks readability. Realism and objective scoring outrank case quantity. Verified evidence outranks plausible explanation.

## Claim Map and Scope Discipline
Before generation, write `benchmark_claim_map` with:

```yaml
system_under_test:
evaluation_goal:
decision_use:
deployment_or_usage_claim:
target_population:
excluded_populations:
representation_debt:
validity_risk_budget:
forbidden_claims:
required_validation_tier:
release_status:
```

If target population, evaluator contract, oracle, or sources are undefined, create only an exploratory suite. Do not claim production readiness, global superiority, compliance sufficiency, or domain-general superiority without real anchors and release gates.

## Evaluator Contract Discovery
Treat evaluator compatibility as a validity requirement, not a formatting afterthought. Inspect, in order:

1. Native schema or type definitions.
2. Runner entrypoint, CLI flags, environment variables, and working directory assumptions.
3. Parser constraints: required fields, optional fields, enums, escaping, file encodings, line formats, token limits, attachment handling, and path rules.
4. Existing accepted fixtures and rejected fixtures.
5. CI scripts, validators, scorer code, adapters, and output examples.
6. Scoring inputs, scoring outputs, aggregation rules, failure classes, and tie-breaking.
7. Side-effect boundaries: network, credentials, filesystem writes, destructive actions, rate limits, and external dependencies.

Record unresolved fields as blockers unless a neutral adapter can translate format without changing semantics.

## Validity Hierarchy
Prefer direct real traces, sanitized real traces, and lightly mutated real traces. Composite real-derived cases are allowed only with provenance and causal-skeleton documentation. Expert-modeled synthetic gap cases are capped at 10% for ranking suites. Toy, keyword-shaped, benchmark-shaped, ungrounded, symmetric, no-consequence, or answer-leaking cases are invalid.

## Source Ledger and Admissibility Map
Every realism claim must be tied to a source-ledger entry. Each entry records:

```yaml
source_id:
validity_tier: direct_real | sanitized_real | lightly_mutated_real | composite_real_derived | expert_modeled_gap | invalid
source_type:
acquisition_mode:
timeframe:
population:
observed_fields:
measured_fields:
inferred_fields:
assumed_fields:
preserved_properties:
transformed_properties:
redactions_or_sanitization:
inadmissible_claims:
allowed_case_uses:
final_admissibility:
```

Use claim tags: `observed`, `measured`, `inferred`, `assumed`, `external-cited`, `external-unverified`, and `not-evaluated`. Never upgrade an inferred or assumed field into an observed fact.

## Real Task Anatomy
Extract the practical structure that makes the case real:

```yaml
actor:
intent:
stakes_or_consequence:
domain_context:
initial_state:
available_information:
hidden_information:
artifact_state:
constraints:
ambiguities:
noise_or_error_profile:
required_decision_or_action:
observable_success_signal:
plausible_failure_modes:
```

A case without actor intent, constraints, state, and consequence is usually not benchmark-grade.

## Causal Skeleton and Mutation Budget
Represent each case as a causal skeleton:

```yaml
trigger:
context_dependencies:
necessary_evidence:
reasoning_or_action_path:
decision_boundary:
expected_behavior:
failure_mechanism:
oracle_basis:
```

Mutations may alter names, dates, quantities, locale, format, order, surface wording, noise level, or non-causal distractors only when the expected behavior and oracle remain causally valid. Mutations must not introduce impossible states, remove required evidence, leak answers, or create shortcuts.

## Coverage Model
Cover actor, task family, domain, language/locale, artifact family, environment, risk level, interaction length, error/noise profile, expected decision, oracle type, and failure mechanism. Include easy, medium, hard, adversarial, and regression-protection cases when justified by the claim. Sibling cases from the same skeleton are capped unless declared metamorphic tests.

## Sampling, Calibration, and Fixture Design
Create a `sampling_plan` before writing cases. It records claim dimensions, target proportions, minimum boundary cases, excluded populations, known source gaps, fixture count, split policy, and calibration anchors. Do not fill a matrix cell with a synthetic placeholder unless it is marked `expert_modeled_gap` and counted against the synthetic budget.

Every ranking suite should include:

- ordinary cases that represent the target population;
- boundary cases near the decision threshold;
- negative cases where the system should not act or should abstain;
- adversarial or noisy cases only when the deployment claim includes such pressure;
- regression cases for capabilities that previous systems often break;
- calibration anchors with obvious pass/fail outcomes to detect scorer drift.

Separate development, calibration, and held-out fixtures when the evaluator will be tuned. If only one fixture set exists, label the result fixture-bounded and do not claim generalization.

## Leakage, Shortcut, and Memorization Checks
Before release, perform a shortcut audit. Flag cases where the answer can be obtained from filenames, ordering, IDs, repeated wording, benchmark-specific phrases, source metadata, category labels, hidden oracle leakage, or distribution artifacts rather than the intended capability.

Use at least one of these checks when feasible: remove surface keywords, shuffle order, perturb non-causal fields, mask category labels, test a distractor-only variant, or compare against a trivial baseline. If a trivial baseline can pass, quarantine or rewrite the case. Record `shortcut_risk`, `leakage_channel`, `mitigation`, and `residual_risk` in the case inventory.

## Global Differentiability Machinery
A suite must differentiate cases globally, not just look varied. Build a `differentiability_matrix` with one row per case and columns for:

```text
case_id, source_cluster, skeleton_id, actor, task_family, domain, locale, artifact_type,
risk_level, interaction_length, noise_profile, required_capability, expected_decision,
oracle_type, failure_mechanism, surface_form, distractor_type, safety_boundary,
tool_or_retrieval_dependency, scoring_dimension
```

Compute or manually assess pairwise distance across semantic and operational axes. Flag near-duplicates when cases share the same source cluster, skeleton, expected decision, oracle type, and failure mechanism, even if wording differs.

Release gates:

- No more than 20% of ranking cases may share the same source cluster unless the benchmark claim is cluster-specific.
- No more than 15% may share the same causal skeleton unless marked as metamorphic variants.
- Every primary claim dimension must have at least one positive, one negative, and one boundary case where applicable.
- Each added case must improve coverage, calibration, regression protection, or failure localization.
- Pairwise-distance debt must be reported with accepted exceptions.

## Minimum Case Contract
Each case records:

```yaml
id:
title:
category:
difficulty:
validity_tier:
source_ids:
benchmark_claim_alignment:
format_fit:
realism:
task_anatomy:
causal_skeleton:
initial_state:
stimulus:
expected_behavior:
oracle:
scoring:
readiness:
diagnostics:
differentiability_tags:
known_limitations:
shortcut_risk:
leakage_channel:
residual_risk:
```

Use the native evaluator format when known. Otherwise, provide a neutral adapter that only translates representation and does not alter semantics.

## Construction Rules
Construct cases from sources by preserving causal structure first, evaluator format second, and surface realism third. Keep hidden facts unavailable to the system out of the stimulus. Add distractors only when they occur naturally in the task family or test a stated capability. For multilingual cases, preserve script, locale, register, code-switching, units, currencies, legal/business conventions, and culturally required interpretation.

## Oracle Sealing
The oracle must be stored outside the prompt, input artifact, retrieval corpus visible to the system, and any metadata the system can inspect. Record oracle basis, required evidence, allowed equivalent outputs, disallowed shortcuts, scoring tolerances, and abstention policy. If the oracle is subjective, score it as rubric-based rather than objective.

## Guardrails and Refusal/Fallback
Reject or quarantine cases with no source ledger, vague expert intuition, hidden answer leakage, benchmark vocabulary in the stimulus, keyword shortcuts, symmetric toy artifacts, no consequence, subjective oracle scored as objective, near-duplicate skeletons, prohibited credentials/network/destructive actions, or hidden facts unavailable to the system.

For safety-sensitive work, include `must_refuse`, `must_comply_safely`, `must_redirect`, `must_not_over_refuse`, privacy-preserving, prompt-injection, and secret-handling cases. When ambiguity is material, ask only for the missing contract; otherwise mark assumptions and cap the claim.

## Evidence and Validation
Preflight using schema validation, static parsing, dry-load in a clone, checksum verification, fixture path inspection, dependency inspection, oracle consistency check, scorer linting, adapter round-trip, sandbox smoke test, or manual contract review. Never claim a command ran, artifact existed, API behaved, source passed, or fixture loaded unless verified.

Validation must be rerunnable without consuming the real attempt.

## Validation Tier and Claim Caps
Classify results before scoring:

| Tier | Basis | Claim cap |
|---|---|---|
| T0 | Source and package inspection only | structural/proxy only |
| T1 | Fixed fixtures plus deterministic scoring | fixture-bounded behavior |
| T2 | Repeated live model/API calls with variance notes | measured live behavior within run policy |
| T3 | Qualified independent human review | externally reviewed validity |

Do not imply live behavior from T0/T1. Recompute ranks from raw rows and report sensitivity to weights, objective, estimator, and fixture coverage.

## Repeatable Harness
When a benchmark runner is absent, ship a neutral fixture harness:

```text
fixtures.jsonl
scripts/adapter.py
scripts/validate_cases.py
scripts/score_cases.py
scripts/run_matrix.py
scripts/recompute_rank.py
```

Commands must emit CSV or JSONL rows with case_id, category, difficulty, validity_tier, source_ids, locale, artifact_type, expected_decision, oracle_type, performance_score, pass flag, critical_failure, validity sub-scores, validity_weighted_score, failure_class, token estimate, and notes.

Recommended smoke commands:

```bash
python scripts/validate_cases.py cases/ fixtures/ --dry-load
python scripts/score_cases.py cases/ outputs/ --matrix results/score_matrix.csv
python scripts/recompute_rank.py results/row_results.jsonl
```

## Executable Bundle Schema
When no native package format exists, emit this bundle tree exactly unless the user requests another layout:

```text
benchmark_bundle/
  manifest.json
  cases/
  fixtures/
  sources/source_ledger.csv
  oracles/oracle_metadata.jsonl
  results/score_matrix.csv
  results/row_results.jsonl
  results/differentiability_matrix.csv
  scripts/validate_cases.py
  scripts/score_cases.py
  scripts/recompute_rank.py
  CHECKSUMS.sha256
  LIMITATIONS.md
```

`manifest.json` must record benchmark claim, release status, validation tier, fixture count, source count, oracle storage path, evaluator contract, scoring formula, excluded claims, run commands, and checksum file. `LIMITATIONS.md` must list unsupported populations, weak source regions, synthetic gap cases, unvalidated dependencies, and claim caps in plain language.

## Failure Taxonomy and Recomputable Results
Use stable failure labels so results are comparable across runs: `format_error`, `load_error`, `source_gap`, `oracle_leak`, `oracle_ambiguity`, `near_duplicate`, `shortcut_pass`, `coverage_gap`, `unsafe_case`, `scorer_error`, `adapter_error`, `dependency_missing`, `claim_overreach`, and `not_run`.

A recomputable result packet stores raw row outcomes before prose summaries. Rank from rows, not narrative. If a row is excluded, record `exclusion_reason` and whether exclusion happened before or after seeing the system output. Do not change row weights after inspecting outputs unless the run is explicitly labeled exploratory and rerun with fixed weights.

## Scoring
Use performance and validity scores.

Performance defaults:

| Dimension | Weight |
|---|---:|
| outcome correctness | 25 |
| evidence quality | 15 |
| artifact/action correctness | 15 |
| constraint compliance | 15 |
| oracle requirements | 15 |
| safety/failure handling | 10 |
| efficiency/cost | 5 |

Validity sub-scores: non-synthesized closeness, source grounding, format validity, first-shot readiness, oracle quality, global differentiability, calibration, and decision relevance. For LLMs add prompt sensitivity, stochasticity handling, context fidelity, hallucination resistance, tool protocol validity, safety boundary, multilingual locale, judge reliability, and cost realism. Overall validity is the minimum applicable sub-score unless the benchmark contract explicitly defines a stricter aggregation rule.

## LLM Evaluation Extension
When the system under test is an LLM, prompt, agent, RAG system, tool-using assistant, coding assistant, evaluator judge, or model-mediated workflow, record model/system type, interaction mode, controls, output contract, scorer/judge type, deployment risks, run policy, allowed variance, tool contract, retrieval assumptions, context pressure, refusal boundary, hallucination risk, judge risk, and token-cost pressure.

LLM cases must cover materially different behaviors: instruction following, ambiguity handling, evidence grounding, retrieval, tool use, code reasoning, mathematical reasoning, transformation fidelity, summarization fidelity, long-context selection, multi-turn state, planning, safety/refusal boundaries, privacy, multilingual/locale handling, output-format discipline, self-correction, error recovery, and cost discipline. Score observable outputs and evidence, never private chain-of-thought.

## Handoff and Audit Ledger
Preserve paths, assumptions, decisions, rejected risks, validation run/not run status, next action, checksums, and release-gate result. Create `run_manifest.json`, `case_inventory.csv`, `evidence_ledger.csv`, `score_matrix.csv`, `row_results.jsonl`, `differentiability_matrix.csv`, `sampling_plan.yaml`, `shortcut_audit.csv`, `iteration_log.csv` when variants are synthesized, and `correction_audit.csv` when challenged. Prose, matrices, ledgers, and manifests must agree.

Every saved path must be marked `created`, `reused`, `ignored`, or `not_run`.

## Output Contract
Return a suite manifest, case files, fixture files, source ledger, differentiability matrix, oracle metadata hidden from the system under test, scoring rubric or executable scorer, runner instructions, checksums, preflight result, validation tier, release status, limitations, and score matrix.

## Release Status
Mark each bundle `ready`, `exploratory_only`, `quarantine`, or `reject`.

`ready` requires explicit claim/decision use, known or safely adapted evaluator contract, source-ledger coverage, objective or properly rubric-scored oracle, format validation, first-shot readiness, sealed oracle, differentiability, synthetic gap budget compliance, zero critical failures, reported limitations, and checksum/audit consistency.

## Baselines, Ablations, and Sensitivity Checks
When measuring a suite, include lightweight baselines where feasible: schema-only loader, trivial majority or constant answer, keyword matcher, retrieval-only answer, random-choice baseline for closed tasks, and previous accepted suite. A benchmark is weak if a baseline performs near the target system for reasons unrelated to the intended capability.

Run ablations that remove or mask non-causal cues, category labels, source order, filenames, and distractors. Record whether the expected decision changes. If removing a non-causal cue changes the oracle, the case is not causally stable.

For close decisions, report sensitivity to fixture subset, scorer weights, validity tier, source cluster dominance, locale mix, difficulty mix, and oracle tolerance. Label the recommendation margin-sensitive when rank changes under reasonable perturbations.

## Internal Review Gate
Before final handoff, run a compact adversarial review against the bundle:

1. What hidden assumption would invalidate the benchmark claim?
2. Which source cluster, locale, actor type, or task family dominates the suite?
3. Could a trivial baseline, memorized pattern, or label shortcut pass?
4. Are any oracle facts visible to the system under test?
5. Would changing the scorer weight, fixture split, validation tier, or source mix reverse the recommendation?
6. Do manifest, ledgers, matrices, checksums, limitations, and prose make the same claim?

If any answer exposes a critical issue, mark `quarantine` or `exploratory_only`; do not bury it as a limitation while claiming `ready`.

## Fixture Benchmark Protocol
Use identical fixtures, weights, formula, estimator, validation tier, pass/fail criteria, and relevance labels for all variants. Store `row_results.jsonl` and `recompute_rank.py`, then accept a successor only if production improves by at least 0.05 or fixes a high-severity failure without regression.

## Correction Protocol
When challenged, reopen sources, recompute raw rows, publish old score, corrected score, delta, mistaken assumption, affected categories, obsolete conclusion, corrected recommendation, validation tier, remaining uncertainty, and corrected artifact paths.

## Maintainability Rules
Use modular sections: identity, activation, target map, evaluator contract, source ledger, task anatomy, causal skeleton, construction, oracle sealing, validation, sampling, LLM extension, scoring, harness, audit, and release gates. Avoid duplicate rules; use one priority ladder and one score formula. Preserve legacy behavior unless explicitly deprecated for safety or target mismatch. Store schemas and rubrics so new case types extend the benchmark without rewriting old cases.

## Token Discipline
Minimize words only after correctness, safety, scope, evidence, validation, audit, and localization are preserved. Prefer compact tables, schemas, and checklists over repeated explanations. Do not delete release gates, source-ledger requirements, oracle sealing, validation-tier honesty, safety boundaries, differentiability checks, or handoff fields to save tokens. Track estimated input, output, fixture, and scoring-token cost separately from effectiveness.

## Language, Tone, Locale
Use direct operational language. Preserve exact code, logs, paths, identifiers, error strings, dates, units, currencies, legal/business conventions, domain terms, and user-provided language. For multilingual benchmarks, state whether success requires same-language response, translation, localization, cross-lingual retrieval, or culturally correct interpretation.

## Final Rule
A case is benchmark-grade only when an evaluator can determine from the initial state and stimulus whether the system performed the required real-world capability, why the oracle is valid, how the case differs from the rest of the suite, and whether the result can be trusted for the stated decision.
