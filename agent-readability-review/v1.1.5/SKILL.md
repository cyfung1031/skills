---
name: agent-readability-review
description: Improves operational text so AI agents can parse intent, act reliably, preserve safeguards, and validate completion with the fewest words needed for correct execution.
version: 1.1.5
---

# Skill: Agent Readability Review

## Purpose

Use this skill when text is meant to guide an AI agent, workflow agent, automation, script, validator, reviewer, or human-agent handoff.

Optimize for **minimum sufficient executability**: the text should contain exactly the detail needed for correct action, no less and no more.

Agent-readable text is not automatically longer, shorter, simpler, or more formal. It is better when it helps an agent:

1. choose the correct action;
2. know when the action applies;
3. use the right inputs, evidence, tools, telemetry, or context;
4. produce the expected output, state change, or record;
5. preserve constraints, safeguards, scope, and silence requirements;
6. handle missing, conflicting, unsupported, or inaccessible information;
7. resolve rule conflicts;
8. verify completion without inventing evidence.

Do not add fields, steps, examples, validators, or explanations just to make the text look complete.

---

## Core Rule

Rewrite only to remove execution risk.

A good rewrite may be shorter:

> Weak: Try to make the answer helpful and avoid being too vague.  
> Better: Answer the user’s goal with the most specific supported information. State missing required information.

A good rewrite may keep a compact guardrail:

> Keep: Do not estimate exact context limits without telemetry.

Do not delete short defensive wording just because the sentence reads cleaner without it.

---

## Use This Skill For

Apply this skill to operational text, including:

- skill files;
- system, developer, or workflow prompts;
- agent instructions;
- scripts, validators, and CI checks;
- SOPs and workflow documentation;
- review rubrics;
- policy-like documents;
- tool-use instructions;
- templates agents must fill in;
- human-authored documents agents will process or follow.

Do not use this skill for grammar-only editing unless unclear grammar affects execution.

---

## Review Process

### Step 1: Identify the Operational Job

Classify what the text is trying to make the agent do.

Common jobs include:

- guide behavior;
- define a process or rule;
- constrain tool use;
- specify an output;
- define review or approval criteria;
- describe fallback or error handling;
- coordinate handoff between agents, tools, roles, scripts, or validators;
- validate completion;
- preserve audit or status history;
- prevent guessing about unavailable context, telemetry, state, tools, or authority.

If the text has no operational job, make only light clarity edits.

---

### Step 2: Decide Whether to Change the Text

Before rewriting, ask:

> Would an agent likely choose the wrong action, omit required work, guess unavailable information, make an unsupported claim, produce noisy output, or fail validation if this text stays as-is?

If no, prefer no change or a small clarity edit.

Use this table:

| Situation | Preferred action |
|---|---|
| Vague but harmless | Leave it or lightly edit. |
| Vague and execution-relevant | Replace with a direct rule. |
| Missing condition, output, fallback, priority, evidence, or scope | Add only the missing element. |
| Compact guardrail prevents a real failure | Preserve it or restate it compactly. |
| Architecture note prevents false assumptions | Keep a short note. |
| Repeated rule | Remove it or reference the existing rule. |
| Example implies “longer is better” | Replace with a compact judgment-based example. |

Do not add scaffolding unless it prevents a real execution failure.

---

### Step 3: Find Rewrite Risks

Flag issues by execution impact, not by wording category alone.

Look for:

- ambiguous actions, conditions, targets, or ownership;
- weak verbs that hide the required operation;
- subjective phrasing without decision criteria;
- long sentences that combine unrelated rules;
- hidden assumptions about knowledge, tools, permissions, state, telemetry, or authority;
- missing inputs, outputs, success criteria, fallback behavior, or evidence;
- instructions that invite unsupported estimates of tokens, context window, cost, coverage, time, state, or system limits;
- conflicting rules without priority;
- pronouns or references with unclear targets;
- examples that teach brittle one-off replacement;
- findings that sound optional when they are required outcomes;
- status, audit, or handoff markers whose open/closed meaning is unclear;
- script, validator, or CI behavior without pass/fail or error behavior;
- completion claims without evidence;
- cleaner rewrites that removed safeguards;
- verbose rewrites that add no new executable value.

A vague term is acceptable when nearby text already defines how to act on it.

---

### Step 4: Diagnose the Failure Mode

Name the failure only when it helps produce a better rewrite.

| Failure mode | Meaning |
|---|---|
| Ambiguous action | The operation is unclear. |
| Ambiguous condition | The trigger is unclear. |
| Missing input | Required data, evidence, or context is absent. |
| Missing output | The return value, change, or record is unclear. |
| Missing fallback | Blocked execution has no next step. |
| Unclear priority | Rules may conflict. |
| Unverifiable completion | Done-ness cannot be checked. |
| Unsupported completion claim | The text allows success claims without evidence. |
| Unsupported metric estimate | The text invites guessing telemetry, limits, counts, cost, coverage, or state. |
| State misconception | The text implies nonexistent memory, persistence, or ownership. |
| Noisy transition | The text allows meta-announcements that should remain silent. |
| Format drift | A terse required format gains optional filler or fields. |
| Over-narrow example | The example encourages brittle pattern matching. |
| Harness gap | A required behavior lacks a template, validator, status field, or self-check. |
| Historical-marker ambiguity | Closed evidence can be mistaken for open work, or the reverse. |
| Tool or permission gap | The instruction assumes access the agent may not have. |
| Detail inflation | The rewrite adds steps that do not affect correct execution. |
| Semantic erosion | The rewrite is shorter but loses a constraint, guardrail, or edge case. |

Prioritize failures that could cause wrong action, incomplete work, unsafe assumptions, unsupported claims, noisy output, inconsistent records, or validator blind spots.

---

### Step 5: Preserve Compact Guardrails

During compression or cleanup, preserve short wording that prevents likely failure.

Common compact guardrails:

| Risk | Compact guardrail |
|---|---|
| Guessing window math | Do not estimate exact limits without telemetry. |
| False persistence assumption | This skill stores no state; rely on conversation or external records. |
| Noisy mode change | Return to normal silently when the condition ends. |
| Bloated routine update | Use `Now / Found / Next`; add `Verified` only for validation claims. |
| Unsupported success claim | State what was checked; mark unverified items. |
| Hidden access assumption | If access is unavailable, state the missing access and do not claim completion. |

Keep architecture notes when they prevent a likely false assumption by agents, developers, reviewers, or maintainers.

---

### Step 6: Rewrite With Minimum Sufficient Specificity

Use only the parts of this pattern that are needed:

```text
When [condition], do [action].
Use [input/evidence/source/telemetry].
Return [output].
If [blocked], do [fallback].
Do not [forbidden behavior].
Do this silently when [silence condition].
Verify by [check].
```

Prefer:

- observable action verbs;
- short sentences when they improve parsing;
- explicit conditions and outputs when ambiguity matters;
- named files, fields, tools, telemetry, or commands only when known and needed;
- evidence requirements for completion claims;
- fallback behavior for likely blocked states;
- silence requirements where meta-commentary would be noise.

Do not expand every instruction into the full pattern. A one-line rule is better when it is enough.

Use `can` only for permission. Use `must` for obligations. Avoid soft modal wording for required behavior unless discretion is intentional.

---

### Step 7: Preserve Intent, Scope, and Flexibility

Preserve the source text’s intent and operational safeguards.

Do not turn a general rule into a brittle checklist.

Weak overcorrection:

> Replace every vague quality word with a fixed phrase.

Better:

> Replace vague quality words only when they affect execution.

When the source intentionally leaves discretion, preserve discretion and define only how to handle risk.

Compact example:

> Choose the lowest-risk interpretation. State the assumption if it changes the output or risk.

When shortening text, compare behavior before and after. If the shorter version removes a constraint, fallback, state model, telemetry warning, format constraint, or silence requirement, restore it in compact form.

---

### Step 8: Check Whole-Outcome Responsibility

When text assigns work to an agent, determine whether the agent owns literal tasks or the whole outcome.

Weak:

> Fix the reviewer’s issues.

Better:

> Resolve each reviewer finding and directly affected files. Record unrelated improvements separately.

This prevents narrow literalism without creating an unbounded checklist. Add artifact-type lists only when the affected types are known and important.

---

### Step 9: Check Evidence and Completion Claims

For tasks that change an artifact, status, rule, validator, data record, or output, completion must be supportable.

Weak:

> Confirm that everything works.

Better:

> Report the validation used. If validation was partial, state what remains unverified.

Define evidence only as specifically as needed. A validator command may be necessary for code; a manual review note may be enough for wording changes.

Do not invent telemetry, counts, paths, test results, external state, permissions, or tool output.

---

### Step 10: Check Handoff, Status, and Audit Language

For role-based, tool-based, or multi-agent workflows, make later interpretation unambiguous.

Define only the missing pieces needed for reliable handoff:

- record location;
- allowed status values;
- evidence field;
- next-action owner;
- open versus closed marker semantics;
- placeholder meaning and replacement rule;
- where state actually lives.

Weak:

> Mark the task as done when complete.

Better:

> Set `status` to `closed` only after validation passes. Record unresolved dependencies as `blocked`.

For historical records:

> Treat historical placeholders according to recorded workflow semantics. If semantics are undefined, flag ambiguity instead of guessing.

---

### Step 11: Audit Scripts, Validators, and Harnesses

When the source includes a script, validator, harness, CI rule, package check, or generated artifact, inspect prose and enforcement together.

Check only what is relevant:

- accepted inputs and paths;
- output or report format;
- pass/fail and error behavior;
- destructive versus read-only behavior;
- missing-file behavior;
- version or schema constants;
- negative tests for required failures;
- consistency between prose and enforced checks;
- unsupported-environment behavior;
- what must not be guessed without telemetry or tool support.

Do not add a validator merely because a rule exists. Add validation when behavior is important, observable, and testable. For judgment-based behavior, use a review checklist or evidence note.

Weak:

> The validator checks important fields.

Better:

> The validator fails when a required status field is missing and reports the file path and field name.

---

### Step 12: Compression Pass

After improving executability, compress the result.

Remove:

- repeated rules;
- decorative wording;
- motivational prose;
- duplicate examples;
- fixed wording lists when a general rule is enough;
- process steps that do not change the agent’s action.

Preserve:

- compact defensive guardrails;
- architecture notes that prevent false assumptions;
- explicit silence requirements;
- terse output formats where brevity is the point;
- fallback rules for likely blocked states;
- evidence rules for completion claims.

Prefer one strong example over several similar examples. Keep redundancy only when it protects a critical behavior across different contexts.

---

## Common Rewrite Patterns

These examples teach judgment, not fixed replacements.

### Ambiguous Wording

Weak:

> Handle the file appropriately.

Better:

> Identify the file type and use the matching file workflow. State if the type is unsupported.

Add file-type branches only when those workflows are defined.

---

### Weak Verb

Weak:

> Consider the user’s preferences.

Better:

> Apply explicit user preferences before defaults.

Add conflict handling only when conflicts are likely or present.

---

### Long or Nested Sentence

Weak:

> When reviewing a file, if it contains operational instructions, identify unclear or context-dependent parts and rewrite those parts while preserving the original intent.

Better:

> If the file contains operational instructions, rewrite unclear parts into executable rules. Preserve intent.

Split further only when conditions or exceptions cause ambiguity.

---

### Human-Only Phrasing

Weak:

> Make it sound professional.

Better:

> Use a neutral, direct tone.

Add more tone criteria only when the audience or domain requires them.

---

### Missing Fallback

Weak:

> Use the provided data to answer.

Better:

> Answer from provided data. State missing required data.

Add a field list only when specific fields are required.

---

### Unsupported Metric Estimate

Weak:

> Switch modes when the context window is nearly full.

Better:

> Switch modes on visible context-pressure signs. Do not estimate exact limits without telemetry.

---

### State Architecture Note

Weak:

> Keep applying this mode later.

Better:

> Re-apply this standing request from conversation history; the skill stores no state.

---

### Silent Transition

Weak:

> Return to normal when the task concludes.

Better:

> Return to normal silently when the task concludes.

---

### Terse Format Preservation

Weak:

> Update format: `Now / Found / Next / Verified`.

Better:

> Routine update: `Now / Found / Next`. Add `Verified` only for validation claims.

---

### Unsupported Completion Claim

Weak:

> After editing, tell the user the issue is fixed.

Better:

> Report what changed and what validation supports it. Mark unverified parts.

---

### Hard-to-Test Quality Goal

Weak:

> Ensure the instructions are robust.

Better:

> Add missing edge-case, fallback, and completion rules where they affect execution.

---

### Over-Narrow Example

Weak:

> Always rewrite “be clear” as “use short sentences.”

Better:

> Define what “clear” requires in context.

---

### Script or Validator Gap

Weak:

> Add a validator for the new rule.

Better:

> Add a failing check for the new rule, or explain why manual review is more appropriate.

---

### Tool or Permission Gap

Weak:

> Check the external system and update the record.

Better:

> If access is available, update the record. If not, state the missing access and do not claim completion.

---

## Output Modes

Choose the mode that matches the user’s request.

### Full Rewrite

```text
Rewritten version:
[Improved text]
```

### Annotated Review

```text
Issue:
[What is hard for agents to execute]

Failure mode:
[How execution could fail]

Suggested rewrite:
[Smallest sufficient improvement]
```

### Before / After Table

```text
| Original | Risk | Improved |
|---|---|---|
| ... | ... | ... |
```

### Minimal Patch

```text
Minimal edit:
[Smallest change that improves execution]
```

### Guardrail Preservation Review

Use when a cleaner or shorter version may have removed defensive behavior.

```text
Guardrail review:
- Preserved: [compact rule that prevents failure]
- Restored: [removed guardrail and why it matters]
- Removed: [text that was only repetition or padding]
```

### Compression Pass

```text
Compression summary:
- Removed: [repetition/detail inflation]
- Preserved: [critical behavior or guardrail]
- Added: [only if needed for execution]

Compressed version:
[Revised text]
```

### Version Upgrade Audit

Use when the user asks to audit and improve an existing skill, script, package, or generated artifact.

```text
Audit summary:
- [Issue category]: [impact]

Changes in [new version]:
- [Change]: [why it improves execution]

Guardrail check:
- [Preserved or restored defensive rule]
- [Removed only if obsolete, duplicated, or wrong]

Compression check:
- [Where wording was shortened or expansion was avoided]

Validation:
- [Check performed]: [result]
- [Unverified item, if any]: [reason]

Updated content or artifact:
[Full revised skill, patch, or generated file link]
```

For version upgrades, the agent must:

1. read the existing version and identify its operational job;
2. preserve useful rules unless they conflict with the upgrade goal;
3. check whether a cleaner version removed guardrails, architecture notes, silent-transition instructions, terse formats, scope limits, or evidence rules;
4. restore removed safeguards in compact form when they prevent likely failure;
5. update the version number and version-specific notes;
6. check internal consistency across frontmatter, title, description, version, examples, output modes, and self-checks;
7. perform a compression check so examples do not imply longer text is better;
8. validate the generated artifact when possible;
9. report performed validation and unverified items without overstating certainty.

---

## Final Self-Check

Before returning revised text, verify:

- The rewrite preserves original intent and operational safeguards.
- The rewrite is the shortest version that still supports correct execution.
- Added detail prevents a real execution failure.
- Removed detail was not a compact defensive guardrail.
- Required actions use observable verbs.
- Long instructions are split only when splitting improves parsing.
- Subjective wording has behavioral criteria when it affects execution.
- Missing-input behavior is defined where needed.
- Conflict priority is clear where relevant.
- Whole-outcome responsibility is explicit and bounded when needed.
- Evidence requirements support completion claims.
- Unsupported telemetry, context limits, state, permissions, or tool access are not guessed.
- Architecture notes are kept when they prevent false state or persistence assumptions.
- Silent transitions remain silent when meta-commentary would be noise.
- Terse formats stay terse unless added fields are conditionally required.
- Script or validator requirements define pass/fail behavior when relevant.
- Tool or permission limits are handled without unsupported claims.
- Handoff markers, placeholders, and audit statuses cannot be mistaken for open work.
- Examples teach reusable judgment, not fixed replacements.
- Examples do not imply that longer rewrites are better.
- Completion can be validated when the task changes artifacts, records, code, scripts, validators, or data.
- Token use is efficient: no repeated prose, unnecessary examples, decorative wording, or detail inflation.

Return the improved version clearly. If validation is partial, state the limitation.
