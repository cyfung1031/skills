#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, mimetypes
from datetime import datetime, timezone
from pathlib import Path
IMAGE={'.png','.jpg','.jpeg','.webp','.gif','.bmp','.tif','.tiff','.svg'}; SOURCE={'.html','.htm','.css','.js','.jsx','.ts','.tsx','.json','.svg','.xml','.md'}
IGNORE={'.DS_Store'}; IGNORE_PARTS={'__MACOSX','node_modules','.git','__pycache__'}
def sha256(p: Path) -> str:
    h=hashlib.sha256();
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1048576), b''): h.update(c)
    return h.hexdigest()
def kind(p: Path) -> str:
    e=p.suffix.lower()
    if e in IMAGE and e!='.svg': return 'raster_image'
    if e=='.svg': return 'source_backed_svg'
    if e in SOURCE: return 'source_file'
    return 'other'
def route(p: Path, k: str) -> str:
    s=str(p).lower()
    if k in ('source_backed_svg','source_file'): return 'source-backed graphic'
    for key,r in [('chart','chart/data'),('map','map/spatial'),('diagram','diagram/system'),('screenshot','UI/product'),('ui','UI/product'),('photo','photo/scene'),('object','creature/object'),('creature','creature/object'),('meme','meme/social'),('abstract','abstract/formal'),('scientific','scientific/industrial'),('scan','scan/document')]:
        if key in s: return r
    return 'photo/scene or visual artifact' if k=='raster_image' else 'unknown'
def img_meta(p: Path) -> dict:
    try:
        from PIL import Image
        with Image.open(p) as im: return {'width':im.size[0], 'height':im.size[1], 'mode':im.mode, 'format':im.format}
    except Exception as e: return {'decode_error':str(e).split('\n')[0][:180]}
def ignored(p: Path) -> bool: return p.name in IGNORE or any(part in IGNORE_PARTS for part in p.parts)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input', required=True); ap.add_argument('--output', required=True); ap.add_argument('--sample-reports', action='store_true'); args=ap.parse_args()
    inp=Path(args.input).resolve(); out=Path(args.output).resolve(); out.mkdir(parents=True, exist_ok=True)
    rep=out/'sample_reports'
    if args.sample_reports: rep.mkdir(exist_ok=True)
    rows=[]
    for i,p in enumerate(sorted([x for x in inp.rglob('*') if x.is_file() and not ignored(x)]),1):
        rel=p.relative_to(inp); k=kind(p); row={'id':f'sample_{i:05d}','path':str(rel),'size_bytes':p.stat().st_size,'sha256':sha256(p),'mime_guess':mimetypes.guess_type(str(p))[0] or '','kind':k,'route_hint':route(rel,k),'route_confidence':'medium' if k in ('raster_image','source_file','source_backed_svg') else 'low','validation_depth':'D1 static classification','status':'ok'}
        if k=='raster_image':
            row.update(img_meta(p))
            if row.get('decode_error'): row['status']='partial_decode_error'; row['route_confidence']='low'
        if args.sample_reports:
            rp=rep/f'{row["id"]}.md'
            img_phrase=', image metadata' if k=='raster_image' else ''
            rp.write_text(f'''# Analysis Report: {row["id"]}\n\n## Identity and route\n- Artifact role: corpus sample\n- Visible/source role: {row['kind']}\n- Dominant lens: {row['route_hint']}\n- Mode: Ultra-Compact corpus row\n- Route confidence: {row['route_confidence']}\n\n## Evidence boundary\n- Evidence used: path, extension, size, checksum, coarse metadata{img_phrase}\n- Evidence not verified: deep visual interpretation, OCR, rendering, runtime behavior, accessibility tree, external facts\n- Exactness level: exact for file metadata; pattern-only/unavailable for visual semantics\n\n## Compact model\nD1 mechanical inventory record only.\n\n## Detail-overall bridge\nThe route hint follows from file type and path/metadata; it is not a substitute for manual visual analysis.\n\n## Risks and limits\n- Filename or folder labels may be coarse or misleading.\n- Visual/source content was not deeply interpreted in this stub.\n\n## Validation\n- Depth: D1 static classification\n- Tools/checks run: checksum, stat, extension/mime guess{img_phrase}\n- Checks not run: OCR, browser rendering, accessibility, domain validation, external lookup\n''', encoding='utf-8')
            row['report_path']=str(Path('sample_reports')/rp.name)
        else: row['report_path']=''
        rows.append(row)
    fields=sorted({k for r in rows for k in r})
    with (out/'analysis_index.csv').open('w', newline='', encoding='utf-8') as f: w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    counts={}
    for r in rows: counts[r['kind']]=counts.get(r['kind'],0)+1
    (out/'run_manifest.json').write_text(json.dumps({'input':str(inp),'output':str(out),'timestamp':datetime.now(timezone.utc).isoformat(timespec='seconds'),'records':len(rows),'validation_depth':'D0/D1','sample_reports_written':args.sample_reports,'limitations':['no deep visual interpretation','no OCR','no rendering','no accessibility tooling','no external lookup']}, indent=2), encoding='utf-8')
    (out/'corpus_summary.md').write_text('# Corpus Summary\n\n## Scope\nD0/D1 mechanical probe.\n\n## Inventory\n'+'\n'.join(f'- {k}: {v}' for k,v in sorted(counts.items()))+'\n\n## Validation limits\nNo OCR, rendering, accessibility tooling, external lookup, or deep visual interpretation was run.\n', encoding='utf-8')
    print(json.dumps({'status':'pass','records':len(rows),'output':str(out)}, indent=2)); return 0
if __name__ == '__main__': raise SystemExit(main())
