#!/usr/bin/env python3
"""Summarize AI Development Loop state without replacing source evidence."""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys
from pathlib import Path

STATUS_HEADINGS = ["Current Branch","Current Focus","Latest R Review","Latest K Response","Latest Context Note","Decisions","Approval State","Open Required Findings","Completed Items","Next Expected Role Action","Next Item","Blockers"]

def read(p: Path, limit: int = 200_000) -> str:
    try:
        return p.read_text(encoding='utf-8')[:limit]
    except FileNotFoundError:
        return ''

def section(text: str, name: str) -> str:
    m = re.search(rf"^##\s+{re.escape(name)}\s*$", text, re.M)
    if not m: return ''
    start = m.end()
    n = re.search(r"^##\s+", text[start:], re.M)
    end = start + n.start() if n else len(text)
    return text[start:end].strip()

def latest(dir_path: Path, suffix: str = '.md') -> str | None:
    if not dir_path.is_dir(): return None
    files = sorted(p for p in dir_path.glob(f'*{suffix}') if p.name != 'README.md')
    return str(files[-1].relative_to(dir_path.parents[1])) if files else None

def git_info(project: Path) -> dict:
    def run(args):
        return subprocess.run(['git','-C',str(project),*args], text=True, capture_output=True, timeout=5)
    info = {'inside_work_tree': False, 'branch': None, 'dirty_paths': [], 'error': None}
    try:
        r = run(['rev-parse','--is-inside-work-tree'])
        if r.returncode != 0:
            info['error'] = (r.stderr or r.stdout).strip(); return info
        info['inside_work_tree'] = r.stdout.strip() == 'true'
        b = run(['branch','--show-current'])
        info['branch'] = b.stdout.strip() if b.returncode == 0 else None
        s = run(['status','--short'])
        info['dirty_paths'] = s.stdout.splitlines() if s.returncode == 0 else []
    except Exception as exc:
        info['error'] = str(exc)
    return info

def main() -> int:
    ap = argparse.ArgumentParser(description='Emit a concise AI Development Loop state summary.')
    ap.add_argument('project_root', nargs='?', default='.', type=Path)
    ap.add_argument('--json', action='store_true', help='Emit JSON only.')
    args = ap.parse_args()
    project = args.project_root.resolve()
    loop = project/'.ai-dev-loop'
    status_path = loop/'status.md'
    status = read(status_path)
    result = {
        'project_root': str(project),
        'loop_dir_exists': loop.is_dir(),
        'status_exists': status_path.is_file(),
        'missing_status_headings': [h for h in STATUS_HEADINGS if not re.search(rf"^##\s+{re.escape(h)}\s*$", status, re.M)],
        'next_expected_role_action': section(status, 'Next Expected Role Action')[:500],
        'overall_status': None,
        'open_required_findings': section(status, 'Open Required Findings')[:1000],
        'blockers': section(status, 'Blockers')[:1000],
        'latest_r_review': latest(loop/'reviews'),
        'latest_k_response': latest(loop/'responses'),
        'latest_context': latest(loop/'context'),
        'latest_decision': latest(loop/'decisions'),
        'git': git_info(project),
        'summary_is_evidence': False,
    }
    m = re.search(r"^-\s*Overall Status:\s*(.+)$", status, re.M)
    if m: result['overall_status'] = m.group(1).strip()
    # Lightweight alert hints only; R/K must verify against files.
    alerts = []
    if not result['loop_dir_exists']: alerts.append('missing .ai-dev-loop directory')
    if result['missing_status_headings']: alerts.append('status headings incomplete')
    if result['open_required_findings'] and result['open_required_findings'].lower() not in {'none','none.'}:
        alerts.append('open required findings present')
    if result['blockers'] and result['blockers'].lower() not in {'none','none.'}:
        alerts.append('blockers present')
    if result['git']['inside_work_tree'] and result['git']['dirty_paths']:
        alerts.append('working tree has uncommitted paths')
    result['alerts'] = alerts
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True)); return 0 if result['loop_dir_exists'] and result['status_exists'] else 2
    print('AI_DEV_LOOP_STATE_SUMMARY')
    print(f"project: {result['project_root']}")
    print(f"loop_dir: {'present' if result['loop_dir_exists'] else 'missing'}")
    print(f"overall_status: {result['overall_status'] or 'unknown'}")
    print(f"next_expected_role_action: {result['next_expected_role_action'] or 'unknown'}")
    print(f"latest_r_review: {result['latest_r_review'] or 'none'}")
    print(f"latest_k_response: {result['latest_k_response'] or 'none'}")
    print(f"git_inside_work_tree: {result['git']['inside_work_tree']}")
    print(f"git_branch: {result['git']['branch'] or 'unknown'}")
    print(f"dirty_path_count: {len(result['git']['dirty_paths'])}")
    print('alerts: ' + ('; '.join(alerts) if alerts else 'none'))
    print('note: summary targets reads; verify material claims against written records/source files')
    return 0 if result['loop_dir_exists'] and result['status_exists'] else 2

if __name__ == '__main__':
    raise SystemExit(main())
