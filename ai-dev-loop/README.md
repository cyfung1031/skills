# AI Development Loop

AI Development Loop is a tool-agnostic workflow package for efficient, auditable AI-assisted software development. It defines a durable two-role loop:

- **R — Reviewer/Auditor**, who audits specs, plans, implementation, risks, and evidence.
- **K — Implementer/Keeper**, who responds to R, performs whole-change impact scans, updates all directly affected repository artifacts, validates changes, and records evidence.

## Fast path

1. Extract the zip into an empty staging directory.
2. Run `python3 scripts/install-ai-dev-loop-template.py /path/to/project`.
3. Tell your coding assistant: `Use .ai-dev-loop/SKILL.md and begin with R unless status.md says K is next.`

## File map

- `QUICKSTART.md` — shortest safe installation path.
- `SKILL.md` — canonical compact operating instruction file; sufficient for normal role turns.
- `REFERENCE.md` — optional expansion for edge cases, degraded mode, blockers, context compression, and release/package work.
- `scripts/install-ai-dev-loop-template.py` — creates a project-local `.ai-dev-loop/` template with compact skill, reference, status file, and record directories.
- `examples/.ai-dev-loop/` — illustrative R/K records.
- `examples/.ai-dev-loop/status.md` — example placeholder status, not live project state.
- `scripts/validate-ai-dev-loop-package.py` — release/package validation.
- `INSTALLATION.md` and `COMPLETE-PACKAGE-GUIDE.md` — detailed setup and package guidance.

## Important notes

This package does not ship a root `.ai-dev-loop/` directory. The installer generates that directory inside your target project. Replace the generated placeholder `status.md` with project-specific status before the first R review.

For safest installation, extract the zip into a new empty staging directory first, then copy or install only the intended files into the target project.

Examples are illustrative and use placeholder commit hashes. Real use requires actual repository state, commands, changed files, validation results, and local commit hashes when available. v1.4.2 reduces SKILL.md token load by compressing sections duplicated across `## Gates`, `## Core principles`, and `## Autonomous workflow`; moves validator/installer hardening detail to `REFERENCE.md`; and adds an optional-omission rule for `## Next Item` / `## Blockers` in live `status.md`. Safety model, explicit R/K clarification and objection gates, terminal R review gate, and whole-change impact scan responsibility are unchanged. R findings are required outcomes, not exhaustive task lists. K must fix directly related docs/examples/tests/validator/installer/package discrepancies discovered while implementing, even when R did not name those files explicitly.
Committed historical records may contain `pending current commit` for the same commit that introduced the record/status update; later turns must treat that literal value as a closed audit marker, not as missing evidence.

## Version

**Version**: 1.4.2
**Last Updated**: 2026-06-16
