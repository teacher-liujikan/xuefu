"""一、二年級國語：從試卷（無答案）裁每題圖。"""
import pymupdf,re,json,sys
from PIL import Image
from build_zh import trim,save
from qpos12 import qpos
SC=2.4
def heads(p,col,W):
    hs=[]
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            t=''.join(s['text'] for s in l['spans']).strip()
            x=l['bbox'][0]
            if re.match(r'^[一二三四五六]\s*[、，]',t) and ((x<W/2-20)==(col==0)): hs.append(l['bbox'][1])
            if t.startswith('※') and ((x<W/2-20)==(col==0)): hs.append(l['bbox'][1]-6)
    return sorted(hs)
def run(g,y,psg=None):
    f=f'/home/claude/papers_zh12/g{g}-{y}-q.pdf'; d,P=qpos(f); res={}
    ns=sorted(P)
    for n in ns:
        pg,col,x,yy,xe,ye=P[n]; p=d[pg]; W=p.rect.width; H=p.rect.height
        nxt=[P[m][3] for m in ns if P[m][0]==pg and P[m][1]==col and P[m][3]>yy]
        hs=[h for h in heads(p,col,W) if h>yy+5]
        bot=min(nxt+hs+[H-60])
        tab=(g==1 and n<=4); fillrow=(g==1 and 5<=n<=8) or (g==2 and n<=5)
        top=yy-32 if tab else (yy-19 if fillrow else yy-8)
        if tab: bot=(min(nxt) if nxt else yy+44)-32 if n<4 else yy+44
        if not tab and nxt and bot==min(nxt): bot-=6
        if fillrow: bot=yy+27
        a=0 if col==0 else W/2+10; b=W/2-8 if col==0 else W-6
        if not tab and not fillrow and not nxt:
            while bot<H-22:
                st=p.get_pixmap(matrix=pymupdf.Matrix(1,1),clip=pymupdf.Rect(a,bot-2,b,bot+1),alpha=False)
                if min(st.samples)>200: break
                bot+=3
        pm=p.get_pixmap(matrix=pymupdf.Matrix(SC,SC),clip=pymupdf.Rect(a,top,b,bot),alpha=False)
        im=Image.frombytes('RGB',(pm.width,pm.height),pm.samples)
        if not tab:
            import numpy as np
            from scipy import ndimage
            arr=np.array(im); ink=arr.min(axis=2)<170; lab,_=ndimage.label(ink,structure=np.ones((3,3)))
            for i in set(lab[:2].ravel())|set(lab[-2:].ravel()):
                if not i: continue
                ys,xs=np.where(lab==i)
                if ys.max()-ys.min()<34: arr[ndimage.binary_dilation(lab==i,iterations=2)]=255
            im=Image.fromarray(arr)
        from PIL import ImageDraw
        ImageDraw.Draw(im).rectangle([(x-1-a)*SC,(yy-1-top)*SC,(xe+1-a)*SC,(ye+1-top)*SC],fill=(255,255,255))
        im=trim(im)
        nm=save(im,f'g{g}-{y}-{n}.png'); res[n]=(nm,im.width,im.height)
    if psg:  # (pg,col,y0,y1)
        pg,col,y0,y1=psg; p=d[pg]; W=p.rect.width
        a=0 if col==0 else W/2+14; b=W/2-4 if col==0 else W-6
        pm=p.get_pixmap(matrix=pymupdf.Matrix(SC,SC),clip=pymupdf.Rect(a,y0,b,y1),alpha=False)
        im=trim(Image.frombytes('RGB',(pm.width,pm.height),pm.samples)); res['psg']=(save(im,f'g{g}-{y}-p23.png'),im.width,im.height)
    return res
if __name__=='__main__':
    out={}
    for g in (1,2):
      for y in ('114','113','112','111'):
        d,P=qpos(f'/home/claude/papers_zh12/g{g}-{y}-q.pdf')
        # 閱讀文章：第 23 題上方（右欄，第二頁），從「四、/三、閱讀測驗」標題下到第 23 題
        pg,col,x,yy,_,_=P[23]; p=d[pg]; hs=[h for h in heads(p,1,p.rect.width) if h<yy]
        out[(g,y)]=run(g,y,(pg,1,max(hs)+16,yy-8))
    json.dump({(f'{g}-{k}' if y=='114' else f'{g}-{y}-{k}'):v for (g,y),r in out.items() for k,v in r.items()},open('/home/claude/work/zh/zh12_imgs.json','w'),ensure_ascii=False)
    print({k:len(r) for k,r in out.items()})
