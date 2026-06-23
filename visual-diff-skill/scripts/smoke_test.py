#!/usr/bin/env python3
"""Create deterministic fixtures, run the comparator, and validate key outputs."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
VISUAL_DIFF = ROOT / "visual_diff.py"
VALIDATE = ROOT / "scripts" / "validate_report.py"


def _make_fixtures(work: Path) -> tuple[Path, Path, Path]:
    a = Image.new("RGB", (96, 64), "white")
    draw = ImageDraw.Draw(a)
    draw.rectangle((12, 12, 42, 42), fill="navy")
    draw.line((55, 10, 84, 44), fill="black", width=3)

    b = a.copy()
    draw_b = ImageDraw.Draw(b)
    draw_b.rectangle((12, 12, 42, 42), fill="navy")
    draw_b.rectangle((60, 18, 86, 46), fill="red")

    c = a.copy()

    a_path = work / "a.png"
    b_path = work / "b.png"
    c_path = work / "c.png"
    a.save(a_path)
    b.save(b_path)
    c.save(c_path)
    return a_path, b_path, c_path


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="visual_diff_skill_smoke_") as tmp:
        work = Path(tmp)
        a_path, b_path, c_path = _make_fixtures(work)

        same_dir = work / "same_report"
        same_json = same_dir / "report.json"
        same = _run([
            sys.executable,
            str(VISUAL_DIFF),
            str(a_path),
            str(c_path),
            "--output-dir",
            str(same_dir),
            "--json-out",
            str(same_json),
            "--quiet",
        ])
        if same.returncode != 0:
            print(same.stdout)
            print(same.stderr, file=sys.stderr)
            return 1
        same_data = json.loads(same_json.read_text(encoding="utf-8"))
        if same_data["decision"] != "same" or not same_data["is_exact_match"]:
            print("expected identical fixtures to be same", file=sys.stderr)
            return 1

        diff_dir = work / "diff_report"
        diff_json = diff_dir / "report.json"
        diff = _run([
            sys.executable,
            str(VISUAL_DIFF),
            str(a_path),
            str(b_path),
            "--output-dir",
            str(diff_dir),
            "--json-out",
            str(diff_json),
            "--fail-on",
            "different",
            "--quiet",
        ])
        if diff.returncode != 1:
            print(diff.stdout)
            print(diff.stderr, file=sys.stderr)
            print("expected --fail-on different to exit 1", file=sys.stderr)
            return 1
        diff_data = json.loads(diff_json.read_text(encoding="utf-8"))
        if diff_data["decision"] != "different":
            print("expected changed fixture to be different", file=sys.stderr)
            return 1
        if not diff_data["regions"] or not diff_data["edge_regions"]:
            print("expected region and edge-region evidence", file=sys.stderr)
            return 1
        if diff_data["audit"]["skill_version"] != "0.2.0":
            print("expected audit skill_version 0.2.0", file=sys.stderr)
            return 1

        validation = _run([sys.executable, str(VALIDATE), str(diff_json)])
        if validation.returncode != 0:
            print(validation.stdout)
            print(validation.stderr, file=sys.stderr)
            return 1

    print("smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
