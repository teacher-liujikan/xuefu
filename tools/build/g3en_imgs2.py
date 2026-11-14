import pymupdf,json
from PIL import Image
from build_zh import trim
OUT='/home/claude/repo-xuefu/english/img/'; SC=2.4
res=json.load(open('/home/claude/work/zh/g3en_imgs.json'))
def save(p,clip,name):
    pm=p.get_pixmap(matrix=pymupdf.Matrix(SC,SC),clip=clip,alpha=False)
    im=trim(Image.frombytes('RGB',(pm.width,pm.height),pm.samples))
    im.convert('L').quantize(16).save(OUT+name,optimize=True); print(name,im.size); return [name,im.width,im.height]
# 112：同 113 版面（右欄 22–25）
d=pymupdf.open('/home/claude/papers_en/g3-112-q.pdf'); p=d[1]; W=p.rect.width; mid=W/2; ws=p.get_text('words')
nums={int(w[4][:2]):w for w in ws if w[0]>mid and w[4] in ('22.','23.','24.','25.')}
labs=sorted([w for w in ws if w[0]>mid and w[4]=='(1)'],key=lambda w:w[1])
for n in (22,23,24,25):
    lab=[w for w in labs if w[1]>nums[n][1]][0]; top=lab[1]-3
    bot=(nums[n+1][1]-6) if n<25 else top+150
    res[f'112-{n}']=save(p,pymupdf.Rect(mid+18,top,W-30,bot),f'g3-112-{n}.png')
# 111：14、15 左欄，16 右欄最上方
d=pymupdf.open('/home/claude/papers_en/g3-111-q.pdf'); p=d[1]; W=p.rect.width; mid=W/2; ws=p.get_text('words')
def num(t,right): return [w for w in ws if w[4]==t and ((w[0]>mid)==right)][0]
L=sorted([w for w in ws if w[4]=='(1)'],key=lambda w:w[1])
n14,n15,n16=num('14.',False),num('15.',False),num('16.',True)
sec3=[w for w in ws if '三' in w[4] and w[0]>mid][0] if any('三' in w[4] and w[0]>mid for w in ws) else None
l14=[w for w in L if w[0]<mid and w[1]>n14[1]][0]; l15=[w for w in L if w[0]<mid and w[1]>n15[1]][0]; l16=[w for w in L if w[0]>mid and w[1]>n16[1]-5][0]
res['111-14']=save(p,pymupdf.Rect(40,l14[1]-3,mid-14,n15[1]-6),'g3-111-14.png')
res['111-15']=save(p,pymupdf.Rect(40,l15[1]-3,mid-14,l15[1]+120),'g3-111-15.png')
res['111-16']=save(p,pymupdf.Rect(mid+18,l16[1]-3,W-30,l16[1]+112),'g3-111-16.png')
json.dump(res,open('/home/claude/work/zh/g3en_imgs.json','w'))
