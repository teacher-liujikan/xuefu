import pymupdf
from PIL import Image
from build_zh import trim
OUT='/home/claude/repo-xuefu/english/img/'
SC=2.4
res={}
for y in ('113','114'):
    d=pymupdf.open(f'/home/claude/papers_en/g3-{y}-a.pdf'); p=d[1]; W=p.rect.width; mid=W/2
    ws=p.get_text('words')
    nums={}
    for w in ws:
        if w[0]>mid and w[4] in ('22.','23.','24.','25.'): nums[int(w[4][:2])]=w
    labs=sorted([w for w in ws if w[0]>mid and w[4]=='(1)'],key=lambda w:w[1])
    for n in (22,23,24,25):
        y0=nums[n][1]
        lab=[w for w in labs if w[1]>y0][0]
        top=lab[1]-3
        bot=(nums[n+1][1]-6) if n<25 else top+150
        clip=pymupdf.Rect(mid+18,top,W-30,bot)
        pm=p.get_pixmap(matrix=pymupdf.Matrix(SC,SC),clip=clip,alpha=False)
        im=trim(Image.frombytes('RGB',(pm.width,pm.height),pm.samples))
        name=f'g3-{y}-{n}.png'; im.convert('L').quantize(16).save(OUT+name,optimize=True)
        res[(y,n)]=(name,im.width,im.height); print(y,n,im.size)
import json; json.dump({f'{k[0]}-{k[1]}':v for k,v in res.items()},open('/home/claude/work/zh/g3en_imgs.json','w'))
