---
name: context-compressor
description: Compress context while preserving task-critical state, exact artifacts, verification, language/tone constraints, and handoff continuity. Use for low-token, brief, compression, continuation, or long-thread state-loss risk.
version: 1.3.0
last_updated: 2026-06-17
---

# Context Compressor

Reduce new context without losing what is needed to continue accurately.

## Activate / stop

Use when the user asks to reduce tokens, keep replies brief, compress/summarize current state, preserve task-critical facts, switch to low-token mode, or prepare continuation/handoff; when a system/tool/runtime signal indicates compaction, truncation, limited context, or token pressure; or when state-loss risk is visible: 10+ substantial turns, large pasted content, repeated tool output, multiple changed files, accepted decisions, or non-obvious findings.

Do not use for one-off document/article summaries, one-off shortening, or ordinary code review unless the user also asks for standing compact mode or continuation state. Explicit low-token mode is standing until the user asks for normal/verbose/detailed mode or the task ends. Proactive activation is temporary for the current phase, compaction event, or handoff; return to normal silently when the task shifts or ends unless silence would confuse the user.

## Priority

Brevity never overrides required behavior:

1. Safety, privacy, permissions, policy.
2. Required tools, artifacts, validation, citations, fixed formats.
3. Latest user request for detail, code, examples, explanation, tone, or language.
4. Compression.

When another skill applies, follow its substantive workflow; compress only narration, repeated setup, transcripts, and nonessential explanation.

## Operating rules

- Answer the latest request first; put requested code, artifact, decision, or summary before background.
- Use the smallest sufficient form: micro status, ordinary update, full handoff, or detailed answer when required.
- Default to 1-4 bullets or one compact paragraph unless detail is requested or required.
- In long work, state only new action, finding, verification, blocker, changed next step, or risk.
- Prefer exact identifiers: paths, symbols, branches, issue numbers, dates, commands, tests, source names, line ranges.
- Ask at most one clarifying question when blocked; otherwise make a safe explicit assumption and proceed.
- Record assumptions only when they affect behavior, scope, safety, correctness, permissions, citations, or output format.
- Preserve requested language, tone, register, domain terms, and grammar quirks when material. Do not translate, normalize, or repair protected literals, multilingual text, names, commands, code, logs, quoted wording, or fixed-format fields unless asked.
- Do not claim exact token savings, remaining context window, truncation risk, coverage, validation, or completion unless supported by visible telemetry or evidence.

## Preserve / compress

Preserve:

- Active goal, latest correction, and superseding instructions.
- Constraints affecting safety, permissions, tools, citations, format, style, language, tone, or acceptance criteria.
- Plan state, blockers, decisions, behavior-changing assumptions, remaining work, owner/next action.
- Files changed, commands run, test/validation status, decision-relevant tool output, source anchors/citations.
- Minimal code/content structure: paths, public interfaces, data shapes, invariants, changed logic, source titles, line ranges.
- Decision/procedure/source essentials: chosen answer and reason, ordered dependencies, required warnings, future-relevant rejected alternatives, evidence anchors for sourced claims.
- Exact protected content: code, errors, logs, regexes, schemas, API signatures, config keys, prompts, user literals, domain terms, names, multilingual text, quotes, placeholders, fixed-format fields, and tokens where spelling/order/whitespace matters.

Compress/drop rejected or superseded alternatives, filler, motivational language, redundant caveats, repeated process explanations, raw logs, large pasted content, and large code blocks after extracting relevant facts, structure, decisions, risks, and action-critical exact snippets.

## Dense-source format

Use for code or dense source material; omit empty fields.

```markdown
Path/Source: ...
Symbols/Topic: ...
Behavior/State: ...
Evidence: ...        (tests, commands, citations, anchors, or "not verified")
Issues/Risks: ...
Needed exact: ...    (small action-critical snippets only)
```

Keep exact snippets only when small and needed: failing line, stack frame, regex, query, schema, migration, API signature, config key, prompt, patch-sized block, or text where whitespace/order/quoting/syntax matters.

## Resume / reverify

After compaction, continuation, or resume, treat summaries as working notes. Before using a load-bearing fact, re-check the latest user request, relevant file existence/content, current branch, changed files, failing tests, external state, citations, tool outputs, and superseded instructions.

## Output formats

Full handoff: use when asked to compress, hand off, continue, prepare continuation, or prevent state-loss rework. Omit empty fields; use absolute dates when relative dates may become ambiguous.

```markdown
Goal: ...
State: ...
Decisions: ...
Assumptions: ...    (behavior-affecting only)
Changed: ...
Verified: ...       (evidence checked; state partial/absent)
Next: ...           (owner/action if not continuing immediately)
Risks: ...          (unverified items, blockers, assumptions, likely rework)
```

Ordinary update: include only fields with new information; add `Verified` only when evidence was checked.

```markdown
Now: ...
Found: ...
Verified: ...
Next: ...
```

## Final quality gate

Before finishing, check that the latest request is answered first; required detail, validation, citations, tools, fixed formats, language/tone, and protected tokens survived; decision/procedure/source anchors remain usable; `Verified` names evidence or `Risks` names what is unverified; no unsupported token/coverage/completion claim is made.
