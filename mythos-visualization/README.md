# Mythos Visualization Package

This package is standalone and token-efficient. It covers the full agent visual arc: perceive → ground/act → extract → diagnose → link-to-code → verify → trust → appraise.

- `SKILL.md` is the compact always-load kernel.
- `modules/` contains optional markdown packs loaded only when a task needs them (01-07 perceive/route/evidence/corpus/source/output/release; 08 diagnosis; 09 spatial grounding & action targeting; 10 visual trust & injection defense; 11 structured extraction; 12 visual verification & regression; 13 quality/value appraisal; 14 visual-to-code linking, capture-constrained).
- `scripts/` contains mechanical helpers for package state, corpus inventory, report schemas, and weighted-rubric appraisal scoring.
- `skill_contract.json` captures machine-checkable invariants and module references.

## Recommended loading behavior

Load `SKILL.md` first. Load optional modules only when the task trigger matches the table in `SKILL.md`. For ordinary single-image answers, the kernel is sufficient.

## Python checks

```bash
python3 scripts/mythos_state_check.py --package . --write-checksums
python3 scripts/mythos_corpus_probe.py --input /path/to/corpus --output /tmp/mythos_probe
python3 scripts/mythos_report_lint.py --reports sample_reports
python3 scripts/mythos_appraisal_score.py appraisal.json --matrix score_matrix.csv
python3 scripts/mythos_image_meta.py /path/to/image_or_dir --target 320x240 --expect-aspect 16:9
python3 scripts/mythos_contrast.py "#1a1a1a" "#ffffff" --font-pt 14 --bold
python3 scripts/mythos_layout_check.py boxes.json --strict
python3 scripts/mythos_source_locator.py --root ./src --text "Submit" --color "#3366cc" --token btn-primary
```

Scripts compute mechanical/measurable facts only (state, geometry, color math, file metadata). They do not replace visual reasoning or judgment.
