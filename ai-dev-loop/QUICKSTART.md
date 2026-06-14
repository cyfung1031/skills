# AI Development Loop Quickstart

Use this when you want the fastest safe install path.

## 1. Stage the package

Extract the zip into an empty temporary/staging directory, not directly into a live project root.

## 2. Install into a project

Recommended:

```bash
python3 scripts/install-ai-dev-loop-template.py /path/to/project
```

The installer creates `.ai-dev-loop/` from the package root files. It includes the compact `SKILL.md`, `REFERENCE.md`, placeholder `status.md`, and empty review/response/context/decision directories.

Minimal manual equivalent:

```bash
test ! -e /path/to/project/.ai-dev-loop || { echo ".ai-dev-loop already exists"; exit 1; }
mkdir -p /path/to/project/.ai-dev-loop/{reviews,responses,context,decisions}
printf "%s\n" "# AI Development Loop Coordination Directory" > /path/to/project/.ai-dev-loop/README.md
printf "%s\n" "Create NNNN-context.md files for compact durable handoffs." > /path/to/project/.ai-dev-loop/context/README.md
printf "%s\n" "Create NNNN-decision.md files only for durable decisions." > /path/to/project/.ai-dev-loop/decisions/README.md
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

## 3. Start the loop

Tell your coding assistant:

```text
Use .ai-dev-loop/SKILL.md as the operating instructions.
Read .ai-dev-loop/status.md. Begin with R unless status says K is next.
Write durable records under .ai-dev-loop/ and update status.md before finishing the role turn.
```

## 4. Validate a package revision

```bash
python3 scripts/validate-ai-dev-loop-package.py
```

## Version

**Version**: 1.3.3
**Last Updated**: 2026-06-14
