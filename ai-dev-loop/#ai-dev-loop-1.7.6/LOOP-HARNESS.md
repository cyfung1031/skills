# AI Development Loop Runtime Harness

This runtime harness expands the compact `SKILL.md`. Use it only when templates, package work, degraded modes, objections, release consistency, terminal review, or uncertain record shape need more detail.


## Glossary and compact concepts
- **R:** reviewer role that opens, closes, or accepts risk for findings.
- **K:** implementer role that changes artifacts and records validation evidence.
- **Finding:** source-grounded issue or note with severity, status, and required outcome.
- **Response:** K's evidence-backed answer to each open finding.
- **Status:** canonical project state in `.ai-dev-loop/status.md`.
- **Evidence:** observed file, diff, command, test, log, commit, status, record, or explicit limitation.
- **Handoff:** concise next-role instruction with scope, files, validation, risks, and open items.
- **Accepted risk:** R-owned closure that leaves a known risk intentionally unresolved.

## Mode details
Minimal mode is for small known-file work with clear acceptance criteria. It reduces prose and repeated explanation, not source identity, R/K separation, validation-tier honesty, status updates, whole-change responsibility, or R-owned closure. Escalate to release mode when the task touches package versions, manifest entries, validator logic, installers, scoring artifacts, examples, archives, or conflicting package files.


## Token budget and loading order
Default to `SKILL.md`, `scripts/check-ai-dev-loop-state.py` output when available, `status.md`, latest required R/K records, and directly affected source files. Load this harness only for first-record templates, uncertain record shape, degraded-mode details, terminal acceptance, package/release work, scoring details, or contradiction handling. Keep records compact by using tables, path references, command summaries, and context/audit files for long evidence. Token savings may compress wording and automate checks, but must not remove required gates, evidence, validation honesty, or local-commit/degraded-mode rules.

## Written-record authority and restriction harness
The loop must be recoverable from files alone. At every role boundary, rebuild the active state from `.ai-dev-loop/status.md`, latest R/K records, context notes, decisions, repository instructions, specs/docs/tests/source, diffs, and command output. Conversation context can point to likely files, but it is not evidence unless copied into a durable record.

Written records and repository files control: open findings, status values, approval, accepted risk, validation evidence, changed-file scope, and next role. If chat conflicts with written records, use the stricter safe interpretation, record the contradiction, and require R or human written acceptance before weakening the requirement.

When creating the first R/K/status record, or when record shape is uncertain, load `LOOP-HARNESS.md` templates before writing.

## Operational command pattern
Use this repeatable sequence for each role turn: load written state; identify current focus, open required findings, and next expected role; perform only the current issue; update directly affected artifacts; run validation or cap claims; write R review or K response; synchronize `status.md`; continue same-session to the next role unless blocked, missing authority, no safe action exists, or R records terminal approval.

## Current-issue lock and no silent softening
Latest R review plus `status.md` open-finding ledger is a hard gate. K must address every current R-required issue and all directly related consistency fallout before any next implementation, roadmap item, refactor, cleanup, or opportunistic work. K cannot skip, reorder, batch around, defer, or silently weaken current R-required issues. K must fix with evidence, ask R, object with evidence, prove unsafe/impossible, block, or obtain written R/human accepted risk.

No silent softening: do not reinterpret MUST, required, never, hard gate, severity, status, or finding language as advisory for speed, token limits, tool limits, or convenience. Compress wording, not obligations.

## Documentation drift prevention and terminal review
Documentation drift prevention is a hard gate: changed behavior is not complete while docs, specs, examples, tests, validators, scripts, installer notes, package guidance, or user-visible instructions are stale. K records `Documentation Updates` or a source-grounded no-doc rationale; R verifies code-doc-test consistency with file or diff evidence.

Terminal R review is required. A K response can request review but can never be final approval. The loop ends only when R records `Approved` or `Approved with notes` with no required K follow-up and `Next Expected Role Action: Stop`. If `Next Expected Role Action` names R or K, writing that field is not enough; continue in the same session unless a stop condition applies.

## Claim cap table
| Claim type | Allowed support | Cap |
|---|---|---|
| Observed | Read file, diff, log, status, record, or user-provided source | State what was visible only. |
| Measured | Command, test, script, checksum, deterministic fixture, or API/model run in this task | State exact command and output boundary. |
| Inferred | Direct reasoning from observed or measured evidence | Mark as inference and name missing evidence. |
| Assumed | Plausible but unchecked premise | Do not use as release proof. |
| Unavailable | Capability, input, or authority missing | Record limitation and safe fallback. |

## R review record template

```markdown
# R Review NNNN: <topic>

## Scope
Files, specs, diffs, commits, commands, or records reviewed. State explicit limits.

## Summary
Decision summary and risk posture.

## Evidence
- Branch: `<branch or limitation>`
- Git status: `<clean/dirty/unavailable plus reason>`
- Recent commits reviewed: `<commits or None>`
- Files reviewed: `<paths>`
- Commands run: `<exact commands or None>`
- Coverage: `<scope and exclusions>`
- Validation result: `<pass/fail/limited/not run plus reason>`

## Findings

### Finding R-NNNN-01: <title>
- Severity: Critical | High | Medium | Low | Note
- Status: Open | Closed | Accepted risk
- Type: Bug | Spec gap | Test gap | Documentation gap | Process issue | Security | Performance | Maintainability | Packaging | Validation | Other
- Location: `<path:line or path>`
- Evidence: `<source-grounded support>`
- Details: `<problem>`
- Required action: `<observable outcome or None for note>`

## Clarifications Needed
None. OR numbered questions.

## Clarification and Objection Responses
None. OR responses to pending K questions/objections.

## Approval Status
- Spec/Plan Status: Not started | Changes requested | Approved for implementation | Approved with notes | Approved | Not applicable
- Implementation Status: Not started | Changes requested | Pending implementation | Approved with notes | Approved | Not applicable
- Overall Status: Blocked | Changes requested | Pending implementation | Approved with notes | Approved

## Next Expected K Action
One exact next action or `No K action required`.
```

## K response record template

```markdown
# K Response NNNN: <topic>

## Review Addressed
Path to R review, finding IDs, and commit/status harness if available.

## Summary
What changed and what remains.

## Evidence
- Branch: `<branch or limitation>`
- Git status: `<clean/dirty/unavailable plus reason>`
- Files changed: `<paths or None>`
- Commands run: `<exact commands or None>`
- Finding coverage: `<each open finding addressed, objected, or blocked>`
- Whole-change impact scan: `<direct and indirect affected artifacts checked; not a complete mechanical task list>`
- Validation result: `<pass/fail/limited/not run plus reason>`
- Known limitations: `<None or details>`

## Finding Responses

### Response to R-NNNN-01
- Status: Addressed | Partially addressed | Not addressed | Objected | Blocked
- Changes made: `<paths and behavior>`
- Evidence: `<file/diff/command/test/log/limitation>`
- Notes: `<risk, rationale, or carry-forward>`

## Spec Updates
None. OR affected specs/plans.

## Documentation Updates
None with rationale. OR affected docs/examples/guides.

## Implementation Updates
None. OR affected source/scripts/config/data.

## Tests and Validation
- Command: `<exact command>`
- Working directory: `<path>`
- Exit status: `<code>`
- Output summary: `<summary>`
- Failures: `<None or details>`
- Skipped checks: `<None or details and acceptable/blocking rationale>`

## Clarifications or Objections
- Questions for R: None. OR numbered questions.
- Objections: None. OR finding ID with source-grounded rationale.

## Compact Context
Goal: ...
State: ...
Decisions: ...
Changed: ...
Verified: ...
Next: ...
Risks: ...

## Next Expected R Action
One exact next action.
```

## Status vocabulary
Use only these canonical values.

- **Spec/Plan Status:** Not started; Changes requested; Approved for implementation; Approved with notes; Approved; Not applicable.
- **Implementation Status:** Not started; Changes requested; Pending implementation; Approved with notes; Approved; Not applicable.
- **Overall Status:** Blocked; Changes requested; Pending implementation; Approved with notes; Approved.

Most restrictive wins. Missing safe input or missing authority is `Blocked`. Any unresolved required finding, unresolved K question, unresolved K objection, or failed required validation is `Changes requested`. R alone can close required findings or accept risk.

## Whole-change impact scan
K must evaluate the whole change, not only files listed by R. A literal bullet list and file mentions from R are not a complete mechanical task list. Behavior/API/CLI/config/data/workflow/validation/packaging/user-visible changes can require source, tests, docs, examples, validators, installers, schemas, migration notes, release notes, and package guidance even if R did not explicitly list them.

## K objection and blocker rules
K should object instead of making unsafe or unsupported edits when a finding is unclear, contradicted by source evidence, already satisfied, outside authority, destructive, or dependent on unavailable credentials. The response must name the finding, cite evidence, describe safe partial work, and set the next expected R action. K may not silently drop a finding.

## Local git authority model
Local commits are mandatory audit records when git can commit; degraded mode is fallback only when commit creation is unavailable; remote, wrapper, destructive, or shared-history git operations require explicit authority.

## Degraded environments
When git, commands, network, file writes, external systems, or human authority are unavailable, record: unavailable capability, attempted command or inspection if any, exact error or limitation, safe partial path, validation not run, and whether the limitation blocks approval. Do not present skipped validation as passed.

## Context compression
Create `.ai-dev-loop/context/NNNN-context.md` when state is long, cross-session continuity is likely, or a milestone handoff occurred. Preserve open findings, blockers, changed paths, validation limits, decisions, status values, and the next expected role. Compress repeated prose; never compress away evidence required for audit.

## Package/release checklist
Release work must verify all of the following:
1. Required files and directories exist.
2. No root `.ai-dev-loop/` directory ships in the package.
3. Examples remain under `examples/.ai-dev-loop/` and are clearly illustrative.
4. Installer refuses broad paths and existing live records unless explicit force flags are used.
5. Validator checks required files, headings, canonical status values, R/K templates, whole-change guidance, artifact hygiene, installer smoke behavior, version harnesss, and manifest checksums.
6. Docs, examples, scripts, and manifest agree on version, paths, and vocabulary.
7. No `__MACOSX`, `.DS_Store`, caches, editor metadata, compiled Python, temporary files, or live project state ship.
8. `python3 scripts/validate-ai-dev-loop-package.py` passes from the package root.
9. `PACKAGE-MANIFEST.json` is regenerated after all file changes.
10. The zip contains a single clean top-level directory and excludes forbidden artifacts.


## Contradiction handling
When package files disagree, record the conflict before editing broadly. Manifest/file mismatches require inventory verification and manifest regeneration. Passing validation with stale examples or docs is not release-ready; treat the stale artifact as an open finding. If README, SKILL, harness docs, validator, installer, schemas, or examples disagree, apply the stricter safety/evidence requirement until R records a decision.

## Package-diff audit
For version synthesis or release edits, include a changed-file summary that explains why each changed file was necessary. Mark unchanged files that were intentionally preserved. Link each material change to a finding, contradiction, validation requirement, usability improvement, or release hygiene rule.

## Terminal acceptance checklist
Before terminal approval, verify closed or accepted-risk findings, resolved objections, validation evidence, status consistency, changed-file summary, manifest checksums, directly affected artifacts, residual risk, and one final next action.

## Decision record guidance
Use `.ai-dev-loop/decisions/NNNN-decision.md` only when a durable decision changes future behavior or review assumptions. Include context, options considered, decision, evidence, rejected risks, owner, date, and follow-up.

## Release acceptance
Accept a release update only when it improves production effectiveness, fixes a high-severity failure without regression, or reduces safe operating cost without deleting required behavior. Stop when further edits are cosmetic, duplicative, or token-expanding. Before packaging, keep user-facing files focused on behavior, usage, constraints, validation, and maintenance. Put audit-only notes outside the package unless the user requests them.
## Scoring schema and evidence ledger
For comparative review, challenged-score, or benchmark work, keep `SCORING-EVIDENCE-SCHEMA.json` as the category and claim-cap contract. Evidence rows must name candidate, category, relevance, score, evidence tag, source locator, positive evidence, missing evidence, confidence, validation tier, and cap applied.
## Fixture contract
Benchmark fixtures are release artifacts when used for scoring. Treat malformed fixtures as build failures. Do not repair format by trial-and-error after a live run unless the correction audit records the failed fixture and obsolete claim.


## Release-note hygiene
User-facing package files must not mention unrelated internal revision processes, private review labels, hidden synthesis history, score provenance, or process archaeology unless the user explicitly asks for a separate audit artifact.
