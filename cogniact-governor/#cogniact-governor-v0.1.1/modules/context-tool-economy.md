# Context and tool economy

Context, tool calls, and user attention are budgets. Load only what improves the next decision or final answer.

## Loading strategy

1. Start with names, headings, metadata, search results, diffs, or summaries.
2. Open only relevant regions, rows, pages, functions, or snippets.
3. Expand outward when references, tests, contradictions, or risk require it.
4. Record compact conclusions so they are not re-derived.

Keep user requirements, decisions, authoritative facts, file paths, commands run, verification results, unresolved risks, and the current stop rule. Drop long logs after extracting the failing line, repeated boilerplate, irrelevant alternatives, and source text that does not change the outcome.

## Tool-use rules

- Use tools when they reduce uncertainty, risk, or manual token work more than they cost.
- Batch independent reads, searches, and checks when the platform supports it.
- Prefer targeted queries and narrow commands over broad browsing or full-file reads.
- Prefer deterministic scripts for counting, formatting, validation, packaging, and repeated checks.
- Use existing project commands and conventions before inventing new workflows.
- Use current authoritative sources for facts that may have changed; use local files for user-provided or repository-specific truth; use screenshots or visual inspection when layout, images, charts, or PDFs matter.

## Failure handling

Read the relevant error, adjust once using evidence, and avoid retry loops. Retry transient infrastructure failures only briefly. If failure blocks success, report the blocker, the consequence, and the best completed partial result.
