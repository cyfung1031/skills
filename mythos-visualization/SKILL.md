---
name: mythos-visualization
version: 3.1.0
description: Standalone, token-efficient visual-understanding skill for images, screenshots, source-backed graphics, visual systems, and visual corpora. v3.1.0 keeps the compact always-load kernel, adds clearer routing and audit gates, and preserves on-demand modules plus optional Python checks.
last_updated: 2026-06-18
module_strategy: compact_kernel_plus_on_demand_modules
standalone_package: true
---

# Mythos Visualization

Use this skill to understand, describe, critique, reconstruct, classify, compare, validate, or reason about visual artifacts: photos, screenshots, scans, artwork, memes, abstract visuals, charts, maps, diagrams, technical drawings, scientific/industrial imagery, creatures/objects/scenes, SVG, HTML/CSS/JS, Canvas/WebGL, animation/video frames, and mixed folders.

Do not use it for non-visual tasks except when the user asks about source that produces a visual or about a visual-corpus/release package.

## Always-load kernel

Primary outcome: produce the smallest evidence-grounded answer that preserves both local detail and global meaning.

Core invariant: **artifact identity → user intent → smallest sufficient mode → one dominant lens → supporting/pruned lenses → evidence boundary → compact scene/source model → detail-overall bridge → risks/limits → stop**.

Protected behavior that must not regress:

1. Use the smallest sufficient mode; do not add sections or tools because the skill mentions them.
2. Choose exactly one dominant lens unless the user explicitly asks for multi-lens comparison.
3. Use supporting lenses only when they change the answer.
4. Separate **observed**, **measured**, **inferred**, and **not verified** claims.
5. Keep source, rendered appearance, runtime behavior, accessibility tree, and external facts as separate evidence layers.
6. Avoid unsupported certainty about identity, intent, statistics, geography, medicine/science, accessibility compliance, or runtime behavior.
7. Bridge details to the overall meaning, task, classification, critique, reconstruction, or validation.
8. Stop when new detail would not change the answer.
9. Preserve exact paths, labels, code snippets, visible text, units, colors, coordinates, and IDs when they matter.
10. State validation run/not-run only for checks actually performed.

## Routing algorithm

1. Identify the artifact: type, visual class, source availability, and whether it is a single visual, sequence, source-backed render, or corpus.
2. Identify the user's task: caption, analysis, critique, extraction, comparison, reconstruction, implementation guidance, verification, corpus report, or release audit.
3. Choose the smallest mode: Ultra-Compact, Tiny, Quick, Compressed Standard, Standard, Forensic, or Corpus/Release profile.
4. Choose one dominant lens: UI/product, chart/data, map/spatial, diagram/system, photo/scene, creature/object, artwork/style, meme/social, abstract/formal, scientific/industrial, source-backed graphic, motion/video, or mixed-corpus.
5. Add only supporting lenses that materially change the answer.
6. Name the evidence boundary before any claim that could be overread.
7. End with the relevant limit, validation status, or next action only when it helps the user.

## Mode ladder

| Mode | Use when | Output shape |
|---|---|---|
| Ultra-Compact | Direct identification, alt-text-like answer, simple artifact, high-volume corpus row. | One sentence: identity + one cue + limit if needed. |
| Tiny | Caption, single-purpose answer, light classification. | 1–2 evidence-bounded sentences. |
| Quick | Quick read, simple critique, plain explanation. | Identity, meaning, 1–3 details, one limit. |
| Compressed Standard | Most screenshots, charts, photos, diagrams, maps, artwork, source-backed files. | Identity, lens, evidence boundary, compact model, bridge, risks/limits. |
| Standard | User asks analysis, critique, extraction, comparison, reconstruction, implementation guidance. | Target map, evidence, model, findings, risks, validation. |
| Forensic | High-stakes, disputed, reproducibility, source-to-render, accessibility/compliance, pixel-level or audit work. | Evidence ledger, measurements/tool outputs, validation artifacts. |
| Corpus/Release profile | Folders, benchmarks, repeated reports, successor versions. | Inventory, route, sample/verify, aggregate, audit packet. |

Escalate only when missing evidence could materially change the answer. De-escalate when a concise direct answer satisfies the request.

## Evidence boundary

- **Observed**: visible in the image, frame, scan, chart, source snippet, or provided file preview.
- **Measured**: dimensions, checksums, color samples, parsed counts, OCR output, rendered comparison, accessibility result, or deterministic checks actually run.
- **Inferred**: likely task, meaning, style, category, relation, mood, or classification from evidence.
- **Not verified**: DOM/CSS cascade, JavaScript behavior, backend data, accessibility tree, screen-reader behavior, responsive layout, animation timing, identity/provenance, exact species, artist intent, exact map truth, statistical significance, diagnosis, industrial safety, compliance, or external facts unless tested/cited.

Use “appears,” “visually suggests,” “is consistent with,” and “not tested” when evidence is partial. Do not convert filename, surrounding prose, or user labels into visual fact when they conflict with observed or measured evidence.

## Source/render/runtime rule

For source-backed visuals:

- Static source facts can support declarations, tags, selectors, shapes, colors, data arrays, imports, and probable purpose.
- Rendered facts require rendering, screenshots, or measured pixels.
- Runtime facts require execution or logs.
- Accessibility-tree facts require an accessibility check, not a visual screenshot alone.

Never collapse these layers. Rendering, OCR, browser execution, external lookup, or accessibility tooling is optional and should be used only when it materially changes the answer or the user requests verification.

## Guardrails and fallback

- Refuse or redirect only when the visual task would require unsafe instructions, privacy-invasive identification, unsupported diagnosis/compliance certification, or other disallowed help.
- For ambiguous visuals, give the best bounded reading and the uncertainty source instead of forcing a single identity.
- For high-stakes domains, describe visible features and limits; do not diagnose, certify, optimize operations, or assert legal/scientific truth from appearance alone.
- For protected or exact content, preserve code, logs, labels, paths, IDs, visible text, numbers, units, and user-provided constraints unless asked to transform them.
- If evidence is unavailable, answer from available layers and say what would be needed to verify the missing layer.

## Output patterns

- Direct visual answer: `What it is → what matters → evidence → uncertainty/limit`.
- Screenshot UI: page/app/state; intended task; visible regions supporting the task; 3–5 visible risks; not-verified line.
- Chart/map/data: encoding/labels that are readable; apparent pattern; exactness level; missing source/scale/context.
- Artwork/meme/abstract: visible subject/form; style/mood; plausible reading; ambiguity; avoid definitive intent.
- Source-backed file: static facts; probable visual role; what rendering/runtime/accessibility would be needed to verify.
- Corpus/release work: inventory; routing/confidence; coverage depth; sample reports; aggregate patterns; validation log; checksums.

## Handoff and audit discipline

For saved reports, corpus work, release audits, or disputed analysis, preserve:

- input paths and output paths;
- assumptions and evidence tags;
- decisions and rejected risks;
- validation run/not-run status;
- checksums or stable size markers where files are compared;
- the next action only when the current answer cannot close the task.

Keep process history, evaluator names, and generated-by wording out of release artifacts unless the user explicitly asks for an audit appendix.

## Token-efficiency and on-demand module loading

This `SKILL.md` is the always-load kernel. Load optional markdown modules only when the task needs them. If modules cannot be retrieved, the kernel is sufficient for normal answers.

| Trigger | Optional module |
|---|---|
| Need detailed mode/lens definitions or output schemas | `modules/01_modes_lenses.md` |
| Need claim tags, exact extraction rules, or domain claim boundaries | `modules/02_evidence_claims.md` |
| Need domain examples for UI, charts, maps, diagrams, photos, artwork, memes, scientific images, motion | `modules/03_domain_lenses.md` |
| Need folder/corpus processing, sampling, manifests, or report packets | `modules/04_corpus_batch.md` |
| Need source-backed graphics, SVG/HTML/CSS/JS, rendering, runtime, accessibility separation | `modules/05_source_render_runtime.md` |
| Need saved report schemas and answer templates | `modules/06_output_contracts.md` |
| Need successor-version review, score matrices, or release gates | `modules/07_release_review.md` |

## Mechanical state checks

Use Python only for mechanical state where it materially improves reliability, especially package/release work, corpus inventory, checksum/index matching, report schema validation, route summaries, score matrices, and metadata/header consistency. Do not use scripts to invent visual interpretations.

Bundled scripts:

- `scripts/mythos_state_check.py`: validate this package, version metadata, module links, protected invariants, token estimates, and checksums.
- `scripts/mythos_corpus_probe.py`: inventory a corpus, compute file metadata/checksums, classify coarse kind, and create D0/D1 audit artifacts.
- `scripts/mythos_report_lint.py`: check per-sample markdown report schemas and coverage disclosures.

Suggested smoke commands for release or corpus work:

```bash
python3 scripts/mythos_state_check.py --package . --write-checksums
python3 scripts/mythos_corpus_probe.py --input tests/fixtures/corpus --output /tmp/mythos_probe --sample-reports
python3 scripts/mythos_report_lint.py --reports /tmp/mythos_probe/sample_reports
```

## Tiny self-audit

Before finalizing, silently check: smallest sufficient mode, correct dominant lens, pruned irrelevant lenses, evidence-bound interpretations, no unsupported runtime/source/accessibility/scientific/statistical/location/identity/intent claims, preserved exact content where needed, validation status honest, and no decorative bloat.
