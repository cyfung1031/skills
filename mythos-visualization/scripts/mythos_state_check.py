#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
REQUIRED = ['smallest sufficient mode','one dominant lens','observed','measured','inferred','not verified','source','render','runtime','stop']
def sha256(p: Path) -> str:
    h=hashlib.sha256();
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1048576), b''): h.update(c)
    return h.hexdigest()
def fm(text: str) -> dict:
    if not text.startswith('---\n'): raise ValueError('missing frontmatter')
    end=text.find('\n---\n',4)
    if end < 0: raise ValueError('unterminated frontmatter')
    out={}
    for line in text[4:end].splitlines():
        if ':' in line:
            k,v=line.split(':',1); out[k.strip()]=v.strip().strip('"\'')
    return out
def approx_tokens(text: str) -> int: return max(1, int(len(re.findall(r'\S+', text))*1.33))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--package',default='.'); ap.add_argument('--write-checksums', action='store_true'); args=ap.parse_args()
    root=Path(args.package).resolve(); errors=[]; warnings=[]
    skill=root/'SKILL.md'; contract=root/'skill_contract.json'
    if not skill.exists(): errors.append('SKILL.md missing'); text=''; meta={}
    else:
        text=skill.read_text(encoding='utf-8');
        try: meta=fm(text)
        except Exception as e: meta={}; errors.append(f'frontmatter parse failed: {e}')
    data=json.loads(contract.read_text(encoding='utf-8')) if contract.exists() else {}
    if not data: errors.append('skill_contract.json missing')
    ver=meta.get('version')
    if ver != data.get('version'): errors.append(f'version mismatch: {ver} vs {data.get("version")}')
    for term in REQUIRED:
        if term not in text.lower(): errors.append(f'invariant term missing: {term}')
    for mod in data.get('modules',[]):
        if not (root/mod).exists(): errors.append(f'module missing: {mod}')
        if mod not in text: warnings.append(f'module not referenced in SKILL.md: {mod}')
    for scr in data.get('scripts',[]):
        p=root/scr
        if not p.exists(): errors.append(f'script missing: {scr}')
        else: compile(p.read_text(encoding='utf-8'), str(p), 'exec')
    low=text.lower()
    if 'must use ocr' in low or 'always render' in low or 'must render' in low: errors.append('mandatory OCR/rendering language found')
    tokens={'SKILL.md': approx_tokens(text)}
    for mod in data.get('modules',[]):
        p=root/mod
        if p.exists(): tokens[mod]=approx_tokens(p.read_text(encoding='utf-8'))
    if tokens['SKILL.md'] > 3200: warnings.append(f'always-load token estimate high: {tokens["SKILL.md"]}')
    if args.write_checksums:
        lines=[]
        for p in sorted(root.rglob('*')):
            if p.is_file() and p.name != 'artifact_checksums.sha256' and not p.name.endswith('.zip'):
                lines.append(f'{sha256(p)}  {p.relative_to(root)}')
        (root/'artifact_checksums.sha256').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps({'status':'pass' if not errors else 'fail','version':ver,'module_count':len(data.get('modules',[])),'script_count':len(data.get('scripts',[])),'rough_token_estimates':tokens,'errors':errors,'warnings':warnings}, indent=2))
    return 0 if not errors else 1
if __name__ == '__main__': raise SystemExit(main())
