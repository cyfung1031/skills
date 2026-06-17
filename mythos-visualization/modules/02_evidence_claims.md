# Module 02 — Evidence, Exactness, and Claim Boundaries

Load this module when exact extraction, high-risk domains, or strong uncertainty discipline is needed.

## Claim tags

- **Observed**: visible or directly present.
- **Measured**: deterministic tool output actually run.
- **Inferred**: plausible conclusion from evidence.
- **Assumed**: needed to proceed but not verified.
- **External-cited**: supported by cited external source.
- **Not verified**: plausible but not tested, measured, or cited.

Use tags explicitly in reports and audits; use natural language in ordinary answers.

## Exactness ladder

Use for text, chart values, coordinates, measurements, counts, distances, labels, colors, timing, and source/render properties.

- **Exact**: source-backed, measured, OCR/manual verified, or deterministic.
- **Approximate**: visibly estimated and clearly non-final.
- **Pattern-only**: trend/layout/category is visible but values/details are unreliable.
- **Unavailable**: extraction would be guesswork.

Do not invent precision. Say “pattern-only” or “not recoverable from this image” when needed.

## Domain boundary table

| Domain | Safe claim | Unsafe without evidence |
|---|---|---|
| UI screenshot | visible regions, task cues, visible risks | DOM order, JS behavior, backend state, accessibility compliance |
| Chart/data | encodings, readable axes/labels, apparent pattern | source data, significance, causality, exact values if not readable |
| Map/GIS | visible labels, routes, layers, approximate relations | shortest route, legal boundary, distance, projection accuracy, live traffic |
| Photo/object | visible pose, broad category, occlusion, lighting | real-person identity, exact species, age/health/status, provenance |
| Art/meme | visible motifs, style, mood, plausible reading | artist intent, definitive symbolism, universal audience reaction |
| Scientific/medical/industrial | visible structures and measurement limits | diagnosis, safety/compliance, operational suitability, treatment |
| Source-backed visual | static declarations and probable role | computed layout, runtime behavior, accessibility tree, source-to-render fidelity |

## Uncertainty phrasing

Prefer: “appears,” “visually suggests,” “is consistent with,” “likely,” “from the provided evidence,” “not tested,” “not enough evidence to verify.”

Avoid: “proves,” “definitely,” “guarantees,” “compliant,” “intended,” “statistically significant,” “diagnostic,” unless evidence supports it.
