# Module 11 — Structured Visual Extraction

Load this module to extract structured content from a visual: tables, forms, receipts/invoices, ID/labels, dashboards, multi-column documents, code/log screenshots, handwriting, or any "read the values out of this image" task. Goal: extract faithfully with cell/field integrity, never silently fabricating or misaligning data.

## Exactness tiers (declare which you used)

- **Source/selectable text**: if the underlying source or selectable text is available, use it — most reliable.
- **OCR/measured**: deterministic OCR or tool output actually run → `measured`.
- **Visual read**: read by eye from pixels → `observed` for clear glyphs, drop to **approximate** for small/blurred, **unavailable** when guessing (Module 02 exactness ladder).

Never present a visual read as if OCR-verified. Flag low-confidence characters (`0/O`, `1/l/I`, `5/S`, `rn/m`, decimal vs thousands separators, trailing zeros) explicitly.

## Table integrity

1. **Fix the grid first**: count columns and rows from headers/rulings before reading cells; lock the header row.
2. **Preserve structure**: keep row↔column alignment exact. Empty cell = explicit empty, not skipped — a dropped cell shifts every value after it.
3. **Handle merges/spans**: note merged cells, spanned headers, grouped rows; do not duplicate or collapse silently.
4. **Multi-line & wrapped cells**: a wrapped value is one cell, not two rows. Distinguish a wrap from a real new row by the ruling/alignment.
5. **Units & types**: capture header units, currency, %, dates; keep the number's exact form (separators, sign, precision).
6. **Self-check**: re-derive any visible totals/subtotals from extracted cells; a mismatch means a misread — locate and fix before reporting.
7. **Output**: emit machine-faithful structure (CSV/TSV/markdown table/JSON) preserving order and blanks; note any cell you could not read rather than guessing.

## Form / key-value / document extraction

- Pair each label with its value by spatial association (label-left or label-above); flag ambiguous pairings.
- Preserve field order and section grouping; note checkboxes/radios as checked/unchecked, signatures as present/absent (not their content).
- For multi-column or multi-page docs, establish **reading order** before transcribing (Z-order within column, then next column); state assumed order when columns are ambiguous.
- For receipts/invoices: line items as a table, plus totals/tax/date/vendor as key-value; reconcile line sum to total as a self-check.

## Code / log / terminal screenshots

Preserve characters exactly: indentation, brackets, quotes, operators, and whitespace are load-bearing. Flag truncation (cut lines, horizontal scroll, ellipsis). Mark uncertain glyphs. Prefer asking for the text source over transcribing long code from pixels.

## Dashboards (mixed)

Route each panel to its lens (chart→Module 03, table→here, KPI→key-value); do not average across heterogeneous panels. Keep each panel's own scale/time-range; flag cross-panel scale mismatches.

## Faithfulness guardrails

- Extract only what is visible; do not infer missing cells, complete partial numbers, or "correct" apparent typos in the source — transcribe and flag.
- Do not let a caption/filename override the visible value (Module 04 firewall).
- State coverage: "rows 1–N of a table cut at the fold; remainder not visible."

## Output

`structure: <table/kv/doc> | tier: <source|OCR|visual-approx> | grid: RxC verified | uncertain: <cells/glyphs> | reconciliation: <totals checked?> | coverage: <complete|truncated>`.
