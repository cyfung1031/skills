#!/usr/bin/env python3
"""Validate the AI Development Loop package structure and key invariants."""
from __future__ import annotations

import argparse
from collections import OrderedDict
import io
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# Compact skill budgets use provider-neutral proxies. They leave roughly 20%
# maintenance headroom over the compact skill while still catching bloat.
MAX_SKILL_BYTES = 21_000
MAX_SKILL_LINES = 290
MAX_SKILL_WORDS = 2_700
MAX_TEXT_FILE_BYTES = 2_000_000
# Keep import-time validator use fast without letting long-lived processes grow
# memory unboundedly. The defaults cover the package's normal repeated-read
# pattern with headroom while limiting retained text to a small, predictable
# amount. Tests may monkeypatch these constants.
MAX_TEXT_CACHE_ENTRIES = 256
MAX_TEXT_CACHE_BYTES = 32_000_000
TextCacheKey = tuple[str, int, int, int]
_TEXT_CACHE: OrderedDict[TextCacheKey, tuple[str, int]] = OrderedDict()
_TEXT_CACHE_BYTES = 0

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
    "Open Required Findings",
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
    "Clarification and Objection Responses",
    "Approval Status",
    "Next Expected K Action",
]
REQUIRED_K_HEADINGS = [
    "Review Addressed",
    "Summary",
    "Evidence",
    "Finding Responses",
    "Spec Updates",
    "Documentation Updates",
    "Implementation Updates",
    "Tests and Validation",
    "Clarifications or Objections",
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


def markdown_headings(text: str) -> set[str]:
    """Return normalized Markdown headings in one linear scan."""
    return {
        match.group(1).strip()
        for match in re.finditer(r"^##+\s+(.+?)\s*$", text, re.MULTILINE)
    }


def has_heading(text: str, heading: str) -> bool:
    return heading in markdown_headings(text)


class TextReadError(ValueError):
    """Raised when a text file cannot be read within validator limits."""


def clear_text_cache() -> None:
    """Release all cached file text retained by imported validator use."""
    global _TEXT_CACHE_BYTES
    _TEXT_CACHE.clear()
    _TEXT_CACHE_BYTES = 0


def _evict_text_cache_if_needed() -> None:
    """Evict least-recently-used entries until cache bounds are satisfied."""
    global _TEXT_CACHE_BYTES
    max_entries = max(0, MAX_TEXT_CACHE_ENTRIES)
    max_cache_bytes = max(0, MAX_TEXT_CACHE_BYTES)
    while _TEXT_CACHE and (len(_TEXT_CACHE) > max_entries or _TEXT_CACHE_BYTES > max_cache_bytes):
        _, (_, byte_count) = _TEXT_CACHE.popitem(last=False)
        _TEXT_CACHE_BYTES -= byte_count


def _cache_text(key: TextCacheKey, text: str, byte_count: int) -> None:
    """Store text in the bounded LRU cache when it fits the configured budget."""
    global _TEXT_CACHE_BYTES
    max_entries = max(0, MAX_TEXT_CACHE_ENTRIES)
    max_cache_bytes = max(0, MAX_TEXT_CACHE_BYTES)
    if max_entries == 0 or max_cache_bytes == 0 or byte_count > max_cache_bytes:
        return

    previous = _TEXT_CACHE.pop(key, None)
    if previous is not None:
        _TEXT_CACHE_BYTES -= previous[1]
    _TEXT_CACHE[key] = (text, byte_count)
    _TEXT_CACHE_BYTES += byte_count
    _evict_text_cache_if_needed()


def read_text(path: Path, max_bytes: int | None = None) -> str:
    """Read UTF-8 text with a hard size cap and a bounded stat-keyed LRU cache.

    The cache preserves repeated-read speedup for validator phases while
    keeping long-lived imported use memory-bounded by entry count and retained
    bytes. The stat tuple prevents stale reads when files change during tests.
    """
    if max_bytes is None:
        max_bytes = MAX_TEXT_FILE_BYTES

    try:
        stat = path.stat()
    except OSError as exc:
        raise TextReadError(f"{path} cannot be stat'ed: {exc}") from exc

    size = stat.st_size
    if size > max_bytes:
        raise TextReadError(f"{path} exceeds max readable size: {size} bytes > {max_bytes}")

    key = (os.fspath(path), size, stat.st_mtime_ns, max_bytes)
    cached = _TEXT_CACHE.get(key)
    if cached is not None:
        _TEXT_CACHE.move_to_end(key)
        return cached[0]

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise TextReadError(f"{path} is not valid UTF-8 text: {exc}") from exc
    except OSError as exc:
        raise TextReadError(f"{path} cannot be read: {exc}") from exc

    _cache_text(key, text, size)
    return text


def read_text_or_report(path: Path, root: Path, errors: list[str]) -> str | None:
    """Read text for validator phases that should continue after local IO errors."""
    try:
        return read_text(path)
    except TextReadError as exc:
        fail(str(exc), errors)
        return None


def validate_headings(
    path: Path,
    headings: list[str],
    label: str,
    root: Path,
    errors: list[str],
    text: str | None = None,
) -> None:
    """Validate required headings, optionally reusing pre-loaded text to avoid a second disk read."""
    if not path.exists():
        fail(f"missing {rel(path, root)}", errors)
        return
    if text is None:
        text = read_text_or_report(path, root, errors)
        if text is None:
            return

    found_headings = markdown_headings(text)
    for heading in headings:
        if heading not in found_headings:
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


def normalize_options(raw_line: str) -> set[str]:
    """Normalize a documented pipe-separated status vocabulary line.

    This keeps validation strict about allowed values while tolerating harmless
    Markdown decoration and spacing differences.
    """
    clean_line = re.sub(
        r"^(Overall Status|Spec/Plan Status|Implementation Status|Status):\s*",
        "",
        raw_line,
        flags=re.IGNORECASE,
    )
    clean_line = clean_line.replace("`", "").replace("*", "").replace("_", "")
    return {item.strip() for item in clean_line.split("|") if item.strip()}


CANONICAL_STATUS_OPTIONS = {
    "Spec/Plan Status": [
        "Not started",
        "Changes requested",
        "Approved for implementation",
        "Approved with notes",
        "Approved",
        "Not applicable",
    ],
    "Implementation Status": [
        "Not started",
        "Changes requested",
        "Pending implementation",
        "Approved with notes",
        "Approved",
        "Not applicable",
    ],
    "Overall Status": [
        "Blocked",
        "Changes requested",
        "Pending implementation",
        "Approved with notes",
        "Approved",
    ],
}


def validate_status_option_lists(path: Path, text: str, root: Path, errors: list[str]) -> None:
    status_specs = CANONICAL_STATUS_OPTIONS

    for match in re.finditer(r"^-\s*(Spec/Plan Status|Implementation Status|Overall Status):\s*([^\n]+)$", text, re.MULTILINE):
        label, value = match.groups()
        if "|" not in value:
            continue
        found = split_template_options(value)
        expected = status_specs[label]
        if normalize_options(" | ".join(found)) != normalize_options(" | ".join(expected)):
            fail(
                f"{rel(path, root)}: Mismatched vocabulary format.\n"
                f"  Expected (normalized): {sorted(normalize_options(' | '.join(expected)))}\n"
                f"  Found (normalized):    {sorted(normalize_options(' | '.join(found)))}",
                errors,
            )


def validate_k_response_status_templates(root: Path, errors: list[str]) -> None:
    for rel_path in ("SKILL.md", "REFERENCE.md"):
        path = root / rel_path
        if path.exists():
            text = read_text_or_report(path, root, errors)
            if text is None:
                continue
            if EXPECTED_K_RESPONSE_STATUS_LINE not in text:
                fail(f"{rel_path} missing canonical K response status template", errors)


def validate_k_response_status_values(path: Path, text: str, root: Path, errors: list[str]) -> None:
    for value in re.findall(r"^-\s*Status:\s*([^\n]+)$", text, re.MULTILINE):
        value = value.strip()
        if value not in ALLOWED_K_RESPONSE_STATUS:
            fail(f"{rel(path, root)} has non-canonical K response Status: {value}", errors)


def iter_blocks(text: str, heading_pattern: str):
    """Yield (heading_title, block_content) by parsing line-by-line.

    This avoids unanchored full-document Markdown section regexes and guarantees
    linear O(N) behavior even with malformed or heavily nested headings.
    StringIO avoids splitlines() list materialization while remaining fast on
    CPython for this validator-sized text workload.
    """
    current_heading: str | None = None
    current_block: list[str] = []
    compiled_pattern = re.compile(rf"^{heading_pattern}")

    for raw_line in io.StringIO(text):
        line = raw_line.rstrip("\n")
        if compiled_pattern.match(line):
            if current_heading is not None:
                yield current_heading, "\n".join(current_block) + "\n"
            current_heading = line
            current_block = [line]
        elif current_heading is not None:
            current_block.append(line)

    if current_heading is not None:
        yield current_heading, "\n".join(current_block) + "\n"


def validate_r_finding_templates(path: Path, text: str, root: Path, errors: list[str]) -> None:
    found = False
    for title, block in iter_blocks(text, r"### Finding R-\d{4}-\d{2}: .+"):
        found = True
        title = title.strip()
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
    if not found:
        fail(f"{rel(path, root)} has no R finding blocks", errors)


def validate_k_response_templates(path: Path, text: str, root: Path, errors: list[str]) -> None:
    found = False
    for title, block in iter_blocks(text, r"### Response to R-\d{4}-\d{2}"):
        found = True
        title = title.strip()
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
    if not found:
        fail(f"{rel(path, root)} has no K response blocks", errors)


def section_body(text: str, heading: str) -> str:
    """Return an exact level-2 section body without matching heading prefixes.

    The search is anchored to Markdown heading lines so headings such as
    ``## Name Extra`` do not satisfy ``## Name``. It uses ``str.find`` plus
    boundary checks for speed while preserving exact-heading semantics.
    """
    target = f"## {heading}"
    search_from = 0
    while True:
        idx = text.find(target, search_from)
        if idx == -1:
            return ""

        at_line_start = idx == 0 or text[idx - 1] == "\n"
        line_end = text.find("\n", idx)
        if line_end == -1:
            line_end = len(text)
        line = text[idx:line_end].strip()
        if at_line_start and line == target:
            body_start = line_end + (1 if line_end < len(text) else 0)
            if text.startswith("## ", body_start):
                return ""
            next_heading = text.find("\n## ", body_start)
            if next_heading == -1:
                return text[body_start:]
            return text[body_start:next_heading]

        search_from = idx + len(target)


def validate_r_clarification_response_section(path: Path, text: str, root: Path, errors: list[str]) -> None:
    body = section_body(text, "Clarification and Objection Responses")
    if not body.strip():
        fail(f"{rel(path, root)} has empty Clarification and Objection Responses section", errors)


def validate_k_clarification_objection_section(path: Path, text: str, root: Path, errors: list[str]) -> None:
    body = section_body(text, "Clarifications or Objections")
    if not body.strip():
        fail(f"{rel(path, root)} has empty Clarifications or Objections section", errors)
        return
    if "Questions for R:" not in body or "Objections:" not in body:
        if "Questions for R:" not in body:
            fail(f"{rel(path, root)} Clarifications or Objections missing canonical field: Questions for R:", errors)
        if "Objections:" not in body:
            fail(f"{rel(path, root)} Clarifications or Objections missing canonical field: Objections:", errors)
    if re.search(r"^None\.?\s*$", body.strip(), re.IGNORECASE):
        fail(f"{rel(path, root)} uses bare None in Clarifications or Objections instead of canonical fields", errors)


def validate_whole_change_evidence_label(path: Path, text: str, root: Path, errors: list[str]) -> None:
    if path.name.endswith("k-response.md") and "Whole-change impact scan:" not in text:
        fail(f"{rel(path, root)} missing Whole-change impact scan evidence label", errors)
    if "Drift scan:" in text:
        fail(f"{rel(path, root)} uses stale/narrow Drift scan label; use Whole-change impact scan", errors)


def validate_reference_status_vocabulary(root: Path, errors: list[str]) -> None:
    for rel_path in ("SKILL.md", "REFERENCE.md"):
        path = root / rel_path
        if path.exists():
            text = read_text_or_report(path, root, errors)
            if text is not None:
                validate_status_option_lists(path, text, root, errors)


def validate_reference_bullet_status_lists(root: Path, errors: list[str]) -> None:
    """Check that bold-header bullet lists in REFERENCE.md use only canonical status values."""
    ref = root / "REFERENCE.md"
    if not ref.exists():
        return
    text = read_text_or_report(ref, root, errors)
    if text is None:
        return
    sections = {
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
    if path.suffix in FORBIDDEN_PACKAGE_SUFFIXES:
        return True
    parts = path.relative_to(root).parts
    # Fast evaluation avoids set intersections inside inner loops
    for forbidden in FORBIDDEN_PACKAGE_ARTIFACTS:
        if forbidden in parts:
            return True
    return False


def validate_required_paths(root: Path, errors: list[str]) -> None:
    for rel_path in REQUIRED_FILES:
        if not (root / rel_path).is_file():
            fail(f"missing required file: {rel_path}", errors)
    for rel_path in REQUIRED_DIRS:
        if not (root / rel_path).is_dir():
            fail(f"missing required directory: {rel_path}", errors)


def scan_package_tree(root: Path, errors: list[str]) -> dict[str, str]:
    """Single tree scan for packaging artifacts and Markdown text checks.

    Returns successfully read Markdown files keyed by package-relative path.
    This keeps package-wide checks O(one filesystem walk) and bounds per-file
    memory with read_text().
    """
    markdown_text: dict[str, str] = {}
    if (root / ".ai-dev-loop").exists():
        fail("forbidden duplicate root .ai-dev-loop template found", errors)
    for dirpath, dirnames, filenames in os.walk(root):
        base = Path(dirpath)

        kept_dirnames: list[str] = []
        for dirname in dirnames:
            if dirname in FORBIDDEN_PACKAGE_ARTIFACTS:
                fail(f"forbidden packaging artifact found: {rel(base / dirname, root)}", errors)
            else:
                kept_dirnames.append(dirname)
        dirnames[:] = kept_dirnames

        for filename in filenames:
            path = base / filename
            if filename in FORBIDDEN_PACKAGE_ARTIFACTS:
                fail(f"forbidden packaging artifact found: {rel(path, root)}", errors)
                continue
            if path.suffix in FORBIDDEN_PACKAGE_SUFFIXES:
                fail(f"forbidden generated file found: {rel(path, root)}", errors)
                continue
            if path.suffix != ".md":
                continue
            text = read_text_or_report(path, root, errors)
            if text is None:
                continue
            rel_path = rel(path, root)
            markdown_text[rel_path] = text
            for pattern in STALE_PATTERNS:
                if pattern.search(text):
                    fail(f"{rel_path} contains stale git-bootstrap language: {pattern.pattern}", errors)
    return markdown_text


def validate_stale_language(root: Path, errors: list[str]) -> None:
    scan_package_tree(root, errors)


def validate_clean_package(root: Path, errors: list[str]) -> None:
    scan_package_tree(root, errors)


def get_skill_version(root: Path, errors: list[str]) -> str | None:
    skill = root / "SKILL.md"
    if not skill.exists():
        return None
    text = read_text_or_report(skill, root, errors)
    if text is None:
        return None
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
    version_re = re.compile(r"(?<![>=<!~])(?:^|\b)(?:v)?([0-9]+\.[0-9]+\.[0-9]+)\b", re.MULTILINE)
    for path in [root / "SKILL.md", *md_files]:
        if not path.exists():
            continue
        text = read_text_or_report(path, root, errors)
        if text is None:
            continue
        for match in version_re.finditer(text):
            found = match.group(1)
            if found != expected:
                fail(f"{rel(path, root)} has version {found}; expected {expected}", errors)
    readme = root / "README.md"
    if readme.exists():
        readme_text = read_text_or_report(readme, root, errors)
        if readme_text is not None and f"**Version**: {expected}" not in readme_text:
            fail(f"README.md missing documented version {expected}", errors)


def validate_compact_skill(root_skill: Path, root: Path, errors: list[str]) -> None:
    if not root_skill.exists():
        return
    text = read_text_or_report(root_skill, root, errors)
    if text is None:
        return
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
        "K must address current R-required issues before any new implementation",
        "K shall not move to the next implementation while",
        "Current-issue lock",
        "Latest R review is a hard gate",
        "No silent softening",
        "open required findings block next implementation",
        "Documentation consistency is a hard gate",
        "Documentation drift prevention",
        "Open required findings ledger",
        "K must address all open required findings listed in status",
        "R must carry forward unresolved findings",
        "Scope-change freeze",
        "Scope-change control",
        "Code-doc-test-harness matrix",
        "R must verify code-doc-test consistency",
        "whole-change impact scan",
        "K can ask R for clarification",
        "K records evidence, risk, proposed safe path",
        "Clarifications or Objections",
        "R must answer",
        "Clarification and Objection Responses",
        "R findings define required outcomes, not complete K task checklists",
        "docs/specs/examples/tests/validators/scripts/package guidance",
        "not only literal R bullet items or requested files",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            fail(f"SKILL.md missing compact-skill safeguard phrase: {phrase}", errors)


def validate_embedded_record_templates(root: Path, errors: list[str]) -> None:
    """Ensure documented R/K templates keep the canonical section structure."""
    for rel_path in ("SKILL.md", "REFERENCE.md"):
        path = root / rel_path
        if not path.exists():
            continue
        text = read_text_or_report(path, root, errors)
        if text is None:
            continue
        found_headings = markdown_headings(text)
        for heading in REQUIRED_R_HEADINGS:
            if heading not in found_headings:
                fail(f"{rel_path} missing embedded R template heading: {heading}", errors)
        for heading in REQUIRED_K_HEADINGS:
            if heading not in found_headings:
                fail(f"{rel_path} missing embedded K template heading: {heading}", errors)
        for expected_line in (EXPECTED_R_SEVERITY_LINE, EXPECTED_R_FINDING_STATUS_LINE):
            if expected_line not in text:
                fail(f"{rel_path} missing canonical R finding template line: {expected_line}", errors)


def extract_manual_status_blocks(text: str) -> list[str]:
    """Return manual status.md heredoc bodies embedded in markdown docs."""
    blocks: list[str] = []
    marker = "status.md <<'EOF'"
    start = 0
    while True:
        marker_index = text.find(marker, start)
        if marker_index == -1:
            break
        body_start = text.find("\n", marker_index)
        if body_start == -1:
            break
        body_start += 1
        body_end = text.find("\nEOF", body_start)
        if body_end == -1:
            break
        blocks.append(text[body_start:body_end])
        start = body_end + 4
    return blocks


def validate_manual_status_templates(root: Path, errors: list[str]) -> None:
    """Ensure manual-install docs keep the same required status ledger as the installer."""
    doc_paths = ("QUICKSTART.md", "INSTALLATION.md", "COMPLETE-PACKAGE-GUIDE.md")
    for rel_path in doc_paths:
        path = root / rel_path
        if not path.exists():
            continue
        text = read_text_or_report(path, root, errors)
        if text is None:
            continue
        if "## Open Required Findings" not in text:
            fail(f"{rel_path} manual status template missing: ## Open Required Findings", errors)
        blocks = extract_manual_status_blocks(text)
        if not blocks:
            fail(f"{rel_path} missing manual status.md heredoc template", errors)
            continue
        for index, block in enumerate(blocks, start=1):
            for heading in REQUIRED_STATUS_HEADINGS:
                if f"## {heading}" not in block:
                    fail(f"{rel_path} manual status template #{index} missing heading: {heading}", errors)
            if "first R review must populate" not in block:
                fail(f"{rel_path} manual status template #{index} missing Open Required Findings bootstrap text", errors)
            if "unresolved K questions/objections" not in block:
                fail(f"{rel_path} manual status template #{index} missing K question/objection ledger text", errors)


def validate_installer_status_template(root: Path, errors: list[str]) -> None:
    installer = root / "scripts" / "install-ai-dev-loop-template.py"
    if not installer.exists():
        return
    text = read_text_or_report(installer, root, errors)
    if text is None:
        return
    for phrase in ("## Open Required Findings", "first R review must populate", "unresolved K questions/objections"):
        if phrase not in text:
            fail(f"installer status template missing: {phrase}", errors)


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

        expected_paths = (
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
        )
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


def validate_agent_readability_guidance(root: Path, errors: list[str]) -> None:
    """Ensure package docs keep agent-readable instruction semantics."""
    checks = {
        "SKILL.md": ["K can ask R for clarification or object", "K records evidence, risk, proposed safe path", "Command order:"],
        "REFERENCE.md": ["## Agent-Readable Instruction Style", "imperative verbs", "Avoid soft guidance for required behavior", "Use agent-readable control flow"],
        "README.md": ["explicit R/K clarification and objection gates"],
        "QUICKSTART.md": ["K must not blindly implement", "R is not a complete task-list generator"],
        "INSTALLATION.md": ["explicit clarification/objection gates"],
        "COMPLETE-PACKAGE-GUIDE.md": ["explicit clarification/objection gates"],
    }
    for rel_path, phrases in checks.items():
        path = root / rel_path
        if not path.exists():
            continue
        text = read_text_or_report(path, root, errors)
        if text is None:
            continue
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel_path} missing agent-readable instruction phrase: {phrase}", errors)


def validate_security_hardening(root: Path, errors: list[str]) -> None:
    """Ensure validator and installer keep the hardening fixes."""
    validator = root / "scripts" / "validate-ai-dev-loop-package.py"
    installer = root / "scripts" / "install-ai-dev-loop-template.py"
    if validator.exists():
        text = read_text_or_report(validator, root, errors)
        if text is None:
            return
        required = [
            "def iter_blocks(text: str, heading_pattern: str):",
            "linear O(N) behavior",
            "compiled_pattern.match(line)",
            "def normalize_options(raw_line: str) -> set[str]:",
            "Mismatched vocabulary format",
            "MAX_TEXT_FILE_BYTES",
            "def scan_package_tree(root: Path, errors: list[str]) -> dict[str, str]:",
        ]
        for phrase in required:
            if phrase not in text:
                fail(f"validator missing hardening phrase: {phrase}", errors)
        old_iter_body = "heading_pattern}" + "[" + r"\s\S" + "]*?"
        if old_iter_body in text:
            fail("validator still contains backtracking-prone global iter_blocks regex", errors)
    if installer.exists():
        text = read_text_or_report(installer, root, errors)
        if text is None:
            return
        for phrase in ("Permission denied writing", "Could not write template files", "locked these files"):
            if phrase not in text:
                fail(f"installer missing local write-error diagnostic phrase: {phrase}", errors)


def validate_pending_current_commit_semantics(root: Path, errors: list[str]) -> None:
    """Ensure pending-current-commit is documented as a closed historical marker."""
    checks = {
        "SKILL.md": ["`pending current commit` is valid", "do not treat it later as missing evidence"],
        "REFERENCE.md": ["literal value `pending current commit`", "valid, closed audit entry", "must not be flagged as an uncommitted file, missing evidence, or open finding"],
        "COMPLETE-PACKAGE-GUIDE.md": ["treat `pending current commit`", "valid, closed audit entry", "not as missing evidence or an open finding"],
        "README.md": ["`pending current commit`", "closed audit marker", "not as missing evidence"],
        "QUICKSTART.md": ["`pending current commit`", "valid closed marker", "not as missing evidence or an open item"],
        "INSTALLATION.md": ["`pending current commit`", "closed evidence", "not as degraded mode"],
    }
    for rel_path, phrases in checks.items():
        path = root / rel_path
        if not path.exists():
            continue
        text = read_text_or_report(path, root, errors)
        if text is None:
            continue
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel_path} missing pending-current-commit semantic phrase: {phrase}", errors)


def validate_whole_change_guidance(root: Path, errors: list[str]) -> None:
    """Ensure the whole-change responsibility is visible beyond compact SKILL.md."""
    checks = {
        "README.md": ["whole-change impact", "not exhaustive task lists", "did not name those files explicitly"],
        "QUICKSTART.md": ["whole-change impact scan", "complete task-list generator", "not a file-by-file task list"],
        "INSTALLATION.md": ["whole-change impact", "not a task checklist", "did not explicitly mention"],
        "COMPLETE-PACKAGE-GUIDE.md": ["whole-change responsibility", "not exhaustive K task lists", "did not explicitly list"],
        "REFERENCE.md": ["whole-change impact scan", "not a complete mechanical task list", "literal bullet list and file mentions"],
    }
    for rel_path, phrases in checks.items():
        path = root / rel_path
        if not path.exists():
            continue
        text = read_text_or_report(path, root, errors)
        if text is None:
            continue
        for phrase in phrases:
            if phrase not in text:
                fail(f"{rel_path} missing whole-change guidance phrase: {phrase}", errors)


def main() -> int:
    # Avoid retaining text between CLI runs when this module is invoked from a
    # long-lived Python process, while preserving cache benefits within the run.
    clear_text_cache()
    args = parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    if not root.exists() or not root.is_dir():
        print(f"AI Development Loop package validation failed:\n- package root does not exist or is not a directory: {root}")
        return 1

    validate_required_paths(root, errors)
    markdown_text = scan_package_tree(root, errors)
    validate_version_consistency(root, errors)

    root_skill = root / "SKILL.md"
    if root_skill.exists():
        validate_compact_skill(root_skill, root, errors)

    validate_reference_status_vocabulary(root, errors)
    validate_reference_bullet_status_lists(root, errors)
    validate_k_response_status_templates(root, errors)
    validate_embedded_record_templates(root, errors)
    validate_manual_status_templates(root, errors)
    validate_whole_change_guidance(root, errors)
    validate_agent_readability_guidance(root, errors)
    validate_pending_current_commit_semantics(root, errors)
    validate_security_hardening(root, errors)
    validate_installer_status_template(root, errors)
    validate_installer_smoke_test(root, errors)

    for status_path in [root / "examples" / ".ai-dev-loop" / "status.md"]:
        if status_path.exists():
            validate_headings(status_path, REQUIRED_STATUS_HEADINGS, "status", root, errors)

    reviews_dir = root / "examples" / ".ai-dev-loop" / "reviews"
    responses_dir = root / "examples" / ".ai-dev-loop" / "responses"
    
    if reviews_dir.exists():
        for path in sorted(reviews_dir.glob("*.md")):
            text = read_text_or_report(path, root, errors)
            if text is None:
                continue
            # Performance optimization: pass pre-loaded text directly to bypass secondary disk read
            validate_headings(path, REQUIRED_R_HEADINGS, "R", root, errors, text=text)
            validate_r_finding_templates(path, text, root, errors)
            validate_r_clarification_response_section(path, text, root, errors)
            
    if responses_dir.exists():
        for path in sorted(responses_dir.glob("*.md")):
            text = read_text_or_report(path, root, errors)
            if text is None:
                continue
            # Performance optimization: pass pre-loaded text directly to bypass secondary disk read
            validate_headings(path, REQUIRED_K_HEADINGS, "K", root, errors, text=text)
            validate_k_response_status_values(path, text, root, errors)
            validate_k_response_templates(path, text, root, errors)
            validate_k_clarification_objection_section(path, text, root, errors)
            validate_whole_change_evidence_label(path, text, root, errors)


    try:
        if errors:
            print("AI Development Loop package validation failed:")
            for err in errors:
                print(f"- {err}")
            return 1

        print("AI Development Loop package validation passed.")
        return 0
    finally:
        clear_text_cache()


if __name__ == "__main__":
    sys.exit(main())
