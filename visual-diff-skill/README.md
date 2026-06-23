# visual-diff-skill 0.2.0

Standalone, agent-ready raster image comparison skill.

It produces deterministic JSON metrics, residual statistics, edge/shape evidence, changed-region boxes, object-like component coordinates, visual artifacts, and an audit block with input hashes and runtime metadata.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python visual_diff.py before.png after.png \
  --output-dir visual_diff_report \
  --json-out visual_diff_report/report.json
```

## Validate

```bash
python scripts/smoke_test.py
python scripts/validate_report.py visual_diff_report/report.json
```

See `SKILL.md` for the full agent contract, guardrails, and handoff format.
