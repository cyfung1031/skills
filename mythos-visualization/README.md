# Mythos Visualization v3.1.0 Package

This package is standalone and token-efficient.

- `SKILL.md` is the compact always-load kernel.
- `modules/` contains optional markdown packs loaded only when a task needs them.
- `scripts/` contains mechanical validators for package state, corpus inventory, and report schemas.
- `skill_contract.json` captures machine-checkable invariants and module references.

## Recommended loading behavior

Load `SKILL.md` first. Load optional modules only when the task trigger matches the table in `SKILL.md`. For ordinary single-image answers, the kernel is sufficient.

## Python checks

```bash
python3 scripts/mythos_state_check.py --package . --write-checksums
python3 scripts/mythos_corpus_probe.py --input /path/to/corpus --output /tmp/mythos_probe
python3 scripts/mythos_report_lint.py --reports sample_reports
```

Scripts check mechanical state only. They do not replace visual reasoning.
