#!/usr/bin/env python3
"""Mechanical done gate for the cogniact-governor skill."""
from __future__ import annotations
import argparse, json, os, sys
from datetime import datetime, timezone
PHASES=["scope","plan","execute","verify","report","done"]
FORWARD={"scope":{"scope","plan"},"plan":{"scope","execute"},"execute":{"scope","execute","verify"},"verify":{"scope","execute","report"},"report":{"scope","execute","done"},"done":{"scope"}}
TIERS={"trivial":(1,"simple answer or one local edit"),"standard":(1,"multi-step task with focused verification"),"complex":(2,"cross-cutting, high-risk, or unfamiliar work")}
HEDGES=["looks right","looks good","looks correct","should work","should be","should pass","probably","i think","seems to","seems fine","appears to","todo","tbd","n/a","not run","didn't run","did not run","untested","assume","assuming","presumably","in theory","ought to","maybe"]
OBSERVED_TERMS=["ran ","exit ","passed","failed","observed","verified","checked","opened","rendered","compiled","lint","test","zip","created","wrote","read ","inspected","matched","exists","diff","screenshot"]
def state_path():
    return os.environ.get("COGNIACT_STATE") or os.path.join(os.environ.get("TMPDIR","/tmp"),"cogniact-task-state.json")
def now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def die(msg,code=2): print(f"error: {msg}",file=sys.stderr); sys.exit(code)
def load():
    p=state_path()
    if not os.path.exists(p): die(f"no state file at {p}. run: state.py init '<goal>' --tier standard")
    with open(p,encoding="utf-8") as f: return json.load(f)
def save(st):
    st["updated"]=now()
    with open(state_path(),"w",encoding="utf-8") as f: json.dump(st,f,indent=2,ensure_ascii=False); f.write("\n")
def validate_evidence(evidence):
    ev=" ".join(evidence.strip().split())
    if len(ev)<16: die("evidence too thin: name what was checked and what was observed")
    low=ev.lower(); hit=next((h for h in HEDGES if h in low),None)
    if hit: die(f"evidence reads as a guess or placeholder ('{hit}'); cite what was checked and observed")
    if not any(term in low for term in OBSERVED_TERMS): die("evidence must include an observed check/result, such as ran/checked/observed/passed/failed/exists")
def cmd_init(a):
    if a.tier not in TIERS: die(f"unknown tier '{a.tier}'; choose: {', '.join(TIERS)}")
    st={"goal":a.goal.strip(),"tier":a.tier,"phase":"scope","criteria":[],"open_questions":[],"notes":[],"created":now(),"updated":now()}; save(st)
    print(f"init: '{st['goal']}' tier={a.tier} (needs >= {TIERS[a.tier][0]} criterion before leaving scope)"); print(f"state: {state_path()}")
def cmd_add(a):
    st=load(); text=a.text.strip()
    if not text: die("criterion cannot be empty")
    cid=f"C{len(st['criteria'])+1}"; st["criteria"].append({"id":cid,"text":text,"status":"open","evidence":""}); save(st); print(f"added {cid}: {text}")
def cmd_meet(a):
    st=load(); validate_evidence(a.evidence)
    for c in st["criteria"]:
        if c["id"]==a.id:
            c["status"]="met"; c["evidence"]=" ".join(a.evidence.strip().split()); save(st); print(f"{a.id} met: {c['evidence']}"); return
    die(f"no criterion {a.id}")
def cmd_reopen(a):
    st=load()
    for c in st["criteria"]:
        if c["id"]==a.id: c["status"]="open"; c["evidence"]=""; save(st); print(f"{a.id} reopened"); return
    die(f"no criterion {a.id}")
def cmd_phase(a):
    st=load(); cur=st["phase"]; tgt=a.to
    if tgt not in PHASES: die(f"unknown phase '{tgt}'; choose: {', '.join(PHASES)}")
    if tgt not in FORWARD[cur]: die(f"illegal transition {cur} -> {tgt}; legal: {', '.join(sorted(FORWARD[cur]))}")
    if cur=="scope" and tgt=="plan" and len(st["criteria"])<TIERS[st["tier"]][0]: die(f"cannot leave scope: tier '{st['tier']}' needs >= {TIERS[st['tier']][0]} criterion, have {len(st['criteria'])}")
    st["phase"]=tgt; save(st); print(f"phase: {cur} -> {tgt}")
def cmd_note(a):
    st=load(); bucket="open_questions" if a.question else "notes"; st[bucket].append(a.text.strip()); save(st); print(f"{bucket}: {a.text.strip()}")
def cmd_resolve(a):
    st=load()
    if not (1<=a.n<=len(st["open_questions"])): die(f"no open question #{a.n}")
    removed=st["open_questions"].pop(a.n-1); save(st); print(f"resolved: {removed}")
def cmd_show(_a): print(json.dumps(load(),indent=2,ensure_ascii=False))
def failures(st):
    out=[]
    if not st.get("criteria"): out.append("no acceptance criteria recorded")
    for c in st.get("criteria",[]):
        if c.get("status")!="met": out.append(f"{c.get('id')} not met: {c.get('text')}")
        elif not c.get("evidence","").strip(): out.append(f"{c.get('id')} marked met but has no evidence")
    if st.get("open_questions"): out.append(f"{len(st['open_questions'])} open question(s) unresolved")
    if st.get("phase") not in ("report","done"): out.append(f"phase is '{st.get('phase')}', not report/done")
    return out
def cmd_check(_a):
    st=load(); probs=failures(st)
    if probs:
        print("NOT DONE — do not claim completion:",file=sys.stderr)
        for p in probs: print(f"  - {p}",file=sys.stderr)
        sys.exit(1)
    print(f"DONE: {len(st['criteria'])}/{len(st['criteria'])} criteria met with evidence, no open questions.")
    if st["phase"]=="report": st["phase"]="done"; save(st)
def cmd_done(_a):
    st=load(); probs=failures(st)
    if probs:
        print("NOT DONE — gate failed:",file=sys.stderr)
        for p in probs: print(f"  - {p}",file=sys.stderr)
        sys.exit(1)
    os.remove(state_path()); print("DONE and state file removed.")
def build_parser():
    p=argparse.ArgumentParser(prog="state.py",description=__doc__); sub=p.add_subparsers(dest="cmd",required=True)
    for name,fn,args in [("init",cmd_init,[("goal",{}),("--tier",{"default":"standard"})]),("add",cmd_add,[("text",{})]),("meet",cmd_meet,[("id",{}),("evidence",{})]),("reopen",cmd_reopen,[("id",{})]),("phase",cmd_phase,[("to",{})]),("note",cmd_note,[("text",{}),("--question",{"action":"store_true"})]),("resolve",cmd_resolve,[("n",{"type":int})])]:
        s=sub.add_parser(name)
        for a,kw in args: s.add_argument(a,**kw)
        s.set_defaults(fn=fn)
    s=sub.add_parser("show"); s.set_defaults(fn=cmd_show)
    s=sub.add_parser("check"); s.set_defaults(fn=cmd_check)
    s=sub.add_parser("done"); s.set_defaults(fn=cmd_done)
    return p
def main(argv=None):
    a=build_parser().parse_args(argv); a.fn(a)
if __name__=="__main__": main()
