#!/usr/bin/env python3
"""Fast selfcheck and package-audit harness for cogniact-governor."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
REQUIRED_SKILL_PATTERNS=["Always-on operating contract","Tiered CogniAct loop","No harmful optimization","High-stakes caution","Current-source discipline","Language and fixed formats","Mechanical state gate","scripts/selfcheck.py","value per unit effort","Do not re-read"]
REQUIRED_MODULES=["modules/contract-calibration.md","modules/context-tool-economy.md","modules/evidence-state.md","modules/boundaries-localization.md","modules/communication.md"]
def fail(msg): print(f"FAIL: {msg}",file=sys.stderr); raise SystemExit(1)
def audit_package(path:Path)->int:
    skill=path/"SKILL.md"
    if not skill.exists(): fail("SKILL.md missing")
    text=skill.read_text(encoding="utf-8")
    for pat in REQUIRED_SKILL_PATTERNS:
        if pat not in text: fail(f"required package text missing: {pat}")
    for rel in REQUIRED_MODULES:
        p=path/rel
        if not p.exists(): fail(f"module missing: {rel}")
        if rel not in text: fail(f"module not linked from SKILL.md: {rel}")
    for rel in ["scripts/state.py","scripts/selfcheck.py"]:
        p=path/rel
        if not p.exists(): fail(f"script missing: {rel}")
        compile(p.read_text(encoding="utf-8"),str(p),"exec")
    print("PASS: cogniact-governor package audit passed")
    return 0
def main(argv=None):
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True); a=sub.add_parser("audit-package"); a.add_argument("path",nargs="?",default="."); ns=ap.parse_args(argv)
    if ns.cmd=="audit-package": return audit_package(Path(ns.path).resolve())
    return 2
if __name__=="__main__": raise SystemExit(main())
