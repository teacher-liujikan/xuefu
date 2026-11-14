import json,re,os,sys,importlib.util
import pymupdf
from PIL import Image,ImageDraw
from parse_en import parse
from build_zh import trim
import build_zh
OUT='/home/claude/repo-xuefu/english/'
SC=2.4
PAPERS=[(g,y) for g in (4,5,6) for y in ('114','113')]
SECTAG={'聽辨語音':'L1','聽辨單字':'L2','聽辨常用語或句子':'L3','辨識單字':'R1','辨識句子':'R2'}
def save(im,name):
    build_zh.OUT=OUT; return build_zh.save(im,name)
def cropq(d,q):
    p=d[q['pg']]; W=p.rect.width; mid=W/2
    a=q['nx']-40; b=(mid-5 if q['col']==0 else W-8)
    a=max(a,(0 if q['col']==0 else mid+5))
    clip=pymupdf.Rect(a,q['y0']-5,b,q['y1'])
    pm=p.get_pixmap(matrix=pymupdf.Matrix(SC,SC),clip=clip,alpha=False)
    im=Image.frombytes('RGB',(pm.width,pm.height),pm.samples)
    ImageDraw.Draw(im).rectangle([0,0,(q['nend']+1.5-clip.x0)*SC,(q['ny'][1]+3-clip.y0)*SC],fill=(255,255,255))
    return trim(im)
def loadsrc(g,y):
    p=f'src_en/g{g}_{y}.py'
    if not os.path.exists(p): return None
    spec=importlib.util.spec_from_file_location(f'e{g}_{y}',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
AUDSRC={(4,'114'):('/mnt/user-data/uploads/Downloads/114年篩選測驗英語科4年級試卷聽力檔.mp3','/home/claude/work/audio/t4_114.json'),
        (4,'113'):('/mnt/user-data/uploads/Downloads/113年篩選測驗英語科4年級試卷聽力檔.mp3','/home/claude/work/audio/t4_113.json')}
AUD={}
AUDFIX={(4,'113'):{1:(111.5,125.0),2:(125.0,137.7)}}   # 第二題的「第二題」語音沒被辨識出來，手動指定
def load_aud():
    from audio_cut import items
    for k,(src,tr) in AUDSRC.items():
        if os.path.exists(src) and os.path.exists(tr):
            its={n:(a,b_) for n,a,b_,_ in items(json.load(open(tr))) if n<=10}
            for n,(a_,b2) in AUDFIX.get(k,{}).items(): its[n]=(a_,b2)
            assert sorted(its)==list(range(1,11)),(k,sorted(its))
            AUD[k]=(src,its)
def main(sheets=False):
    load_aud()
    QS=[];rep=[]
    for g,y in PAPERS:
        d,qs,secs=parse(f'g{g}-{y}-a')
        m=loadsrc(g,y); EX=getattr(m,'EX',{}) if m else {}; OPT=getattr(m,'OPT',{}) if m else {}; STEM=getattr(m,'STEM',{}) if m else {}
        ims=[]
        for q in qs:
            n=q['no']; sec=q['sec']['name']; tag=SECTAG[sec]
            if tag[0]=='L' and not sheets and (g,y) not in AUD: continue   # 沒有音檔的聽力題先不放
            im=cropq(d,q); ims.append((n,im))
            o=dict(id=f'g{g}-{y}-{n}',grade=g,year=y,no=n,type='choice',stem=STEM.get(n,''),options=OPT.get(n,['(1)','(2)','(3)']),answer=q['ans'],
                   img=save(im,f'g{g}-{y}-{n}.png'),iw=im.width,ih=im.height,xf=[f'{tag[0]}-{g}-{tag[1]}'],listen=tag[0]=='L',sec=sec)
            if tag[0]=='L':
                from audio_cut import cut
                src,its=AUD[(g,y)]; aud=f'audio/g{g}-{y}-{n}.mp3'; cut(src,its[n][0],its[n][1],OUT+aud); o['audio']=aud
            if n in EX: o['ex']=EX[n]
            prob=[]
            if o['answer'] not in (1,2,3): prob.append('noans')
            if n not in EX: prob.append('noex')
            elif f"所以選 {'①②③'[o['answer']-1]}" not in o['ex'][-1]: prob.append('exans')
            if n not in OPT: prob.append('noopt')
            if prob: rep.append((o['id'],prob))
            QS.append(o)
        if sheets:
            for part,(a,b) in enumerate([(1,10),(11,25)]):
                sel=[(n,i) for n,i in ims if a<=n<=b]
                cols=3 if part==0 else 3
                tw=560; cells=[]
                for n,i in sel:
                    r=tw/i.width; j=i.resize((tw,int(i.height*r)))
                    c=Image.new('RGB',(tw+8,j.height+30),'white'); c.paste(j,(4,26)); ImageDraw.Draw(c).text((6,4),f'Q{n}  ans={[q for q in qs if q["no"]==n][0]["ans"]}',fill=(200,0,0)); cells.append(c)
                rows=[cells[k:k+cols] for k in range(0,len(cells),cols)]
                H=sum(max(c.height for c in r) for r in rows); o=Image.new('RGB',(cols*(tw+8),H),'#999'); yy=0
                for r in rows:
                    for k,c in enumerate(r): o.paste(c,(k*(tw+8),yy))
                    yy+=max(c.height for c in r)
                o.save(f'/home/claude/papers_en/pg/sheet_g{g}-{y}-{part}.png'); print('sheet',g,y,part,o.size)
    json.dump(QS,open(OUT+'data/questions.json','w'),ensure_ascii=False,indent=1)
    json.dump({},open(OUT+'data/passages.json','w'))
    LAB={'L0':'字母聽寫','L1':'聽辨語音','L2':'聽辨單字','L3':'聽辨常用語或句子','R1':'辨識單字','R2':'辨識句子'}
    json.dump({'xuefu':{f'{k[0]}-{g}-{k[1]}':{'label':v,'summary':''} for g in (3,4,5,6) for k,v in LAB.items()}},open(OUT+'data/codes.json','w'),ensure_ascii=False,indent=1)
    print('total',len(QS),'problems',len(rep)); 
    for r in rep[:12]: print(' !',r)
if __name__=='__main__': main('sheets' in sys.argv)
