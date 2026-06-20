#!/usr/bin/env python3
"""Deterministic color + WCAG contrast toolkit (pure stdlib).

Turns design/UX accessibility and aesthetic-color claims from `inferred` into
`measured`: WCAG 2.x relative luminance, contrast ratio, AA/AAA pass for normal/
large text and UI components, plus basic hue-harmony relations. Inputs are known
colors (hex or r,g,b) — it cannot sample colors from an image by itself.

Usage:
  mythos_contrast.py <fg> <bg> [--large] [--font-pt N --bold]
  mythos_contrast.py --pairs pairs.json          # [{"fg":"#111","bg":"#fff","label":"body"}]
  mythos_contrast.py --harmony "#3366cc" "#cc6633"
Colors: #rgb, #rrggbb, or "r,g,b".
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

AA_NORMAL, AA_LARGE, AAA_NORMAL, AAA_LARGE, UI = 4.5, 3.0, 7.0, 4.5, 3.0


def parse_color(s: str):
    s = s.strip()
    if s.startswith("#"):
        h = s[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) != 6:
            raise ValueError(f"bad hex: {s}")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    parts = [int(x) for x in s.replace(" ", "").split(",")]
    if len(parts) != 3 or any(not 0 <= v <= 255 for v in parts):
        raise ValueError(f"bad rgb: {s}")
    return tuple(parts)


def _lin(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb) -> float:
    r, g, b = (_lin(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg) -> float:
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return round((hi + 0.05) / (lo + 0.05), 2)


def is_large(font_pt, bold) -> bool:
    return bool(font_pt) and (font_pt >= 18 or (bold and font_pt >= 14))


def grade(ratio: float, large: bool) -> dict:
    return {
        "ratio": ratio,
        "AA_text": ratio >= (AA_LARGE if large else AA_NORMAL),
        "AAA_text": ratio >= (AAA_LARGE if large else AAA_NORMAL),
        "AA_ui_component": ratio >= UI,
        "text_size": "large" if large else "normal",
    }


def _rgb_to_hsl(rgb):
    r, g, b = (x / 255 for x in rgb)
    mx, mn = max(r, g, b), min(r, g, b); d = mx - mn
    l = (mx + mn) / 2
    if d == 0:
        h = 0.0; s = 0.0
    else:
        s = d / (1 - abs(2 * l - 1))
        if mx == r:
            h = ((g - b) / d) % 6
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h *= 60
    return round(h, 1), round(s, 3), round(l, 3)


def harmony(c1, c2) -> dict:
    h1 = _rgb_to_hsl(c1)[0]; h2 = _rgb_to_hsl(c2)[0]
    diff = abs(h1 - h2) % 360
    diff = min(diff, 360 - diff)
    if diff <= 15:
        rel = "monochrome/analogous-tight"
    elif diff <= 40:
        rel = "analogous"
    elif 80 <= diff <= 100:
        rel = "near-complementary (triad-ish)"
    elif 150 <= diff <= 180:
        rel = "complementary"
    elif 110 <= diff <= 130:
        rel = "triadic"
    else:
        rel = "unclassified"
    return {"hue1": h1, "hue2": h2, "hue_delta": round(diff, 1), "relation": rel}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("colors", nargs="*", help="fg bg  (or two colors with --harmony)")
    ap.add_argument("--large", action="store_true")
    ap.add_argument("--font-pt", type=float)
    ap.add_argument("--bold", action="store_true")
    ap.add_argument("--pairs", help="JSON list of {fg,bg,label,large?}")
    ap.add_argument("--harmony", nargs=2, metavar=("C1", "C2"))
    args = ap.parse_args()

    if args.harmony:
        print(json.dumps(harmony(parse_color(args.harmony[0]), parse_color(args.harmony[1])), indent=2))
        return 0

    if args.pairs:
        rows = json.loads(Path(args.pairs).read_text(encoding="utf-8"))
        out = []
        for r in rows:
            g = grade(contrast(parse_color(r["fg"]), parse_color(r["bg"])), bool(r.get("large")))
            g["label"] = r.get("label", "")
            out.append(g)
        fails = [r["label"] or i for i, r in enumerate(out) if not r["AA_text"]]
        print(json.dumps({"pairs": out, "aa_text_failures": fails}, indent=2))
        return 1 if fails else 0

    if len(args.colors) != 2:
        ap.error("provide fg and bg colors (or use --pairs / --harmony)")
    large = args.large or is_large(args.font_pt, args.bold)
    g = grade(contrast(parse_color(args.colors[0]), parse_color(args.colors[1])), large)
    print(json.dumps(g, indent=2))
    return 0 if g["AA_text"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
