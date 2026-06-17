#!/usr/bin/env python3
"""Estimate text load cost for AI Development Loop files using a deterministic chars/4 proxy."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def units(n: int) -> int:
    return (n + 3) // 4

def main() -> int:
    ap = argparse.ArgumentParser(description='Estimate token-load cost for selected package/project files.')
    ap.add_argument('paths', nargs='*', type=Path, default=[Path('.')])
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    rows = []
    for base in args.paths:
        base = base.resolve()
        files = [base] if base.is_file() else sorted(p for p in base.rglob('*') if p.is_file() and p.suffix in {'.md','.json','.py','.txt','.csv'})
        for p in files:
            try: data = p.read_bytes()
            except OSError: continue
            rel = str(p.relative_to(base)) if base.is_dir() else p.name
            rows.append({'base': str(base), 'path': rel, 'bytes': len(data), 'token_proxy': units(len(data))})
    rows.sort(key=lambda r: (-r['bytes'], r['base'], r['path']))
    if args.json:
        print(json.dumps({'estimator':'ceil(utf8_bytes/4)','rows':rows}, indent=2)); return 0
    print('TOKEN_COST_ESTIMATE estimator=ceil(utf8_bytes/4)')
    for r in rows[:80]:
        print(f"{r['token_proxy']:6d} {r['bytes']:7d} {r['path']}")
    print(f"total_token_proxy {sum(r['token_proxy'] for r in rows)}")
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
