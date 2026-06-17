#!/usr/bin/env python3
"""Lightweight lint for InsightForge review artifacts (v1.2.1)."""
from __future__ import annotations
import re, sys
from pathlib import Path

TAGS = {"observed", "measured", "inferred", "assumed", "external-cited", "external-unverified", "not-evaluated"}
FIELDS = ["Severity", "Finding", "Evidence", "Why", "Better amendment", "Validation", "Confidence", "Residual risk"]
# Minimum-viable finding line: severity | finding | tag+locator | amendment | validation -> 5 fields, 4 pipes.
MIN_PIPES = 4

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: insightforge_review_lint.py <review.md>")
        return 2
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not any(tag in text for tag in TAGS):
        errors.append("no evidence tag found")
    # Finding rows: a pipe-delimited line tagged with a severity level.
    rows = [line for line in text.splitlines() if "|" in line and re.search(r"blocker|high|medium|low|polish", line, re.I)]
    for i, row in enumerate(rows, 1):
        if row.count("|") < MIN_PIPES:
            errors.append(
                f"finding row {i} has fewer than 5 fields "
                f"(need: severity | finding | evidence tag + locator | amendment | validation)"
            )
        if not any(tag in row for tag in TAGS):
            errors.append(f"finding row {i} missing verbatim evidence tag")
    # Heading-style reviews with no delimited rows should still name the core fields.
    if not rows and "Finding" in text:
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
