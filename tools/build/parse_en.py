import re,sys,json,pymupdf
import ext
QRE=re.compile(r'^(\d ?\d?)\s?\.\s*(.*)$')
HRE=re.compile(r'^([一二三四五六])、\s*(\S+?)\s*[\(（]第\s*(\d+)\s*[-–~～]\s*(\d+)\s*題')
def parse(name):
    ext.P='/home/claude/papers_en/'
    d,ls=ext.load(name)
    W=d[0].rect.width; mid=W/2
    ls.sort(key=lambda L:(L['pg'],L['col'],L['yc']))
    isred=lambda c:(c['col']>>16)>150 and ((c['col']>>8)&255)<110
    items=[]; nextq=1; part=''; secs=[]
    for L in ls:
        t=L['txt']; real=L['real']
        if '評量' in t and '試卷' in t and L['y0']>1000 or re.search(r'第\s*\d+\s*頁',t): items.append(('foot',L)); continue
        m=re.match(r'^第([一二])部分：(\S+)',t)
        if m: part=m.group(2); items.append(('hdr',L)); continue
        h=HRE.match(t)
        if h: secs.append(dict(part=part,name=h.group(2),a=int(h.group(3)),b=int(h.group(4)))); items.append(('hdr',L)); continue
        body=[c for c in real]; ans=None
        if len(real)>3 and real[0]['c']=='(' and isred(real[1]) and real[1]['c'] in '123' :
            ans=int(real[1]['c']); body=real[3:]
        tt=''.join(c['c'] for c in body)
        m=QRE.match(tt.strip())
        if m and int(m.group(1).replace(' ',''))==nextq and (ans or name.endswith('q')):
            k=0;seen=''
            while not seen.endswith('.'): seen+=body[k]['c'];k+=1
            items.append(('q',L,dict(no=nextq,ans=ans,nend=body[k-1]['x1'],nx=body[0]['x0'],sx=(body[k]['x0'] if k<len(body) else body[k-1]['x1']+6),ny=(L['y0'],L['y1']),txt=m.group(2))))
            nextq+=1; continue
        if re.match(r'^作答說明|^第.部分作答完畢|^本試卷|^試題結束',t) : items.append(('hdr',L)); continue
        items.append(('t',L))
    # build question blocks
    out=[]
    for i,it in enumerate(items):
        if it[0]!='q': continue
        L=it[1]; q=it[2]; texts=[q['txt']]; y1=L['y1']
        ynext=None
        for jt in items[i+1:]:
            Lj=jt[1]
            if Lj['pg']!=L['pg'] or Lj['col']!=L['col']: break
            if jt[0] in('q','hdr','foot'): ynext=Lj['y0']-6; break
            texts.append(Lj['txt']); y1=max(y1,Lj['y1'])
        if ynext is None: ynext=d[L['pg']].rect.height-70
        sec=[s for s in secs if s['a']<=q['no']<=s['b']]
        q.update(pg=L['pg'],col=L['col'],y0=L['y0'],ty1=y1,band=ynext,texts=texts,sec=sec[-1] if sec else None)
        out.append(q)
    # attach pictures: each image goes to the question whose band it overlaps most
    for q in out: q['y1']=q['ty1']+4
    for pi,p in enumerate(d):
        mid=p.rect.width/2
        boxes=[pymupdf.Rect(i['bbox']) for i in p.get_image_info()]
        for dr in p.get_drawings():
            r=dr['rect']
            if r.width>12 and r.height>12 and r.width<380 and r.height<300: boxes.append(r)
        for r in boxes:
            if r.width<8 or r.height<8 or r.y0<0: continue
            col=0 if (r.x0+r.x1)/2<mid else 1
            best=None;bo=0
            for q in out:
                if q['pg']!=pi or q['col']!=col: continue
                ov=min(r.y1,q['band'])-max(r.y0,q['y0']-12)
                if ov>bo: bo=ov;best=q
            if best and bo>0.45*r.height:
                best['y0']=min(best['y0'],r.y0-3); best['y1']=max(best['y1'],r.y1+3)
    return d,out,secs
if __name__=='__main__':
    d,out,secs=parse(sys.argv[1])
    print(secs)
    for q in out: print(q['no'],q['ans'],q['pg'],q['col'],round(q['y0']),round(q['y1']),q['sec']['name'] if q['sec'] else None,'|',' / '.join(q['texts'])[:110])
