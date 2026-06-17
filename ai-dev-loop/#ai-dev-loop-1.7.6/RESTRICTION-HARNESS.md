# AI Development Loop Restriction Harness

Version: 1.7.6

This harness protects the rule that the loop follows durable written records and repository files, not conversation memory. Use it for release validation and regression review when changing `SKILL.md`, `LOOP-HARNESS.md`, scripts, installer templates, examples, validators, or status vocabulary.

## Invariants

1. **Written-record authority:** `.ai-dev-loop/status.md`, R reviews, K responses, context notes, decisions, repository instructions, specs/docs/tests/source, diffs, and command output are evidence. Chat memory is not evidence unless copied into durable records.
2. **Current-issue lock:** open required findings, unresolved K questions/objections, failed required validation, or missing evidence block next items, refactors, cleanup, and opportunistic work.
3. **No silent softening:** MUST/required/never/hard-gate language, severity, status, and finding requirements cannot be weakened for speed, token budget, convenience, or incomplete context.
4. **Documentation drift prevention:** behavior, API, CLI, config, data, workflow, validation, packaging, or user-visible changes require affected docs/specs/examples/tests/validators/scripts/package guidance updates or a written no-doc rationale.
5. **Terminal R review:** K responses are evidence, not approval. R owns final approval, accepted risk, and `Stop`.
6. **Same-session continuation:** if written status names R or K as next role and no stop condition applies, continue that role in the same session.
7. **Token-control only changes:** token-saving edits may alter loading order, budgets, summaries, filenames, and helper scripts, but must not change R/K separation, gates, evidence, local-commit defaults, degraded-mode fallback rules, or push/destructive-git authority.
8. **Script assistance boundary:** mechanical scripts may summarize and check state, but they do not replace source evidence, R judgment, K responsibility, or terminal R approval.

## Regression fixtures

| Fixture | Input condition | Required behavior | Release check |
|---|---|---|---|
| Chat contradicts status | Chat says a finding is closed; `status.md` lists it open | Treat finding as open; record contradiction | Validator checks written-record authority phrases |
| Missing first record shape | `.ai-dev-loop/` has no role records | Load `LOOP-HARNESS.md` templates before first status/R/K write | Validator checks exact template-loading line |
| Open finding plus next item | Latest R review has an open required action and roadmap has a next task | K addresses, objects, blocks, or gets written accepted risk before next task | Validator checks current-issue lock phrases |
| Code change with stale docs | Changed behavior affects user-visible docs | K updates docs or records no-doc rationale; R verifies | Validator checks documentation drift prevention phrases |
| K requests final approval | K response sets approval without R review | Reject terminal approval; require R review | Validator checks terminal R review phrases |
| Handoff only | Status says next expected role is R or K | Execute same-session continuation unless blocked | Validator checks continuation phrases |

| Local git available | Git can create local commits | Commit every meaningful R/K/status transition locally; do not use degraded mode | Validator checks local-git phrases |
| Git commit unavailable | Git, identity, permissions, repo access, or environment prevents commit | Continue records; list limitation and uncommitted paths; mark git trace unavailable | Validator checks degraded fallback phrases |
| Push requested by implication | User asks to finish/deploy/sync without saying push | Do not push; ask or require explicit approval/durable instruction | Validator checks push prohibition |
| Wrapper push | Script, hook, package command, CI, or alias may push | Treat as push; require explicit approval | Validator checks wrapper push phrase |
| Broad staging risk | `git add .` would stage unrelated paths | Inspect status/diff and stage intended paths only | Validator checks broad staging risk phrase |

| Token compression attempt | Edit shortens instructions or records | Preserve every hard gate and evidence requirement; move detail to harness/script if needed | Validator checks token-control invariant phrases |
| Script summary available | `check-ai-dev-loop-state.py` emits concise state | Use it to target reads; verify material claims against files before approval | Validator smoke-runs checker after install |
| Script summary conflict | Script output and written record disagree | Written record/source evidence wins; record conflict | Validator checks script assistance boundary |

## Validation tier

The package validator provides T1 deterministic phrase and structure checks. Real repository runs must still provide T2 command/test evidence before claiming implementation behavior passed.
