import pymupdf,re
def qpos(f):
    """題號位置：(頁, 欄, x0, y0, 題號（含點）右緣, y1)"""
    d=pymupdf.open(f); out={}
    for pi,p in enumerate(d):
        W=p.rect.width
        for b in p.get_text('rawdict')['blocks']:
            for l in b.get('lines',[]):
                chars=[c for s in l['spans'] for c in s['chars']]
                t=''.join(c['c'] for c in chars).lstrip()
                cs=[c for c in chars if c['c'].strip()]
                m=re.match(r'^(\d{1,2})\.',''.join(c['c'] for c in cs))
                if not m: continue
                x0=cs[0]['bbox'][0]
                if not (x0<80 or W/2-20<x0<W/2+60): continue
                n=int(m.group(1))
                if 1<=n<=25 and n not in out:
                    k=len(m.group(0)); bb=[c['bbox'] for c in cs[:k]]
                    out[n]=(pi,0 if x0<W/2-20 else 1,x0,min(b_[1] for b_ in bb),max(b_[2] for b_ in bb),max(b_[3] for b_ in bb))
    return d,out
