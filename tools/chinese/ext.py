import pymupdf, re, json, sys, collections
P='/home/claude/papers_zh/'
def fontkind(f):
    try: g=f.encode('latin1').decode('big5',errors='replace')
    except Exception: g=f
    if '寬注音' in g or '寬破音' in g: return 'Z'      # zhuyin only
    if '注音' in g or '破音' in g: return 'R'   # char with ruby
    return ''
def page_lines(p):
    W=p.rect.width; mid=W/2
    chars=[]
    for b in p.get_text('rawdict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                k=fontkind(s['font']); bi=bool(s['flags']&2) and ('Times' not in s['font'])
                for ch in s['chars']:
                    if ch['c'].strip()=='' : 
                        chars.append(dict(c=' ',x0=ch['bbox'][0],x1=ch['bbox'][2],y0=ch['bbox'][1],y1=ch['bbox'][3],k=k,col=s['color'],sz=s['size'],f=s['font'],bi=bi));continue
                    chars.append(dict(c=ch['c'],x0=ch['bbox'][0],x1=ch['bbox'][2],y0=ch['bbox'][1],y1=ch['bbox'][3],k=k,col=s['color'],sz=s['size'],f=s['font'],bi=bi))
    # underlines
    und=[]
    for d in p.get_drawings():
        r=d['rect']
        if r.width>6 and r.height<3: und.append((r.x0,r.x1,(r.y0+r.y1)/2))
    cols=[[],[]]
    for c in chars:
        cols[0 if (c['x0']+c['x1'])/2<mid else 1].append(c)
    out=[]
    for ci,cs in enumerate(cols):
        cs=[c for c in cs]
        cs.sort(key=lambda c:(c['y0']+c['y1'])/2)
        lines=[]
        for c in cs:
            yc=(c['y0']+c['y1'])/2
            if lines and abs(yc-lines[-1]['yc'])<max(5,c['sz']*0.45):
                L=lines[-1]; L['cs'].append(c); n=len(L['cs']); L['yc']=(L['yc']*(n-1)+yc)/n
            else: lines.append(dict(yc=yc,cs=[c]))
        for L in lines:
            L['cs'].sort(key=lambda c:c['x0'])
            # underline flags
            for c in L['cs']:
                c['u']=0
                for (x0,x1,y) in und:
                    if x0-1<=(c['x0']+c['x1'])/2<=x1+1 and -2<y-c['y1']<6: c['u']+=1
            txt=''
            prev=None
            for c in L['cs']:
                if c['c']==' ':
                    if prev is not None and not txt.endswith(' '): txt+=' '
                    continue
                txt+=c['c']; prev=c
            real=[c for c in L['cs'] if c['c']!=' ']
            if not real: continue
            L.update(col=ci,x0=real[0]['x0'],x1=real[-1]['x1'],y0=min(c['y0'] for c in real),y1=max(c['y1'] for c in real),txt=txt.strip(),real=real)
            out.append(L)
    return out,und
def load(name):
    d=pymupdf.open(P+name+'.pdf'); res=[]
    for pi,p in enumerate(d):
        ls,und=page_lines(p)
        for L in ls: L['pg']=pi; res.append(L)
    return d,res
if __name__=='__main__':
    d,ls=load(sys.argv[1])
    for L in ls:
        fl=''.join(sorted(set(c['k'] for c in L['real'])))
        u='U' if any(c['u'] for c in L['real']) else ''
        print(L['pg'],L['col'],round(L['x0']),round(L['y0']),fl,u,'|',L['txt'])
