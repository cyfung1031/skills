#!/usr/bin/env python3
"""Deterministic layout / geometry checker over bounding boxes (pure stdlib).

Serves design/UX appraisal (alignment, spacing, grid), spatial grounding
(reachability, minimum hit size, coordinate/DPR transforms), and diagnosis
(overlap, clipping, off-canvas). It computes geometry facts (`measured`) from
boxes you provide; it does not detect boxes from an image.

Input JSON:
{
  "canvas": [width, height],          # optional
  "dpr": 2,                           # optional, for px<->css transforms
  "tolerance": 2,                     # px slack for alignment/spacing, default 2
  "min_hit": 24,                      # min interactive size px, default 24
  "boxes": [
    {"id":"btn","x":10,"y":20,"w":120,"h":40,"interactive":true},
    {"id":"icon","x":10,"y":80,"w":16,"h":16,"interactive":true}
  ]
}
Boxes accept x,y,w,h OR x0,y0,x1,y1.

Usage:
  mythos_layout_check.py boxes.json [--strict]
  mythos_layout_check.py --transform "x,y" --from WxH --to WxH [--dpr N]
"""
from __future__ import annotations
import argparse, json, sys
from itertools import combinations
from pathlib import Path


def norm(b: dict) -> dict:
    if "w" in b and "h" in b:
        x0, y0, w, h = b["x"], b["y"], b["w"], b["h"]
        x1, y1 = x0 + w, y0 + h
    else:
        x0, y0, x1, y1 = b["x0"], b["y0"], b["x1"], b["y1"]
        w, h = x1 - x0, y1 - y0
    return {"id": b.get("id", "?"), "x0": x0, "y0": y0, "x1": x1, "y1": y1,
            "w": w, "h": h, "cx": (x0 + x1) / 2, "cy": (y0 + y1) / 2,
            "interactive": bool(b.get("interactive"))}


def overlap_area(a, b) -> float:
    ix = max(0, min(a["x1"], b["x1"]) - max(a["x0"], b["x0"]))
    iy = max(0, min(a["y1"], b["y1"]) - max(a["y0"], b["y0"]))
    return ix * iy


def align_groups(boxes, tol):
    out = {}
    for edge, key in (("left", "x0"), ("right", "x1"), ("hcenter", "cx"),
                      ("top", "y0"), ("bottom", "y1"), ("vcenter", "cy")):
        groups = []
        for box in sorted(boxes, key=lambda z: z[key]):
            for g in groups:
                if abs(g["val"] - box[key]) <= tol:
                    g["ids"].append(box["id"]); g["val"] = (g["val"] * (len(g["ids"]) - 1) + box[key]) / len(g["ids"])
                    break
            else:
                groups.append({"val": box[key], "ids": [box["id"]]})
        shared = [{"at": round(g["val"], 1), "ids": g["ids"]} for g in groups if len(g["ids"]) > 1]
        if shared:
            out[edge] = shared
    return out


def spacing_rhythm(boxes, tol, axis):
    key0, key1 = ("x0", "x1") if axis == "x" else ("y0", "y1")
    s = sorted(boxes, key=lambda z: z[key0])
    gaps = [round(s[i + 1][key0] - s[i][key1], 1) for i in range(len(s) - 1)]
    consistent = len(gaps) > 1 and (max(gaps) - min(gaps)) <= tol
    return {"order": [b["id"] for b in s], "gaps": gaps, "consistent": consistent}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="?")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--transform", help="point 'x,y' to remap between frames")
    ap.add_argument("--from", dest="src", help="source WxH")
    ap.add_argument("--to", dest="dst", help="target WxH")
    ap.add_argument("--dpr", type=float, default=1.0)
    args = ap.parse_args()

    if args.transform:
        x, y = (float(v) for v in args.transform.split(","))
        out = {"input": [x, y], "dpr": args.dpr}
        if args.src and args.dst:
            sw, sh = (float(v) for v in args.src.lower().split("x"))
            dw, dh = (float(v) for v in args.dst.lower().split("x"))
            rx, ry = x * dw / sw, y * dh / sh
            out["scaled"] = [round(rx, 2), round(ry, 2)]
            out["normalized"] = [round(x / sw, 4), round(y / sh, 4)]
            out["device_px"] = [round(rx * args.dpr, 2), round(ry * args.dpr, 2)]
        else:
            out["device_px"] = [round(x * args.dpr, 2), round(y * args.dpr, 2)]
        print(json.dumps(out, indent=2))
        return 0

    if not args.input:
        ap.error("provide boxes JSON, or use --transform")
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    tol = data.get("tolerance", 2)
    min_hit = data.get("min_hit", 24)
    canvas = data.get("canvas")
    boxes = [norm(b) for b in data["boxes"]]

    findings = []
    for a, b in combinations(boxes, 2):
        ov = overlap_area(a, b)
        if ov > 0:
            findings.append(f"overlap: {a['id']} & {b['id']} ({round(ov)} px^2)")
    if canvas:
        cw, ch = canvas
        for b in boxes:
            if b["x0"] < 0 or b["y0"] < 0 or b["x1"] > cw or b["y1"] > ch:
                findings.append(f"off-canvas/clipped: {b['id']}")
    small = [b["id"] for b in boxes if b["interactive"] and (b["w"] < min_hit or b["h"] < min_hit)]
    for sid in small:
        findings.append(f"hit-target below {min_hit}px: {sid}")

    out = {
        "status": "fail" if (args.strict and findings) else "pass",
        "boxes": len(boxes),
        "alignment": align_groups(boxes, tol),
        "spacing_x": spacing_rhythm(boxes, tol, "x"),
        "spacing_y": spacing_rhythm(boxes, tol, "y"),
        "findings": findings,
    }
    print(json.dumps(out, indent=2))
    return 1 if (args.strict and findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
