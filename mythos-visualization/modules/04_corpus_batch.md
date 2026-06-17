# Module 04 — Corpus Batch Workflow

Load this module for folders, benchmarks, repeated sample reports, or “analyze all samples” tasks.

## Depth ladder

- **D0 inventory**: file counts, formats, sizes, checksums, manifest reconciliation.
- **D1 static classification**: kind, dominant lens, route confidence, degraded/duplicate flags, source/image metadata.
- **D2 representative visual/source review**: seeds, outliers, conflicts, degraded samples, representative clusters.
- **D3 targeted verification**: OCR, rendering, accessibility, geospatial/scientific/domain checks only for material claims.
- **D4 forensic reproduction**: full measurement, source-to-render logs, fixtures, independent review.

Disclose depth as `scope × depth × exclusions`, for example: `442/442 records at D1; selected outliers at D2; no D3 OCR/rendering`.

## Batch process

1. Inventory all feasible records and ignore caches, `__MACOSX`, temp files, thumbnails, duplicates, and generated outputs unless in scope.
2. Route each sample using observed/measured evidence first; use filename/manifest as hints.
3. Cluster exact duplicates by checksum and optionally near-duplicates by perceptual similarity when bias matters.
4. Prioritize deep inspection: user seeds, unreadable files, tiny/low-entropy files, label conflicts, high-risk domains, source-backed render gaps, and representative clusters.
5. Generate compact per-sample reports and move repeated patterns to the corpus summary.
6. Validate index row count, report count, schema fields, coverage disclosure, and checksums.

## Recommended artifacts

- `run_manifest.json`: input, output, timestamp, skill version, validation tier, counts.
- `analysis_index.csv`: one row per sample: path, kind, size, checksum, route, mode, confidence, report path, status.
- `sample_reports/`: one concise markdown report per sample when requested.
- `corpus_summary.md`: patterns, conflicts, degraded files, coverage, validation limits.
- `validation_log.txt`: deterministic checks and not-run checks.
- `evidence_ledger.csv`: material findings and evidence tags when review-grade.
- `score_matrix.csv/.md`: when comparing variants/releases/models.

## Manifest firewall

Filenames, folders, manifest buckets, and user labels are hints, not ground truth. If they conflict with observed/source evidence, trust observed/measured evidence, lower confidence, and mention the conflict only if it changes routing or risk.
