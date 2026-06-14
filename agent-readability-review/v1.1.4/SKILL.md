---
name: agent-readability-review
description: Improves operational text so AI agents can parse intent, act reliably, and validate completion with the fewest words needed for correct execution.
version: 1.1.4
---

# Skill: Agent Readability Review

## Purpose

Use this skill when text is meant to guide an AI agent, workflow agent, automation, script, validator, reviewer, or human-agent handoff.

Optimize for **minimum sufficient executability**.

Agent-readable text is not automatically longer. It is better when it makes the required action easier to choose, perform, and verify. The best rewrite may be shorter, longer, or the same length as the source.

A rewrite is successful when an agent can answer the relevant questions below without guessing:

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

## Core Principle

Replace vague or hard-to-operationalize text with the **smallest clear instruction that preserves intent**.

Weak:

> Try to make the answer helpful and avoid being too vague.

Better:

> Answer the user’s goal with the most specific supported information. State missing required information.

Why this is better:

- It removes weak verbs.
- It defines the action and fallback.
- It is not padded with extra process.

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
- templates that agents must fill in;
- human-authored documents that agents will process or follow.

Do not use this skill for grammar-only editing unless unclear grammar affects execution.

---

## Review Process

### Step 1: Identify the Operational Job

Classify what the text is trying to make the agent do.

Common jobs:

- guide behavior;
- define a process;
- define a rule;
- constrain tool use;
- specify an output;
- define review or approval criteria;
- describe fallback or error handling;
- coordinate handoff between agents, tools, roles, scripts, or validators;
- validate completion;
- preserve audit or status history;
- produce evidence for later review.

If the text has no operational job, make only light clarity edits.

---

### Step 2: Decide Whether More Detail Is Needed

Before expanding text, ask:

> Would an agent likely choose the wrong action, omit required work, make an unsupported claim, or fail validation without more detail?

If no, prefer a concise rewrite or no change.

Use this decision rule:

| Situation | Preferred action |
|---|---|
| Text is vague but harmless | Leave it or make a light edit. |
| Text is vague and affects execution | Replace it with a direct rule. |
| Text lacks a required condition, output, fallback, or priority | Add only that missing element. |
| Text repeats an existing rule | Remove or reference the existing rule. |
| Text has examples that imply longer is better | Replace with compact examples that teach judgment. |

Do not add operational scaffolding unless it prevents a real execution failure.

---

### Step 3: Locate Agent-Readability Risks

Flag wording when it creates execution risk. Do not flag wording only because it belongs to a broad category.

Look for:

- vague quality terms without behavioral criteria;
- weak verbs that hide the required operation;
- subjective human-only phrasing without decision criteria;
- long sentences with multiple actions, exceptions, or conditions;
- hidden assumptions about reader knowledge, context, tools, permissions, or authority;
- missing inputs, outputs, success criteria, or evidence requirements;
- rules without fallback behavior;
- exceptions without priority order;
- pronouns or references with unclear targets;
- examples that teach one-off replacement instead of reusable judgment;
- review findings that read like optional suggestions when they are required outcomes;
- status, audit, or handoff markers that can be mistaken for open work;
- script or validator behavior without input, output, error, or exit criteria;
- required checks described in prose but absent from templates, validators, examples, or self-checks;
- claims of completion without evidence;
- instructions that require unavailable tools, permissions, data, or external state;
- added detail that increases tokens without improving execution.

A vague term is acceptable when nearby text already defines how to act on it.

---

### Step 4: Diagnose the Failure Mode

For each important issue, identify the execution failure it could cause.

| Failure mode | Meaning |
|---|---|
| Ambiguous action | The agent cannot tell what operation to perform. |
| Ambiguous condition | The agent cannot tell when the rule applies. |
| Missing input | Required data or context is absent. |
| Missing output | The expected return value, change, or record is unclear. |
| Missing fallback | Normal execution can be blocked with no next step. |
| Unclear priority | Rules may conflict and no winner is defined. |
| Unverifiable completion | The agent cannot tell whether the task is done. |
| Unsupported completion claim | The text allows a completion claim without evidence. |
| Over-narrow example | The example encourages brittle pattern matching. |
| Harness gap | Required behavior lacks a template, validator, status field, or self-check. |
| Historical-marker ambiguity | A closed audit marker can be mistaken for open work, or the reverse. |
| Tool or permission gap | The instruction assumes access the agent may not have. |
| Token waste | Extra wording consumes context without improving execution. |
| Detail inflation | The rewrite adds steps that are not required by the source intent. |

Prioritize issues that could cause wrong action, incomplete work, unsafe assumptions, inconsistent records, unsupported claims, or validator blind spots.

---

### Step 5: Rewrite With Minimum Sufficient Specificity

Use only the parts of this pattern that are needed:

```text
When [condition], do [action].
Use [input/evidence/source].
Return [output].
If [blocked], do [fallback].
Do not [forbidden behavior].
Verify by [check].
```

Prefer:

- observable action verbs;
- one instruction per sentence when it improves parsing;
- explicit conditions and outputs only when ambiguity matters;
- named files, fields, tools, or commands only when known and necessary;
- testable success criteria;
- explicit conflict priority when rules may collide;
- fallback behavior for likely blocked states;
- evidence requirements for completion claims.

Do not expand every rule into the full pattern. A one-line instruction is better when it is enough.

Use `can` only for permission. Use `must` for obligations. Avoid soft modal wording for required behavior unless the source intentionally leaves discretion.

---

### Step 6: Preserve Intent, Scope, and Flexibility

Preserve the source text’s intent.

Do not turn a general rule into a brittle checklist.

Weak overcorrection:

> Replace every vague quality word with a fixed phrase.

Better:

> Replace vague quality words only when they affect execution.

When the source intentionally leaves discretion, preserve discretion and define how to report it.

Compact example:

> Choose the lowest-risk interpretation. State the assumption if it changes the output or risk.

---

### Step 7: Check Whole-Outcome Responsibility

When text assigns work to an agent, determine whether the agent owns literal tasks or the whole outcome.

Weak:

> Fix the reviewer’s issues.

Better:

> Resolve each reviewer finding and directly affected files. Record unrelated improvements separately.

Why this is better:

- It prevents narrow literalism.
- It bounds scope.
- It avoids a long list of possible affected artifacts.

Add a detailed list only when the affected artifact types are known and important.

---

### Step 8: Check Evidence and Completion Claims

For tasks that change an artifact, status, rule, validator, data record, or output, verify that completion can be supported.

Weak:

> Confirm that everything works.

Better:

> Report the validation check used. If validation was partial, state what remains unverified.

Define evidence only as specifically as needed. For example, a validator command may be necessary for code; a brief manual review note may be enough for wording changes.

Do not claim full validation when evidence is partial or unavailable.

---

### Step 9: Check Handoff, Status, and Audit Language

For role-based, tool-based, or multi-agent workflows, make later interpretation unambiguous.

Define only the missing pieces needed for reliable handoff:

- durable record location;
- allowed status values;
- evidence field;
- next-action owner;
- open versus closed marker semantics;
- placeholder meaning and replacement rule.

Weak:

> Mark the task as done when complete.

Better:

> Set `status` to `closed` only after validation passes. Record unresolved dependencies as `blocked`.

Historical markers require explicit semantics when they can affect later audits.

Compact rule:

> Treat historical placeholders according to the workflow’s recorded semantics. If semantics are undefined, flag ambiguity instead of guessing.

---

### Step 10: Audit Scripts, Validators, and Harnesses

When the source includes a script, validator, harness, CI rule, package check, or generated artifact, inspect prose and enforcement together.

Check whether the script or harness defines the necessary parts:

- inputs and accepted paths;
- output or report format;
- pass and fail behavior;
- destructive versus read-only behavior;
- missing-file behavior;
- version or schema constants;
- negative tests for required failures;
- consistency between prose and enforced checks;
- unsupported-environment behavior.

Do not add a validator merely because a rule exists. Add validation when behavior is important, observable, and testable. For judgment-based behavior, use a review checklist or evidence note.

Weak:

> The validator checks important fields.

Better:

> The validator fails when a required status field is missing and reports the file path and field name.

---

### Step 11: Reduce Token Use

After improving executability, compress the result.

Remove:

- repeated rules;
- decorative wording;
- motivational prose;
- examples that duplicate earlier examples;
- fixed wording lists when a general rule is enough;
- process steps that do not change the agent’s action.

Prefer:

- short rules;
- compact tables for repeated patterns;
- one strong example over several similar examples;
- references to named sections instead of restating rules;
- examples where the improved version is concise when possible.

Keep redundancy only when it protects a critical behavior across different contexts.

---

## Common Rewrite Patterns

These examples show that agent-readable text is not always longer. Prefer the shortest rewrite that prevents the failure.

### Ambiguous Wording

Weak:

> Handle the file appropriately.

Better:

> Identify the file type and perform the matching file workflow. State if the type is unsupported.

Add file-type branches only when the document actually defines those workflows.

---

### Weak Verb

Weak:

> Consider the user’s preferences.

Better:

> Apply explicit user preferences before defaults.

Add conflict handling only when conflicting preferences are likely or already present.

---

### Long or Nested Sentence

Weak:

> When reviewing a file, if it contains operational instructions, identify unclear or context-dependent parts and rewrite those parts while preserving the original intent.

Better:

> If the file contains operational instructions, rewrite unclear parts into executable rules. Preserve intent.

Split into more steps only when multiple conditions or exceptions cause ambiguity.

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

Add a detailed missing-field list only when the task depends on specific fields.

---

### Unsupported Completion Claim

Weak:

> After editing, tell the user the issue is fixed.

Better:

> Report what changed and what validation, if any, supports the fix.

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

> If access is available, update the record. If not, state the missing access and preserve the record.

---

## Output Modes

Choose the mode that matches the user’s request.

### Full Rewrite

Use when the user asks for an improved version.

```text
Rewritten version:
[Improved text]
```

### Annotated Review

Use when the user asks for feedback or diagnosis.

```text
Issue:
[What is hard for agents to execute]

Failure mode:
[How execution could fail]

Suggested rewrite:
[Smallest sufficient improvement]
```

### Before / After Table

Use when many small edits are easier to compare.

```text
| Original | Risk | Improved |
|---|---|---|
| ... | ... | ... |
```

### Minimal Patch

Use when the user wants the original style preserved.

```text
Minimal edit:
[Smallest change that improves execution]
```

### Compression Pass

Use when the text is already operational but too verbose.

```text
Compression summary:
- Removed: [repetition/detail inflation]
- Preserved: [critical behavior]
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

Compression check:
- [Where wording was shortened or expansion was avoided]

Validation:
- [Check performed]: [result]
- [Unverified item, if any]: [reason]

Updated content or artifact:
[Full revised skill, patch, or generated file link]
```

For version upgrades, the agent must:

1. Read the existing version and identify its operational job.
2. Preserve useful rules unless they conflict with the upgrade goal.
3. Update the version number and version-specific notes.
4. Check internal consistency across title, description, version, examples, output modes, and self-checks.
5. Perform a compression check so examples do not imply that longer text is always better.
6. Validate the generated artifact when possible.
7. Report performed validation and unverified items.

---

## Final Self-Check

Before returning the revised text, verify:

- The rewrite preserves the original intent.
- The rewrite is the shortest version that still supports correct execution.
- Added detail prevents a real execution failure.
- Required actions use observable verbs.
- Long instructions are split only when splitting improves parsing.
- Subjective wording has behavioral criteria when it affects execution.
- Missing-input behavior is defined where needed.
- Conflict priority is clear where relevant.
- Whole-outcome responsibility is explicit and bounded when the agent owns an outcome.
- Evidence requirements are defined for completion claims.
- Script or validator requirements define pass/fail behavior when relevant.
- Tool or permission limits are handled without unsupported claims.
- Handoff markers, placeholders, and audit statuses cannot be mistaken for open work.
- Examples teach reusable judgment, not one-off replacements.
- Examples do not imply that longer rewrites are better.
- Completion can be validated when the task changes artifacts, records, code, scripts, validators, or data.
- Token use is efficient: no repeated prose, unnecessary examples, decorative wording, or detail inflation.

Return the improved version clearly. If validation is partial, state the limitation.
