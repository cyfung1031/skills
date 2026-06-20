#!/usr/bin/env python3
"""Deterministic image metadata probe (pure stdlib, no PIL).

Parses real file bytes to report format, pixel dimensions, aspect ratio, bit
depth/color type, DPI, animation, file size, and megapixels for PNG, JPEG, GIF,
BMP, WebP, and SVG. Converts many "inferred/not-verified" appraisal and
grounding claims (resolution adequacy, aspect/DPI fitness, raster scale) into
`measured` facts. Reports fitness flags; it measures, it does not judge.

Usage:
  mythos_image_meta.py <file-or-dir> [--target WxH] [--expect-aspect W:H] [--json out.json]
"""
from __future__ import annotations
import argparse, json, re, struct
from math import gcd
from pathlib import Path

SOF = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
PNG_COLOR = {0: "grayscale", 2: "rgb", 3: "indexed", 4: "grayscale+alpha", 6: "rgba"}


def _png(b: bytes) -> dict:
    out = {"format": "png", "width": int.from_bytes(b[16:20], "big"),
           "height": int.from_bytes(b[20:24], "big"),
           "bit_depth": b[24], "color_type": PNG_COLOR.get(b[25], str(b[25]))}
    i = 8
    while i + 8 <= len(b):
        ln = int.from_bytes(b[i:i + 4], "big"); typ = b[i + 4:i + 8]
        body = b[i + 8:i + 8 + ln]
        if typ == b"pHYs" and len(body) >= 9:
            ppux = int.from_bytes(body[0:4], "big"); unit = body[8]
            if unit == 1 and ppux:
                out["dpi"] = round(ppux * 0.0254, 1)
        elif typ == b"acTL" and len(body) >= 4:
            out["animated"] = True; out["frames"] = int.from_bytes(body[0:4], "big")
        elif typ == b"IEND":
            break
        i += 12 + ln
    return out


def _jpeg(b: bytes) -> dict:
    out = {"format": "jpeg"}; i = 2; n = len(b)
    while i + 4 < n:
        if b[i] != 0xFF:
            i += 1; continue
        m = b[i + 1]; seg = int.from_bytes(b[i + 2:i + 4], "big")
        if m in SOF:
            out["bit_depth"] = b[i + 4]
            out["height"] = int.from_bytes(b[i + 5:i + 7], "big")
            out["width"] = int.from_bytes(b[i + 7:i + 9], "big")
            out["color_type"] = {1: "grayscale", 3: "ycbcr/rgb", 4: "cmyk"}.get(b[i + 9], str(b[i + 9]))
        elif m == 0xE0 and b[i + 4:i + 8] == b"JFIF":
            units = b[i + 11]; xd = int.from_bytes(b[i + 12:i + 14], "big")
            if units == 1 and xd:
                out["dpi"] = float(xd)
            elif units == 2 and xd:
                out["dpi"] = round(xd * 2.54, 1)
        if m in (0xD9, 0xDA):
            break
        i += 2 + seg
    return out


def _gif(b: bytes) -> dict:
    w = struct.unpack("<H", b[6:8])[0]; h = struct.unpack("<H", b[8:10])[0]
    frames = b.count(b"\x21\xf9")  # graphic control extensions ~ frames
    out = {"format": "gif", "width": w, "height": h}
    if frames > 1:
        out["animated"] = True; out["frames"] = frames
    return out


def _bmp(b: bytes) -> dict:
    w = struct.unpack("<i", b[18:22])[0]; h = abs(struct.unpack("<i", b[22:26])[0])
    out = {"format": "bmp", "width": w, "height": h, "bit_depth": struct.unpack("<H", b[28:30])[0]}
    ppmx = struct.unpack("<i", b[38:42])[0]
    if ppmx:
        out["dpi"] = round(ppmx * 0.0254, 1)
    return out


def _webp(b: bytes) -> dict:
    out = {"format": "webp"}; c = b[12:16]
    try:
        if c == b"VP8X":
            out["width"] = (b[24] | b[25] << 8 | b[26] << 16) + 1
            out["height"] = (b[27] | b[28] << 8 | b[29] << 16) + 1
            if b[20] & 0b00000010:
                out["animated"] = True
        elif c == b"VP8 ":
            out["width"] = struct.unpack("<H", b[26:28])[0] & 0x3FFF
            out["height"] = struct.unpack("<H", b[28:30])[0] & 0x3FFF
        elif c == b"VP8L":
            bits = b[21] | b[22] << 8 | b[23] << 16 | b[24] << 24
            out["width"] = (bits & 0x3FFF) + 1
            out["height"] = ((bits >> 14) & 0x3FFF) + 1
    except Exception:
        pass
    return out


def _svg(b: bytes) -> dict:
    t = b[:4096].decode("utf-8", "ignore")
    out = {"format": "svg", "scalable": True}
    vb = re.search(r'viewBox\s*=\s*["\']\s*[\d.\-]+\s+[\d.\-]+\s+([\d.]+)\s+([\d.]+)', t)
    if vb:
        out["viewbox_w"] = float(vb.group(1)); out["viewbox_h"] = float(vb.group(2))
    for dim in ("width", "height"):
        m = re.search(rf'\b{dim}\s*=\s*["\']\s*([\d.]+)', t)
        if m:
            out[dim] = float(m.group(1))
    if "width" not in out and "viewbox_w" in out:
        out["width"] = out["viewbox_w"]; out["height"] = out["viewbox_h"]
    return out


def detect(p: Path) -> dict:
    b = p.read_bytes()
    sig = b[:16]
    try:
        if sig.startswith(b"\x89PNG\r\n\x1a\n"):
            d = _png(b)
        elif sig.startswith(b"\xff\xd8"):
            d = _jpeg(b)
        elif sig[:3] in (b"GIF",) or sig.startswith(b"GIF8"):
            d = _gif(b)
        elif sig.startswith(b"BM"):
            d = _bmp(b)
        elif sig.startswith(b"RIFF") and b[8:12] == b"WEBP":
            d = _webp(b)
        elif b.lstrip()[:5].lower().startswith(b"<?xml") or b"<svg" in b[:4096].lower():
            d = _svg(b)
        else:
            d = {"format": "unknown"}
    except Exception as e:
        d = {"format": "error", "error": str(e)}
    d["file"] = str(p); d["bytes"] = len(b)
    w, h = d.get("width"), d.get("height")
    flags = []
    if w and h:
        g = gcd(int(w), int(h)) or 1
        d["aspect"] = f"{int(w)//g}:{int(h)//g}"
        d["megapixels"] = round(w * h / 1e6, 2)
        if min(w, h) < 100 and not d.get("scalable"):
            flags.append("very-small")
    elif d["format"] not in ("error",):
        flags.append("dimensions-not-readable")
    d["flags"] = flags
    return d


def fitness(d: dict, target, aspect) -> list:
    f = []
    w, h = d.get("width"), d.get("height")
    if target and w and h and not d.get("scalable"):
        tw, th = target
        if w < tw or h < th:
            f.append(f"below-target {int(w)}x{int(h)} < {tw}x{th}")
        if w < 2 * tw or h < 2 * th:
            f.append("under-2x-for-hidpi")
    if aspect and "aspect" in d:
        if d["aspect"] != aspect:
            f.append(f"aspect {d['aspect']} != expected {aspect}")
    if "dpi" not in d and d["format"] not in ("svg", "unknown", "error"):
        f.append("no-dpi-metadata")
    return f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--target", help="WxH minimum render size, e.g. 320x240")
    ap.add_argument("--expect-aspect", help="W:H, e.g. 16:9")
    ap.add_argument("--json", help="write results to JSON path")
    args = ap.parse_args()
    target = tuple(int(x) for x in args.target.lower().split("x")) if args.target else None
    aspect = None
    if args.expect_aspect:
        a, b = args.expect_aspect.split(":"); g = gcd(int(a), int(b)) or 1
        aspect = f"{int(a)//g}:{int(b)//g}"

    root = Path(args.path)
    files = [root] if root.is_file() else sorted(q for q in root.rglob("*") if q.is_file())
    results = []
    for p in files:
        d = detect(p)
        ff = fitness(d, target, aspect)
        if ff:
            d["fitness_flags"] = ff
        results.append(d)
    out = {"count": len(results), "results": results}
    if args.json:
        Path(args.json).write_text(json.dumps(out, indent=2), encoding="utf-8")
        out["json"] = args.json
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
