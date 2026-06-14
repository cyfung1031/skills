---
name: agent-readability-review
description: Improves operational text so AI agents can act reliably while preserving intent, safeguards, human maintainability, and minimum sufficient wording.
version: 1.1.7
---

# Skill: Agent Readability Review

## Purpose

Use this skill to revise operational text read by agents, automations, validators, reviewers, or human-agent teams.

Optimize for **minimum sufficient executability**: the shortest clear wording that preserves correct behavior, defensive guardrails, validation evidence, and human maintainability.

Agent-readable text is not automatically longer, shorter, denser, or more formal. A good rewrite may compress, expand, preserve, or restore text depending on what prevents failure.

Do not rewrite for polish alone. Rewrite when the current text could cause wrong action, unsupported claims, lost safeguards, noisy output, validation gaps, or future maintenance mistakes.

A rewrite is successful when the relevant reader can answer the necessary questions without guessing:

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

Only answer the questions that matter for the text’s operational job. Do not add fields, steps, examples, or validation rules merely to make the text look complete.

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

### 1. Preserve behavioral meaning before optimizing wording

A cleaner rewrite is worse if it removes a rule, fallback, warning, state model, silence requirement, scope limit, evidence requirement, or lightweight verification path.

Bad compression:

> Use signs of context pressure.

Better:

> Use visible context-pressure signs. Do not estimate exact context limits without telemetry.

### 2. Add only detail that changes execution or maintenance

Longer text is not more agent-readable unless the added detail prevents a real failure.

Bad expansion:

> Use a neutral, direct, professional, concise, polished, non-emotional, audience-aware, jargon-sensitive tone.

Better:

> Use a neutral, direct tone.

Add more criteria only when the audience or domain requires them.

### 3. Keep activation simple

A trigger section should say when the skill or rule applies. Do not overload it with telemetry checks, validation procedures, or enforcement details.

Better:

> Use this mode on explicit user request or visible context-pressure signs. Do not estimate exact limits without telemetry.

### 4. Preserve useful rationale for humans

Dense wording may be efficient for runtime agents but harder for developers to audit. Keep short architecture notes when they prevent false assumptions.

Better for maintainers:

> The skill stores no state; the standing request lives in conversation history.

### 5. Report evidence without forcing verbosity

Progress formats should stay terse. Add verification only when evidence was actually checked.

Default:

```text
Now: ...
Found: ...
Next: ...
```

Optional in rapid test or terminal loops:

```text
Verified: ...
```

Do not use `Verified` for intentions, guesses, or unchecked claims.

---

## Review Process

### Step 1: Identify the operational job and reader

Determine what the text must make someone or something do.

Common jobs:

- trigger a behavior;
- define a process or rule;
- constrain tool use;
- specify output format;
- validate completion;
- handle errors, missing data, or unsupported states;
- coordinate handoff across humans, agents, tools, scripts, or validators;
- preserve audit history or state semantics.

Also identify the reader:

- runtime agent;
- human developer or reviewer;
- future maintainer;
- validator or CI harness;
- mixed human-agent workflow.

If the text has no operational job, make only light clarity edits.

### Step 2: Identify the root cause before rewriting

Do not fix symptoms by adding generic detail. First identify why the text may fail.

Use these root-cause questions:

1. **Action:** What operation is unclear?
2. **Trigger:** When does the rule apply?
3. **Input:** What evidence, context, tool, telemetry, or file is required?
4. **Output:** What should be returned, changed, recorded, or preserved?
5. **Fallback:** What happens if information, access, telemetry, or support is missing?
6. **Priority:** Which rule wins if requirements conflict?
7. **State:** Where does persistent information actually live?
8. **Evidence:** What proves completion?
9. **Silence:** Should the agent avoid announcing the transition?
10. **Maintenance:** Would a human maintainer understand why the rule exists?

Rewrite only the part needed to fix the root cause.

### Step 3: Classify the rewrite risk

Use the classification only when it helps choose a better rewrite.

| Risk | Meaning | Typical fix |
|---|---|---|
| Ambiguous action | The required operation is unclear. | Use an observable verb. |
| Ambiguous trigger | The activation condition is unclear. | State the condition directly. |
| Trigger overloading | The trigger contains too much validation logic. | Move validation to execution rules. |
| Missing input | Required data, evidence, tool, or context is absent. | Name the input or fallback. |
| Missing output | The return value, change, or record is unclear. | State the output. |
| Missing fallback | Blocked execution has no next step. | Add the blocked-state behavior. |
| Unsupported metric estimate | The text invites guessing counts, limits, cost, coverage, telemetry, or state. | Require evidence or say not to estimate. |
| State misconception | The text implies nonexistent memory or persistence. | State where state actually lives. |
| Semantic erosion | A shorter rewrite lost a safeguard or edge case. | Restore the safeguard compactly. |
| Detail inflation | The rewrite adds words without changing behavior. | Remove decorative or duplicate detail. |
| Noisy transition | The text allows meta-announcements that should be silent. | Add `silently` or equivalent. |
| Format drift | A terse format gains filler or loses useful evidence. | Restore required lines; make optional lines conditional. |
| Verification blind spot | Routine work hides what was actually checked. | Add optional verification evidence when checked. |
| Maintainability erosion | The rewrite is concise but harder to audit. | Keep a short rationale. |
| Harness gap | Required behavior is not represented in templates, validators, or self-checks. | Add a check or explain manual verification. |
| Tool or permission gap | The instruction assumes access that may not exist. | State access fallback and forbid unsupported claims. |

Prioritize risks that cause wrong action, unsafe assumptions, missing evidence, inconsistent state, or maintenance errors.

### Step 4: Rewrite with the smallest sufficient rule

Use only the pieces needed:

```text
When [condition], do [action].
Use [input/evidence/source/telemetry].
Return [output].
If [blocked], do [fallback].
Do not [forbidden behavior].
Do this silently when [silence condition].
Verify by [check].
```

Do not expand every instruction into the full pattern. A one-line rule is better when it is complete.

Use `must` for obligations. Use `can` for permission. Avoid `should`, `try to`, and `as appropriate` for required behavior unless discretion is intentional.

### Step 5: Preserve compact guardrails

During cleanup, preserve short rules that prevent likely failure.

| Failure prevented | Guardrail to preserve or restore |
|---|---|
| Hallucinated context math | Do not estimate exact limits without telemetry. |
| False persistent memory | The skill stores no state; use conversation history or external records. |
| Maintainer confusion | The standing request lives in conversation history. |
| Noisy mode switch | Return to normal silently when the condition ends. |
| Unsupported success claim | State what was checked and what remains unverified. |
| Hidden access assumption | If access is unavailable, state the missing access and do not claim completion. |
| Routine update bloat | Use `Now / Found / Next`; add `Verified` only when evidence was checked. |

Do not remove these just because they look like extra words.

### Step 6: Check whole-outcome responsibility

When an agent is assigned a finding or change, decide whether it owns only the literal bullet or the directly affected outcome.

Weak:

> Fix the reviewer’s issues.

Better:

> Resolve each reviewer finding and directly affected files. Record unrelated improvements separately.

This prevents narrow literalism without creating unbounded scope.

### Step 7: Check evidence and validation

Completion claims must be supported by evidence.

Weak:

> Confirm everything works.

Better:

> Report the validation used. If validation was partial, state what remains unverified.

For code or validators, evidence may be a command result. For wording changes, evidence may be a manual review note. Do not invent telemetry, paths, counts, tool results, external state, or exact context limits.

After compaction, continuation, or resume, re-check load-bearing facts before treating prior notes as verified evidence.

### Step 8: Check handoff, status, and audit language

For role-based, tool-based, or multi-agent workflows, make later interpretation unambiguous without adding unnecessary process.

Define only the missing pieces needed for reliable handoff:

- durable record location, when a record must survive the current response;
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

When the text includes a script, validator, CI rule, package check, or generated artifact, compare prose with enforcement.

Check only relevant items:

- accepted inputs or paths;
- output or report format;
- pass, fail, and error behavior;
- destructive versus read-only behavior;
- missing-file behavior;
- version or schema constants;
- negative tests for required failures;
- unsupported-environment behavior;
- consistency between documentation and checks.

Do not add a validator merely because a rule exists. Add validation when behavior is important, observable, and testable. Use a review checklist for judgment-based behavior.

### Step 10: Compress after fixing root causes

After the rewrite, remove:

- repeated rules;
- decorative wording;
- motivational prose;
- duplicate examples;
- fixed wording lists when a general rule is enough;
- process steps that do not change behavior.

Preserve:

- defensive guardrails;
- short architecture notes;
- simple activation triggers;
- silence requirements;
- terse output formats;
- optional lightweight verification lines;
- fallback rules;
- evidence rules for completion claims.

---

## Rewrite Patterns

These examples teach judgment, not fixed replacements.

### Ambiguous wording

Weak:

> Handle the file appropriately.

Better:

> Identify the file type and use the matching file workflow. State if the type is unsupported.

Add file-type branches only when those workflows are defined.

### Weak verb

Weak:

> Consider the user’s preferences.

Better:

> Apply explicit user preferences before defaults.

Add conflict handling only when conflicts are likely or present.

### Long sentence

Weak:

> When reviewing a file, if it contains operational instructions, identify unclear or context-dependent parts and rewrite those parts while preserving the original intent.

Better:

> If the file contains operational instructions, rewrite unclear parts into executable rules. Preserve intent.

Split further only when conditions or exceptions cause ambiguity.

### Human-only phrasing

Weak:

> Make it sound professional.

Better:

> Use a neutral, direct tone.

Add more tone criteria only when the audience or domain requires them.

### Missing fallback

Weak:

> Use the provided data to answer.

Better:

> Answer from provided data. State missing required data.

Add a field list only when specific fields are required.

### Unsupported metric estimate

Weak:

> Switch modes when the context window is nearly full.

Better:

> Switch modes on visible context-pressure signs. Do not estimate exact limits without telemetry.

### Overloaded trigger

Weak:

> Use this mode only after validating telemetry and checking all compression safeguards.

Better:

> Use this mode on explicit request or visible context-pressure signs. Apply safeguards during execution.

### State architecture

Weak:

> Keep applying this mode later.

Better:

> Re-apply this standing request from conversation history; the skill stores no state.

For developer-facing docs, this may be clearer:

> The skill stores no state; the standing request lives in conversation history.

### Silent transition

Weak:

> Return to normal when the task concludes.

Better:

> Return to normal silently when the task concludes.

### Terse format preservation

Weak:

> Ordinary updates must always include `Now / Found / Next / Verified`.

Better:

> Routine update: `Now / Found / Next`. Add `Verified` only when evidence was checked.

### Fast verification loop

Weak:

> Use the full handoff template after each compile attempt.

Better:

> In rapid test loops, add `Verified: [check/result]` to the ordinary update.

### Unsupported completion claim

Weak:

> After editing, tell the user the issue is fixed.

Better:

> Report what changed and what validation supports it. Mark unverified parts.

### Hard-to-test quality goal

Weak:

> Ensure the instructions are robust.

Better:

> Add missing edge-case, fallback, and completion rules where they affect execution.

### Over-narrow example

Weak:

> Always rewrite “be clear” as “use short sentences.”

Better:

> Define what “clear” requires in context.

### Tool or permission gap

Weak:

> Check the external system and update the record.

Better:

> If access is available, update the record. If not, state the missing access and do not claim completion.

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
- Verified evidence: [what evidence must be named]
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

For version upgrades, the agent must:

1. identify the existing version’s job and reader;
2. identify root causes, not just surface differences;
3. preserve useful rules unless they conflict with the upgrade goal;
4. check whether a cleaner version removed guardrails, state notes, silent transitions, terse formats, scope limits, evidence rules, handoff semantics, or lightweight verification paths;
5. check whether a hardened version overloaded activation logic or harmed human maintainability;
6. restore safeguards in compact form when they prevent likely failure;
7. update frontmatter version and any version-specific notes;
8. check consistency across frontmatter, title, description, examples, output modes, and self-checks;
9. perform a compression check so examples do not imply longer text is better;
10. report performed validation and unverified items without overstating certainty.

---

## Final Self-Check

Before returning revised text, verify:

- The root cause is identified before rewriting.
- The rewrite preserves original intent and operational safeguards.
- The rewrite is the shortest version that still supports correct execution and maintenance.
- Added detail prevents a real execution or maintenance failure.
- Removed detail was not a compact guardrail, useful rationale, or lightweight verification path.
- Required actions use observable verbs.
- Activation logic remains simple.
- Telemetry and validation rules are not incorrectly moved into triggers.
- Subjective wording has criteria only when it affects execution.
- Missing-input behavior is defined where needed.
- Conflict priority is clear where relevant.
- Whole-outcome responsibility is explicit and bounded when needed.
- Evidence requirements support completion claims.
- Unsupported telemetry, context limits, state, permissions, or tool access are not guessed.
- Architecture notes are kept when they prevent false state or persistence assumptions.
- Silent transitions remain silent when meta-commentary would be noise.
- Terse formats stay terse.
- Optional `Verified` lines are used only when evidence was checked or rapid verification tracking matters.
- Validator requirements define pass/fail behavior when relevant.
- Tool or permission limits are handled without unsupported claims.
- Handoff markers, placeholders, and audit statuses cannot be mistaken for open work.
- Examples teach reusable judgment, not fixed replacements.
- Examples do not imply that longer rewrites are better.
- Human-facing prompt libraries remain understandable enough for developers to audit.
- Token use is efficient: no repeated prose, unnecessary examples, decorative wording, or detail inflation.

Return the improved version clearly. If validation is partial, state the limitation.
