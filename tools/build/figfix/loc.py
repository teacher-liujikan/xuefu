import pymupdf,cv2,numpy as np,json,os,re,sys
from PIL import Image
IMG='/home/claude/repo-xuefu/math/img/'; PAP='/home/claude/papers/'
_pages={}
def pages(g,y,k):
    key=(g,y,k)
    if key not in _pages:
        f=f'{PAP}g{g}-{y}-{k}.pdf'
        if not os.path.exists(f): _pages[key]=None
        else:
            d=pymupdf.open(f); out=[]
            for p in d:
                pm=p.get_pixmap(dpi=200,alpha=False); a=np.frombuffer(pm.samples,np.uint8).reshape(pm.height,pm.width,3)
                out.append(cv2.cvtColor(a,cv2.COLOR_RGB2GRAY))
            _pages[key]=out
    return _pages[key]
def locate(name):
    m=re.match(r'g(\d)-(\d{3})-(\d+)(.*)\.png',name)
    if not m: return None
    g,y,n,rest=m.groups(); k='a' if 'ans' in rest else 'q'
    ps=pages(g,y,k)
    if ps is None: return None
    t=cv2.cvtColor(np.array(Image.open(IMG+name).convert('RGB')),cv2.COLOR_RGB2GRAY)
    # 去掉 6px 白邊再比對
    tt=t[4:-4,4:-4] if min(t.shape)>20 else t
    best=None
    for pi,pg in enumerate(ps):
        if tt.shape[0]>=pg.shape[0] or tt.shape[1]>=pg.shape[1]: continue
        r=cv2.matchTemplate(pg,tt,cv2.TM_CCOEFF_NORMED); _,mx,_,ml=cv2.minMaxLoc(r)
        if best is None or mx>best[0]: best=(mx,pi,ml[0],ml[1],tt.shape[1],tt.shape[0])
    return dict(name=name,g=g,y=y,k=k,score=round(float(best[0]),3),pg=best[1],x=best[2],y0=best[3],w=best[4],h=best[5])
if __name__=='__main__':
    names=sorted(f for f in os.listdir(IMG) if re.match(r'g\d-1\d\d-',f) and f.endswith('.png'))
    out=[]
    for f in names:
        r=locate(f)
        if r: out.append(r)
    json.dump(out,open('loc.json','w'))
    bad=[r for r in out if r['score']<0.9]; print(len(out),'located; low score',len(bad))
    for r in bad: print(r['name'],r['score'])
