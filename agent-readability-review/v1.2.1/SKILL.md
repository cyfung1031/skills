---
name: agent-readability-review
description: Revises operational text for agent execution with minimal wording while preserving intent, safeguards, protected tokens, validation evidence, handoff state, scripts, and localization.
version: 1.2.1
last_updated: 2026-06-17
---

# Skill: Agent Readability Review

## Purpose

Revise operational text for agents, automations, validators, reviewers, scripts, CI, SOPs, templates, or human-agent handoffs.

Goal: **minimum sufficient executability**: the shortest wording that preserves correct behavior, safety, protected tokens, evidence, status semantics, localization, and maintainability, while making validation limits explicit.

Do wording-level work only: clarify, compress, reorder, or restore existing meaning. Keep source text boundaries clear: quoted/code/source content is preserved unless the user asks to rewrite it. Do not invent requirements, facts, citations, tool access, validators, workflows, roles, files, measurements, or completion. Rewrite only when wording can cause wrong action, unsafe assumption, lost safeguard, noisy output, validation gap, format drift, token corruption, localization loss, or maintenance error.

Success means the reader can identify action, trigger, actor, input/source/evidence, output/state/file/format, exact tokens, fallback, priority, verification, completion proof, owner, open/closed status, and validation limits.

## Use / Do Not Use

Use for skills, prompts, workflow rules, SOPs, templates, tool instructions, rubrics, handoff docs, scripts, validators, CI checks, package checks, generated artifacts, and user-facing instructions where wording controls action, safety, validation, or output format.

Do not use for polish alone. If there is no operational job or real execution risk, make only light clarity edits and say no operational rewrite was needed.

## Priority Ladder

When goals conflict, preserve in order:
1. safety, policy, permissions, refusal, and fallback;
2. user intent, scope, and outcome;
3. protected tokens and fixed formats: exact strings, code, logs, commands, paths, IDs, schema keys, status values, citations, names, multilingual text, acronyms, capitalization, and domain terms;
4. evidence, validation, state, audit trail, handoff, owner, and open/closed semantics;
5. human maintainability and necessary rationale;
6. brevity, style, and polish.

Shorter loses if it removes required behavior, guardrails, protected tokens, silence rules, fallback, evidence, status meaning, auditability, localization, or maintainability.

## Procedure

1. **Identify job and reader.** Name the operational job and reader: agent, developer, reviewer, maintainer, validator, CI harness, script, support role, or mixed workflow.
2. **Diagnose before editing.** Find the root cause: unclear action/trigger/owner/input/output/fallback/priority/scope/state/evidence/silence; protected-token risk; unsupported claims about counts, limits, costs, coverage, telemetry, permissions, tool access, persistence, validation, or external facts; semantic erosion; detail inflation; duplicate wording; noisy transition; format drift; localization loss; verification blind spot; harness/access gap; or maintainer-confusing density.
3. **Classify only useful risk.** Use labels only when they affect the rewrite: ambiguous action/trigger, trigger overload, missing input/output/fallback, protected-token risk, unsupported claim, state misconception, semantic erosion, detail inflation, noisy transition, format drift, verification blind spot, handoff ambiguity, localization drift, harness/access gap, maintainability erosion.
4. **Rewrite the smallest sufficient rule.** Use observable verbs and only needed fields: `When [condition], do [action].` `Use [source/evidence].` `Preserve exactly: [tokens/formats/terms].` `Return [output].` `If [blocked], do [fallback].` `Do not [forbidden behavior].` `Verify by [check].` Use `must` for obligations and `can` for permission; avoid `should`, `try to`, and `as appropriate` for required behavior.
5. **Preserve compact guardrails.** Do not estimate exact limits, counts, costs, coverage, telemetry, validation, or external facts without evidence. Do not claim tool access, file changes, validation, or completion unless checked. Preserve exact strings, code, logs, commands, paths, IDs, schema keys, JSON keys, status values, citations, examples, fixed formats, names, acronyms, multilingual text, capitalization, and domain terms unless the user explicitly asks to translate or normalize them. The skill stores no state; use conversation history, files, or external records.
6. **Check outcome scope.** State whether the change fixes the literal sentence, the directly affected outcome, or both. Record unrelated improvements separately.
7. **Check evidence and validation.** Completion claims need proof. Report checked evidence such as command output, tests, diff, path, checksum, artifact link, source citation, or manual review note. Mark partial validation and unverified items. For sourced claims, preserve citations and separate source-supported facts from inference.
8. **Check handoff and audit.** For role/tool/file/durable-record workflows, preserve or add only missing essentials: record location, allowed status values, evidence standard, next owner/action, open/closed markers, placeholder replacement rule, blockers, assumptions, risks, and rework causes. `Verified` means evidence checked, not confidence; `Next` names owner/action.
9. **Check scripts, validators, harnesses, and CI.** When prose describes enforcement, compare with the script, validator, harness, CI rule, package check, config, or generated artifact: accepted inputs/paths; output/report format; pass/fail/error/destructive/read-only/missing-file behavior; versions; schema; status constants; negative tests; unsupported-environment behavior; documentation consistency. Add validation only when observable and necessary.
10. **Check language and tone.** Keep the user's language unless asked otherwise; preserve terminology, honorifics, locale-specific statuses, and mixed-script text. Preserve multilingual text and domain terms. Do not replace culturally or legally specific wording with generic English assumptions. Keep tone constraints only when they affect user-facing behavior or safety.
11. **Compress after correctness.** Remove repeated rules, decorative wording, motivational prose, duplicate examples, obsolete text, and steps that do not change behavior. Preserve guardrails, protected tokens, source/evidence rules, fallback, silence rules, state notes, fixed or terse formats, handoff semantics, lightweight verification, maintainability, and token discipline.

## Output Modes

Choose the smallest output mode that satisfies the request.

```text
Minimal edit:
[smallest change]
```

```text
Issue: [execution/maintenance risk]
Root cause: [why it may fail]
Suggested rewrite: [smallest sufficient fix]
Validation: [checked / partial / unverified]
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

For skills, scripts, packages, specs, or generated artifacts, use **Version Upgrade Audit**: audit summary; changes in new version; guardrail/token check; activation/compression check; validation with unverified items; updated content/artifact. Update frontmatter version and version-specific notes. Check frontmatter, title, description, examples, output modes, self-checks, constants, and exact tokens. Declare one version best only when priority is explicit or measurement supports it.

## Final Self-Check

Before returning, verify: root cause identified before rewrite; intent, safeguards, fallback, protected tokens, silence, state, evidence, language, and audit meaning preserved; added detail prevents real failure; removed detail was repetition, padding, obsolete, duplicated, or wrong; actions use observable verbs; conflict priority and missing-input behavior are clear; activation remains simple; completion claims have checked evidence or are marked unverified; exact strings/code/logs/error text/commands/paths/IDs/schema keys/status values/citations/quoted text/multilingual text/domain terms are unchanged unless allowed; fixed and terse formats stay fixed; `Verified` only follows checked evidence; scripts/validators/harnesses/CI/package checks define pass/fail behavior when relevant; handoff markers, placeholders, and audit statuses cannot be mistaken for open work; prompt libraries remain auditable; token use has no repeated prose, unnecessary examples, decorative wording, or detail inflation.

Return the improved version or artifact clearly. State validation limits when partial; do not add a footer unless the user asks for audit detail.
