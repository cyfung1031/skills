# AI Development Loop Installation Guide

## Requirements

- A repository or project directory the assistant is authorized to read and edit.
- Python 3 for the installer and validator.
- Permission to create a project-local `.ai-dev-loop/` directory.

## Recommended installation

```bash
python3 scripts/install-ai-dev-loop-template.py /path/to/project
```

The installer copies `SKILL.md` and `modules/LOOP-HARNESS.md`, creates `status.md`, installs the concise state checker, and creates `reviews/`, `responses/`, `context/`, `decisions/`, and `scripts/` under `/path/to/project/.ai-dev-loop/`.

## Installer safety behavior

The installer refuses broad directories such as `/`, `/mnt`, `/mnt/data`, `/tmp`, `/var/tmp`, `/workspace`, `/workspaces`, `/home`, and the user home directory. It also refuses unmarked project roots unless `--allow-unmarked-root` is used, and refuses existing `.ai-dev-loop/` directories unless force flags are explicit.

## Safe replacement

```bash
python3 scripts/install-ai-dev-loop-template.py /path/to/project --force
```

If live records exist, both flags are required:

```bash
python3 scripts/install-ai-dev-loop-template.py /path/to/project --force --force-live-records
```

Use force only after preserving or migrating existing records.

## Manual install

Manual install is acceptable only when the script cannot run. This is a fallback, not a task checklist for bypassing installer safety.

```bash
test ! -e /path/to/project/.ai-dev-loop || { echo ".ai-dev-loop already exists"; exit 1; }
mkdir -p /path/to/project/.ai-dev-loop/{reviews,responses,context,decisions,scripts}
printf "%s\n" "# AI Development Loop Coordination Directory" > /path/to/project/.ai-dev-loop/README.md
cp SKILL.md /path/to/project/.ai-dev-loop/SKILL.md
mkdir -p /path/to/project/.ai-dev-loop/modules
cp modules/*.md /path/to/project/.ai-dev-loop/modules/
cp scripts/check-ai-dev-loop-state.py /path/to/project/.ai-dev-loop/scripts/check-ai-dev-loop-state.py
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

Run the first R review against available specs, plans, roadmap, tickets, issue notes, diffs, or design docs. If none exist, record the missing requirements as the safe stopping point.

## Blockers

Template only. No project-specific requirements have been loaded yet.
EOF
```

## Whole-change responsibility

Installation only creates the loop. During operation, K still owns whole-change impact checks. R findings are not exhaustive task lists, and affected docs, tests, examples, validators, installers, or package guidance must be updated even when R did not explicitly mention them.

## Degraded environments

If commands, git, network, file writes, external systems, or human authority are unavailable, record the limitation, safe partial path, validation not run, and exact next role action. Do not claim skipped validation or unrun commands passed.

## Token-efficient state check

After installation, use this helper to get a concise mechanical summary before loading long records:

```bash
python3 /path/to/project/.ai-dev-loop/scripts/check-ai-dev-loop-state.py /path/to/project
```

The summary targets reads and does not replace source evidence, R judgment, K responsibility, or terminal R approval.
