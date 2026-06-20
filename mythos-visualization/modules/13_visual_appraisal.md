# Module 13 — Visual Appraisal & Quality Evaluation

Load this module to **judge** a visual's quality, craft, design, effectiveness, or worth: "is this good", "rate/critique this", "which is better", design/UX review, photo/art critique, image-quality assessment, brand/asset review, or value estimation. Appraisal is a graded judgment against explicit criteria — distinct from describing (Module 03), diagnosing defects (Module 08), or verifying a change (Module 12). Goal: a defensible, criteria-anchored verdict, not taste asserted as fact.

## Appraisal contract (set before judging)

1. **Purpose & audience**: what is the visual *for*, and for whom? Quality is fitness-for-purpose, not abstract beauty. A meme, a medical figure, and a luxury ad are judged on different axes.
2. **Standard of comparison**: against intent, a brief, a reference/exemplar, a peer set, or a convention. Name it; an appraisal with no baseline is opinion.
3. **Criteria & weights**: pick the rubric below that fits, weight criteria by what matters for the purpose, and state the weighting. Do not average unrelated axes into one number silently.
4. **Evidence per judgment**: every score/verdict cites a visible feature (`observed`) or a measured value (`measured`); separate taste/convention (`inferred`) from fact. No bare "looks good/bad".

## Rubrics (choose and adapt; score each 0–10 with evidence)

**Aesthetic / compositional** (photo, art, illustration, scene): composition & framing, balance/weight, focal point & visual flow, color harmony/palette, light & tonal range, depth & space, texture/detail, rhythm/pattern, craft/finish, originality, emotional/expressive impact, coherence of style.

**Technical image quality** (photo, scan, render, capture): exposure, focus/sharpness, motion/handshake, noise/grain, dynamic range & clipping, white balance/color accuracy, resolution adequacy for use, compression/artifacts (banding, blocking, moiré, halos), distortion/aberration, crop/horizon, cleanliness (dust, sensor spots). Prefer measured metrics (Module 11 tiers) over eyeballing where available; `scripts/mythos_image_meta.py` measures format/dimensions/aspect/DPI/animation and resolution-fitness deterministically from the file.

**Design / UX quality** (UI, layout, graphic, slide, document): visual hierarchy, alignment & grid, spacing/rhythm, consistency (type scale, color tokens, components), legibility (size, contrast, line length), color/contrast accessibility (risk only — confirm with tooling, Module 05), affordance & state clarity, density/whitespace, responsiveness cues, information clarity, brand fit, error/empty/edge presentation. When colors or box coordinates are known, `scripts/mythos_contrast.py` gives measured WCAG ratios/harmony and `scripts/mythos_layout_check.py` gives measured alignment/spacing/overlap/hit-size.

**Communication effectiveness** (chart, diagram, infographic, ad, poster): clarity of the main message, signal-to-noise, honesty of encoding (no truncated axes/misleading scale — flag as quality *defects*), labeling/legend sufficiency, accessibility of meaning, memorability, call-to-action clarity, audience fit.

**Asset/production quality** (deliverable, export): correct dimensions/aspect/DPI for target, color space, bleed/safe-area, file-format fitness, asset completeness, naming/versioning hygiene (state-only, not content).

Use the smallest set of criteria that decides the question; do not run all axes when one dimension governs the verdict.

## Scoring discipline

- Anchor the scale: 0–2 unacceptable, 3–4 weak, 5–6 adequate, 7–8 strong, 9–10 exemplary. State the anchor so a score is interpretable.
- A score **above 8 needs specific positive evidence**; **above 9 needs strong evidence and no material weakness** (mirrors release scoring, Module 07).
- Tie each score to its feature; list the top strengths and the highest-leverage improvements, ranked by impact on the purpose.
- Weighted aggregate only when criteria share a purpose. For mechanical, reproducible aggregation and inflation/evidence checks across one or many candidates, use `scripts/mythos_appraisal_score.py` — the script aggregates and flags, it does not judge.
- Distinguish **objective** quality (technical defects, accessibility risks, broken alignment) from **subjective/convention** quality (style, taste) — never present taste as defect or vice versa.

## Comparative appraisal & ranking

For "which is better" / shortlisting: hold criteria and weights constant across candidates; score each on the same evidence basis; rank by weighted aggregate but surface dimension-level trade-offs (A wins clarity, B wins craft). Report ties honestly; do not manufacture a winner when the gap is within evidence noise. Use `score_matrix.csv` for >2 candidates or repeated rounds.

## Worth / valuation boundary (hard limit)

Monetary or market value, authenticity, provenance, rarity, and grading **cannot be derived from appearance alone**. Estimate worth only from external market data — comparable sales, edition data, condition grading, expert authentication — cited (`external-cited`) and never invented. From an image you may give visible condition cues and category, explicitly tagged `not verified` for value, and point to qualified appraisal/authentication for anything consequential. Never assert a price, a forgery/genuine verdict, or investment advice from pixels (also Module 10 deception limits, privacy/identity guards).

## Appraisal guardrails

- No criteria → no verdict; state the assumed purpose/standard first.
- Accessibility, contrast, and compliance are *risks* from an image; confirm with tooling before passing/failing (Module 05).
- Keep appraisal fair to intent: judge against the visual's actual purpose, not a genre it never aimed at.
- Honesty cues in data visuals (axis truncation, dual axes, cherry-picked range) are quality defects — flag them; do not reward polish that misleads.

## Appraisal report schema

```markdown
# Visual Appraisal: <artifact>

## Frame
- Purpose / audience:
- Standard of comparison:
- Rubric + weights:

## Scores
| Criterion | Weight | Score (0–10) | Evidence (observed/measured) |
|---|---|---|---|

## Verdict
- Weighted aggregate (+ scale anchor):
- Top strengths:
- Highest-leverage improvements (ranked):

## Comparison (if multiple)
- Ranking + per-dimension trade-offs:

## Worth / value
- Visible condition/category only; value not verified from image — needs <market data/expert>.

## Limits
- Subjective vs objective split; accessibility/value/authenticity not confirmed from pixels.
```

## Output (compact form)

`purpose/standard | rubric + weights | per-criterion score + evidence | weighted verdict (anchored) | strengths/improvements | value: not-from-image | limits`.
