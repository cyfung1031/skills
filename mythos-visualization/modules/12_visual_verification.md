# Module 12 — Visual Verification & Regression Loop

Load this module to **prove** a visual outcome: confirm a UI change works, validate a fix from Module 08, gate a before/after, or check for visual regressions. Core rule: a visual change is unverified until a fresh capture observably shows the expected state. Reading code or asserting "should now render" is not verification.

## Verification ladder (climb to the height the claim needs)

- **V0 source** — the change exists in source. Necessary, never sufficient for a visual claim. When re-capture is disallowed, this is the floor; raise it with the deterministic non-visual checks in Module 14's capture-free verification path (winning-rule confirmation, contrast/layout/meta scripts, type-check/build, existing snapshot tests) rather than re-screenshotting.
- **V1 static/build** — it compiles, the asset/style is referenced, the selector matches. Still not visual proof.
- **V2 rendered observation** — capture the actual rendered state and observe the expected appearance. **Minimum tier to claim a visual fix works** (maps to InsightForge T2 / verification-discipline "it behaves").
- **V3 measured/regression** — pixel/measurement comparison, contrast/measure values, or a baseline diff across a set.

Async/effect-loop, auto-reload/retry, animation, race, and "intermittent" visual bugs cannot be cleared below V2 — require at least one live reproduction before asserting fixed.

## Fix-verification loop (pairs with Module 08)

1. **Restate the expected delta** from diagnosis: the specific pixels/region/state that must change, and what must stay unchanged.
2. **Capture after** the change, at the **same** state, viewport, theme, and data as the failing case — otherwise the comparison is noise.
3. **Confirm the target delta resolved** (the symptom is gone) AND **scan for regressions** in neighbors, other breakpoints, the opposite theme, and previously-correct states.
4. **If not fixed**: do not stack speculative edits — return to the discriminating check (Module 08), the cause was wrong.
5. **Report** observed before→after with the capture as evidence, the tier reached, and what was not checked.

## State & flake control (avoid false pass/fail)

Stabilize before judging — most flaky visual checks are state, not code:

- Wait for load/network idle, fonts loaded, animations/transitions settled, skeletons gone.
- Pin nondeterminism: fixed viewport & DPR, seeded/mocked data, frozen time/clock, disabled caret blink, `prefers-reduced-motion` where relevant.
- Same auth/role, locale, and feature flags as the reference.
- Mask known-dynamic regions (timestamps, ads, avatars, random ids) before diffing.

A "difference" caused by unstabilized state is a false regression; an unstabilized "match" is a false pass.

## Before/after & visual-regression comparison

1. Align captures (same element, state, size, DPR) before diffing — see Module 08 comparison rules.
2. Classify each delta: intended change vs regression; rank regressions by user impact.
3. Distinguish a **meaningful** diff from anti-aliasing/sub-pixel noise — use a tolerance, don't fail on 1-px shimmer.
4. For a baseline set, report counts: unchanged / intended-change / regressions, with the worst regressions located.

## Acceptance & honesty

- Pass only when the expected state is observed at the required tier; otherwise report "edited but not visually verified — no render available" rather than implying success.
- Never weaken the expected state to make it pass. If the spec/baseline is wrong, say so as a separate visible note.
- State residual risk: states/sizes/themes/data not exercised.

## Output

`claim: <what is verified> | tier: <V0|V1|V2|V3> | before→after: <observed delta> | regressions: <none|located> | stabilized: <waits/pins applied> | not-verified: <states/sizes/themes left>`.
