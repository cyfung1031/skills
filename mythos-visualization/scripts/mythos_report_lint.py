#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
REQ=['# Analysis Report:','## Identity and route','## Evidence boundary','## Compact model','## Detail-overall bridge','## Risks and limits','## Validation']
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--reports', required=True); args=ap.parse_args(); root=Path(args.reports)
    files=sorted(root.rglob('*.md')) if root.exists() else []; failures=[]
    for p in files:
        text=p.read_text(encoding='utf-8', errors='replace'); missing=[s for s in REQ if s not in text]
        if missing: failures.append({'path':str(p),'missing':missing})
    print(json.dumps({'status':'pass' if not failures else 'fail','reports':len(files),'failures':failures}, indent=2)); return 0 if not failures else 1
if __name__ == '__main__': raise SystemExit(main())
