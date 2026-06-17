---
name: realitybench-caseforge
description: objective - accepted successor synthesized by best-version-builder from measured variant gaps
version: 1.1.0
last_updated: 2026-06-17
---

# RealityBench CaseForge — Production Synthesis


## Activation and Non-Goals
Use this skill when asked to synthesize, repair, validate, benchmark, score, or package benchmark cases for prompts, agents, models, APIs, apps, workflows, retrieval systems, document pipelines, or other systems. Do not use it to create toy examples, marketing demos, or cases that cannot be loaded by the evaluator.

A released case must be realistic, source-grounded, format-valid, globally differentiable, first-shot-ready, objectively scoreable, and decision-relevant. If any property is unknown, label the suite exploratory and lower the validity claim.

## Mandatory Operating Order
1. Define the benchmark claim and decision use.
2. Identify target population, exclusions, and representation debt.
3. Discover the evaluator format, runner entrypoint, parser constraints, scoring inputs, and scoring outputs.
4. Build the source ledger and admissibility map.
5. Extract task anatomy and causal skeleton.
6. Construct or transform cases inside the mutation budget.
7. Seal the oracle away from the stimulus.
8. Preflight without consuming the real attempt.
9. Check realism, anti-synthetic risk, pairwise distance, coverage debt, oracle quality, diagnostic capture, and validity scores.
10. Package a ready-to-test bundle with manifest, fixtures, scorer, adapter if needed, checksums, limitations, and run status.

## Validity Hierarchy
Prefer direct real traces, sanitized real traces, and lightly mutated real traces. Composite real-derived cases are allowed with provenance and causal-skeleton documentation. Expert-modeled synthetic gap cases are capped at 10% for ranking suites. Toy, keyword, benchmark-shaped, ungrounded, or answer-leaking cases are invalid.

## Minimum Case Contract
Each case records id, title, category, difficulty, validity_tier, source_ids, benchmark claim alignment, format_fit, realism, initial_state, stimulus, expected_behavior, oracle, scoring, readiness, diagnostics, and known limitations. Use native evaluator format when known; otherwise use a neutral adapter that only translates format and does not alter semantics.

## Executable Sequence
Run as a checklist. Stop on blockers instead of guessing. A blocker is any unknown required field, unloadable format, ambiguous scoring output, missing fixture, unsealed oracle, prohibited side effect, unavailable dependency, or case that requires the real run to discover whether it can load. Prefer direct commands, concrete file paths, explicit pass/fail gates, and one output bundle.

## Output Contract
Return a suite manifest, case files, fixture files, source ledger, oracle metadata hidden from the system under test, scoring rubric or executable scorer, runner instructions, checksums, preflight result, and a score matrix. Every saved path must be preserved exactly and marked created, reused, ignored, or not run.

## Claim Map and Scope Discipline
Before generation, write a benchmark_claim_map with system_under_test, evaluation_goal, decision_use, deployment_or_usage_claim, target_population, excluded_populations, representation_debt, validity risk budget, and forbidden claims. If target population or evaluator contract is undefined, create only an exploratory suite. Do not claim production readiness, global superiority, compliance sufficiency, or domain-general superiority without real anchors and release gates.

## Coverage Model
Cover actor, task family, domain, language/locale, artifact family, environment, risk level, interaction length, error/noise profile, expected decision, oracle type, and failure mechanism. Sibling cases from the same skeleton are capped unless declared metamorphic tests.

## Guardrails and Refusal/Fallback
Reject or quarantine cases with no source ledger, vague expert intuition, hidden answer leakage, benchmark vocabulary in the stimulus, keyword shortcuts, symmetric toy artifacts, no consequence, subjective oracle scored as objective, near-duplicate skeletons, prohibited credentials/network/destructive actions, or hidden facts unavailable to the system. For safety-sensitive work, include must_refuse, must_comply_safely, must_redirect, must_not_over_refuse, privacy-preserving, prompt-injection, and secret-handling cases. When ambiguity is material, ask only for the missing contract; otherwise mark assumptions and cap the claim.

## Precedence
Native evaluator schema, runner code, existing accepted fixtures, CI scripts, and scoring outputs outrank prose preference. System/developer safety rules outrank user convenience. Oracle sealing outranks readability. Realism and objective scoring outrank case quantity.

## Evidence and Validation
Every realism claim is tied to a source ledger entry with validity tier, source type, acquisition mode, timeframe, population, observed/measured/inferred/assumed fields, preserved and transformed properties, inadmissible claims, and final admissibility. Use claim tags: observed, measured, inferred, assumed, external-cited, external-unverified, not-evaluated.

Preflight using schema validation, static parsing, dry-load in a clone, checksum verification, fixture path inspection, dependency inspection, oracle consistency check, scorer linting, adapter round-trip, sandbox smoke test, or manual contract review. Never claim a command ran, artifact existed, API behaved, or source passed unless verified.

## Handoff and Audit Ledger
Preserve paths, assumptions, decisions, rejected risks, validation run/not run status, next action, checksums, and release gate result. Create run_manifest.json, candidate or case inventory CSV, evidence_ledger.csv, score_matrix.csv, row_results.jsonl, iteration_log.csv when variants are synthesized, and correction_audit.csv when challenged. Prose, matrices, ledgers, and manifests must agree.

## Release Status
Mark each bundle ready, exploratory_only, quarantine, or reject. Ready requires explicit claim/decision use, known or safely adapted evaluator contract, source-ledger coverage, objective oracle, format validation, first-shot readiness, sealed oracle, differentiability, synthetic gap budget compliance, zero critical failures, and reported limitations.

## Repeatable Harness
When a benchmark runner is absent, ship a neutral fixture harness: fixtures.jsonl, adapter.py, validate_cases.py, score_cases.py, and run_matrix.py. Commands must emit CSV or JSONL rows with case_id, category, difficulty, validity_tier, source_ids, locale, artifact_type, expected_decision, oracle_type, performance_score, pass flag, critical_failure, validity sub-scores, validity_weighted_score, failure_class, token estimate, and notes.

Recommended smoke commands:
```bash
python scripts/validate_cases.py cases/ fixtures/ --dry-load
python scripts/score_cases.py cases/ outputs/ --matrix results/score_matrix.csv
python scripts/recompute_rank.py results/row_results.jsonl
```
Validation must be rerunnable without consuming the real attempt.

## Maintainability Rules
Use modular sections: identity, activation, target map, evaluator contract, source ledger, task anatomy, causal skeleton, construction, oracle sealing, validation, sampling, LLM extension, scoring, harness, audit, release gates. Avoid duplicate rules; use one priority ladder and one score formula. Preserve legacy behavior unless explicitly deprecated for safety or target mismatch. Store schemas and rubrics so new case types extend the benchmark without rewriting old cases.

## Token Discipline
Minimize words only after correctness, safety, scope, evidence, validation, audit, and localization are preserved. Prefer compact tables, schemas, and checklists over repeated explanations. Do not delete release gates, source-ledger requirements, oracle sealing, validation-tier honesty, safety boundaries, or handoff fields to save tokens. Track estimated input, output, fixture, and scoring-token cost separately from effectiveness.

## Language, Tone, Locale
Use direct operational language. Preserve exact code, logs, paths, identifiers, error strings, dates, units, currencies, legal/business conventions, domain terms, and user-provided language. For multilingual benchmarks, state whether success requires same-language response, translation, localization, cross-lingual retrieval, or culturally correct interpretation. Use concise, precise wording; expand only when ambiguity, safety, validation, or audit requires it.

## LLM Evaluation Extension
When the system under test is an LLM, prompt, agent, RAG system, tool-using assistant, coding assistant, evaluator judge, or model-mediated workflow, record model/system type, interaction mode, controls, output contract, scorer/judge type, deployment risks, run policy, allowed variance, tool contract, retrieval assumptions, context pressure, refusal boundary, hallucination risk, judge risk, and token-cost pressure.

LLM cases must cover materially different behaviors: instruction following, ambiguity handling, evidence grounding, retrieval, tool use, code reasoning, mathematical reasoning, transformation fidelity, summarization fidelity, long-context selection, multi-turn state, planning, safety/refusal boundaries, privacy, multilingual/locale handling, output-format discipline, self-correction, error recovery, and cost discipline. Score observable outputs and evidence, never private chain-of-thought.

## Scoring
Use performance and validity scores. Performance defaults: outcome correctness 25, evidence quality 15, artifact/action correctness 15, constraint compliance 15, oracle requirements 15, safety/failure handling 10, efficiency/cost 5. Validity sub-scores: non-synthesized closeness, source grounding, format validity, first-shot readiness, oracle quality, global differentiability, calibration, and decision relevance. For LLMs add prompt sensitivity, stochasticity handling, context fidelity, hallucination resistance, tool protocol validity, safety boundary, multilingual locale, judge reliability, and cost realism. Overall validity is the minimum applicable sub-score.

## Final Rule
A case is benchmark-grade only when an evaluator can determine from the initial state and stimulus whether the system performed the required real-world capability and whether that result can be trusted for the stated decision.

## Validation Tier and Claim Caps
Classify results before scoring: T0 source inspection only capped as structural/proxy, T1 fixed fixtures plus deterministic scoring, T2 repeated live model/API calls with variance notes, and T3 qualified independent human review. Do not imply live behavior from T0/T1. Recompute ranks from raw rows and report sensitivity to weights, objective, estimator, and fixture coverage.

## Correction Protocol
When challenged, reopen sources, recompute raw rows, publish old score, corrected score, delta, mistaken assumption, affected categories, obsolete conclusion, corrected recommendation, validation tier, remaining uncertainty, and corrected artifact paths.

## Fixture Benchmark Protocol
Use identical fixtures, weights, formula, estimator, validation tier, pass/fail criteria, and relevance labels for all variants. Store row_results.jsonl and recompute_rank.py, then accept a successor only if production improves by at least 0.05 or fixes a high-severity failure without regression.
