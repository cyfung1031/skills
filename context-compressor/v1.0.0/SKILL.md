---
name: context-compressor
description: Compress and conserve conversation context by using terse responses, compact progress updates, explicit context pruning, and concise handoff summaries. Use when the user asks to reduce token usage, avoid excessive context consumption, compress context, summarize current state, keep replies brief, switch to low-token mode, preserve only task-critical facts, or prepare a compact continuation summary for a long thread.
---

# Context Compressor

Use this skill to minimize context growth while preserving enough state to keep working accurately.

## Operating Mode

Default to short, direct answers. Prefer 1-4 bullets or one compact paragraph unless the user asks for detail.

When working in a long task:

- State only the current action and the reason it matters.
- Avoid restating stable instructions, previously accepted decisions, or command output unless needed.
- Replace verbose reasoning with decisions, assumptions, and verification results.
- Prefer file paths, command names, and exact identifiers over prose descriptions.
- Ask at most one clarifying question when blocked; otherwise make a reasonable assumption and proceed.

## Context Pruning

Keep:

- The active user goal and latest user correction.
- Constraints that affect behavior, safety, permissions, or output format.
- Current plan state, blockers, and decisions already made.
- Files changed, commands run, test status, and remaining work.
- Non-obvious facts discovered from code, tools, or external sources.

Drop or compress:

- Old alternatives that were rejected.
- Full command logs after summarizing the result.
- Repeated explanations of standard process.
- Large pasted content after extracting the relevant facts.
- Polite filler, motivational language, and redundant caveats.

## Compression Formats

Use this compact handoff format when the user asks to compress context, when a thread is near compaction, or when preparing a continuation:

```markdown
Goal: ...
State: ...
Decisions: ...
Changed: ...
Verified: ...
Next: ...
Risks: ...
```

For ordinary updates, use:

```markdown
Now: ...
Found: ...
Next: ...
```

Omit empty fields.

## Response Rules

When this skill is active:

- Answer the latest request first.
- Use dense but readable wording.
- Prefer summaries over transcripts.
- Use exact dates, paths, branch names, issue numbers, and test names when relevant.
- Do not hide uncertainty; state it in one sentence.
- Expand only when accuracy, safety, or the user's explicit request requires it.

## Interaction With Other Skills

When another skill is also required, follow that skill's substantive workflow and apply this skill only to reduce narration and context size. Do not skip required validation, citations, safety checks, or user-requested detail just to save tokens.
