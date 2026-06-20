#!/usr/bin/env python3
"""Deterministic visual-cue -> source locator (pure stdlib).

Links what is *seen* in a visual to *where it lives* in code without rendering or
re-capturing: greps a source tree for visible strings, colors, class/id-like
tokens, and pixel sizes, then ranks candidate files by match specificity and cue
diversity. Built for capture-constrained work where trial-and-error screenshots
are not allowed — front-load localization from one artifact + the source.

It finds candidates; it does not prove a file renders the pixels (that is a
render fact, kept separate per the skill's source/render boundary).

Usage:
  mythos_source_locator.py --root SRC [--text "Submit" ...] [--color "#3366cc" ...]
                           [--token btn-primary ...] [--size 120 ...]
                           [--spec cues.json] [--ext .tsx,.css,...] [--max N]
cues.json: {"text":["Submit"],"color":["#3366cc"],"token":["btn-primary"],"size":[120]}
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

DEFAULT_EXT = {".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".jsx",
               ".ts", ".tsx", ".vue", ".svelte", ".svg", ".xml", ".json", ".py",
               ".rb", ".php", ".astro", ".md", ".styl"}
IGNORE_DIRS = {".git", "node_modules", "dist", "build", "out", ".next", "vendor",
               "__pycache__", "coverage", ".venv", "venv"}
# cue kind -> base weight (specificity); longer text scales higher
WEIGHT = {"text": 5.0, "color": 3.0, "token": 3.0, "size": 1.0}
MAX_BYTES = 2_000_000


def norm_hex(c: str):
    c = c.strip().lstrip("#").lower()
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    if len(c) != 6 or any(ch not in "0123456789abcdef" for ch in c):
        return None
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return c, (r, g, b)


def color_patterns(c: str):
    nh = norm_hex(c)
    if not nh:
        return []
    hexv, (r, g, b) = nh
    pats = [re.compile(f"#{hexv}", re.I), re.compile(rf"#{hexv[0]}{hexv[2]}{hexv[4]}\b", re.I)]
    pats.append(re.compile(rf"rgba?\(\s*{r}\s*,\s*{g}\s*,\s*{b}\b"))
    return pats


def build_cues(args) -> list:
    cues = []
    for t in args.text:
        cues.append(("text", t, [re.compile(re.escape(t))], min(2.0, 0.15 * len(t)) + WEIGHT["text"]))
    for c in args.color:
        ps = color_patterns(c)
        if ps:
            cues.append(("color", c, ps, WEIGHT["color"]))
    for tok in args.token:
        cues.append(("token", tok, [re.compile(rf"\b{re.escape(tok)}\b")], WEIGHT["token"]))
    for s in args.size:
        s = str(s).rstrip("px")
        cues.append(("size", s + "px", [re.compile(rf"\b{re.escape(s)}px\b"),
                                        re.compile(rf"[:\s]{re.escape(s)}\b")], WEIGHT["size"]))
    return cues


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--text", action="append", default=[])
    ap.add_argument("--color", action="append", default=[])
    ap.add_argument("--token", action="append", default=[])
    ap.add_argument("--size", action="append", default=[])
    ap.add_argument("--spec", help="JSON cue spec")
    ap.add_argument("--ext", help="comma list overriding default extensions")
    ap.add_argument("--max", type=int, default=50, help="max matches to list")
    ap.add_argument("--json", help="write full result to JSON path")
    args = ap.parse_args()

    if args.spec:
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
        args.text += spec.get("text", [])
        args.color += spec.get("color", [])
        args.token += spec.get("token", [])
        args.size += [str(x) for x in spec.get("size", [])]

    cues = build_cues(args)
    if not cues:
        print(json.dumps({"status": "fail", "errors": ["no cues provided"]}, indent=2))
        return 1
    exts = set(e if e.startswith(".") else "." + e for e in args.ext.split(",")) if args.ext else DEFAULT_EXT

    root = Path(args.root)
    matches = []
    file_score: dict = {}
    file_cuekinds: dict = {}
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in exts:
            continue
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        try:
            if p.stat().st_size > MAX_BYTES:
                continue
            lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        rel = str(p.relative_to(root))
        for ln, line in enumerate(lines, 1):
            for kind, raw, pats, weight in cues:
                if any(pat.search(line) for pat in pats):
                    matches.append({"file": rel, "line": ln, "cue": raw, "kind": kind,
                                    "text": line.strip()[:160]})
                    file_score[rel] = file_score.get(rel, 0.0) + weight
                    file_cuekinds.setdefault(rel, set()).add(kind)

    # diversity bonus: a file matched by several distinct cue kinds is likelier the source
    ranked = []
    for f, sc in file_score.items():
        kinds = file_cuekinds[f]
        score = round(sc * (1 + 0.5 * (len(kinds) - 1)), 2)
        conf = "high" if (len(kinds) >= 2 or any(m["kind"] == "text" for m in matches if m["file"] == f)) else \
               ("medium" if kinds & {"color", "token"} else "low")
        ranked.append({"file": f, "score": score, "cue_kinds": sorted(kinds), "confidence": conf})
    ranked.sort(key=lambda r: r["score"], reverse=True)

    out = {
        "status": "pass",
        "cues": [{"kind": k, "cue": r} for k, r, _, _ in cues],
        "match_count": len(matches),
        "ranked_files": ranked[:args.max],
        "matches": matches[:args.max],
        "note": "candidates only; renders-the-pixels is a render fact, not proven here",
    }
    if args.json:
        Path(args.json).write_text(json.dumps(out, indent=2), encoding="utf-8")
        out["json"] = args.json
    print(json.dumps(out, indent=2))
    return 0 if matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
