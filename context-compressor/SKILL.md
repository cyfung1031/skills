---
name: context-compressor
description: Compress and conserve conversation context by using terse responses, compact progress updates, explicit context pruning, compact code/content summaries, and concise handoff summaries. Use when the user asks to reduce token usage, avoid excessive context consumption, compress context, summarize current state, keep replies brief, switch to low-token mode, preserve only task-critical facts, or prepare a compact continuation summary for a long thread.
version: 1.2.1
last_updated: 2026-06-14
---

# Context Compressor

Minimize context growth while preserving enough state to keep working accurately. This skill should practice what it preaches: keep it short.

## When to use

Activate when any of these hold:

- The user asks to reduce tokens, keep replies brief, compress context, summarize current state, preserve only task-critical facts, switch to low-token mode, or prepare a continuation/handoff summary.
- A system, developer, runtime, or tool signal indicates compaction, truncation, continuation, limited context, or token pressure.
- The thread is long enough that losing earlier decisions, files, tests, constraints, or non-obvious findings would cause rework or correctness risk.

"Long enough" is a qualitative judgment, not token math (don't attempt exact window accounting without reliable telemetry): roughly 10+ substantial turns, large pasted content, repeated tool output, multiple changed files, or several accepted decisions. Do not activate just because a task is mildly complex, or because a simple question arrives inside an existing long thread.

Not this skill: one-off document/article summarization, one-off shortening of a single answer, or ordinary code review. Those are normal tasks unless the user also asks for a standing compact mode or continuation summary.

Treat an explicit user request for low-token mode as standing until they ask for normal/verbose/detailed mode or the task ends, and re-apply it on each relevant turn (the skill carries no state of its own — the standing request lives in the conversation history). Proactive activation is temporary: use it for the current phase, compaction event, or handoff, then silently return to normal when the task concludes or shifts to an unrelated goal. Mention the transition only if the user asked about mode/state, if silence would confuse them, or if ending with a handoff/summary.

## Operating mode

Default to short, direct answers — 1-4 bullets or one compact paragraph unless the user asks for detail. In a long task:

- State the current action and why it matters; skip restating stable instructions, settled decisions, or raw command output.
- Replace verbose reasoning with decisions, assumptions, and verification results.
- Prefer exact identifiers — file paths, command/test names, symbols — over prose.
- When blocked, ask at most one clarifying question; otherwise make a reasonable assumption and proceed.
- Record an assumption only when it affects behavior, scope, safety, correctness, or output format. (This rule applies everywhere below.)

## Priority when brevity conflicts

Brevity never overrides correctness, safety, required workflow, or explicit user needs. Resolve in this order:

1. Safety, privacy, permissions, policy.
2. Required tool/artifact workflow, validation, citations, format constraints.
3. The user's latest explicit request for detail, full code, examples, or explanation.
4. Compression and terse style.

So if the user wants both terse and detailed output, answer the concrete ask first in the most useful form. If they asked for code, start with the code or patch, then add a brief note. If they asked for a decision or diagnosis, start with the conclusion, then give only needed detail. Use a summary-first layout only when it improves usability and does not delay the requested artifact/answer. When another skill also applies, follow its substantive workflow and use this skill only to cut narration and repeated setup — never to drop required validation, citations, safety checks, artifacts, tool steps, or requested detail.

## What to keep vs. drop

Keep: the active goal and latest correction; constraints affecting behavior/safety/permissions/citations/format; current plan state, blockers, decisions, behavior-changing assumptions; files changed, commands run, test status, remaining work and immediate next actions; non-obvious findings from code/tools/docs/sources; minimal code structure to continue (path, public interfaces, names, data shapes, invariants, error messages, changed logic).

Drop or compress: rejected alternatives; full command logs once summarized; repeated explanations of standard process; large pasted content once the relevant facts are extracted; large code blocks once structure/intent/interfaces/risky details are captured; filler, motivational language, redundant caveats.

## Compressing code

Don't preserve full code blocks by default — summarize structurally unless exact code is needed next:

```markdown
Path: file/repo path or source label
Symbols: function/class/API names and signatures
Behavior: what it does
State: inputs, outputs, side effects, dependencies
Issues: bugs, failing tests, stack traces, risky edges
Needed: exact snippets still required, if any
```

Keep exact snippets only when small and necessary: a failing line, stack frame, regex, query, schema, migration, prompt, config key, or API signature; a patch-sized block to copy verbatim; or code where whitespace/ordering/quoting/syntax is the point.

## Handoff and update formats

Full handoff — use when asked to compress/hand off/continue, when a trigger above fires, or when preparing a continuation. Omit empty fields.

```markdown
Goal: ...
State: ...
Decisions: ...
Assumptions: ...   (only if behavior-affecting)
Changed: ...
Verified: ...
Next: ...
Risks: ...
```

Example:

```markdown
Goal: Fix checkout tax rounding bug in `billing-service`.
State: Reproduced mismatch on JPY orders; isolated to per-line rounding before discount allocation.
Decisions: Round only after order-level tax aggregation; keep USD behavior unchanged.
Assumptions: Tax API contract cannot change.
Changed: `src/tax/calculate.ts`, `tests/tax-rounding.test.ts`.
Verified: `npm test -- tax-rounding` passes; full suite not run.
Next: Run full tests, then prepare patch summary.
Risks: Multi-currency fixtures may hide another rounding path.
```

Ordinary update — use only the fields carrying new information; don't pad for rhythm:

```markdown
Now: ...     (current action or status)
Found: ...   (new discovery, result, blocker, or verification outcome)
Next: ...    (only if the next step changed or would otherwise be unclear)
```

## Response rules

Answer the latest request first: requested code/artifact/decision goes before background summary. Use dense but readable wording, summaries over transcripts, and exact dates/paths/branches/issue numbers/test names when relevant. State uncertainty in one sentence rather than hiding it. Expand only when accuracy, safety, citations, validation, required workflow, or the user's explicit request demands it.
