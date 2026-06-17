---
name: context-compressor
description: Compress context while preserving task-critical state, exact artifacts, validation, language/tone constraints, and handoff continuity. Use for low-token, brief, compression, continuation, or long-thread state-loss risk.
version: 1.3.1
last_updated: 2026-06-17
---

# Context Compressor

Core invariant: **preserve what changes future work; compress everything else.**

## Activate / stop
Use when the user requests low-token, terse, brief, compressed, continuation, handoff, or task-critical-state preservation; when a system/tool signal indicates compaction, truncation, limited context, or token pressure; or when state-loss risk is visible: long thread, large pasted content, repeated tool output, multiple changed files, accepted decisions, non-obvious findings, or unresolved validation.

Do not use for ordinary article summaries, one-off shortening, or code review unless the user also wants compact mode or continuation state. Explicit compact mode persists until the user asks for normal/detail or the task ends. Proactive use is temporary for the current phase or handoff.

## Priority ladder
1. Safety, privacy, permissions, policy.
2. Required tool/artifact workflow, validation, citations, fixed formats, and exact user constraints.
3. Latest user request for detail, code, examples, language, tone, or format.
4. Compression.

When another skill applies, run that skill's required workflow and compress only narration, repeated setup, logs, and nonessential explanation.

## Operating rules
- Answer the latest request first; put requested code, decision, artifact, or summary before background.
- Use the smallest sufficient form: micro update, concise answer, dense-source note, or full handoff.
- In long work, mention only new action, finding, verification, blocker, changed next step, or material risk.
- Prefer exact identifiers: paths, symbols, branches, issue numbers, dates, commands, tests, source names, line ranges.
- Ask at most one clarifying question only when blocked; otherwise state a safe behavior-affecting assumption and proceed.
- Preserve requested language, tone, register, domain terms, grammar quirks, and localization constraints when material.
- Never translate, normalize, paraphrase, reorder, or repair protected literals unless asked: code, commands, logs, errors, regexes, schemas, API signatures, config keys, URLs, paths, prompts, placeholders, names, quotes, multilingual text, and fixed-format fields.
- Do not claim exact token savings, remaining context window, truncation risk, coverage, validation, or completion without visible telemetry or evidence.

## Preserve / compress
Preserve: active goal, latest correction, superseding instructions, safety/permission/tool/citation/format constraints, plan state, blockers, decisions, behavior-changing assumptions, files changed, commands run, test/validation status, remaining work, owner/next action, source anchors, and minimal code/content structure needed to continue.

Compress/drop: rejected or superseded alternatives, filler, motivational language, redundant caveats, repeated process explanations, raw logs after extracting failures/status, large pasted content after extracting facts/decisions/risks, and large code blocks after retaining interfaces and action-critical snippets.

## Output formats
Micro update: `Now: ... / Found: ... / Next: ...` Use only populated fields.

Dense source:
```markdown
Path/Source: ...
Symbols/Topic: ...
Behavior/State: ...
Evidence: ...        (tests, commands, citations, anchors, or "not verified")
Issues/Risks: ...
Needed exact: ...    (small action-critical snippets only)
```

Full handoff:
```markdown
Goal: ...
State: ...
Decisions: ...
Assumptions: ...
Changed: ...
Verified: ...
Next: ...
Risks: ...
```

## Resume / quality gate
After compaction, continuation, or resume, treat summaries as working notes. Re-check load-bearing facts before acting: latest user request, file existence/content, current branch, changed files, failing tests, external state, citations, tool outputs, and superseded instructions.

Before sending, verify: latest request answered; required exact tokens preserved; language/tone constraints kept; no unsupported telemetry claims; no required workflow was skipped for brevity.
