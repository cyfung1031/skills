---
name: agent-readability-review
description: Revises operational text so agents act correctly with minimal wording while preserving intent, safeguards, protected tokens, evidence, and audit semantics.
version: 1.2.0
---

# Skill: Agent Readability Review

## Purpose

Revise operational text for agents, automations, validators, reviewers, scripts, CI, or human-agent teams.

Goal: **minimum sufficient executability**: shortest wording that preserves correct behavior, safety, protected tokens, evidence, handoff meaning, and maintainability.

Do wording-level work only: clarify, compress, reorder, or restore existing meaning. Do not invent requirements, workflows, roles, validators, scoring rubrics, artifacts, external facts, citations, tool access, or behavior. Rewrite only when wording can cause wrong action, unsafe assumption, lost safeguard, noisy output, validation gap, format drift, token damage, or maintenance error.

Success means the reader can identify: action, trigger, input/source/evidence, output/state/file/format, exact tokens, fallback, priority, verification, completion proof, and open/closed status.

## Use / Do Not Use

Use for skills, prompts, workflow rules, SOPs, templates, tool instructions, rubrics, handoff docs, scripts, validators, CI checks, package checks, generated artifacts, and user-facing instructions where wording controls action, safety, validation, or output format.

Do not use for polish alone. If there is no operational job or real execution failure, make only light clarity edits.

## Priority Ladder

When goals conflict, preserve in order: 1) safety/policy/permissions/refusal/fallback; 2) user intent/scope/outcome; 3) protected tokens and formats: exact strings, code, logs, commands, paths, IDs, schema keys, status values, citations, names, multilingual text, acronyms, capitalization, domain terms; 4) evidence, validation, state, status, audit, handoff; 5) maintainability and rationale; 6) brevity/style/polish. Shorter loses if it removes required behavior, guardrails, exact tokens, silence rules, fallback, evidence, status meaning, or auditability.

## Procedure

### 1. Identify job and reader
Name the operational job and actor: trigger behavior, process, tool constraint, output/fixed format, protected-token preservation, validation, blocked-state handling, handoff, or audit history. Reader may be agent, developer, reviewer, maintainer, validator, CI harness, script, or mixed workflow.

### 2. Diagnose root cause before editing
Find the failure mode: unclear action/trigger/owner/input/output/fallback/priority/scope/state/evidence/silence; protected-token risk to exact strings, fixed formats, code blocks, logs, paths, IDs, schema keys, citations, quoted text, multilingual text, names, acronyms, capitalization, or domain terms; unsupported claim about counts, limits, costs, coverage, telemetry, permissions, tool access, context, persistence, state, validation, or external facts; semantic erosion, detail inflation, duplicate wording, noisy transition, format drift, verification blind spot, harness/access gap, or maintainer-confusing density. Edit only what fixes that root cause.

### 3. Classify risk when useful
Use labels only if they affect the rewrite: ambiguous action, ambiguous trigger, trigger overloading, missing input/output/fallback, protected-token risk, unsupported claims, state misconception, semantic erosion, detail inflation, noisy transition, format drift, verification blind spot, handoff ambiguity, harness/access gap, maintainability erosion. Prioritize unsafe action, wrong execution, corrupted tokens, false completion, missing evidence, inconsistent state, or rework.

### 4. Rewrite with the smallest sufficient rule
Use only needed fields: `When [condition], do [action].` `Use [input/source/evidence].` `Preserve exactly: [tokens/format/terms].` `Return [output].` `If [blocked], do [fallback].` `Do not [forbidden behavior].` `Do this silently when [silence condition].` `Verify by [check].` Prefer observable verb wording; use `must` for obligations and `can` for permission. Avoid `should`, `try to`, and `as appropriate` for required behavior unless discretion is intentional.

### 5. Preserve compact guardrails
Do not estimate exact limits, counts, costs, coverage, telemetry, validation, or external facts without evidence. Do not claim tool access, file changes, validation, or completion unless checked. Preserve exactly: backticks, quotes, code, logs, commands, paths, IDs, schema keys, JSON keys, status values, citations, examples, fixed formats, names, acronyms, multilingual text, capitalization, and domain terms unless translation or normalization is explicitly requested. The skill stores no state; use conversation history, files, or external records. Return to normal silently when a temporary mode ends. Routine update: `Now / Found / Next`; add `Verified` only when evidence was checked. If access is missing, state missing access and do not claim completion.

### 6. Check outcome scope
For each finding/change, decide whether the owner must fix the literal bullet or the directly affected outcome. Prefer: resolve each finding and directly affected files; record unrelated improvements separately.

### 7. Check evidence, sources, and validation
Completion claims need proof. Report what was checked; mark partial validation and unverified items. Evidence may be command output, tests, diff, path, checksum, artifact link, or manual review note. For sourced claims, preserve citations and distinguish source-supported facts from inference. Do not invent telemetry, paths, counts, citations, tool results, external facts, validation outcomes, or access.

### 8. Check handoff, status, and audit
For role/tool/multi-agent/file/durable-record workflows, define only missing essentials: record location, allowed status values, evidence standard, next owner/action, open/closed markers, placeholder meaning/replacement rule, risks, assumptions, blockers, or rework causes. `Verified` means evidence checked, not confidence. `Next` names owner/action. If historical marker semantics are undefined, flag ambiguity instead of guessing.

### 9. Check scripts, validators, harnesses, and CI
When prose describes enforcement, compare it with the script, validator, harness, CI rule, package check, config, or generated artifact: accepted inputs/paths; output/report format; pass/fail/error/destructive/read-only/missing-file behavior; versions, schema, status, config constants; negative tests; unsupported-environment behavior; documentation-check consistency. Do not add validators merely because rules exist; add validation only when important, observable, and testable. Use review checklists for judgment-based behavior.

### 10. Compress after correctness
Remove repeated rules, decorative wording, motivational prose, duplicate examples, obsolete text, and process steps that do not change behavior. Preserve guardrails, protected tokens, source/evidence rules, fallback, silence rules, state notes, fixed or terse formats, handoff semantics, lightweight verification, maintainability, and token use discipline.

## Output Modes

Choose the smallest output mode that answers the user.

```text
Minimal edit:
[smallest change]
```

```text
Issue: [execution/maintenance risk]
Root cause: [why it may fail]
Suggested rewrite: [smallest sufficient fix]
```

```text
| Original | Root cause | Improved |
|---|---|---|
| ... | ... | ... |
```

```text
Guardrail/protected-token review:
- Preserved: [failure-preventing rule]
- Restored: [removed guardrail and why]
- Removed: [padding, duplication, obsolete, or wrong text]
- Preserve exactly: [tokens/terms/formats]
- May change: [allowed prose/fields]
- Risk: [what breaks if changed]
```

```text
Activation/maintainability/handoff review:
- Activation: [trigger clear; validation/telemetry kept in execution rules]
- Maintainability: [rationale kept or density reduced]
- Handoff: [status semantics, checked evidence, next owner/action, risks/open items]
```

```text
Compression summary:
- Removed: [repetition/detail inflation]
- Preserved: [critical behavior/token/rationale/guardrail]
- Added: [only if needed]

Compressed version:
[revised text]
```

```text
Trade-off summary:
- Runtime brevity: [version/reason]
- Safety or validation: [version/reason]
- Human maintainability: [version/reason]
- Recommended merge: [specific retained changes]
```

For skills, scripts, packages, specs, or generated artifacts, use **Version Upgrade Audit**: audit summary; changes in new version; guardrail/token check; activation/compression check; validation with unverified items; updated content/artifact. Update frontmatter version and version-specific notes. Check frontmatter, title, description, examples, output modes, self-checks, and exact constants. Declare one version best only when priority is explicit or measurement supports it.

## Final Self-Check

Before returning revised text, verify: root cause before rewrite; intent, safeguards, fallback, protected tokens, silence, state, evidence, and audit meaning preserved; added detail prevents real failure; removed detail was repetition, padding, obsolete, duplicated, or wrong; actions use observable verbs; conflict priority and missing-input behavior are clear; activation remains simple; completion claims have checked evidence or are marked unverified; exact strings/code/logs/error text/commands/paths/IDs/schema keys/status values/citations/quoted text/multilingual text/domain terms are unchanged unless allowed; fixed and terse formats stay fixed/terse; `Verified` only follows checked evidence; scripts/validators/harnesses/CI/package checks define pass/fail behavior when relevant; handoff markers, placeholders, and audit statuses cannot be mistaken for open work; prompt libraries remain understandable enough to audit; token use has no repeated prose, unnecessary examples, decorative wording, or detail inflation.

Return the improved version or artifact clearly. State validation limits when partial.
