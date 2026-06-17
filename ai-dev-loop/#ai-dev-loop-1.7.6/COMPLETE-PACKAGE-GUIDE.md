# AI Development Loop Complete Package Guide

## Purpose

This package installs a durable R/K development loop into a repository. It is tool-agnostic: any repository-editing assistant can use it if it can read files, write files, run allowed commands, and follow project-local instructions.

## Package map

```text
ai-dev-loop/
├── SKILL.md
├── LOOP-HARNESS.md
├── README.md
├── QUICKSTART.md
├── INSTALLATION.md
├── COMPLETE-PACKAGE-GUIDE.md
├── VALIDATION.md
├── PACKAGE-MANIFEST.json
├── scripts/
└── examples/.ai-dev-loop/
```

The distributable package intentionally does not contain a root `.ai-dev-loop/` directory. The installer creates that directory inside the target project.

## Lifecycle

1. R bootstraps by reading status, repository evidence, specs, docs, tests, diffs, decisions, context, and directly affected files.
2. R writes a review with evidence, findings, required outcomes, approval state, and next K action.
3. K addresses every open required finding or records a supported clarification request, objection, or blocker.
4. K performs whole-change responsibility: R findings are not exhaustive K task lists, and source/docs/tests/examples/scripts/validators/installers/package guidance may need updates even if R did not explicitly list them.
5. K validates and records command, working directory, exit status, summarized output, skipped checks, failed checks, and limitations.
6. R performs terminal review, closes findings or requests changes, and updates status.

## Maintenance rules

When behavior changes, update these together as directly affected: `SKILL.md`, `LOOP-HARNESS.md`, README, quickstart, installation guide, package guide, validation notes, examples, installer, validator, and manifest. Keep examples illustrative and separate from live project state.

## Release checklist

1. Confirm required files and directories exist.
2. Confirm no root `.ai-dev-loop/` directory ships in the package.
3. Confirm examples are under `examples/.ai-dev-loop/` and marked illustrative.
4. Confirm installer refuses broad paths and existing live records unless force flags are explicit.
5. Confirm validator checks required files, headings, key phrases, canonical statuses, R/K templates, artifact hygiene, installer smoke behavior, and manifest checksums.
6. Confirm docs, examples, scripts, and manifest agree on version, paths, and operating vocabulary.
7. Confirm no `__MACOSX`, `.DS_Store`, caches, editor metadata, compiled Python, temporary build files, or live records ship.
8. Confirm release contents contain no irrelevant internal process provenance, tool names, generated-by metadata, or build-process labels unless the user requested a provenance appendix.
8. Run `python3 scripts/validate-ai-dev-loop-package.py
│   ├── check-ai-dev-loop-state.py
│   └── estimate-ai-dev-loop-token-cost.py` from the package root.
9. Rebuild `PACKAGE-MANIFEST.json` with current checksums.
10. Create the zip from the parent directory so it contains one clean top-level folder.

## Handoff rule

A package or repository turn is not complete until status, relevant R/K records, validation evidence or limitation, and one next expected role action agree. A new agent should be able to continue from durable files alone.

## Final release gate
Before distribution, verify version-line consistency across metadata, validator constants, installer templates, manifest, docs, examples, schema files, fixture contract, mode table, and release archives. Added artifacts must reduce measurable risk or improve auditability; otherwise do not ship them.

## Token-efficiency controls

Keep `SKILL.md` compact, use `LOOP-HARNESS.md` only for expanded templates/gates, and use `scripts/check-ai-dev-loop-state.py` to summarize mechanical state before loading long records. Use `scripts/estimate-ai-dev-loop-token-cost.py` to compare load sets during package work. These controls may reduce tokens and execution overhead but must not change R/K behavior, evidence requirements, local-commit defaults, degraded-mode fallback, or push/destructive-git authority.
