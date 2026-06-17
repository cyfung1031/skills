#!/usr/bin/env python3
"""Validate the standalone AI Development Loop package."""
from __future__ import annotations

import argparse, hashlib, json, os, re, subprocess, sys, tempfile
from pathlib import Path

VERSION = "1.7.6"
REQUIRED_FILES = [
    "README.md", "QUICKSTART.md", "INSTALLATION.md", "COMPLETE-PACKAGE-GUIDE.md",
    "LOOP-HARNESS.md", "MODE-HARNESS.md", "BENCHMARK-HARNESS.md", "SKILL.md", "VALIDATION.md", "SCORING-EVIDENCE-SCHEMA.json", "PACKAGE-MANIFEST.json", "RESTRICTION-HARNESS.md",
    "examples/.ai-dev-loop/README.md", "examples/.ai-dev-loop/status.md",
    "examples/.ai-dev-loop/context/README.md", "examples/.ai-dev-loop/decisions/README.md",
    "examples/.ai-dev-loop/reviews/0001-r-bootstrap-review.md",
    "examples/.ai-dev-loop/responses/0001-k-validation-response.md",
    "scripts/validate-ai-dev-loop-package.py", "scripts/install-ai-dev-loop-template.py", "scripts/check-ai-dev-loop-state.py", "scripts/check-ai-dev-loop-flow.py", "scripts/estimate-ai-dev-loop-token-cost.py",
]
REQUIRED_DIRS = [
    "examples/.ai-dev-loop/reviews", "examples/.ai-dev-loop/responses",
    "examples/.ai-dev-loop/context", "examples/.ai-dev-loop/decisions",
]
STATUS_HEADINGS = ["Current Branch","Current Focus","Latest R Review","Latest K Response","Latest Context Note","Decisions","Approval State","Open Required Findings","Completed Items","Next Expected Role Action","Next Item","Blockers"]
SKILL_PHRASES = [
    "status.md scope -> R finding ledger -> K response/evidence -> whole-change scan -> validation -> R terminal review",
    "Operational command pattern",
    "Written-record authority",
    "When creating the first R/K/status record, or when record shape is uncertain, load `LOOP-HARNESS.md` templates before writing.",
    "Token and loading budget",
    "Compress prose, not obligations",
    "scripts/check-ai-dev-loop-state.py/check-ai-dev-loop-flow.py output when available",
    "Inline record contracts",
    "Current-issue lock",
    "No silent softening",
    "Documentation drift prevention",
    "K may request clarification or object",
    "Most restrictive wins",
    "Continue same-session handoff",
    "Writing `Next Expected Role Action` is not performing it",
    "Do not invent commands, outputs, commits, tests, file reads, user approvals, or external evidence",
    "Every claim must cite a file, diff, command, test, log, commit, status record, review/response record, or explicit limitation",
    "Release work must check package structure",
    "Git authority and degraded-mode defaults",
    "Local git commits are the default audit and rollback mechanism",
    "every meaningful R/K/status transition must be committed locally",
    "Degraded mode is a fallback, not a convenience bypass",
    "Never push, force-push, configure remotes",
    "SCORING-EVIDENCE-SCHEMA.json",
    "Keep delivered files focused",
]
REFERENCE_PHRASES = ["R review record template", "K response record template", "Status vocabulary", "Package/release checklist", "Whole-change impact scan", "Release acceptance", "Written-record authority and restriction harness", "Operational command pattern", "Current-issue lock and no silent softening", "Documentation drift prevention and terminal review", "Local git authority model"]
FORBIDDEN_NAMES = {"__MACOSX", ".DS_Store", "__pycache__", ".pytest_cache", ".git", ".idea", ".vscode"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".tmp", ".swp"}
ALLOWED_SPEC = {"Not started", "Changes requested", "Approved for implementation", "Approved with notes", "Approved", "Not applicable"}
ALLOWED_IMPL = {"Not started", "Changes requested", "Pending implementation", "Approved with notes", "Approved", "Not applicable"}
ALLOWED_OVERALL = {"Blocked", "Changes requested", "Pending implementation", "Approved with notes", "Approved"}
ALLOWED_FINDING_SEVERITY = {"Critical", "High", "Medium", "Low", "Note"}
ALLOWED_FINDING_STATUS = {"Open", "Closed", "Accepted risk"}
ALLOWED_RESPONSE_STATUS = {"Addressed", "Partially addressed", "Not addressed", "Objected", "Blocked"}

PROCESS_LEAKAGE_PATTERNS = [
    r"best" + r"-version-builder",
    r"insight" + r"forge",
    r"plat" + r"eau",
    r"repeated" + r" revision",
    r"revision" + r" building",
    r"generated" + r"-successor",
    r"generated" + r"_at",
    r"release" + r"-content hygiene",
    r"release" + r"\s+content" + r"\s+hygiene",
]

WHOLE_CHANGE_DOCS = {
    "README.md": ["whole-change impact", "not exhaustive task lists", "did not name those files explicitly"],
    "QUICKSTART.md": ["whole-change impact scan", "not a complete task-list generator"],
    "INSTALLATION.md": ["Whole-change responsibility", "not exhaustive task lists", "did not explicitly mention"],
    "COMPLETE-PACKAGE-GUIDE.md": ["whole-change responsibility", "not exhaustive K task lists", "did not explicitly list"],
    "LOOP-HARNESS.md": ["Whole-change impact scan", "not a complete mechanical task list", "did not explicitly list"],
}

def parse_args():
    p = argparse.ArgumentParser(description="Validate standalone AI Development Loop package")
    p.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    return p.parse_args()

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def has_heading(text: str, heading: str) -> bool:
    return re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.M) is not None

def add(errors, msg):
    errors.append(msg)

def validate_status_values(text: str, rel: str, errors: list[str]) -> None:
    patterns = [("Spec/Plan Status", ALLOWED_SPEC), ("Implementation Status", ALLOWED_IMPL), ("Overall Status", ALLOWED_OVERALL)]
    for label, allowed in patterns:
        for value in re.findall(rf"^-\s*{re.escape(label)}:\s*([^\n]+)$", text, re.M):
            value = value.strip()
            if "|" in value:  # documented option line in templates is allowed elsewhere
                continue
            if value not in allowed:
                add(errors, f"{rel} has non-canonical {label}: {value}")

def validate_r_record(path: Path, root: Path, errors: list[str]) -> None:
    text = read(path); rel = str(path.relative_to(root))
    for heading in ["Scope", "Summary", "Evidence", "Findings", "Clarifications Needed", "Clarification and Objection Responses", "Approval Status", "Next Expected K Action"]:
        if not has_heading(text, heading): add(errors, f"{rel} missing R heading: {heading}")
    validate_status_values(text, rel, errors)
    for block in re.split(r"^###\s+Finding\s+", text, flags=re.M)[1:]:
        sev = re.search(r"^-\s*Severity:\s*([^\n]+)$", block, re.M)
        status = re.search(r"^-\s*Status:\s*([^\n]+)$", block, re.M)
        if not sev or sev.group(1).strip() not in ALLOWED_FINDING_SEVERITY:
            add(errors, f"{rel} finding has non-canonical or missing Severity")
        if not status or status.group(1).strip() not in ALLOWED_FINDING_STATUS:
            add(errors, f"{rel} finding has non-canonical or missing Status")

def validate_k_record(path: Path, root: Path, errors: list[str]) -> None:
    text = read(path); rel = str(path.relative_to(root))
    for heading in ["Review Addressed", "Summary", "Evidence", "Finding Responses", "Spec Updates", "Documentation Updates", "Implementation Updates", "Tests and Validation", "Clarifications or Objections", "Compact Context", "Next Expected R Action"]:
        if not has_heading(text, heading): add(errors, f"{rel} missing K heading: {heading}")
    if "Questions for R:" not in text or "Objections:" not in text:
        add(errors, f"{rel} missing canonical clarification/objection fields")
    for block in re.split(r"^###\s+Response to\s+", text, flags=re.M)[1:]:
        status = re.search(r"^-\s*Status:\s*([^\n]+)$", block, re.M)
        if not status or status.group(1).strip() not in ALLOWED_RESPONSE_STATUS:
            add(errors, f"{rel} response has non-canonical or missing Status")

def validate_manifest(root: Path, errors: list[str]) -> None:
    path = root / "PACKAGE-MANIFEST.json"
    if not path.is_file():
        return
    try:
        data = json.loads(read(path))
    except json.JSONDecodeError as exc:
        add(errors, f"PACKAGE-MANIFEST.json invalid JSON: {exc}"); return
    if data.get("version") != VERSION:
        add(errors, f"PACKAGE-MANIFEST.json version must be {VERSION}")
    files = data.get("files")
    if not isinstance(files, list):
        add(errors, "PACKAGE-MANIFEST.json files must be a list"); return
    listed = {entry.get("path"): entry for entry in files if isinstance(entry, dict)}
    actual = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '.git' not in p.parts)
    for rel in actual:
        if rel not in listed:
            add(errors, f"manifest missing file: {rel}")
    for rel, entry in listed.items():
        if not rel:
            add(errors, "manifest has file entry without path"); continue
        p = root / rel
        if not p.is_file():
            add(errors, f"manifest lists missing file: {rel}"); continue
        if rel == 'PACKAGE-MANIFEST.json' and entry.get('sha256') is None and entry.get('bytes') is None:
            continue
        if entry.get("sha256") != sha256(p):
            add(errors, f"manifest checksum mismatch: {rel}")
        if entry.get("bytes") != p.stat().st_size:
            add(errors, f"manifest byte size mismatch: {rel}")

def validate_scoring_schema(root: Path, errors: list[str]) -> None:
    path = root / 'SCORING-EVIDENCE-SCHEMA.json'
    if not path.is_file():
        return
    try:
        data = json.loads(read(path))
    except json.JSONDecodeError as exc:
        add(errors, f"SCORING-EVIDENCE-SCHEMA.json invalid JSON: {exc}"); return
    if data.get('version') != VERSION:
        add(errors, f"SCORING-EVIDENCE-SCHEMA.json version must be {VERSION}")
    for key in ['validation_tiers','evidence_tags','score_anchors','required_categories','score_row_required_fields','claim_caps']:
        if key not in data:
            add(errors, f"SCORING-EVIDENCE-SCHEMA.json missing key: {key}")
    names = {c.get('name') for c in data.get('required_categories', []) if isinstance(c, dict)}
    for name in ['correctness_target_behavior','evidence_validation_reproducibility','observability_audit_handoff','compatibility_regression_safety']:
        if name not in names:
            add(errors, f"SCORING-EVIDENCE-SCHEMA.json missing category: {name}")

def validate_release_templates(root: Path, errors: list[str]) -> None:
    vr = root / 'VALIDATION-RESULTS.md'
    if vr.is_file():
        text = read(vr)
        for phrase in ['Command:', 'Working directory:', 'Exit status:', 'Validation tier:', 'Skipped checks', 'Residual risk']:
            if phrase not in text:
                add(errors, f"VALIDATION-RESULTS.md missing phrase: {phrase}")
    fc = root / 'BENCHMARK-HARNESS.md'
    if fc.is_file():
        text = read(fc)
        for phrase in ['fixture_id', 'oracle', 'format_contract', 'pass_fail_rule', 'Anti-leakage rule']:
            if phrase not in text:
                add(errors, f"BENCHMARK-HARNESS.md missing phrase: {phrase}")
    mt = root / 'MODE-HARNESS.md'
    if mt.is_file():
        text = read(mt)
        for phrase in ['Minimal mode', 'Release mode', 'Degraded mode', 'validation-tier honesty']:
            if phrase not in text:
                add(errors, f"MODE-HARNESS.md missing phrase: {phrase}")

def validate_restriction_harness(root: Path, errors: list[str]) -> None:
    path = root / 'RESTRICTION-HARNESS.md'
    if not path.is_file():
        return
    text = read(path)
    for phrase in [
        'Written-record authority',
        'Current-issue lock',
        'No silent softening',
        'Documentation drift prevention',
        'Terminal R review',
        'Same-session continuation',
        'Chat contradicts status',
        'Missing first record shape',
        'Validator checks exact template-loading line',
        'Local git available',
        'Git commit unavailable',
        'Push requested by implication',
        'Wrapper push',
        'Broad staging risk',
        'Token-control only changes',
        'Script assistance boundary',
        'Token compression attempt',
        'Script summary available',
    ]:
        if phrase not in text:
            add(errors, f"RESTRICTION-HARNESS.md missing phrase: {phrase}")

def main() -> int:
    root = parse_args().root.resolve()
    errors: list[str] = []
    if not root.is_dir():
        print(f"Package root does not exist: {root}"); return 1
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file(): add(errors, f"missing required file: {rel}")
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir(): add(errors, f"missing required directory: {rel}")
    if (root / '.ai-dev-loop').exists(): add(errors, "root package must not contain a live .ai-dev-loop directory")
    for base, dirs, files in os.walk(root):
        for name in list(dirs) + list(files):
            p = Path(base) / name
            if name in FORBIDDEN_NAMES or name.startswith("._") or p.suffix in FORBIDDEN_SUFFIXES:
                add(errors, f"forbidden package artifact: {p.relative_to(root)}")
    skill = root / 'SKILL.md'
    if skill.exists():
        text = read(skill)
        if not re.search(rf"^version:\s*{re.escape(VERSION)}\s*$", text, re.M): add(errors, f"SKILL.md version must be {VERSION}")
        if len(text.encode('utf-8')) > 9150: add(errors, "SKILL.md exceeds token-control size budget")
        for phrase in SKILL_PHRASES:
            if phrase not in text: add(errors, f"SKILL.md missing required phrase: {phrase}")
    ref = root / 'LOOP-HARNESS.md'
    if ref.exists():
        rt = read(ref)
        for phrase in REFERENCE_PHRASES:
            if phrase not in rt: add(errors, f"LOOP-HARNESS.md missing section phrase: {phrase}")
        for phrase in ['Token budget and loading order', 'Token savings may compress wording', 'must not remove required gates']:
            if phrase not in rt: add(errors, f"LOOP-HARNESS.md missing token-control phrase: {phrase}")
    status = root / 'examples/.ai-dev-loop/status.md'
    if status.exists():
        st = read(status)
        for heading in STATUS_HEADINGS:
            if not has_heading(st, heading): add(errors, f"example status missing heading: {heading}")
        validate_status_values(st, 'examples/.ai-dev-loop/status.md', errors)
    for p in (root / 'examples/.ai-dev-loop/reviews').glob('*.md'):
        if p.name != 'README.md': validate_r_record(p, root, errors)
    for p in (root / 'examples/.ai-dev-loop/responses').glob('*.md'):
        if p.name != 'README.md': validate_k_record(p, root, errors)
    for rel, phrases in WHOLE_CHANGE_DOCS.items():
        p = root / rel
        if p.exists():
            text = read(p)
            for phrase in phrases:
                if phrase not in text: add(errors, f"{rel} missing whole-change guidance phrase: {phrase}")
    # version consistency in top-level markdown except manifest generated after files.
    for p in root.glob('*.md'):
        text = read(p)
        stale_versions = [v for v in re.findall(r'v?\d+\.\d+\.\d+(?:-probe)?', text) if v.lstrip('v') != VERSION]
        if stale_versions:
            add(errors, f'{p.name} contains stale version reference: {sorted(set(stale_versions))}')
    installer = root / 'scripts/install-ai-dev-loop-template.py'
    if installer.exists():
        with tempfile.TemporaryDirectory(prefix='ai-dev-loop-standalone-') as td:
            project = Path(td) / 'project'; project.mkdir(); (project / 'README.md').write_text('# Project\n', encoding='utf-8')
            result = subprocess.run([sys.executable, str(installer), str(project)], cwd=str(root), text=True, capture_output=True)
            if result.returncode != 0:
                add(errors, 'installer smoke test failed: ' + (result.stderr.strip() or result.stdout.strip()))
            for rel in ['.ai-dev-loop/SKILL.md','.ai-dev-loop/LOOP-HARNESS.md','.ai-dev-loop/status.md','.ai-dev-loop/reviews','.ai-dev-loop/responses','.ai-dev-loop/context','.ai-dev-loop/decisions','.ai-dev-loop/scripts/check-ai-dev-loop-state.py','.ai-dev-loop/scripts/check-ai-dev-loop-flow.py']:
                if not (project / rel).exists(): add(errors, f"installer missing output: {rel}")
            checker = project / '.ai-dev-loop/scripts/check-ai-dev-loop-state.py'
            if checker.exists():
                cr = subprocess.run([sys.executable, str(checker), str(project)], text=True, capture_output=True)
                if cr.returncode != 0 or 'AI_DEV_LOOP_STATE_SUMMARY' not in cr.stdout:
                    add(errors, 'state checker smoke test failed: ' + (cr.stderr.strip() or cr.stdout.strip()))
            flow = project / '.ai-dev-loop/scripts/check-ai-dev-loop-flow.py'
            if flow.exists():
                fr = subprocess.run([sys.executable, str(flow), str(project)], text=True, capture_output=True)
                if fr.returncode != 0 or 'AI_DEV_LOOP_FLOW_CHECK' not in fr.stdout:
                    add(errors, 'flow checker smoke test failed: ' + (fr.stderr.strip() or fr.stdout.strip()))
            estimator = root / 'scripts/estimate-ai-dev-loop-token-cost.py'
            if estimator.exists():
                er = subprocess.run([sys.executable, str(estimator), str(root / 'SKILL.md')], text=True, capture_output=True)
                if er.returncode != 0 or 'TOKEN_COST_ESTIMATE' not in er.stdout:
                    add(errors, 'token estimator smoke test failed: ' + (er.stderr.strip() or er.stdout.strip()))

    for p in root.rglob('*'):
        if p.is_file() and p.suffix in {'.md', '.json', '.py'} and 'audit' not in p.parts:
            text = read(p)
            for pattern in PROCESS_LEAKAGE_PATTERNS:
                if re.search(pattern, text, re.I):
                    add(errors, f"delivered-file leak in {p.relative_to(root)}: {pattern}")
    validate_scoring_schema(root, errors)
    validate_release_templates(root, errors)
    validate_restriction_harness(root, errors)
    validate_manifest(root, errors)
    if errors:
        print('AI Development Loop standalone package validation failed:')
        for e in errors: print('- ' + e)
        return 1
    print('AI Development Loop standalone package validation passed.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
