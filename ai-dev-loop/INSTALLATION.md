# AI Development Loop — Tool-Agnostic Installation Guide

## Overview

The **AI Development Loop** is a tool-agnostic workflow for AI-assisted software development. It uses two durable roles:

- **R — Reviewer/Auditor**, who audits specs, plans, implementation, risks, and evidence.
- **K — Implementer/Keeper**, who responds to R, performs whole-change impact scans, updates specs/docs/examples/tests/harness artifacts, modifies the real repository, validates changes, and records evidence.

The loop is intentionally generic. v1.4.2 reduces SKILL.md token load while preserving open-finding carry-forward, code-doc-test consistency gates, explicit clarification/objection gates, and the terminal R review gate. Any comparable assistant can use it when the assistant can read and edit a repository, run commands, and maintain local git history. Named tools are only adapter examples, not requirements.

Unresolved K questions or objections are not advisory chatter; they are loop gates. K responses are also not terminal approval: after K responds, R must review the evidence before the loop can stop. R must answer, revise, uphold with evidence, or accept risk before expecting further K implementation. R findings are not a task checklist for K; implementation updates must include all directly related documentation, example, validation, installer, package, and status-template consistency fixes, including affected files R did not explicitly mention.

The only hard requirements are:

- the agent can follow persistent instructions from `SKILL.md` or an equivalent prompt file,
- the agent can read and write project files,
- the workspace is or can become a git repository,
- R/K handoff records are written under `.ai-dev-loop/` or an equivalent project-specific directory.

If local commits cannot be created because of environment limits, the agent can update only safe documentation/bootstrap files by default. Code/spec/test implementation changes require explicit degraded-mode authorization. The agent must record `Commit: not committed: <reason>`, dirty paths, and the intended `R: ...` or `K: ...` commit message in the R/K record and `status.md`.
When a record and `status.md` are committed together, `pending current commit` is valid only for that same-turn commit timing problem. Historical readers must treat it as closed evidence for that committed turn, not as degraded mode.

## Safe extraction rule

Extract the zip into a new empty staging directory first, then copy or install only the intended files into the project root. The v1.4.2 zip uses a clean root layout with no wrapper directory and no root `.ai-dev-loop/` template folder, so staging prevents accidental mixing with unrelated workspace files.

## Fastest Safe Install

From the staged package directory:

```bash
python3 scripts/install-ai-dev-loop-template.py /path/to/project
```

Use `--dry-run` to preview. The installer refuses broad directories and refuses to overwrite an existing `.ai-dev-loop/` unless `--force` is supplied. Dry-run uses the same safety gates as a real install, so previewing a replacement still requires `--force`, and previewing replacement of live R/K records still requires `--force-live-records`. With `--force`, the installer first renames the existing directory to a timestamped `.ai-dev-loop.backup-YYYYMMDD-HHMMSS` directory, then installs the fresh template. Prefer manual merge over `--force` for projects that already have live R/K records.

## Installation Options

### Option 1: Project-local instructions, recommended and most portable

Install the complete project-local coordination directory so any coding assistant can read the instructions and write durable records:

```bash
python3 scripts/install-ai-dev-loop-template.py /path/to/project
```

Then start your coding assistant and instruct it:

```text
Use .ai-dev-loop/SKILL.md as your operating instructions for this repository.
Read .ai-dev-loop/status.md. Begin with R unless status says K is next.
Write durable records under .ai-dev-loop/ and update status.md before finishing the role turn.
```

This works with most tools because it avoids vendor-specific skill directories while creating the full `status.md`, `reviews/`, `responses/`, `context/`, and `decisions/` skeleton.

### Option 2: Tool-specific skill or instruction directory

Some tools support global reusable skills, custom instructions, or prompt libraries. Install the same `SKILL.md` there, using your tool's documented location.

Examples:

```text
Tools with skill/plugin support: install or reference this package through that mechanism.
CLI coding agents: reference `SKILL.md` from the project prompt, repository instructions, or command invocation.
IDE-based agents: add `SKILL.md` to project rules, workspace instructions, or pinned context.
Other agents: place `SKILL.md` wherever persistent workspace instructions are read.
```

Do not depend on any vendor-only command unless your selected tool explicitly requires it.

### Option 3: Manual template mode

Prefer the installer above. The package no longer ships a duplicate root `.ai-dev-loop/` template folder. For a manual install, create the coordination directory, copy the root instruction files, and create a project-specific `status.md`:

```bash
test ! -e /path/to/project/.ai-dev-loop || {
  echo ".ai-dev-loop already exists; refusing to overwrite"
  exit 1
}
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

None yet; first R review must populate any blockers, required findings, or unresolved K questions/objections.

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

Then update `.ai-dev-loop/status.md` with the current project focus and start the first R review. The `.ai-dev-loop/` directory is hidden in many file browsers, so verify it exists when installing manually.

## Package Validation

Before distributing a modified package, run:

```bash
python3 scripts/validate-ai-dev-loop-package.py
```

The validator checks canonical approval statuses, required package files, required example headings, stale example language, installer presence, clean packaging artifacts, compact-skill size, and R/K template consistency. It also checks documented version consistency across the package.

## Bootstrap Directory

When the workflow starts, the agent creates this structure if it does not already exist:

```text
.ai-dev-loop/
  README.md
  reviews/
  responses/
  decisions/
  context/
  status.md
```

The workflow is incomplete until durable markdown records exist for the active R/K turn.

## Quick Start Prompt

Use this prompt with any compatible coding assistant:

```text
Please use .ai-dev-loop/SKILL.md for this repository.
Bootstrap .ai-dev-loop/ if needed.
Act as R first: audit the current specs, roadmap, and implementation plan.
Write the review to .ai-dev-loop/reviews/NNNN-r-review.md, update status.md, and commit the coordination records.
```

If R has already produced a review and K is next:

```text
Please use .ai-dev-loop/SKILL.md for this repository.
Act as K: read the latest R review and status.md, respond in .ai-dev-loop/responses/NNNN-k-response.md, update specs/code/tests as needed, update status.md, and commit the changes.
```

## Expected Workflow

```text
User asks agent to start or continue the loop
        ↓
R reviews specs/plans/code and writes .ai-dev-loop/reviews/NNNN-r-review.md
        ↓
R updates .ai-dev-loop/status.md and commits
        ↓
K reads durable records, responds, performs a whole-change impact scan, updates specs/docs/examples/code/tests/harness artifacts, writes .ai-dev-loop/responses/NNNN-k-response.md
        ↓
K updates .ai-dev-loop/status.md and commits
        ↓
R re-reviews until no required follow-up remains
```

## Key Directories and Files

**`.ai-dev-loop/reviews/`**

R's review findings, severity levels, approval decisions, and evidence.

**`.ai-dev-loop/responses/`**

K's responses, spec updates, implementation notes, test results, and remaining work.

**`.ai-dev-loop/context/`**

Compact handoff notes for long loops, milestone transitions, or when future agents may otherwise depend on stale chat context.

**`.ai-dev-loop/decisions/`**

Durable blocker, escalation, and product/architecture decision records. It may stay empty when no such decision exists.

**`.ai-dev-loop/status.md`**

The single source of truth for current focus, approval state, latest R/K records, active blockers, and next expected role.

## Git Integration

The workflow expects strict local git discipline:

- every R review and status update must be committed with an `R: ...` subject,
- every K response and status update must be committed with a `K: ...` subject,
- every spec/code/test update must be included in the relevant `K: ...` commit,
- `status.md` must be synchronized before a role turn is complete.

Useful checks:

```bash
git status --short
git branch --show-current
git log --oneline -n 20
```

## Tool Adapter Notes

### Tools with skill or plugin support

Use the tool's skill, plugin, rules, or custom-instruction mechanism if available, or use project-local `.ai-dev-loop/SKILL.md`.

### CLI coding agents

Place `SKILL.md` in the repository and tell the agent to load it as the operating instructions. If your CLI setup supports repository instruction files, reference or copy this content there.

### IDE-based agents

Add `SKILL.md` to project rules, workspace instructions, or a pinned context file. The important part is that the agent reads the rules before editing and writes durable R/K records afterward.

### Other coding agents

Use the same pattern: persistent instructions + real repository edits + git commits + durable `.ai-dev-loop/` records.

## Troubleshooting

### The agent keeps relying on chat memory

Tell it to reconstruct state only from git, repository files, `.ai-dev-loop/status.md`, and the latest R/K records. Important chat facts must be copied into `.ai-dev-loop/context/` before use.

### The agent skips `status.md`

Ask it to apply the Status Synchronization Gate from `SKILL.md`. A role turn is incomplete while `status.md` points to stale R/K files.

### The agent says a review is approved but lists required fixes

Ask it to apply the Approval Status Precision rule. `Approved with notes` means no required K follow-up. Required High/Medium findings mean `Changes requested` or separate spec/implementation statuses.

### Validation or tests fail

K must document the exact command, result, likely cause, whether the failure is pre-existing or introduced, and the next action. R must not approve implementation unless failures are resolved or explicitly proven unrelated.

## Version

**Version**: 1.4.2
**Last Updated**: 2026-06-16

## Git Bootstrap Default

Before initializing git, the agent checks `git rev-parse --show-toplevel` to detect an existing repository, worktree, submodule, or parent repository. The skill allows `git init` only when that command fails, the current directory is confirmed as the intended project root, and the directory is not `$HOME`, `/`, `/mnt/data`, or another broad container/workspace parent. The agent must not push, configure remotes, or change external repository settings unless the user explicitly requests it.

If git cannot be initialized or commits cannot be created, the agent records degraded mode in `status.md` and the current R/K record. It lists changed paths. It does not proceed with code implementation beyond safe documentation/bootstrap work unless explicitly authorized.


## Documentation consistency gate

K must keep documentation/specs/examples plus validators, scripts, installer/package guidance, and status templates aligned with behavior or workflow changes, or record why no related artifact update is needed. R must check for these discrepancies before approval.
