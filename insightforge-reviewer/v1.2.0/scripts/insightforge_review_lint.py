#!/usr/bin/env python3
"""Lightweight lint for InsightForge review artifacts."""
from __future__ import annotations
import re, sys
from pathlib import Path

TAGS = {"observed", "measured", "inferred", "assumed", "external-cited", "external-unverified", "not-evaluated"}
FIELDS = ["Severity", "Finding", "Evidence", "Why", "Better amendment", "Validation", "Confidence", "Residual risk"]

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: insightforge_review_lint.py <review.md>")
        return 2
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not any(tag in text for tag in TAGS):
        errors.append("no evidence tag found")
    # Table-style finding rows should have enough pipes and an evidence tag.
    rows = [line for line in text.splitlines() if "|" in line and re.search(r"blocker|high|medium|low|polish", line, re.I)]
    for i, row in enumerate(rows, 1):
        if row.count("|") < 7:
            errors.append(f"finding row {i} has fewer than 8 schema columns")
        if not any(tag in row for tag in TAGS):
            errors.append(f"finding row {i} missing evidence tag")
    # Heading-style reviews should include the core field labels somewhere.
    if rows:
        pass
    elif "Finding" in text:
        missing = [f for f in FIELDS if not re.search(rf"\b{re.escape(f)}\b", text, re.I)]
        if missing:
            errors.append("missing finding fields: " + ", ".join(missing))
    if errors:
        print("INSIGHTFORGE_REVIEW_LINT failed:")
        for e in errors:
            print("- " + e)
        return 1
    print("INSIGHTFORGE_REVIEW_LINT passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
