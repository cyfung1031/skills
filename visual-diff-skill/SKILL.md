---
name: visual-diff-skill
version: 0.2.0
description: Compare two raster images with deterministic pixel, residual, structural, edge, region, object-like component, artifact, and audit outputs. Use for visual regression, screenshot QA, and evidence-backed image-difference reports.
---

# Visual Diff Skill

## Intent and scope

Use this skill when an agent must compare two raster images and give an evidence-backed answer: `same`, `similar`, or `different`.

Best fits:
- UI screenshot regression and design QA.
- Render/photo comparison when exact semantics are not required.
- Locating changed regions, changed edges/lines, and object-like visual components.
- Producing JSON metrics and visual artifacts for handoff or audit.

Out of scope:
- OCR, text extraction, semantic object recognition, identity verification, tamper detection, or forensic authenticity claims.
- Vector/PDF comparison unless pages are first rendered to images.
- Medical, legal, or safety-critical image decisions without expert review.

## Dependencies

```bash
pip install -r requirements.txt
```

Runtime dependencies are intentionally small: Pillow, NumPy, and SciPy.

## Required workflow

1. Save both inputs as local image files.
2. Run the comparator and write a JSON report plus artifacts.
3. Base the answer on `decision`, metrics, regions, edge metrics, residual statistics, and artifact paths.
4. Mention important limits: threshold profile, size policy, alpha background, and any resizing/padding.
5. For audit handoff, preserve the JSON report and all referenced artifact files together.

Minimum CLI:

```bash
python visual_diff.py before.png after.png \
  --output-dir ./visual_diff_report \
  --json-out ./visual_diff_report/report.json
```

CI-style failure when the images are different:

```bash
python visual_diff.py before.png after.png \
  --output-dir ./visual_diff_report \
  --json-out ./visual_diff_report/report.json \
  --fail-on different
```

Python usage:

```python
from visual_diff import CompareConfig, compare_images

result = compare_images(
    "before.png",
    "after.png",
    CompareConfig(size_policy="pad", output_dir="visual_diff_report"),
)

print(result.decision)
print(result.explanation)
print(result.to_dict())
```

## Output contract

The report is JSON-safe and includes:
- `decision`: `same`, `similar`, or `different`.
- Pixel metrics: changed pixels, changed ratio, MAE, MSE, RMSE, max delta, PSNR.
- Structural metric: SSIM-like luminance score.
- Signed residuals: global and per-channel value deltas where positive means image A is brighter than image B.
- Region evidence: changed pixel bounding boxes and changed edge/line bounding boxes.
- Edge evidence: Sobel edge precision, recall, F1, unmatched edge ratio, and distance statistics.
- Object-like component coordinates: connected visual components, not semantic labels.
- `output_files`: normalized inputs, diff, heatmap, mask, overlays, residual maps, edge maps, and box overlays.
- `config`: thresholds and normalization settings used for the run.
- `audit`: skill version, UTC timestamp, elapsed time, dependency versions, input file names/sizes/SHA-256 digests, original sizes, and compared canvas size.

Coordinate convention: `bbox_xyxy` is `[x1, y1, x2, y2]`, where `x2` and `y2` are exclusive.

## Decision guidance

Use `decision` first, then cite the strongest evidence:

- `same`: normalized images are pixel-identical, or pixel and edge differences are below configured same-image thresholds.
- `similar`: differences exist but remain below configured visual-similarity thresholds.
- `different`: pixel residuals or edge/shape differences exceed similarity thresholds.

High-signal fields:
- `changed_pixel_ratio`: proportion of compared pixels above `diff_threshold`.
- `mae` and `residual.global.p95_abs`: average and high-percentile value differences.
- `ssim`: luminance structural similarity; closer to 1 means more similar.
- `edge_metrics.edge_f1`: tolerance-aware shape/line similarity.
- `edge_metrics.edge_changed_ratio`: proportion of pixels with unmatched edge evidence.
- `regions` and `edge_regions`: bounding boxes for localized evidence.
- `output_files.overlay`, `output_files.heatmap`, `output_files.signed_residual`, and `output_files.edge_overlay`: fastest visual checks.

## Guardrails

Do:
- State that object coordinates are component-based, not semantic object detection.
- State when images were resized or padded before comparison.
- Use strict thresholds for UI regression; use looser thresholds for photographs or antialiased renders.
- Preserve JSON and artifacts together when sharing results.
- Treat very large or untrusted inputs cautiously; the default `max_pixels` limit is 80,000,000.

Do not:
- Claim two images are semantically equivalent solely because metrics are close.
- Claim a detected component is a real-world object class unless another tool verifies it.
- Hide threshold choices or normalization choices.
- Summarize from visual artifacts alone when JSON metrics disagree.
- Use `resize` for screenshot regression unless resizing is explicitly intended.

## Threshold starting points

Strict UI regression:

```python
CompareConfig(
    diff_threshold=3,
    same_changed_ratio_max=0.0001,
    same_mae_max=0.15,
    same_ssim_min=0.9995,
    same_edge_f1_min=0.998,
    same_edge_changed_ratio_max=0.0005,
    similar_changed_ratio_max=0.005,
    similar_mae_max=1.0,
    similar_ssim_min=0.985,
    similar_edge_f1_min=0.975,
    similar_edge_changed_ratio_max=0.008,
)
```

General visual comparison:

```python
CompareConfig(
    diff_threshold=8,
    same_changed_ratio_max=0.0005,
    same_mae_max=0.5,
    same_ssim_min=0.998,
    same_edge_f1_min=0.995,
    same_edge_changed_ratio_max=0.001,
    similar_changed_ratio_max=0.02,
    similar_mae_max=4.0,
    similar_ssim_min=0.96,
    similar_edge_f1_min=0.94,
    similar_edge_changed_ratio_max=0.025,
)
```

Photos or rendered scenes:

```python
CompareConfig(
    diff_threshold=14,
    same_changed_ratio_max=0.002,
    same_mae_max=1.5,
    same_ssim_min=0.992,
    same_edge_f1_min=0.985,
    same_edge_changed_ratio_max=0.005,
    similar_changed_ratio_max=0.06,
    similar_mae_max=8.0,
    similar_ssim_min=0.92,
    similar_edge_f1_min=0.88,
    similar_edge_changed_ratio_max=0.06,
)
```

## Handoff format

When reporting results to another agent or user, include:

```text
Decision: <same|similar|different>
Inputs: <A filename/SHA-256 prefix> vs <B filename/SHA-256 prefix>
Normalization: <size_policy>, compared size <W>x<H>, alpha background <R,G,B>
Metrics: changed_ratio=<...>, MAE=<...>, SSIM=<...>, edge_F1=<...>, edge_changed_ratio=<...>
Evidence: top changed regions <bbox list>, top edge regions <bbox list>
Artifacts: report.json, overlay, heatmap, signed_residual, edge_overlay
Limitations: <threshold/profile/resize/object-coordinate caveat if relevant>
```

## Validation harnesses

Run the smoke test before packaging or after dependency upgrades:

```bash
python scripts/smoke_test.py
```

Validate an existing report and referenced artifacts:

```bash
python scripts/validate_report.py visual_diff_report/report.json
```

## Language requirements

Use precise, neutral language:
- Prefer “evidence indicates” over “proves.”
- Prefer “object-like component” over “object” unless a semantic detector was also used.
- Prefer exact numbers and artifact names over broad claims.
- Do not overstate similarity when thresholds are loose or images were resized.
