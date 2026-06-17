# Module 05 — Source, Render, Runtime, and Accessibility Boundaries

Load this module for HTML/CSS/JS/SVG, Canvas/WebGL, source-backed screenshots, rendering fidelity, or accessibility claims.

## Evidence layers

1. **Static source**: declarations, selectors, elements, paths, variables, imports, functions, comments, data arrays.
2. **Build/dependency layer**: preprocessors, bundlers, assets, fonts, frameworks, versions, generated files.
3. **Rendered pixels**: computed layout, actual colors, viewport, fonts, clipping, canvas/SVG rasterization.
4. **Runtime behavior**: events, network, storage, state transitions, animation timing, personalization, errors.
5. **Accessibility tree**: roles, names, focus order, keyboard behavior, screen-reader output, measured contrast.

Claim only the layers actually inspected.

## Render-when-material gate

Render or execute only when it would change the answer: source-to-render fidelity, exact layout, responsive behavior, animation, interaction, visual regression, accessibility, or disputed implementation claims.

## Source-only safe output

When only source is inspected, report: file type, static structure, declarations/data, probable visual role, dependencies, and what rendering/runtime/accessibility would be needed to verify.

## SVG specific

SVG markup can support some shape/color/coordinate facts, but actual appearance can still depend on CSS, fonts, viewport, external assets, filters, and renderer. Distinguish markup facts from rendered pixels.

## Accessibility

A screenshot can show potential risks such as small text, low contrast, missing visible focus, dense layout, or icon-only controls. It cannot verify compliance, focus order, labels, keyboard reachability, or screen-reader output without tools.
