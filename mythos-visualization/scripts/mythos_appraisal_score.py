#!/usr/bin/env python3
"""Deterministic weighted-rubric appraisal scorer for mythos-visualization.

Aggregates criteria scores into weighted verdicts and flags evidence/inflation
problems across one or many candidates. It performs mechanical aggregation only;
it does not judge visuals or invent scores.

Input JSON:
{
  "scale": 10,                      # optional, default 10
  "candidates": {
    "A": [
      {"criterion": "composition", "weight": 3, "score": 8, "evidence": "rule-of-thirds focal point"},
      {"criterion": "color",       "weight": 2, "score": 6, "evidence": "muted but coherent palette"}
    ],
    "B": [ ... ]
  }
}
A single-candidate flat list [ {criterion,...}, ... ] is also accepted.

Guards (reported, not fatal unless --strict):
  - score above 8 with empty/placeholder evidence
  - score above 9 (requires strong evidence + no material weakness — human-confirmed)
  - score out of [0, scale]
  - non-positive weight; all-zero weights
  - duplicate criterion names within a candidate
"""
from __future__ import annotations
import argparse, csv, json, sys
from pathlib import Path

PLACEHOLDER = {"", "n/a", "na", "none", "tbd", "todo", "-", "?"}


def load(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        data = {"candidates": {"candidate": data}}
    if "candidates" not in data and isinstance(data, dict) and "criterion" not in data:
        # allow {"A": [...], "B": [...]} shorthand
        if all(isinstance(v, list) for v in data.values()):
            data = {"candidates": data}
    return data


def score_candidate(name: str, rows: list, scale: float, warnings: list) -> dict:
    seen = set()
    wsum = 0.0
    contrib = 0.0
    for r in rows:
        crit = str(r.get("criterion", "?"))
        if crit in seen:
            warnings.append(f"{name}: duplicate criterion '{crit}'")
        seen.add(crit)
        try:
            w = float(r.get("weight", 1))
            s = float(r.get("score"))
        except (TypeError, ValueError):
            warnings.append(f"{name}/{crit}: non-numeric weight/score")
            continue
        ev = str(r.get("evidence", "")).strip().lower()
        if w <= 0:
            warnings.append(f"{name}/{crit}: non-positive weight {w}")
        if s < 0 or s > scale:
            warnings.append(f"{name}/{crit}: score {s} out of range 0..{scale}")
        if s > 0.8 * scale and ev in PLACEHOLDER:
            warnings.append(f"{name}/{crit}: score {s} > 80% of scale with no evidence")
        if s > 0.9 * scale:
            warnings.append(f"{name}/{crit}: score {s} > 90% of scale — requires strong evidence + no material weakness (confirm)")
        if w > 0:
            wsum += w
            contrib += w * s
    if wsum <= 0:
        warnings.append(f"{name}: total positive weight is zero — cannot aggregate")
        agg = None
    else:
        agg = round(contrib / wsum, 3)
    return {"candidate": name, "criteria": len(rows), "weight_sum": wsum, "weighted_score": agg, "scale": scale}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="appraisal JSON path")
    ap.add_argument("--matrix", help="write score_matrix.csv to this path")
    ap.add_argument("--strict", action="store_true", help="exit non-zero if any warning")
    args = ap.parse_args()

    data = load(args.input)
    scale = float(data.get("scale", 10))
    cands = data.get("candidates", {})
    if not cands:
        print(json.dumps({"status": "fail", "errors": ["no candidates found"]}, indent=2))
        return 1

    warnings: list = []
    results = [score_candidate(name, rows, scale, warnings) for name, rows in cands.items()]
    ranked = sorted(
        [r for r in results if r["weighted_score"] is not None],
        key=lambda r: r["weighted_score"], reverse=True,
    )
    for i, r in enumerate(ranked, 1):
        r["rank"] = i

    if args.matrix:
        crits = []
        for rows in cands.values():
            for r in rows:
                c = str(r.get("criterion", "?"))
                if c not in crits:
                    crits.append(c)
        with open(args.matrix, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["candidate"] + crits + ["weighted_score", "rank"])
            rankmap = {r["candidate"]: r.get("rank", "") for r in results}
            scoremap = {r["candidate"]: r["weighted_score"] for r in results}
            for name, rows in cands.items():
                by = {str(x.get("criterion", "?")): x.get("score", "") for x in rows}
                w.writerow([name] + [by.get(c, "") for c in crits] + [scoremap.get(name, ""), rankmap.get(name, "")])

    out = {
        "status": "fail" if (args.strict and warnings) else "pass",
        "scale": scale,
        "candidates": len(cands),
        "results": results,
        "ranking": [r["candidate"] for r in ranked],
        "warnings": warnings,
    }
    if args.matrix:
        out["matrix"] = args.matrix
    print(json.dumps(out, indent=2))
    return 1 if (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
