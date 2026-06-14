#!/usr/bin/env python3
"""Validate the AI Development Loop package structure and key invariants."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MAX_SKILL_BYTES = 10_000
MAX_SKILL_LINES = 300
MAX_SKILL_WORDS = 1_400

ALLOWED_OVERALL = {
    "Blocked",
    "Changes requested",
    "Pending implementation",
    "Approved with notes",
    "Approved",
}
ALLOWED_SPEC_PLAN = {
    "Not started",
    "Changes requested",
    "Approved for implementation",
    "Approved with notes",
    "Approved",
    "Not applicable",
}
ALLOWED_IMPLEMENTATION = {
    "Not started",
    "Changes requested",
    "Pending implementation",
    "Approved with notes",
    "Approved",
    "Not applicable",
}
ALLOWED_K_RESPONSE_STATUS = {
    "Addressed",
    "Partially addressed",
    "Not addressed",
    "Accepted risk",
}
ALLOWED_R_FINDING_STATUS = {
    "Open",
    "Closed",
    "Accepted risk",
}
ALLOWED_R_SEVERITY = {
    "Critical",
    "High",
    "Medium",
    "Low",
    "Note",
}
EXPECTED_K_RESPONSE_STATUS_LINE = "Status: Addressed | Partially addressed | Not addressed | Accepted risk"
EXPECTED_R_SEVERITY_LINE = "Severity: Critical|High|Medium|Low|Note"
EXPECTED_R_FINDING_STATUS_LINE = "Status: Open | Closed | Accepted risk"
REQUIRED_FILES = [
    "README.md",
    "QUICKSTART.md",
    "INSTALLATION.md",
    "COMPLETE-PACKAGE-GUIDE.md",
    "REFERENCE.md",
    "SKILL.md",
    "examples/.ai-dev-loop/README.md",
    "examples/.ai-dev-loop/status.md",
    "examples/.ai-dev-loop/decisions/README.md",
    "scripts/validate-ai-dev-loop-package.py",
    "scripts/install-ai-dev-loop-template.py",
]
REQUIRED_DIRS = [
    "examples/.ai-dev-loop/reviews",
    "examples/.ai-dev-loop/responses",
    "examples/.ai-dev-loop/context",
    "examples/.ai-dev-loop/decisions",
]
REQUIRED_STATUS_HEADINGS = [
    "Current Branch",
    "Current Focus",
    "Latest R Review",
    "Latest K Response",
    "Latest Context Note",
    "Decisions",
    "Approval State",
    "Completed Items",
    "Next Expected Role Action",
    "Next Item",
    "Blockers",
]
REQUIRED_R_HEADINGS = [
    "Scope",
    "Summary",
    "Evidence",
    "Findings",
    "Clarifications Needed",
    "Approval Status",
    "Next Expected K Action",
]
REQUIRED_K_HEADINGS = [
    "Review Addressed",
    "Summary",
    "Evidence",
    "Finding Responses",
    "Spec Updates",
    "Implementation Updates",
    "Tests and Validation",
    "Remaining Questions",
    "Compact Context",
    "Next Expected R Action",
]
STALE_PATTERNS = [
    re.compile(r"If `\.git/` is absent and git is available, the skill initializes git locally", re.I),
    re.compile(r"initializes git locally before normal operation", re.I),
    re.compile(r"copy the root `?\.ai-dev-loop/`? template directory from this package", re.I),
    re.compile(r"root `?\.ai-dev-loop/`? template directory", re.I),
]
FORBIDDEN_PACKAGE_ARTIFACTS = {
    "__MACOSX",
    ".DS_Store",
    "Thumbs.db",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    ".git",
    ".idea",
    ".vscode",
}
FORBIDDEN_PACKAGE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".swp",
    ".tmp",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the AI Development Loop package structure and key invariants."
    )
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Package root to validate. Defaults to the parent of this script directory.",
    )
    return parser.parse_args()


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def has_heading(text: str, heading: str) -> bool:
    return re.search(rf"^##+\s+{re.escape(heading)}\s*$", text, re.MULTILINE) is not None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_headings(path: Path, headings: list[str], label: str, root: Path, errors: list[str]) -> None:
    if not path.exists():
        fail(f"missing {rel(path, root)}", errors)
        return
    text = read_text(path)
    for heading in headings:
        if not has_heading(text, heading):
            fail(f"{rel(path, root)} missing {label} heading: {heading}", errors)
    validate_statuses(path, text, root, errors)
    validate_status_option_lists(path, text, root, errors)


def validate_statuses(path: Path, text: str, root: Path, errors: list[str]) -> None:
    status_specs = [
        ("Spec/Plan Status", ALLOWED_SPEC_PLAN),
        ("Implementation Status", ALLOWED_IMPLEMENTATION),
        ("Overall Status", ALLOWED_OVERALL),
    ]
    for label, allowed in status_specs:
        for value in re.findall(rf"{re.escape(label)}:\s*([^\n]+)", text):
            value = value.strip()
            if value not in allowed:
                fail(f"{rel(path, root)} has non-canonical {label}: {value}", errors)


def split_template_options(value: str) -> list[str]:
    return [part.strip().strip("`") for part in value.split("|") if part.strip()]


def validate_status_option_lists(path: Path, text: str, root: Path, errors: list[str]) -> None:
    status_specs = {
        "Spec/Plan Status": list(ALLOWED_SPEC_PLAN),
        "Implementation Status": list(ALLOWED_IMPLEMENTATION),
        "Overall Status": list(ALLOWED_OVERALL),
    }
    # Preserve canonical order as documented in SKILL.md.
    status_specs["Spec/Plan Status"] = [
        "Not started",
        "Changes requested",
        "Approved for implementation",
        "Approved with notes",
        "Approved",
        "Not applicable",
    ]
    status_specs["Implementation Status"] = [
        "Not started",
        "Changes requested",
        "Pending implementation",
        "Approved with notes",
        "Approved",
        "Not applicable",
    ]
    status_specs["Overall Status"] = [
        "Blocked",
        "Changes requested",
        "Pending implementation",
        "Approved with notes",
        "Approved",
    ]

    for match in re.finditer(r"^-\s*(Spec/Plan Status|Implementation Status|Overall Status):\s*([^\n]+)$", text, re.MULTILINE):
        label, value = match.groups()
        if "|" not in value:
            continue
        found = split_template_options(value)
        expected = status_specs[label]
        if found != expected:
            fail(
                f"{rel(path, root)} has non-canonical {label} option list: {' | '.join(found)}",
                errors,
            )


def validate_k_response_status_templates(root: Path, errors: list[str]) -> None:
    for rel_path in ["SKILL.md", "REFERENCE.md"]:
        path = root / rel_path
        if path.exists():
            text = read_text(path)
            if EXPECTED_K_RESPONSE_STATUS_LINE not in text:
                fail(f"{rel_path} missing canonical K response status template", errors)


def validate_k_response_status_values(path: Path, text: str, root: Path, errors: list[str]) -> None:
    for value in re.findall(r"^-\s*Status:\s*([^\n]+)$", text, re.MULTILINE):
        value = value.strip()
        if value not in ALLOWED_K_RESPONSE_STATUS:
            fail(f"{rel(path, root)} has non-canonical K response Status: {value}", errors)


def iter_blocks(text: str, heading_pattern: str) -> list[str]:
    pattern = re.compile(rf"^{heading_pattern}[\s\S]*?(?=^{heading_pattern}|^##\s|\Z)", re.MULTILINE)
    return [match.group(0) for match in pattern.finditer(text)]


def validate_r_finding_templates(path: Path, text: str, root: Path, errors: list[str]) -> None:
    blocks = iter_blocks(text, r"### Finding R-\d{4}-\d{2}: .+")
    if not blocks:
        fail(f"{rel(path, root)} has no R finding blocks", errors)
        return
    for block in blocks:
        title = block.splitlines()[0].strip()
        severity = re.search(r"^-\s*Severity:\s*([^\n]+)$", block, re.MULTILINE)
        status = re.search(r"^-\s*Status:\s*([^\n]+)$", block, re.MULTILINE)
        details = re.search(r"^-\s*Details:\s*(.+)$", block, re.MULTILINE)
        action = re.search(r"^-\s*Required action:\s*(.+)$", block, re.MULTILINE)
        if not severity:
            fail(f"{rel(path, root)} {title} missing Severity", errors)
        elif severity.group(1).strip() not in ALLOWED_R_SEVERITY:
            fail(f"{rel(path, root)} {title} has non-canonical Severity: {severity.group(1).strip()}", errors)
        if not status:
            fail(f"{rel(path, root)} {title} missing Status", errors)
        elif status.group(1).strip() not in ALLOWED_R_FINDING_STATUS:
            fail(f"{rel(path, root)} {title} has non-canonical Status: {status.group(1).strip()}", errors)
        if not details:
            fail(f"{rel(path, root)} {title} missing Details", errors)
        if not action:
            fail(f"{rel(path, root)} {title} missing Required action", errors)


def validate_k_response_templates(path: Path, text: str, root: Path, errors: list[str]) -> None:
    blocks = iter_blocks(text, r"### Response to R-\d{4}-\d{2}")
    if not blocks:
        fail(f"{rel(path, root)} has no K response blocks", errors)
        return
    for block in blocks:
        title = block.splitlines()[0].strip()
        status = re.search(r"^-\s*Status:\s*([^\n]+)$", block, re.MULTILINE)
        changes = re.search(r"^-\s*Changes made:\s*(.+)$", block, re.MULTILINE)
        evidence = re.search(r"^-\s*Evidence:\s*(.+)$", block, re.MULTILINE)
        if not status:
            fail(f"{rel(path, root)} {title} missing Status", errors)
        elif status.group(1).strip() not in ALLOWED_K_RESPONSE_STATUS:
            fail(f"{rel(path, root)} {title} has non-canonical Status: {status.group(1).strip()}", errors)
        if not changes:
            fail(f"{rel(path, root)} {title} missing Changes made", errors)
        if not evidence:
            fail(f"{rel(path, root)} {title} missing Evidence", errors)


def validate_reference_status_vocabulary(root: Path, errors: list[str]) -> None:
    for rel_path in ["SKILL.md", "REFERENCE.md"]:
        path = root / rel_path
        if path.exists():
            validate_status_option_lists(path, read_text(path), root, errors)


def validate_reference_bullet_status_lists(root: Path, errors: list[str]) -> None:
    """Check that bold-header bullet lists in REFERENCE.md use only canonical status values."""
    ref = root / "REFERENCE.md"
    if not ref.exists():
        return
    text = read_text(ref)
    sections: dict[str, set[str]] = {
        "Spec/Plan Status": ALLOWED_SPEC_PLAN,
        "Implementation Status": ALLOWED_IMPLEMENTATION,
        "Overall Status": ALLOWED_OVERALL,
    }
    for label, allowed in sections.items():
        pattern = re.compile(
            rf"\*\*{re.escape(label)}:\*\*\s*\n((?:\s*\n|\s*-\s+.+\n?)+)",
            re.MULTILINE,
        )
        for m in pattern.finditer(text):
            block = m.group(1)
            for bullet in re.findall(r"^-\s+`?([^`\n]+?)`?\s*$", block, re.MULTILINE):
                bullet = bullet.strip()
                if bullet not in allowed:
                    fail(
                        f"REFERENCE.md has non-canonical {label} bullet value: {bullet}",
                        errors,
                    )




def is_forbidden_artifact_path(path: Path, root: Path) -> bool:
    parts = set(path.relative_to(root).parts)
    return bool(parts & FORBIDDEN_PACKAGE_ARTIFACTS) or path.suffix in FORBIDDEN_PACKAGE_SUFFIXES

def validate_required_paths(root: Path, errors: list[str]) -> None:
    for rel_path in REQUIRED_FILES:
        path = root / rel_path
        if not path.is_file():
            fail(f"missing required file: {rel_path}", errors)
    for rel_path in REQUIRED_DIRS:
        path = root / rel_path
        if not path.is_dir():
            fail(f"missing required directory: {rel_path}", errors)


def validate_stale_language(root: Path, errors: list[str]) -> None:
    for path in root.rglob("*.md"):
        if is_forbidden_artifact_path(path, root):
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError as exc:
            fail(f"{rel(path, root)} is not valid UTF-8 Markdown: {exc}", errors)
            continue
        for pattern in STALE_PATTERNS:
            if pattern.search(text):
                fail(f"{rel(path, root)} contains stale git-bootstrap language: {pattern.pattern}", errors)


def validate_clean_package(root: Path, errors: list[str]) -> None:
    root_template = root / ".ai-dev-loop"
    if root_template.exists():
        fail("forbidden duplicate root .ai-dev-loop template found", errors)
    for path in root.rglob("*"):
        if is_forbidden_artifact_path(path, root):
            if path.suffix in FORBIDDEN_PACKAGE_SUFFIXES:
                fail(f"forbidden generated file found: {rel(path, root)}", errors)
            else:
                fail(f"forbidden packaging artifact found: {rel(path, root)}", errors)


def get_skill_version(root: Path, errors: list[str]) -> str | None:
    skill = root / "SKILL.md"
    if not skill.exists():
        return None
    text = read_text(skill)
    match = re.search(r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        fail("SKILL.md missing semantic version in front matter", errors)
        return None
    return match.group(1)


def validate_version_consistency(root: Path, errors: list[str]) -> None:
    expected = get_skill_version(root, errors)
    if not expected:
        return
    md_files = [path for path in root.glob("*.md") if path.name != "SKILL.md"]
    # Negative lookbehind excludes dependency-pin comparators (>=, <=, !=, ==, ~=, >, <).
    version_re = re.compile(r"(?<![>=<!~])(?:^|\b)(?:v)?([0-9]+\.[0-9]+\.[0-9]+)\b", re.MULTILINE)
    for path in [root / "SKILL.md", *md_files]:
        if not path.exists():
            continue
        text = read_text(path)
        for match in version_re.finditer(text):
            found = match.group(1)
            if found != expected:
                fail(f"{rel(path, root)} has version {found}; expected {expected}", errors)
    readme = root / "README.md"
    if readme.exists() and f"**Version**: {expected}" not in read_text(readme):
        fail(f"README.md missing documented version {expected}", errors)


def validate_compact_skill(root_skill: Path, root: Path, errors: list[str]) -> None:
    if not root_skill.exists():
        return
    text = read_text(root_skill)
    byte_count = len(text.encode("utf-8"))
    line_count = text.count("\n") + 1
    word_count = len(re.findall(r"\S+", text))
    if byte_count > MAX_SKILL_BYTES:
        fail(f"SKILL.md exceeds compact size budget: {byte_count} bytes > {MAX_SKILL_BYTES}", errors)
    if line_count > MAX_SKILL_LINES:
        fail(f"SKILL.md exceeds compact line budget: {line_count} lines > {MAX_SKILL_LINES}", errors)
    if word_count > MAX_SKILL_WORDS:
        fail(f"SKILL.md exceeds compact word budget: {word_count} words > {MAX_SKILL_WORDS}", errors)
    required_phrases = [
        "`REFERENCE.md` is an optional expansion file",
        "Do not load `REFERENCE.md` by default for simple role turns",
        "If `SKILL.md`, `REFERENCE.md`, examples, and status records conflict",
        "extract into a new empty staging directory first",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            fail(f"SKILL.md missing compact-skill safeguard phrase: {phrase}", errors)



def validate_embedded_record_templates(root: Path, errors: list[str]) -> None:
    """Ensure documented R/K templates keep the canonical section structure."""
    template_files = ["SKILL.md", "REFERENCE.md"]
    for rel_path in template_files:
        path = root / rel_path
        if not path.exists():
            continue
        text = read_text(path)
        for heading in REQUIRED_R_HEADINGS:
            if not has_heading(text, heading):
                fail(f"{rel_path} missing embedded R template heading: {heading}", errors)
        for heading in REQUIRED_K_HEADINGS:
            if not has_heading(text, heading):
                fail(f"{rel_path} missing embedded K template heading: {heading}", errors)
        for expected_line in [EXPECTED_R_SEVERITY_LINE, EXPECTED_R_FINDING_STATUS_LINE]:
            if expected_line not in text:
                fail(f"{rel_path} missing canonical R finding template line: {expected_line}", errors)


def validate_installer_smoke_test(root: Path, errors: list[str]) -> None:
    """Run the installer against temp projects to validate safety and output shape."""
    installer = root / "scripts" / "install-ai-dev-loop-template.py"
    if not installer.exists():
        return
    with tempfile.TemporaryDirectory(prefix="ai-dev-loop-validator-") as tmp_name:
        tmp = Path(tmp_name)
        marked_project = tmp / "marked-project"
        marked_project.mkdir()
        (marked_project / "README.md").write_text("# Marked project\n", encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(installer), str(marked_project)],
            cwd=str(root),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"installer smoke test failed for marked project: {result.stderr.strip() or result.stdout.strip()}", errors)
            return

        expected_paths = [
            ".ai-dev-loop/SKILL.md",
            ".ai-dev-loop/REFERENCE.md",
            ".ai-dev-loop/status.md",
            ".ai-dev-loop/README.md",
            ".ai-dev-loop/reviews",
            ".ai-dev-loop/responses",
            ".ai-dev-loop/context",
            ".ai-dev-loop/context/README.md",
            ".ai-dev-loop/decisions",
            ".ai-dev-loop/decisions/README.md",
        ]
        for rel_path in expected_paths:
            if not (marked_project / rel_path).exists():
                fail(f"installer smoke test missing output path: {rel_path}", errors)

        unmarked_project = tmp / "unmarked-project"
        unmarked_project.mkdir()
        result = subprocess.run(
            [sys.executable, str(installer), str(unmarked_project), "--dry-run"],
            cwd=str(root),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            fail("installer smoke test expected unmarked project root to be rejected", errors)

        live_record = marked_project / ".ai-dev-loop" / "reviews" / "0001-r-review.md"
        live_record.write_text("# Existing review\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(installer), str(marked_project), "--force", "--dry-run"],
            cwd=str(root),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            fail("installer smoke test expected --force without --force-live-records to reject live records", errors)


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    if not root.exists() or not root.is_dir():
        print(f"AI Development Loop package validation failed:\n- package root does not exist or is not a directory: {root}")
        return 1

    validate_required_paths(root, errors)
    validate_clean_package(root, errors)
    validate_version_consistency(root, errors)

    root_skill = root / "SKILL.md"
    if root_skill.exists():
        validate_compact_skill(root_skill, root, errors)

    validate_reference_status_vocabulary(root, errors)
    validate_reference_bullet_status_lists(root, errors)
    validate_k_response_status_templates(root, errors)
    validate_embedded_record_templates(root, errors)
    validate_installer_smoke_test(root, errors)

    for status_path in [root / "examples" / ".ai-dev-loop" / "status.md"]:
        validate_headings(status_path, REQUIRED_STATUS_HEADINGS, "status", root, errors)

    reviews_dir = root / "examples" / ".ai-dev-loop" / "reviews"
    responses_dir = root / "examples" / ".ai-dev-loop" / "responses"
    if reviews_dir.exists():
        for path in sorted(reviews_dir.glob("*.md")):
            text = read_text(path)
            validate_headings(path, REQUIRED_R_HEADINGS, "R", root, errors)
            validate_r_finding_templates(path, text, root, errors)
    if responses_dir.exists():
        for path in sorted(responses_dir.glob("*.md")):
            text = read_text(path)
            validate_headings(path, REQUIRED_K_HEADINGS, "K", root, errors)
            validate_k_response_status_values(path, text, root, errors)
            validate_k_response_templates(path, text, root, errors)

    validate_stale_language(root, errors)

    if errors:
        print("AI Development Loop package validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("AI Development Loop package validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
