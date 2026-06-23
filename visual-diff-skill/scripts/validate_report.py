#!/usr/bin/env python3
"""Validate a visual-diff-skill JSON report and its referenced artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL = {
    "decision",
    "is_exact_match",
    "same_size",
    "image_a_size",
    "image_b_size",
    "compared_size",
    "changed_pixels",
    "total_pixels",
    "changed_pixel_ratio",
    "mae",
    "mse",
    "rmse",
    "max_delta",
    "psnr_db",
    "ssim",
    "residual",
    "edge_metrics",
    "regions",
    "edge_regions",
    "objects_a",
    "objects_b",
    "output_files",
    "config",
    "audit",
    "explanation",
}

VALID_DECISIONS = {"same", "similar", "different"}


def _fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_report(report_path: str | Path) -> list[str]:
    path = Path(report_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        errors.append(f"missing top-level keys: {', '.join(missing)}")

    if data.get("decision") not in VALID_DECISIONS:
        errors.append("decision must be one of same, similar, different")

    for key in ("changed_pixel_ratio", "mae", "mse", "rmse", "ssim"):
        if key in data and not _is_number(data[key]):
            errors.append(f"{key} must be numeric")

    if _is_number(data.get("changed_pixel_ratio")) and not 0 <= data["changed_pixel_ratio"] <= 1:
        errors.append("changed_pixel_ratio must be in 0..1")
    if _is_number(data.get("ssim")) and not -1 <= data["ssim"] <= 1:
        errors.append("ssim must be in -1..1")

    audit = data.get("audit", {})
    if audit.get("skill_name") != "visual-diff-skill":
        errors.append("audit.skill_name must be visual-diff-skill")
    if not str(audit.get("skill_version", "")).startswith("0.2."):
        errors.append("audit.skill_version must be a 0.2.x build")
    for side in ("image_a", "image_b"):
        sha = audit.get("inputs", {}).get(side, {}).get("sha256")
        if not isinstance(sha, str) or len(sha) != 64:
            errors.append(f"audit.inputs.{side}.sha256 must be a SHA-256 hex digest")

    output_files = data.get("output_files", {})
    if output_files:
        for name, artifact in output_files.items():
            artifact_path = Path(artifact)
            if not artifact_path.is_absolute() and not artifact_path.exists():
                artifact_path = path.parent / artifact_path
            if not artifact_path.exists():
                errors.append(f"missing artifact {name}: {artifact}")

    return errors


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        return _fail("usage: validate_report.py REPORT_JSON")
    errors = validate_report(argv[0])
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("report valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
