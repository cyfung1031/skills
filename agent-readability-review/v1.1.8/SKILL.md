---
name: agent-readability-review
description: Improves operational text so AI agents can act reliably while preserving intent, safeguards, human maintainability, and minimum sufficient wording.
version: 1.1.8
---

# Skill: Agent Readability Review

## Purpose

Use this skill to revise operational text read by agents, automations, validators, reviewers, or human-agent teams.

Optimize for **minimum sufficient executability**: the shortest clear wording that preserves correct behavior, defensive guardrails, validation evidence, and human maintainability.

Agent-readable text is not automatically longer, shorter, denser, or more formal. A good rewrite may compress, expand, preserve, or restore text depending on what prevents failure.

Do not rewrite for polish alone. Rewrite only when the current text could cause wrong action, unsupported claims, lost safeguards, noisy output, validation gaps, or future maintenance mistakes.

This is a **wording-level review**. Clarify, compress, reorder, or restore existing meaning. Flag missing decisions instead of inventing new requirements, workflows, scoring rubrics, validators, roles, artifacts, or behavior.

A successful rewrite lets the relevant reader answer the operational questions that matter without guessing:

1. What action is required?
2. When does the action apply?
3. What input, evidence, or context must be used?
4. What output, state change, or record must be produced?
5. What must be preserved or avoided?
6. What fallback applies when information is missing, conflicting, unsupported, or outside scope?
7. Which rule wins when requirements conflict?
8. How can completion be verified?
9. What evidence supports a completion claim?
10. Which status, placeholder, or audit markers are open work versus closed evidence?

Only answer the questions that matter for the text's operational job. Do not add fields, steps, examples, or validation rules merely to make the text look complete.

---

## Use This Skill For

Apply this skill to operational text, including:

- skill files, system prompts, developer prompts, and workflow prompts;
- agent instructions, tool-use rules, review rubrics, and SOPs;
- scripts, validators, CI checks, templates, and generated artifacts;
- role-based, tool-based, or human-agent handoff documentation.

Do not use this skill for grammar-only editing unless unclear grammar affects execution.

---

## Core Principles

1. **Preserve behavioral meaning before optimizing wording.** A cleaner rewrite is worse if it removes a rule, fallback, warning, state model, silence requirement, scope limit, evidence requirement, or lightweight verification path.
2. **Add only detail that changes execution or maintenance.** Longer text is not more agent-readable unless the added detail prevents a real failure. Add criteria only when the audience or domain requires them.
3. **Keep activation simple.** A trigger says when the skill or rule applies. Telemetry checks, validation, and enforcement belong in execution rules.
4. **Preserve useful rationale for humans.** Keep compact architecture notes when they prevent false assumptions, such as: `The skill stores no state; the standing request lives in conversation history.`
5. **Report evidence without forcing verbosity.** Default progress format is `Now / Found / Next`. Add `Verified` only when evidence was actually checked, never for intent, confidence, or guesses.

---

## Review Process

### Step 1: Identify the operational job and reader

Determine what the text must make someone or something do, and who must act on it.

Common jobs: trigger behavior; define a process or rule; constrain tool use; specify output; validate completion; handle errors, missing data, or unsupported states; coordinate handoff across humans, agents, tools, scripts, or validators; preserve audit history or state semantics.

Common readers: runtime agent, human developer or reviewer, future maintainer, validator or CI harness, or mixed human-agent workflow.

If the text has no operational job, make only light clarity edits.

### Step 2: Diagnose the root cause before rewriting

Do not fix symptoms by adding generic detail. Identify the execution or maintenance failure first:

- unclear action, trigger, input, output, fallback, priority, state location, evidence, silence requirement, or maintainer rationale;
- unsupported guess about counts, limits, cost, coverage, telemetry, permissions, tools, context, or persistence;
- semantic erosion from over-compression;
- detail inflation, noisy transition, format drift, verification blind spot, harness gap, or tool/permission gap.

Rewrite only the part needed to fix that root cause.

### Step 3: Classify rewrite risk when useful

Use the classification only when it helps choose a safer rewrite.

| Risk | Meaning | Typical fix |
|---|---|---|
| Ambiguous action | Required operation is unclear. | Use an observable verb. |
| Ambiguous trigger | Activation condition is unclear. | State the condition directly. |
| Trigger overloading | Trigger contains validation or enforcement logic. | Move it to execution rules. |
| Missing input/output | Required data, evidence, tool, context, return value, change, or record is absent. | Name the input/output or fallback. |
| Missing fallback | Blocked execution has no next step. | Add blocked-state behavior. |
| Unsupported metric estimate | Text invites guessing counts, limits, cost, coverage, telemetry, or state. | Require evidence or say not to estimate. |
| State misconception | Text implies nonexistent memory or persistence. | State where state actually lives. |
| Semantic erosion | Shorter wording lost a safeguard or edge case. | Restore the safeguard compactly. |
| Detail inflation | Wording adds words without changing behavior. | Remove decorative or duplicate detail. |
| Noisy transition | Text allows meta-announcements that should be silent. | Add `silently` or equivalent. |
| Format drift | Terse format gains filler or loses useful evidence. | Restore required lines; make optional lines conditional. |
| Verification blind spot | Work hides what was actually checked. | Add verification evidence when checked. |
| Maintainability erosion | Concise text becomes hard to audit. | Keep a short rationale. |
| Harness or permission gap | Required behavior is not testable or assumes unavailable access. | Add a check, manual review note, or access fallback. |

Prioritize risks that cause wrong action, unsafe assumptions, missing evidence, inconsistent state, or maintenance errors.

### Step 4: Rewrite with the smallest sufficient rule

Use only the needed pieces:

```text
When [condition], do [action].
Use [input/evidence/source/telemetry].
Return [output].
If [blocked], do [fallback].
Do not [forbidden behavior].
Do this silently when [silence condition].
Verify by [check].
```

Do not expand every instruction into the full pattern. A complete one-line rule is better than a padded template.

Use `must` for obligations and `can` for permission. Avoid `should`, `try to`, and `as appropriate` for required behavior unless discretion is intentional.

### Step 5: Preserve compact guardrails

During cleanup, preserve or restore short rules that prevent likely failure:

- Do not estimate exact limits without telemetry.
- The skill stores no state; use conversation history or external records.
- The standing request lives in conversation history.
- Return to normal silently when the condition ends.
- State what was checked and what remains unverified.
- If access is unavailable, state the missing access and do not claim completion.
- Use `Now / Found / Next`; add `Verified` only when evidence was checked.

Do not remove these merely because they look like extra words.

### Step 6: Check whole-outcome responsibility

When an agent is assigned a finding or change, decide whether it owns only the literal bullet or the directly affected outcome.

Prefer:

> Resolve each reviewer finding and directly affected files. Record unrelated improvements separately.

This prevents narrow literalism without creating unbounded scope.

### Step 7: Check evidence and validation

Completion claims require evidence. Report the validation used; if validation was partial, state what remains unverified.

For code or validators, evidence may be a command result. For wording changes, evidence may be a manual review note. Do not invent telemetry, paths, counts, tool results, external state, or exact context limits.

After compaction, continuation, or resume, re-check load-bearing facts before treating prior notes as verified evidence.

### Step 8: Check handoff, status, and audit language

For role-based, tool-based, or multi-agent workflows, define only the missing pieces needed for reliable handoff:

- durable record location when a record must survive the current response;
- allowed status values;
- evidence field and what qualifies as evidence;
- next-action owner or next executable action;
- open versus closed marker semantics;
- placeholder meaning and replacement rule.

Compact field rules:

- `Verified` names evidence actually checked, not intent or confidence.
- `Next` names the next owner or executable action when handoff matters.
- `Risks` names unresolved blockers, assumptions, or likely rework causes.

Historical markers require explicit semantics when they can affect later audits. If semantics are undefined, flag ambiguity instead of guessing.

### Step 9: Check scripts, validators, and harnesses

When the text includes a script, validator, CI rule, package check, or generated artifact, compare prose with enforcement only where relevant:

- accepted inputs or paths; output or report format;
- pass, fail, error, destructive, read-only, and missing-file behavior;
- version or schema constants;
- negative tests for required failures;
- unsupported-environment behavior;
- consistency between documentation and checks.

Do not add a validator merely because a rule exists. Add validation only when behavior is important, observable, and testable. Use a review checklist for judgment-based behavior.

### Step 10: Compress after fixing root causes

Remove repeated rules, decorative wording, motivational prose, duplicate examples, fixed wording lists where a general rule is enough, and process steps that do not change behavior.

Preserve defensive guardrails, architecture notes, simple triggers, silence requirements, terse output formats, optional lightweight verification lines, fallback rules, and evidence rules for completion claims.

---

## Rewrite Patterns

These examples teach judgment, not fixed replacements.

### Ambiguity or weak verbs

Weak:

> Handle the file appropriately.

Better:

> Identify the file type and use the matching file workflow. State if the type is unsupported.

Weak:

> Consider the user’s preferences.

Better:

> Apply explicit user preferences before defaults.

### Overlong, subjective, or human-only phrasing

Weak:

> When reviewing a file, if it contains operational instructions, identify unclear or context-dependent parts and rewrite those parts while preserving the original intent.

Better:

> If the file contains operational instructions, rewrite unclear parts into executable rules. Preserve intent.

Weak:

> Make it sound professional.

Better:

> Use a neutral, direct tone.

Add tone criteria only when the audience or domain requires them.

### Missing fallback, unsupported claims, or access assumptions

Weak:

> Use the provided data to answer.

Better:

> Answer from provided data. State missing required data.

Weak:

> Switch modes when the context window is nearly full.

Better:

> Switch modes on visible context-pressure signs. Do not estimate exact limits without telemetry.

Weak:

> Check the external system and update the record.

Better:

> If access is available, update the record. If not, state the missing access and do not claim completion.

### Trigger, state, silence, and format preservation

Weak:

> Use this mode only after validating telemetry and checking all compression safeguards.

Better:

> Use this mode on explicit request or visible context-pressure signs. Apply safeguards during execution.

Weak:

> Keep applying this mode later.

Better:

> Re-apply this standing request from conversation history; the skill stores no state.

Weak:

> Return to normal when the task concludes.

Better:

> Return to normal silently when the task concludes.

Weak:

> Ordinary updates must always include `Now / Found / Next / Verified`.

Better:

> Routine update: `Now / Found / Next`. Add `Verified` only when evidence was checked.

### Verification and quality goals

Weak:

> After editing, tell the user the issue is fixed.

Better:

> Report what changed and what validation supports it. Mark unverified parts.

Weak:

> Ensure the instructions are robust.

Better:

> Add missing edge-case, fallback, and completion rules where they affect execution.

Weak:

> Always rewrite “be clear” as “use short sentences.”

Better:

> Define what “clear” requires in context.

---

## Output Modes

Choose the mode that matches the user’s request.

### Minimal Patch

```text
Minimal edit:
[Smallest change that improves execution or maintenance]
```

### Annotated Review

```text
Issue:
[What is hard to execute or maintain]

Root cause:
[Why the text may fail]

Suggested rewrite:
[Smallest sufficient improvement]
```

### Before / After Table

```text
| Original | Root cause | Improved |
|---|---|---|
| ... | ... | ... |
```

### Guardrail Preservation Review

Use when a cleaner or shorter version may have removed defensive behavior.

```text
Guardrail review:
- Preserved: [compact rule that prevents failure]
- Restored: [removed guardrail and why it matters]
- Removed: [text that was only repetition or padding]
```

### Activation Review

Use when a rewrite may have overloaded the trigger section.

```text
Activation review:
- Trigger kept simple: [yes/no]
- Moved to execution rules: [telemetry/validation/enforcement details]
- Preserved guardrail: [anti-guessing or fallback rule]
```

### Maintainability Review

Use when dense wording may be efficient for agents but harder for developers to audit.

```text
Maintainability review:
- Kept concise rationale: [architecture or state note]
- Compressed without loss: [rule that remains clear]
- Restored clarity: [wording that was too terse]
```

### Handoff Review

Use when a workflow includes roles, statuses, durable records, placeholders, or audit trails.

```text
Handoff review:
- Status semantics: [clear/missing/ambiguous]
- Verified evidence: [evidence actually checked, not claimed or planned]
- Next owner/action: [who or what proceeds next]
- Risks/open items: [blockers, assumptions, or rework causes]
```

### Compression Pass

```text
Compression summary:
- Removed: [repetition or detail inflation]
- Preserved: [critical behavior, rationale, or guardrail]
- Added: [only if needed]

Compressed version:
[Revised text]
```

### Trade-Off Comparison

Use when comparing versions with different priorities.

```text
Trade-off summary:
- Best for runtime brevity: [version/reason]
- Best for safety or validation: [version/reason]
- Best for human maintainability: [version/reason]
- Recommended merge: [specific changes to keep from each]
```

Do not declare one version universally better unless the user’s priority is explicit.

### Version Upgrade Audit

Use when the user asks to audit and improve an existing skill, script, package, or generated artifact.

```text
Audit summary:
- [Root cause]: [impact]

Changes in [new version]:
- [Change]: [why it improves execution or maintenance]

Guardrail check:
- [Preserved or restored defensive rule]
- [Removed only if obsolete, duplicated, or wrong]

Activation check:
- [Trigger remains simple]
- [Validation/telemetry rules are not incorrectly moved into trigger]

Compression check:
- [Where wording was shortened or expansion was avoided]

Validation:
- [Check performed]: [result]
- [Unverified item, if any]: [reason]

Updated content or artifact:
[Full revised skill, patch, or generated file link]
```

For version upgrades, apply the review process to the existing version. Also update frontmatter version and version-specific notes; check consistency across frontmatter, title, description, examples, output modes, and self-checks; report performed validation and unverified items without overstating certainty.

Before finalizing a version upgrade, check that no cleaner version removed guardrails, state notes, silent transitions, terse formats, scope limits, evidence rules, handoff semantics, or lightweight verification paths. Also check that no hardened version overloaded activation logic or harmed human maintainability.

---

## Final Self-Check

Before returning revised text, verify:

- Root cause was identified before rewriting.
- Original intent, safeguards, fallback rules, silence rules, state semantics, and evidence requirements are preserved.
- The rewrite is the shortest version that still supports correct execution and maintenance.
- Added detail prevents a real execution or maintenance failure; removed detail was repetition, padding, obsolete, duplicated, or wrong.
- Required actions use observable verbs; subjective wording has criteria only when it affects execution.
- Activation remains simple; telemetry and validation rules are not incorrectly moved into triggers.
- Missing-input, conflict-priority, whole-outcome, tool-access, permission, and unsupported-state behavior are defined where relevant.
- Completion claims are supported by checked evidence; unverified parts are marked.
- Unsupported telemetry, context limits, state, permissions, tool access, or external facts are not guessed.
- Architecture notes are kept when they prevent false state or persistence assumptions.
- Silent transitions remain silent when meta-commentary would be noise.
- Terse formats stay terse; optional `Verified` lines are used only when evidence was checked or rapid verification tracking matters.
- Validator requirements define pass/fail behavior when relevant.
- Handoff markers, placeholders, and audit statuses cannot be mistaken for open work.
- Human-facing prompt libraries remain understandable enough for developers to audit.
- Examples teach reusable judgment, not fixed replacements or longer-is-better habits.
- Token use is efficient: no repeated prose, unnecessary examples, decorative wording, or detail inflation.

Return the improved version clearly. If validation is partial, state the limitation.
