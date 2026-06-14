# Skill: Agent Readability Review

**Name:** `agent-readability-review`
**Description:** Improves documents, prompts, policies, and skill files so agents can understand, operationalize, and execute them reliably. Focuses on ambiguous wording, weak verbs, long or nested sentences, human-only phrasing, unclear success criteria, and instructions that are difficult for agents to turn into actions.
**Version:** `1.0.0`

---

## Purpose

Use this skill when reviewing or improving any text that an AI agent, workflow agent, or automation system needs to read and act on.

The goal is not merely to make text sound better for humans. The goal is to make the text easier for agents to parse, decide from, and execute.

This skill helps transform instructions from:

> “Try to make the answer helpful and avoid being too vague.”

into:

> “Before answering, identify the user’s goal, list any missing required inputs, and provide the most specific answer possible using the available information. Do not use vague phrases such as ‘various things’ unless the source text is also vague.”

---

## When to Use This Skill

Use this skill when the source text is intended to guide behavior, especially in:

* Skill files
* System prompts
* Agent instructions
* SOPs
* Workflow documentation
* Review rubrics
* Policy-like documents
* Tool-use instructions
* Templates agents must fill in or follow
* Human-written documents that will be processed by agents

Do not use this skill only for grammar polishing. Apply it when clarity affects execution.

---

## Core Review Angle

Review the text from an **agent-readability angle**.

Ask:

> “Could an agent reliably convert this sentence into the right action?”

Look for places where the text depends on human intuition, unstated context, taste, or judgment without giving an operational path.

---

## What to Improve

### 1. Ambiguous Wording

Find wording that can be interpreted in multiple ways.

Weak:

> Handle the file appropriately.

Improved:

> Determine the file type. If it is a document, summarize its main sections. If it is a spreadsheet, inspect the column headers and identify calculation or data-quality issues. If the file type is unsupported, state that clearly.

Why this is better:

* The agent knows what “appropriately” means.
* Different cases are separated.
* The fallback behavior is specified.

---

### 2. Weak Verbs

Replace vague verbs with action verbs that imply a concrete operation.

Weak:

> Consider the user’s preferences.

Improved:

> Identify any explicit user preferences in the request and apply them before using default assumptions.

Weak:

> Make the document better.

Improved:

> Rewrite unclear instructions, split long sentences, replace vague verbs, and add missing success criteria where needed.

Good agent-readable verbs include:

* identify
* extract
* compare
* rewrite
* classify
* validate
* flag
* preserve
* remove
* convert
* summarize
* ask
* cite
* verify
* apply
* return

Do not rely on a fixed word list. Choose verbs that make the required action observable.

---

### 3. Long or Nested Sentences

Break sentences that contain multiple conditions, exceptions, or actions.

Weak:

> When reviewing a file, if it appears to contain operational instructions and some parts are unclear or too dependent on context, improve them where possible while keeping the original intent and avoiding changes that might affect meaning.

Improved:

> When reviewing a file, first decide whether it contains operational instructions.
> If it does, identify unclear or context-dependent instructions.
> Rewrite those instructions so the required action is explicit.
> Preserve the original intent.
> Do not change requirements unless the source text is internally inconsistent.

Why this is better:

* Each sentence contains one action or condition.
* The order of operations is clear.
* The preservation constraint is explicit.

---

### 4. Human-Only Phrasing

Flag phrases that rely on human social judgment, taste, or intuition without explaining how to act.

Weak:

> Make it sound professional.

Improved:

> Use a neutral, direct tone. Remove slang, emotional exaggeration, and unnecessary humor. Keep technical terms only when they help the intended reader act correctly.

Weak:

> Use common sense.

Improved:

> If the instruction does not specify a required behavior, choose the lowest-risk interpretation and state the assumption briefly.

Human-readable phrasing is acceptable when the text is for humans only. For agent-facing instructions, convert subjective phrases into observable behaviors.

---

### 5. Hard-to-Operationalize Instructions

Identify instructions that describe a desired quality but not how to achieve it.

Weak:

> Be thorough.

Improved:

> Check the title, purpose, inputs, outputs, constraints, edge cases, and failure behavior. Report any missing or conflicting information.

Weak:

> Avoid confusion.

Improved:

> Define each role, input, output, and decision point before using it. Avoid pronouns when the referent could be unclear.

---

## Review Process

When applying this skill, use the following process.

### Step 1: Identify the Text’s Job

Determine what the text is supposed to make the agent do.

Ask:

* Is this instruction meant to guide behavior?
* Is it explaining a process?
* Is it defining a rule?
* Is it describing a desired output?
* Is it setting limits or exceptions?

If the text has no operational purpose, apply lighter edits.

---

### Step 2: Find Agent-Readability Risks

Look for:

* Vague modifiers: “good,” “better,” “proper,” “clear,” “reasonable”
* Hidden assumptions
* Missing inputs or outputs
* Long sentences with multiple actions
* Rules without fallback behavior
* Exceptions without priority order
* Pronouns with unclear referents
* Soft verbs such as “consider,” “try,” “handle,” “deal with,” “make sure”
* Human-only phrasing such as “use judgment,” “be sensible,” “as appropriate”
* Goals without success criteria

Do not mechanically replace every vague word. First decide whether the ambiguity affects execution.

---

### Step 3: Rewrite for Execution

When rewriting, prefer:

* Direct action verbs
* One instruction per sentence
* Explicit conditions
* Explicit outputs
* Clear priority order
* Clear fallback behavior
* Concrete examples
* Minimal but sufficient context
* Preservation of original intent

Use this pattern when helpful:

```text
When [condition], do [action].
If [case], do [specific action].
If [missing information], do [fallback action].
Return [expected output].
Do not [forbidden behavior].
```

---

### Step 4: Preserve Scope

Do not make the instruction narrower than necessary.

Avoid turning a general instruction into a brittle checklist unless the source text clearly requires that.

Weak overcorrection:

> Replace the words “good,” “appropriate,” “nice,” “proper,” and “clear” everywhere.

Better:

> Replace vague quality words when they affect execution. Keep them only when surrounding instructions already define the expected behavior.

---

### Step 5: Add Examples Only Where They Teach a Pattern

Examples should help agents generalize.

Good example:

> “Review the document carefully” can become “Check whether each section has a clear purpose, required inputs, expected outputs, and failure behavior.”

This teaches a reusable pattern.

Weak example:

> Always rewrite “carefully” as “check sections.”

This is too narrow.

---

## Output Options

Depending on the user’s request, provide one of the following.

### Option A: Full Rewrite

Use when the user wants an improved version.

Output:

```text
Rewritten version:
[Improved text]
```

### Option B: Annotated Review

Use when the user wants feedback.

Output:

```text
Issue:
[What is hard for agents to operationalize]

Why it matters:
[How it could cause execution errors]

Suggested rewrite:
[Improved version]
```

### Option C: Before / After Table

Use when comparing many small changes.

Output:

```text
| Original | Issue | Improved |
|---|---|---|
| ... | ... | ... |
```

### Option D: Minimal Patch

Use when the user wants to preserve the original style.

Output:

```text
Minimal edit:
[Smallest change that improves agent readability]
```

---

## Quality Bar

A strong agent-readable instruction should answer:

1. What should the agent do?
2. When should it do it?
3. What inputs should it use?
4. What output should it return?
5. What should it avoid?
6. What should it do when information is missing?
7. Which rule wins if instructions conflict?

Not every sentence needs to answer all seven. The document as a whole should answer the ones relevant to its purpose.

---

## Examples

### Example 1: Vague Instruction

Original:

> Make the summary useful.

Problem:

> “Useful” is a goal, not an operation. The agent does not know what to include or exclude.

Improved:

> Summarize the main decision, supporting reasons, unresolved questions, and any action items. Omit background details that do not affect the user’s next step.

---

### Example 2: Weak Verb

Original:

> Consider safety concerns.

Problem:

> “Consider” does not specify whether to identify, explain, refuse, or modify the answer.

Improved:

> Identify safety-sensitive parts of the request. If the request could enable harm, refuse that part and provide a safer alternative.

---

### Example 3: Long Sentence

Original:

> If the user provides a document and asks for improvements, review it for clarity, tone, structure, and consistency while preserving the author’s intent and not adding unsupported claims unless needed.

Improved:

> If the user provides a document and asks for improvements, review clarity, tone, structure, and consistency.
> Preserve the author’s intent.
> Do not add unsupported claims.
> If a claim is needed but missing, flag it as a suggested addition instead of inserting it as fact.

---

### Example 4: Human-Only Phrasing

Original:

> Use your best judgment when deciding whether to ask follow-up questions.

Problem:

> The agent needs criteria for when to ask and when to proceed.

Improved:

> Ask a follow-up question only when a required input is missing and proceeding would likely produce an incorrect or unusable result. Otherwise, state the assumption and continue.

---

### Example 5: Hard-to-Operationalize Requirement

Original:

> Ensure the instructions are robust.

Problem:

> “Robust” is not directly testable.

Improved:

> Check whether the instructions define normal behavior, edge cases, missing-input behavior, and conflict resolution. Add these details where they are necessary for reliable execution.

---

## Final Self-Check

Before returning the improved text, verify:

* The rewrite preserves the original intent.
* Vague goals are converted into executable actions.
* Long instructions are split into smaller steps.
* Subjective wording is supported by behavioral criteria.
* The agent can tell what to do when information is missing.
* Examples teach general patterns, not only one-off replacements.
* The revised text is not over-specified or unnecessarily narrow.

Return the improved version clearly. If changes are substantial, briefly explain the main categories of improvement.
