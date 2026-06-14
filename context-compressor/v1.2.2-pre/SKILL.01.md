---
name: context-compressor
description: Compress and conserve conversation context by using terse responses, compact progress updates, explicit context pruning, compact code/content summaries, and concise handoff summaries. Use when the user asks to reduce token usage, avoid excessive context consumption, compress context, summarize current state, keep replies brief, switch to low-token mode, preserve only task-critical facts, or prepare a compact continuation summary for a long thread.
version: 1.2.2
last_updated: 2026-06-14
---

# Context Compressor

Minimize context growth while preserving the state needed to continue accurately. This skill should practice what it preaches: keep it short.

## When to use

Activate when any of these hold:

- The user asks to reduce tokens, keep replies brief, compress context, summarize current state, preserve only task-critical facts, switch to low-token mode, or prepare a continuation/handoff summary.
- A system, developer, runtime, or tool signal indicates compaction, truncation, continuation, limited context, or token pressure.
- The thread is long enough that losing earlier decisions, files, tests, constraints, or non-obvious findings would cause rework or correctness risk.

"Long enough" is qualitative, not token math. Use signs such as 10+ substantial turns, large pasted content, repeated tool output, multiple changed files, or several accepted decisions. Do not activate only because a task is mildly complex or because a simple question appears inside an old thread.

Not this skill: one-off document/article summarization, one-off shortening of a single answer, or ordinary code review. Those are normal tasks unless the user also asks for a standing compact mode or continuation summary.

Mode duration:

- User-requested low-token mode is standing. Re-apply it on each relevant turn until the user asks for normal, verbose, or detailed mode, or until the task ends.
- Proactive activation is temporary. Use it for the current phase, compaction event, or handoff, then return to normal when the task concludes or shifts to an unrelated goal.
- Mention a mode change only if the user asks about mode/state, silence would confuse them, or the final output is a handoff/summary.

## Operating mode

Default to short, direct answers: 1-4 bullets or one compact paragraph unless the user asks for detail. In a long task:

- State the current action and why it matters only when an update is needed. Do not restate stable instructions, settled decisions, or raw command output.
- Replace verbose reasoning with decisions, assumptions, and verification results.
- Prefer exact identifiers, such as file paths, command/test names, symbols, branches, issue numbers, and dates.
- When blocked, ask at most one clarifying question; otherwise make a reasonable assumption and proceed.
- Record an assumption only when it affects behavior, scope, safety, correctness, or output format.

## Priority when brevity conflicts

Brevity never overrides correctness, safety, required workflow, or explicit user needs. Resolve in this order:

1. Safety, privacy, permissions, policy.
2. Required tool/artifact workflow, validation, citations, format constraints.
3. The user's latest explicit request for detail, full code, examples, or explanation.
4. Compression and terse style.

If the user requests both terse and detailed output, answer the concrete ask first in the most useful form. If they ask for code, start with the code or patch, then add a brief note. If they ask for a decision or diagnosis, start with the conclusion, then give only needed detail. Use a summary-first layout only when it improves usability and does not delay the requested artifact or answer.

When another skill also applies, follow its substantive workflow. Use this skill only to cut narration and repeated setup. Do not drop required validation, citations, safety checks, artifacts, tool steps, or requested detail.

## What to keep vs. drop

Keep: active goal and latest correction; constraints affecting behavior, safety, permissions, citations, or format; current plan state; blockers; decisions; behavior-changing assumptions; files changed; commands run; test status; remaining work and immediate next action; non-obvious findings from code, tools, docs, or sources; minimal code structure needed to continue, such as paths, public interfaces, names, data shapes, invariants, error messages, or changed logic.

Drop or compress: rejected alternatives; full command logs after summarizing the result; repeated explanations of standard process; large pasted content after extracting relevant facts; large code blocks after capturing structure, intent, interfaces, and risky details; filler, motivational language, and redundant caveats.

## Compressing code

Do not preserve full code blocks by default. Summarize structurally unless exact code is needed next:

```markdown
Path: file/repo path or source label
Symbols: function/class/API names and signatures
Behavior: what it does
State: inputs, outputs, side effects, dependencies
Issues: bugs, failing tests, stack traces, risky edges
Needed: exact snippets still required, if any
```

Keep exact snippets only when small and necessary: a failing line, stack frame, regex, query, schema, migration, prompt, config key, API signature, patch-sized block, or code where whitespace, ordering, quoting, or syntax is the point.

## Handoff and update formats

Full handoff: use when asked to compress, hand off, continue, or prepare a continuation. Also use it after a compaction/truncation/token-pressure signal when preserving state matters. Omit empty fields.

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
Verified: `npm test -- tax-rounding` passed. Full suite not run.
Next: Run full tests.
Risks: Multi-currency fixtures may hide another rounding path.
```

Rules for handoff fields:

- `Verified` must name the evidence used, such as a command, manual check, or source reviewed. If validation is partial or absent, state that.
- `Next` must name the next owner/action when it is not the current agent continuing immediately.
- `Risks` must include unresolved blockers, unverified assumptions, or likely rework causes.

Ordinary update: use only the fields carrying new information. Do not pad for rhythm:

```markdown
Now: ...       (current action or status)
Found: ...     (new discovery, result, blocker, or verification outcome)
Verified: ...  (evidence, only when a check just happened)
Next: ...      (only if the next step changed or would otherwise be unclear)
```

## Response rules

Answer the latest request first: requested code, artifact, or decision goes before background summary. Use dense but readable wording, summaries over transcripts, and exact dates, paths, branches, issue numbers, and test names when relevant. State uncertainty in one sentence rather than hiding it. Expand only when accuracy, safety, citations, validation, required workflow, or the user's explicit request demands it.
