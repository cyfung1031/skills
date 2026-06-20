# Module 09 — Spatial Grounding & Action Targeting

Load this module when an agent must **act on** a visual: click, tap, drag, type into, scroll to, or point at a target (computer-use, browser automation, robotic/AR overlay, "where is X", "click the Y"). Goal: hit the right target on the first action instead of guessing coordinates.

## Coordinate contract (state it before emitting any coordinate)

A coordinate is meaningless without its frame. Pin all four before acting:

1. **Origin & axes**: top-left `(0,0)`, x→right, y→down unless the tool says otherwise.
2. **Unit**: CSS/logical pixels vs device pixels. `device_px = css_px × devicePixelRatio`. A 2× display doubles raster coordinates — a frequent off-by-2× miss.
3. **Reference rect**: full screen, the app window, the browser viewport, or the captured image. A screenshot may be a crop or a single window, not the whole screen — its `(0,0)` is the crop's corner.
4. **Scale factor**: `actual_px = reported_px × (native_dimension / displayed_dimension)`. If the screenshot was downscaled, every coordinate must be rescaled back.

Emit targets as both a **normalized** fraction `(x/W, y/H)` and an **absolute** pixel pair so a frame mismatch is recoverable. Normalized survives rescaling; absolute is what most tools consume.

## Targeting method

1. **Identify the element** by its most stable handle, in this priority: accessible name/role or test id (if the tool exposes the tree) > unique visible text label > icon + position relative to a labeled anchor > raw pixels. Prefer semantic handles over pixel hunting whenever the tool offers them.
2. **Localize the click point**: the centroid of the *interactive* region, not the label text. For a checkbox+label row, the box; for a button, its visual center; avoid 1-2px from an edge (sub-pixel + hit-area rounding miss).
3. **Confirm reachability**: is the target fully visible, partially clipped, behind an overlay, disabled, or off-screen? Off-screen → scroll first; covered → dismiss the occluder first (see stacking, Module 08). Do not click a coordinate you cannot see.
4. **Drag/path actions**: state start centroid, end centroid, and whether intermediate hover or a drop-zone highlight is required; many DnD targets need a mid-path `mouseover` to activate.
5. **State the confidence and the fallback**: if the handle is ambiguous (two identical buttons), say which disambiguator you used (order, nearest label, region) and what to check if the action lands wrong.

## Anti-misclick rules

- Never invent pixel coordinates from a description alone — coordinates require an actual image or an element rect (mark `inferred` vs `measured`, Module 02).
- A label's text bounds ≠ the control's hit area; click the control.
- After scrolling/resize/navigation, prior coordinates are stale — re-localize against a fresh capture.
- If two captures disagree on position, the layout moved (animation, async load); wait for stable state before targeting (Module 12).

## Region & relationship grounding ("find X", "what is near Y")

Answer spatial queries with: the region (bbox or quadrant), its anchor relationships (left-of/above/inside/overlapping), and reading/tab order when relevant. Give bbox as normalized `(x0,y0,x1,y1)`. Distinguish **observed** position from **inferred** grouping.

## Degraded / ambiguous capture handling

Bad inputs are the top cause of wrong grounding. Detect and adapt:

| Condition | Tell | Adaptation |
|---|---|---|
| Downscaled/compressed | blur, JPEG ringing, soft edges | rescale coordinates to native; lower exactness; request a sharper capture for fine targets |
| Rotated/mirrored | text/layout orientation | normalize orientation before reading coordinates |
| Partial/cropped/scrolled | cut elements at edges | note that off-frame content exists; scroll/stitch before claiming "absent" |
| High-DPI mismatch | crisp text but 2× size vs reported | apply devicePixelRatio before emitting pixels |
| Occlusion/overlay | element behind modal/tooltip/cursor | resolve z-order first (Module 08); do not target through an occluder |
| Multi-monitor / wrong window | unexpected origin | confirm which display/window the capture is from |

When the capture is too degraded for the precision the action needs, say so and request a better capture rather than emitting a low-confidence coordinate that triggers a wrong action.

## Output

`target: <handle> | click point: norm (x,y) / abs (px,py) | frame: <screen|window|viewport|image> + DPR | reachability: <visible|scroll|occluded> | confidence + disambiguator | fallback check`.
