# Module 08 — Visual Diagnosis (Screenshot → Root Cause)

Load this module when the task is to use a visual (screenshot, render, recording, diff image, error frame, design-vs-build comparison) to **diagnose a defect** and reach a fix, not merely describe it. Goal: resolve the visual issue in one pass without trial-and-error guessing.

## Diagnosis is a delta, not a description

A bug only exists relative to an expected appearance. Before hypothesizing, fix two anchors:

- **Expected**: the intended/correct rendering or behavior, from the spec, the design, a passing reference, sibling elements, or the user's stated intent. If expected is unknown, ask or state the assumed expected — do not guess a cause against an undefined baseline.
- **Actual**: what the visual actually shows, stated as observed/measured evidence (Module 02 tags).

The defect is the precisely localized **delta** between them.

## Diagnostic loop

Run in order; stop as soon as a single cause is confidently isolated.

1. **Localize**: name the exact region/element/coordinates of the defect and its scope (one element, one component, whole viewport, one breakpoint, one state, one platform). Scope alone eliminates most hypotheses.
2. **Characterize the delta**: expected vs actual, with exact values where readable (color, px, count, position, z-order, text, truncation point).
3. **Classify the symptom signature** using the catalog below — this maps appearance to a constrained cause set so you reason from knowledge, not trial-and-error.
4. **Rank hypotheses**: list candidate root causes most-likely first. Each hypothesis must name the **evidence layer** it lives in (static source / build / rendered pixels / runtime / data / environment — Module 05) and the visual evidence that supports *and* the evidence that would refute it.
5. **Pick the one discriminating check** (see below) — the single cheapest observation or command that splits the top hypotheses. Never propose a fix before naming the check that confirms the cause, unless the cause is already proven from the image.
6. **Conclude**: state the most probable root cause, confidence, the fix it implies, and the confirmation step. Keep alternatives only if the discriminating check was not run.

## Anti-trial-error rule

A fix proposed without an identified cause is a guess. For every proposed change, state: the cause it addresses, the visual evidence linking cause to symptom, and the one check that confirms it. If two hypotheses predict the same fix, you may proceed; if they predict different fixes, run the discriminating check first. Prefer one decisive check over several speculative edits.

## Symptom signature catalog

Map the visual symptom to its likely cause cluster and the cheapest discriminating check. Causes are ranked rough-frequency-first; confirm before fixing.

| Visual symptom | Likely causes (ranked) | Discriminating check |
|---|---|---|
| Element overflows / pushes layout / horizontal scrollbar | unconstrained width/min-width, long unbroken token, missing `overflow`/`flex-min-0`, fixed width vs fluid content | inspect computed width + parent constraints; toggle `overflow:hidden` |
| Content clipped / cut off / ellipsis where it shouldn't | fixed height, `overflow:hidden`, `-webkit-line-clamp`, container too small, absolute element under sibling | check computed height/overflow on the clipping ancestor |
| Element invisible but space reserved | `opacity:0`, `visibility:hidden`, color == background, `0` text, transparent asset | check computed opacity/visibility/color vs background |
| Element gone, no space | `display:none`, not mounted, conditional render false, `height:0`, off-screen transform | inspect DOM presence vs CSS; check render condition/state |
| Wrong/overlapping stacking, modal behind content, tooltip clipped | z-index without positioning context, stacking-context trap (`transform`/`filter`/`opacity` ancestor), `overflow:hidden` clipping popover | inspect stacking context chain of the ancestors |
| Misalignment / off-by-a-few-px | box-model (border/padding), `line-height`, `vertical-align`, sub-pixel rounding, inconsistent margins | compare box metrics of the two elements |
| Wrong/missing colors or theme | CSS var not resolved, dark/light mode token, specificity/override, theme class not applied | check computed value + which rule wins (specificity) |
| Unstyled / default-looking content | CSS bundle not loaded (404), class name mismatch, scoped-style/CSS-module hash miss, build not run | check stylesheet network 200 + class attribute matches selector |
| Broken image / icon (alt text, broken glyph, empty box) | wrong/404 src, CORS, missing asset in build, icon-font not loaded, sprite offset | check the asset request status + path |
| Wrong font / fallback font flash | `@font-face` 404, font not preloaded, `font-family` typo, FOUT/FOIT | check font request + computed `font-family` |
| Layout breaks at one screen size only | missing/overlapping media query, fixed px vs responsive unit, container query, viewport meta missing | resize to the breakpoint; inspect active media queries |
| Blank/white screen | JS error before render, failed bundle, hydration crash, unhandled promise, blocking auth/redirect | read console errors + network for failed JS |
| Stale / wrong / partial data shown | loading state stuck, cache, race between fetches, wrong query/key, error swallowed | check network response payload + request timing |
| Flash of wrong content then correct (or vice-versa) | hydration mismatch, default state before fetch, SSR/CSR divergence, optimistic update | compare server HTML vs hydrated DOM; check console hydration warning |
| Duplicated / repeated elements | list key collision, double render/effect, event double-bind | check keys + effect/mount count |
| Text mojibake / boxes / wrong script | encoding mismatch, missing glyph coverage, wrong locale, RTL not applied | check charset + font glyph coverage + `dir` |
| Mirrored / wrong-direction layout | RTL/LTR `dir`, logical vs physical CSS properties, locale | check `dir` + logical-property usage |
| Blurry / pixelated UI or image | DPR/scaling, raster asset below 2x, CSS scale transform, `image-rendering` | check natural vs displayed size + devicePixelRatio |
| Animation janky / stuck / wrong | transform vs layout-triggering props, missing `will-change`, interrupted transition, reduced-motion | inspect which property animates + frame timing |
| Cursor/hover/focus state wrong or missing | `:hover`/`:focus-visible` rules, pointer-events, focus trapped/lost, disabled state | check pseudo-class rules + pointer-events + tabindex |
| Form field rejects / looks valid but submit fails | client vs server validation, controlled/uncontrolled, name/id mismatch, hidden required field | check field value binding + validation source |

When the symptom is not in the catalog, still produce: localized delta → ranked layered hypotheses → discriminating check.

When re-capturing is not allowed, the discriminating check shifts to static source evidence — locate the responsible code from visible cues and inspect the winning rule (Module 14) — rather than a fresh screenshot.

## Evidence-layer discipline for diagnosis

A screenshot alone proves only rendered-pixel facts. Cause attribution to source/runtime/data is **inferred** until the corresponding layer is checked (Module 05). State which layer each hypothesis needs and whether you inspected it. Do not assert "the CSS does X" or "the JS fails" from a screenshot alone — mark it inferred and name the check.

When tooling is available (DOM/accessibility inspector, console, network, computed styles, second screenshot at another state/size, source grep), prefer the one check that is decisive over describing many possibilities. When box coordinates or colors are known, `scripts/mythos_layout_check.py` confirms overlap/clipping/off-canvas/misalignment and `scripts/mythos_contrast.py` confirms a contrast/theme defect deterministically.

## Comparison diagnosis (design-vs-build, before-vs-after, regression)

When two visuals are provided:

1. Align them (same element, same state, same viewport) before comparing — otherwise deltas are artifacts of mismatch.
2. Enumerate deltas by region; classify each (spacing, color, type, asset, state, content, missing/added element).
3. Separate **intended** changes from **regressions**; rank regressions by user impact.
4. For each material delta, give the signature-catalog cause and discriminating check.

## Diagnosis report schema

```markdown
# Visual Diagnosis: <issue>

## Delta
- Expected: <baseline + source>
- Actual: <observed, exact values>
- Localization: <element/region/scope: state, viewport, platform>

## Hypotheses (ranked)
1. <cause> — layer: <source|build|render|runtime|data|env>; supports: <evidence>; refutes: <evidence>
2. ...

## Discriminating check
- Check: <single cheapest decisive observation/command>
- Result (if run): <outcome>

## Root cause
- <cause> — confidence: <high|medium|low>

## Fix
- <change tied to the confirmed cause>

## Confirmation
- <how to verify the fix resolves the delta; regression risk>
```

## Diagnosis guardrails

- No expected baseline → no cause claim; state the assumed expected first.
- One confirmed cause beats three plausible ones; converge, then stop (kernel stop rule).
- Do not let filename, ticket text, or the user's suspected cause override observed pixels (Module 04 manifest firewall) — treat them as hypotheses to test.
- Keep render/runtime/source/data layers separate (Module 05); never collapse an inferred cause into an observed fact.
