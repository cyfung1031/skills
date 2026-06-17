#!/usr/bin/env python3
"""Check mechanical AI Development Loop gates and emit a compact flow report."""
from __future__ import annotations
import argparse, json, re, subprocess
from pathlib import Path

STATUS_HEADINGS = ["Current Branch","Current Focus","Latest R Review","Latest K Response","Latest Context Note","Decisions","Approval State","Open Required Findings","Completed Items","Next Expected Role Action","Next Item","Blockers"]
REQUIRED_GATES = [
    "current_issue_lock",
    "written_record_authority",
    "local_commit_trace_or_degraded_reason",
    "terminal_r_review",
    "documentation_drift_check",
    "same_session_next_action",
]

def read(path: Path, limit: int = 200_000) -> str:
    try: return path.read_text(encoding="utf-8")[:limit]
    except FileNotFoundError: return ""

def section(text: str, heading: str) -> str:
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.M)
    if not m: return ""
    start = m.end(); n = re.search(r"^##\s+", text[start:], re.M)
    return text[start:start + n.start() if n else len(text)].strip()

def latest(loop: Path, name: str) -> Path | None:
    d = loop / name
    if not d.is_dir(): return None
    files = sorted(p for p in d.glob("*.md") if p.name != "README.md")
    return files[-1] if files else None

def git(project: Path) -> dict:
    def run(args: list[str]):
        return subprocess.run(["git", "-C", str(project), *args], text=True, capture_output=True, timeout=5)
    out = {"inside": False, "head": None, "dirty_count": None, "commit_capable_probe": "not-run", "error": None}
    try:
        r = run(["rev-parse", "--is-inside-work-tree"])
        if r.returncode != 0:
            out["error"] = (r.stderr or r.stdout).strip(); return out
        out["inside"] = r.stdout.strip() == "true"
        h = run(["rev-parse", "--short", "HEAD"]); out["head"] = h.stdout.strip() if h.returncode == 0 else None
        s = run(["status", "--short"]); out["dirty_count"] = len(s.stdout.splitlines()) if s.returncode == 0 else None
        # Non-mutating proxy for likely commit usability: identity exists or repo can resolve config.
        n = run(["config", "user.name"]); e = run(["config", "user.email"])
        out["commit_capable_probe"] = "likely" if n.returncode == 0 and e.returncode == 0 and n.stdout.strip() and e.stdout.strip() else "unknown"
    except Exception as exc:
        out["error"] = str(exc)
    return out

def has_any(text: str, phrases: list[str]) -> bool:
    low = text.lower()
    return any(p.lower() in low for p in phrases)

def main() -> int:
    ap = argparse.ArgumentParser(description="Emit compact mechanical R/K flow gate report.")
    ap.add_argument("project_root", nargs="?", default=".", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    project = args.project_root.resolve(); loop = project / ".ai-dev-loop"; status_path = loop / "status.md"
    status = read(status_path); r_path = latest(loop, "reviews"); k_path = latest(loop, "responses")
    latest_text = "\n".join(read(p) for p in [r_path, k_path] if p)
    open_findings = section(status, "Open Required Findings")
    blockers = section(status, "Blockers")
    next_action = section(status, "Next Expected Role Action")
    missing_headings = [h for h in STATUS_HEADINGS if not re.search(rf"^##\s+{re.escape(h)}\s*$", status, re.M)]
    g = git(project)
    gates = {
        "status_shape_ok": not missing_headings,
        "current_issue_lock_needs_attention": bool(open_findings and open_findings.lower() not in {"none", "none."}),
        "blockers_present": bool(blockers and blockers.lower() not in {"none", "none."}),
        "next_action_written": bool(next_action),
        "local_git_trace_present_or_degraded_recorded": bool(g["head"] or has_any(status + latest_text, ["git trace unavailable", "degraded mode", "commit unavailable"])),
        "terminal_r_approval_claim_seen": has_any(status + latest_text, ["terminal approval", "overall status: approved", "next expected role action: stop"]),
        "documentation_drift_check_seen": has_any(latest_text, ["documentation drift", "docs", "whole-change", "validator"]),
    }
    report = {
        "project_root": str(project),
        "loop_dir_exists": loop.is_dir(),
        "status_exists": status_path.is_file(),
        "latest_r_review": str(r_path.relative_to(project)) if r_path else None,
        "latest_k_response": str(k_path.relative_to(project)) if k_path else None,
        "missing_status_headings": missing_headings,
        "next_expected_role_action": next_action[:300],
        "required_gates": REQUIRED_GATES,
        "gate_hints": gates,
        "git": g,
        "summary_is_evidence": False,
        "note": "Use this report to target reads; verify material claims against written records and files.",
    }
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True)); return 0 if loop.is_dir() and status_path.is_file() else 2
    print("AI_DEV_LOOP_FLOW_CHECK")
    print(f"project: {report['project_root']}")
    print(f"loop_dir: {'present' if loop.is_dir() else 'missing'}")
    print(f"status_shape_ok: {gates['status_shape_ok']}")
    print(f"open_findings_attention: {gates['current_issue_lock_needs_attention']}")
    print(f"blockers_present: {gates['blockers_present']}")
    print(f"next_action_written: {gates['next_action_written']}")
    print(f"local_git_trace_or_degraded: {gates['local_git_trace_present_or_degraded_recorded']}")
    print(f"docs_drift_check_seen: {gates['documentation_drift_check_seen']}")
    print("note: target reads only; not approval evidence")
    return 0 if loop.is_dir() and status_path.is_file() else 2

if __name__ == "__main__":
    raise SystemExit(main())
