---
name: benchmark-dataset-builder
description: Build large, diverse, auditable benchmark datasets and measurement harnesses for evaluating prompts, skills, specs, agents, or candidate versions across scenarios, languages, contexts, and risk levels.
version: 1.0.0
--------------

# Benchmark Dataset Builder

## Contract

When active, this skill MUST create or evaluate a benchmark in a way that is reproducible, auditable, and apples-to-apples across all candidates. It must distinguish dataset generation, measurement, synthesis, and final recommendation. Do not claim a candidate is “best” unless it was measured against the full benchmark pool.

## Inputs

Required:

* target artifact type: prompt, skill, spec, agent, policy, workflow, code, or document
* candidate set or base artifact
* benchmark goal
* minimum sample count

Optional:

* languages/scripts
* scenario types
* context/background profiles
* risk levels
* scoring categories
* weighting formula
* pass/fail criteria
* output formats
* live-model/API availability
* workspace path

## Activate Only When

The user asks to benchmark, stress-test, evaluate, compare, score, generate fixtures, build a dataset, run a harness, measure multilingual behavior, retest candidates, or validate a “best” version.

## Do Not Use For

* unsupported claims of model quality without measurement
* unverifiable rankings
* hidden or inconsistent scoring
* benchmarks where different candidates receive different inputs, scoring rules, or weights
* synthetic multilingual benchmarks that pretend to be certified human translations
* unsafe benchmark content that operationalizes harmful, illegal, or abusive behavior

## Required Workflow

### 1. Intake / Workspace

1. Preserve source candidates unchanged.
2. Create generated artifacts in a separate workspace.
3. Inventory:

   * candidate name/version/path
   * artifact type
   * comparison unit
   * size/token estimate
   * declared purpose
   * known constraints
4. State ignored metadata/noise, if any.

### 2. Benchmark Design

Define before generation:

* sample count
* scenario types
* context/background profiles
* language/script coverage, if multilingual
* risk levels
* expected behavior labels
* scoring categories
* weights
* combined-score formula
* validation limits

Default scoring categories, 0–10:

* Clarity / executability
* Intent / scope
* Guardrails
* Evidence / validation
* Handoff / audit
* Scripts / harnesses
* Maintainability
* Token efficiency
* Language / tone / localization

Suggested combined formula:

`combined = effectiveness_score - cost_penalty + coverage_bonus - regression_penalty`

The formula must be defined once and applied consistently to every candidate.

### 3. Dataset Generation

Generate at least the user-requested sample count.

Each sample should include:

* `sample_id`
* `language`
* `script`
* `scenario_type`
* `background_profile`
* `risk_level`
* `topic`
* `input`
* `expected_behavior`
* `evaluation_tags`
* `language_integrity_note`
* `source_or_generation_note`

For multilingual benchmarks:

1. The entire `input` must be in the declared language/script.
2. Do not translate only keywords, labels, or topics.
3. Request, context, constraints, audience, style, and scenario details must all match the declared language.
4. Proper nouns, code, filenames, URLs, and unavoidable technical terms may remain unchanged.
5. Add a language-integrity proxy check.
6. Clearly state that synthetic prompts are not certified human translations unless qualified review was performed.

### 4. Coverage Requirements

Include normal, edge, adversarial, and format-sensitive cases.

Recommended scenario coverage:

* normal request
* missing topic
* nonessential ambiguity
* high-stakes medical
* high-stakes legal
* high-stakes financial
* safety-critical
* coercive/manipulative request
* deceptive request
* guaranteed-outcome request
* sourced-claim request
* fixed-format request
* audit/footer request
* protected-token scan
* multilingual/localization request
* long background/constraints request
* conflicting constraints
* regression-from-legacy-behavior case

Recommended background profiles:

* student
* parent/caregiver
* small-business owner
* nonprofit/team lead
* job seeker
* traveler/newcomer
* technical/project worker
* personal planning
* educator/trainer
* customer/support role

### 5. Measurement Harness

Run every candidate against every sample using the same:

* inputs
* scoring rubric
* weights
* token/cost estimator
* pass/fail criteria
* language-integrity checks
* failure-mode taxonomy

For each candidate/sample row, record:

* candidate
* sample_id
* language/script
* scenario_type
* risk_level
* expected behavior
* category scores
* pass/fail
* token estimate
* cost penalty
* coverage bonus
* regression penalty
* combined score
* failure notes

If deterministic heuristics are used instead of live model/API calls, label the result as a deterministic proxy benchmark. Do not imply live-call accuracy.

### 6. Synthesis Gate

If the benchmark exposes fixable weaknesses:

1. Synthesize one successor candidate.
2. Preserve proven behavior from the strongest candidates.
3. Add only rules that improve execution, safety, validation, auditability, language handling, or maintainability.
4. Remove decorative, duplicate, stale, or conflicting rules.
5. Retest the successor against the full benchmark pool.
6. Recommend it only if it beats the best existing candidate under the same formula.

### 7. Output Artifacts

Save:

* benchmark report Markdown
* dataset JSONL
* dataset CSV
* full candidate-sample result matrix CSV
* candidate summary CSV
* by-language summary CSV, if multilingual
* by-scenario summary CSV
* by-risk-level summary CSV
* failure modes CSV
* language-integrity report CSV, if multilingual
* benchmark config JSON
* reproducible harness script
* synthesized successor file, if created
* ZIP bundle of all artifacts

### 8. Validation / Audit

Final report must include:

* workspace and files inspected
* candidates and comparison unit
* benchmark size
* coverage dimensions
* scoring scale, weights, and formula
* top score matrix
* best existing version before synthesis
* synthesized successor, if any
* measured retest result
* validation run/not run
* deterministic vs live benchmark status
* known limits
* saved artifact links

## Style

Be direct, structured, and audit-ready. Prefer tables, CSV/JSON outputs, stable formulas, and explicit limits over prose claims. Do not overstate benchmark validity.
