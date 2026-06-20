# Module 14 — Visual ↔ Code Linking (capture-constrained)

Load this module to **connect a visual to the source that produces it**: locate the file/component/rule behind a screenshot or design, predict appearance from source without rendering, and land a correct code change in one shot. Designed for when re-capturing or trial-and-error screenshots are **not allowed** — front-load all reasoning from one artifact plus the source.

## Operating assumption: no iterate-by-screenshot

You may get one image (or none) and the codebase. You cannot keep re-rendering to converge. Therefore: extract every usable cue from the given artifact once, ground it in source statically, and make a single well-justified change. Respect the source/render boundary (Module 05) — a static change is `inferred` for rendered effect until rendered; do not claim "verified on screen" without a render. Maximize static evidence and offer a non-visual verification path (below) instead of guessing.

## Cue → source correspondence (the link)

Turn what is visible into searchable source anchors, strongest first:

| Visible cue | Source anchor to grep | Strength |
|---|---|---|
| Exact visible text / label / placeholder / aria text | string literal in markup/JSX/template/i18n file | highest (often unique) |
| Component-looking element (card, modal, nav) | component name, file name, test id, route | high |
| Exact color (hex/rgb) | color literal or design-token/variable | high |
| Class/id-like token, data-testid | selector, `className`, `class=`, `id=` | high |
| Pixel size / spacing / radius | `Npx`, spacing tokens, grid values | medium |
| Icon / asset | asset filename, icon name, sprite id | medium |
| Font / weight | `font-family`, type-scale token | low-medium |

Use `scripts/mythos_source_locator.py --root <src> --text … --color … --token … --size …`: it greps these cues and ranks candidate files by specificity and **cue diversity** (a file hit by several distinct cues is likeliest the source). It returns candidates only — "this file renders those pixels" stays a render fact, not proven by grep.

### Localization workflow

1. **Harvest cues** from the artifact: exact text (most discriminating), colors (use `mythos_image_meta.py`/known palette), tokens/test ids if visible in a design system, sizes, assets.
2. **Locate** with the locator script (or targeted grep); start from the highest-diversity, highest-specificity file.
3. **Trace the chain**: markup/component → applied classes/props → CSS rule / styled definition / token → computed intent. Note where styling could be overridden (specificity, cascade, theme, inline) — the visible result is the *winning* rule, which static reading must reason about, not the first match.
4. **Confirm the mapping** before editing: the located element's text/class/structure matches the visible element; ambiguity (two components, two rules) is named and resolved by the most specific shared cue.

## Static appearance prediction (source → look, no render)

When you cannot render, reason about what source produces and state it as `inferred` with the reasoning:

- Resolve the **winning** declaration: account for specificity, source order, `!important`, inline styles, media/container queries, theme class, and CSS variables (resolve the variable to its value chain).
- Derive layout intent from box model, fl/grid container, and constraints; flag where intrinsic content size is unknown (text length, images) as the residual uncertainty.
- Compute deterministic sub-facts instead of eyeballing: `mythos_contrast.py` for a color pair, `mythos_layout_check.py` for known box geometry, `mythos_image_meta.py` for asset dimensions.
- Keep layers separate: static source supports declarations/structure/probable result; it cannot settle runtime state, data-driven content, JS-applied styles, fonts/metrics, or final pixels.

## One-shot change under capture constraints

1. **Anchor the expected delta** (Module 08): exact element, the property to change, intended value, and what must not change.
2. **Find the winning rule** that currently sets it (not just any rule) — change the source of truth, not a shadowed duplicate.
3. **Make the minimal change** at the right layer (token vs component vs one-off), matching codebase conventions.
4. **Predict the new appearance** statically and the blast radius (every element using that selector/token/component — grep all usages before changing a shared token).
5. **State residual risk** that only a render would close, and name the **single** render/check you would request if/when permitted — one decisive capture, never a trial-and-error loop.

## Capture-free verification path

Substitute deterministic, non-visual evidence for re-screenshotting (maps to Module 12 as a static tier below V2):

- Selector/class now matches the element (grep markup ↔ CSS).
- The changed value is the winning declaration (no higher-specificity override remains).
- Color pair passes `mythos_contrast.py`; box geometry passes `mythos_layout_check.py`; asset fits via `mythos_image_meta.py`.
- Type-checks/build/lint and any component/snapshot/visual-regression tests the repo already has (these run without a manual capture).
- All other usages of the touched token/selector reviewed for regressions.

Report verification honestly: "static-verified (source + deterministic checks); rendered appearance not confirmed — one render needed to close." Never upgrade `inferred` to `observed`/`measured` without the render.

## Code → visual (reverse direction)

Given source, predict its rendered role for review/documentation: parse declarations/structure, resolve tokens, describe probable appearance and states, and flag what depends on data/runtime/fonts. Same boundary: probable, not pixel-confirmed.

## Guardrails

- No source access → say what cues you would grep and stop; do not invent file paths or line numbers.
- A grep match is a candidate, not proof of the rendering source; cascade/runtime can move the truth.
- One reasoned change beats several speculative edits; if two hypotheses imply different edits and no static cue separates them, request the one decisive render rather than guessing (Module 08 anti-trial-error).

## Output

`cues harvested | located source (file:line, confidence) | winning rule + chain | static appearance prediction (inferred) | minimal change + blast radius | capture-free checks passed | residual: render needed? (one)`.
