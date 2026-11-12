import json, re, sys, os, importlib.util, io
import pymupdf
from PIL import Image, ImageChops
from parse import parse
OUT='/home/claude/repo-xuefu/chinese/'
PAPERS=[(g,y,('a' if y in('113','114') else 'q')) for g in (3,4,5,6) for y in ('114','113','112','111')]
SC=2.4
def loadsrc(g,y):
    p=f'src/g{g}_{y}.py'
    if not os.path.exists(p): return None
    spec=importlib.util.spec_from_file_location(f'g{g}_{y}',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def trim(im,pad=6):
    bg=Image.new('RGB',im.size,(255,255,255)); bb=ImageChops.difference(im.convert('RGB'),bg).point(lambda v:255 if v>40 else 0).getbbox()
    if not bb: return im
    x0,y0,x1,y1=bb; return im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
def crop(d,rects,x0=None,padt=4,padb=6,xr=None,wipe=None):
    ims=[]
    for r in rects:
        p=d[r['pg']]; W=p.rect.width; mid=W/2
        a=(x0 if (x0 is not None and r is rects[0]) else (0 if r['col']==0 else mid+5))
        if xr: a,b=xr
        else: b=(mid-5 if r['col']==0 else W)
        clip=pymupdf.Rect(a,r['y0']-padt,b,r['y1']+padb)
        pm=p.get_pixmap(matrix=pymupdf.Matrix(SC,SC),clip=clip,alpha=False)
        im=Image.frombytes('RGB',(pm.width,pm.height),pm.samples)
        if wipe and r is rects[0]:
            from PIL import ImageDraw
            wx0,wx1,wy0,wy1=wipe
            ImageDraw.Draw(im).rectangle([0,max(0,(wy0-2-clip.y0)*SC),(wx1-clip.x0)*SC,(wy1+2-clip.y0)*SC],fill=(255,255,255))
        # blank out left strip before x0 on later lines not needed
        ims.append(trim(im))
    if len(ims)==1: return ims[0]
    w=max(i.width for i in ims); h=sum(i.height for i in ims)+8*(len(ims)-1)
    o=Image.new('RGB',(w,h),(255,255,255)); y=0
    for i in ims: o.paste(i,(0,y)); y+=i.height+8
    return o
def save(im,name):
    g=im.convert('L')
    # keep colour only if image is really colourful
    rgb=im.convert('RGB'); 
    diff=ImageChops.difference(rgb,g.convert('RGB')).convert('L').point(lambda v:255 if v>28 else 0)
    colourful=diff.histogram()[255]>im.width*im.height*0.002
    if colourful: q=rgb.quantize(64,method=Image.Quantize.MEDIANCUT)
    else: q=g.quantize(8)
    q.save(OUT+'img/'+name,optimize=True)
    return 'img/'+name
def clean(s,g):
    s=s.replace('{','').replace('}','')
    s=re.sub(r'<u>([１-９])</u>',lambda m:'〔'+str('１２３４５６７８９'.index(m.group(1))+1)+'〕',s)
    if g==3: s=re.sub(r'</?[ub]>','',s)
    return s.strip()
def main(only=None):
    QS=[];PS={};rep=[]
    for g,y,k in PAPERS:
        m=loadsrc(g,y)
        if not m: continue
        name=f'g{g}-{y}-{k}'
        d,blocks=parse(name)
        psg_of={}
        PSG=getattr(m,'PSG',{}); PATCH=getattr(m,'PATCH',{}); EX=getattr(m,'EX',{}); TAG=getattr(m,'TAG',{}); ANS=getattr(m,'ANS',{}); QIMG=getattr(m,'QIMG',set())
        qblocks={b['no']:b for b in blocks if b['kind']=='q'}
        for b in blocks:
            if b['kind']!='p': continue
            pid=f'g{g}-{y}-p{b["a"]}'
            o=PSG.get(b['a'],{})
            P=dict(id=pid,a=b['a'],b=b['b'],intro=f'請閱讀以下文章，並回答 {b["a"]}～{b["b"]} 題：')
            if o.get('intro'): P['intro']=o['intro']
            if o.get('img') or g==3:
                rects=[r for r in b['rects']]
                # drop the intro line itself from top
                if o.get('rects'): rects=o['rects']
                else:
                    # extend each rect to the start of next block in same column
                    first=qblocks[b['a']]['rects'][0]
                    for r in rects:
                        if r['pg']==first['pg'] and r['col']==first['col'] and first['y0']>r['y0']: r['y1']=max(r['y1'],first['y0']-10)
                        elif o.get('ybot'): r['y1']=o['ybot']
                    rects[0]=dict(rects[0]); rects[0]['y0']=b['rects'][0]['y0']+ (o.get('skiptop',21))
                im=crop(d,rects,padt=2,padb=8)
                P['img']=save(im,f'g{g}-{y}-p{b["a"]}.png'); P['w']=im.width; P['h']=im.height
            P['text']=re.sub(r'<u>([^<]{11,})</u>',r'\1',o.get('text',clean(b['text'],g)))
            for a_,b_ in o.get('sub',[]):
                assert a_ in P['text'],(pid,a_); P['text']=P['text'].replace(a_,b_)
            if o.get('title'):
                P['title']=o['title']
                if P['text'].startswith(o['title']+'\n'): P['text']=P['text'][len(o['title'])+1:]
            PS[pid]=P
            for n in range(b['a'],b['b']+1): psg_of[n]=pid
        for b in blocks:
            if b['kind']!='q': continue
            n=b['no']; pt=PATCH.get(n,{})
            q=dict(id=f'g{g}-{y}-{n}',grade=g,year=y,no=n,type='choice',stem=pt.get('stem',clean(b['stem'],g)),
                   options=pt.get('options',[clean(x,g) for x in b['options']]),
                   answer=b['ans'] if b['ans'] else ANS.get(n))
            if not b['ans']: q['ansSrc']='self'
            if n in psg_of: q['psg']=psg_of[n]
            if g==3 or n in QIMG:
                rr=[dict(r) for r in b['rects']]; rr[-1]['y1']=b['ynext']-6
                im=crop(d,rr,x0=b['nx']-1.5,wipe=(b['nx']-2,b['sx']-0.3,b['ny'][0],b['ny'][1]))
                q['img']=save(im,f'g{g}-{y}-{n}.png'); q['iw']=im.width; q['ih']=im.height
            q['xf']=[f"{TAG[n][0]}-{g}-{TAG[n][1:]}"] if n in TAG else []
            if n in EX: q['ex']=EX[n] if isinstance(EX[n],list) else [EX[n]]
            prob=[]
            if q['answer'] not in (1,2,3,4): prob.append('noans')
            if any(not o for o in q['options']) or len(q['options'])!=4: prob.append('opts')
            if n not in EX: prob.append('noex')
            if n not in TAG: prob.append('notag')
            if n in EX:
                last=q['ex'][-1]; circ='①②③④'[q['answer']-1] if q['answer'] else '?'
                if f'所以選 {circ}' not in last: prob.append('exans:'+last[:14])
            if prob: rep.append((q['id'],prob))
            QS.append(q)
        nq=len([b for b in blocks if b['kind']=='q'])
        print(name,'questions',nq,'passages',len([b for b in blocks if b['kind']=='p']))
    json.dump(QS,open(OUT+'data/questions.json','w'),ensure_ascii=False,indent=1)
    json.dump(PS,open(OUT+'data/passages.json','w'),ensure_ascii=False,indent=1)
    LAB={'A1':'字音','A2':'字形（國字）','A3':'部首','B1':'詞義','B2':'詞語運用','C1':'句意理解','C2':'段落重點','C3':'語句銜接與排序','C4':'刪除多餘語詞','C5':'標點符號','D1':'閱讀：故事','D2':'閱讀：說明文與圖表'}
    json.dump({'xuefu':{f'{k[0]}-{g}-{k[1:]}':{'label':v,'summary':''} for g in (3,4,5,6) for k,v in LAB.items()}},open(OUT+'data/codes.json','w'),ensure_ascii=False,indent=1)
    for r in rep: print('  !',r)
    print('total',len(QS),'passages',len(PS))
if __name__=='__main__': main()
