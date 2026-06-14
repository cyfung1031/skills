# AI Development Loop — Complete Package Guide

## Overview

This package contains a **tool-agnostic AI Development Loop** for software projects. It defines a durable two-role workflow:

- **R — Reviewer/Auditor** reviews specifications, plans, implementation, risks, and evidence.
- **K — Implementer/Keeper** responds to R, updates specs, implements code in the real repository, validates changes, and records evidence.

The package is designed for any comparable repository-editing coding assistant. Named tools are only adapter examples; the workflow itself does not depend on a vendor-specific command, directory, or UI feature.

## What's Included

### Root Files

**`QUICKSTART.md`**

- Fastest safe install path
- One-command template installer usage
- Minimal assistant prompt for starting the loop

**`SKILL.md`**

- Canonical compact operating instructions for normal R/K turns
- Role responsibilities and mandatory markdown templates
- Status synchronization, evidence, approval, degraded-mode, and git-discipline rules

**`REFERENCE.md`**

- Optional expansion for edge cases, release/package maintenance, blockers, and complex handoffs
- Not required for simple role turns, preserving the compact-skill efficiency advantage

**`INSTALLATION.md`**

- Portable installation guidance
- Project-local setup
- Adapter notes for common classes of coding agents

**`scripts/install-ai-dev-loop-template.py`**

- Safe project-local installer for the `.ai-dev-loop/` template
- Refuses broad directories and existing live `.ai-dev-loop/` directories by default

**`scripts/validate-ai-dev-loop-package.py`**

- Package invariant validator
- Checks canonical approval statuses, required package files, required example headings, stale language, installer presence, clean packaging artifacts, absence of a duplicate root `.ai-dev-loop/`, and documented version consistency

### Coordination Directory

The installed project-local `.ai-dev-loop/` directory is the durable handoff layer. The distributable zip intentionally does not ship a duplicate root `.ai-dev-loop/` template folder; use the installer or the manual commands below to create it inside the target project. Because dot-directories are hidden by default in many file browsers, verify the generated directory exists after installation:

```text
/path/to/project/.ai-dev-loop/
├── README.md
├── SKILL.md
├── REFERENCE.md
├── status.md
├── reviews/
├── responses/
├── context/
└── decisions/
```

### Example Review/Response Records

The included examples show how the loop works in practice:

- R writes review records under `reviews/`.
- K writes response records under `responses/`.
- Long-running or transition-heavy loops write compact handoffs under `context/`.
- Blockers, escalations, and durable product or architecture decisions go under `decisions/`.
- `status.md` is updated after each role turn.

## How to Use This Package

### Option 1: Fast template install, recommended

From the staged package directory:

```bash
python3 scripts/install-ai-dev-loop-template.py /path/to/project
```

This installs `SKILL.md`, optional `REFERENCE.md`, placeholder `status.md`, and the required record directories while refusing broad paths and existing live loop state by default.

Then tell your coding assistant:

```text
Use .ai-dev-loop/SKILL.md as the operating instructions for this repository.
Bootstrap .ai-dev-loop/ if needed and continue from status.md.
```

This is the most portable approach because it works with nearly any coding agent.

### Option 2: Tool-specific skill/rules installation

If your tool supports global skills, custom rules, or persistent instructions, install or reference the same `SKILL.md` through that mechanism.

Examples:

```text
Tools with skill/plugin support: install or reference this package through that mechanism.
CLI coding agents: reference `SKILL.md` from the project prompt, repository instructions, or command invocation.
IDE-based agents: add `SKILL.md` to project rules, workspace instructions, or pinned context.
Other coding agents: place `SKILL.md` wherever the agent reads persistent instructions.
```

Tool-specific setup is only an adapter. The required workflow remains the same: `.ai-dev-loop/` records, synchronized `status.md`, evidence-backed validation, and local git commits when git is available; otherwise degraded-mode limitations must be recorded.

### Option 3: Manual project-local instructions

When you do not want to copy the full template, copy only the compact skill and optional reference:

```bash
test ! -e /path/to/project/.ai-dev-loop || { echo ".ai-dev-loop already exists"; exit 1; }
mkdir -p /path/to/project/.ai-dev-loop/{reviews,responses,context,decisions}
printf '%s\n' '# AI Development Loop Coordination Directory' > /path/to/project/.ai-dev-loop/README.md
printf '%s\n' 'Create NNNN-context.md files for compact durable handoffs.' > /path/to/project/.ai-dev-loop/context/README.md
printf '%s\n' 'Create NNNN-decision.md files only for durable decisions.' > /path/to/project/.ai-dev-loop/decisions/README.md
cp SKILL.md /path/to/project/.ai-dev-loop/SKILL.md
cp REFERENCE.md /path/to/project/.ai-dev-loop/REFERENCE.md
cat > /path/to/project/.ai-dev-loop/status.md <<'EOF'
# AI Development Loop Status

## Current Branch

Template only. Replace with the project branch before starting the first R review.

## Current Focus

Template only. Replace this file with project-specific status before starting the first R review.

## Latest R Review

None.

## Latest K Response

None.

## Latest Context Note

None.

## Decisions

None.

## Approval State

- Spec/Plan Status: Not started
- Implementation Status: Not applicable
- Overall Status: Blocked

## Open Required Findings

None yet; first R review must populate any blockers or required findings.

## Completed Items

None.

## Next Expected Role Action

R bootstrap review.

## Next Item

Run the first R review against the available specs, plans, roadmap, tickets, or design notes. If none exist, record the missing requirements as the safe stopping point.

## Blockers

Template only. No project-specific requirements have been loaded yet.
EOF
```

Then update `.ai-dev-loop/status.md` for the project and start the first R review.

Before distributing a modified package, run:

```bash
python3 scripts/validate-ai-dev-loop-package.py
```

## Quick Start Prompts

### Start a new loop

```text
Please use .ai-dev-loop/SKILL.md for this repository.
Act as R first. Audit the current specs, roadmap, and implementation plan.
Write .ai-dev-loop/reviews/NNNN-r-review.md, update status.md, and commit the coordination records.
```

### Continue after an R review

```text
Please use .ai-dev-loop/SKILL.md for this repository.
Act as K. Read status.md and the latest R review, respond in .ai-dev-loop/responses/NNNN-k-response.md, update specs/code/tests as needed, update status.md, and commit the changes.
```

### Continue after a K response

```text
Please use .ai-dev-loop/SKILL.md for this repository.
Act as R. Read status.md and the latest K response, review the durable evidence and repository changes, write the next review, update status.md, and commit the records.
```

## Understanding the Examples

The examples demonstrate the workflow rather than a tool-specific transcript.

### How R Reviews Work

R should:

- read the relevant specs, plans, code, tests, git history, and `.ai-dev-loop/` records,
- identify gaps, contradictions, risks, missing evidence, and required follow-up,
- classify findings by severity,
- distinguish spec approval from implementation approval,
- write a durable review file,
- update `status.md`,
- commit the review and status changes.

### How K Responses Work

K should:

- read R's latest review fully,
- respond finding-by-finding,
- update specs before implementation when requirements are unclear,
- modify the real repository working tree directly,
- run validation commands where feasible,
- write a durable response file,
- update `status.md`,
- commit the response, specs, code, tests, and status changes.

### Context Notes

`context/` should not be used for every small turn. It should be used when the loop is long, a milestone transitions to another phase, the next agent would otherwise need stale chat context, or the latest status cannot compactly explain the current state.

### Decision Records

`decisions/` may stay empty when there are no durable blockers or human/product decisions. Create a decision file when a choice affects architecture, safety, compliance, data loss, user-visible behavior, or when the R/K loop hits a circuit breaker.

## Quality Gates

Before R approval, the records should show:

- latest R/K files are referenced by `status.md`,
- all required template sections are present,
- required findings are resolved or explicitly deferred,
- spec and implementation status are not conflated,
- validation commands and results are recorded,
- known limitations are disclosed,
- git history contains focused local commits when git is available; otherwise degraded-mode limitations must be recorded,
- the real repository working tree was modified, not a detached artifact copy.

## Approval Semantics

Use precise status wording:

```text
Approved: no required follow-up remains.
Approved with notes: no required follow-up remains, but non-blocking observations exist.
Changes requested: required follow-up exists.
Blocked: human/product/architecture decision is required.
```

For plan-to-implementation transitions, use the canonical three-line status block:

```text
Spec/Plan Status: Approved for implementation
Implementation Status: Not started
Overall Status: Pending implementation
```

This avoids saying a project is fully approved when only the plan is approved.

## Tool Adapter Notes

### Tools with skill or plugin support

Use the tool's skill, plugin, rules, or custom-instruction mechanism if available, or use the project-local `.ai-dev-loop/SKILL.md` approach.

### CLI coding agents

Keep `SKILL.md` in the repository and instruct the agent to use it as operating instructions. If your setup has repository instruction files, copy or reference this content there.

### Chat-based coding agents

Attach or place `SKILL.md` in the workspace and ask the agent to follow it before editing. Ensure it writes `.ai-dev-loop/` records and commits real repository changes when git is available; otherwise records degraded-mode limitations.

### IDE-based agents

Add `SKILL.md` to project rules or pinned workspace context. Require the agent to update `.ai-dev-loop/status.md` and R/K records after each role turn.

### Local LLM coding tools

Use `SKILL.md` as the system prompt or project policy file. The tool only needs file access, command execution, and git access.

## Troubleshooting

### The assistant skips durable records

Tell it: `A role turn is incomplete until the required R/K markdown record and status.md update exist and are committed.`

### The assistant relies on chat memory

Tell it to reconstruct state from git, repository files, `.ai-dev-loop/status.md`, reviews, responses, context notes, and decisions. Important chat facts must be copied to durable markdown before use.

### The assistant says approved while requesting fixes

Apply the approval precision rule. Required fixes mean `Changes requested`, not `Approved with notes`.

### `context/` is empty after a long loop

That is technically allowed only when `status.md` and latest records are enough. For long loops, milestone handoffs, or spec-to-implementation transitions, create a compact context file.

### `decisions/` is empty

That is okay when no blocker, escalation, product decision, architectural decision, or circuit breaker occurred. A README explaining the empty state is helpful but not mandatory.

## Recommended First Command Sequence

From the repository root:

```bash
git status --short
git branch --show-current
mkdir -p .ai-dev-loop/{reviews,responses,context,decisions}
```

Then ask your agent to start as R using the quick-start prompt above.

## v1.3.3 Patch Notes

- Added Open Required Findings carry-forward so unresolved R-required issues survive across role turns and cannot be bypassed by roadmap order.
- Added code-doc-test consistency gates: K records doc/spec/example/test impact or a no-doc rationale; R verifies direct evidence before approval.
- Added scope-change controls so K cannot mix unrelated refactors, dependency changes, cleanup, or formatting churn into an R finding fix.
- Added drift-scan and practical failure-prevention validator safeguards.
- Retained prior 1.3.x packaging fixes, including `REFERENCE.md` status-vocabulary validation.
- Removed embedded pseudo-frontmatter block from `REFERENCE.md` body (cosmetic fix; was confusing to YAML-aware tooling).
- Added `validate_reference_bullet_status_lists` validator check so future bold-header bullet lists in `REFERENCE.md` are verified against the canonical allowed sets.
- Tightened version-consistency regex in validator to exclude dependency-pin comparators (`>=`, `<=`, `!=`, `==`, `~=`, `>`, `<`), avoiding false positives on non-version numeric strings.
- Removed vendor-specific `/home/oai` entry from installer `BROAD_DIRS`; `Path.home()` already covers all user home directories.

## v1.3.3 Maintenance Notes

- Keeps the compact `SKILL.md` and optional `REFERENCE.md` structure.
- Preserves durable R/K separation, evidence-first reviews, status synchronization, git discipline, and degraded-mode honesty.
- Keeps conservative token-efficiency guidance while compressing `SKILL.md` to fit validation budgets.
- Keeps provider-neutral byte, line, word, structure, status, template, and packaging checks.
- Uses the documented clean root zip layout with no wrapper directory.
- Keeps canonical R/K templates unchanged so existing records remain compatible.
- Applies audit fixes: status vocabulary clarification, dry-run documentation, quickstart alignment, and `SKILL.md` size headroom.

## Version

**Version**: 1.3.3
**Last Updated**: 2026-06-14


## Commit-hash timing

A role record and `status.md` are often committed together, so `status.md` may not know the hash of the commit that introduces it. Use `pending current commit` inside that commit instead of inventing a hash; a later role may replace it with the actual hash when useful.

## Git Bootstrap Default

Before initializing git, the agent checks `git rev-parse --show-toplevel` to detect an existing repository, worktree, submodule, or parent repository. The skill allows `git init` only when that command fails, the current directory is confirmed as the intended project root, and the directory is not `$HOME`, `/`, `/mnt/data`, or another broad container/workspace parent. The agent must not push, configure remotes, or change external repository settings unless the user explicitly requests it.

If git cannot be initialized or commits cannot be created, the agent records degraded mode in `status.md` and the current R/K record, lists changed paths, and does not proceed with code implementation beyond safe documentation/bootstrap work unless explicitly authorized.
