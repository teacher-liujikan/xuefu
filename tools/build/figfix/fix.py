import pymupdf,cv2,numpy as np,json,os,sys
from PIL import Image
from scipy import ndimage
from loc import pages,IMG,PAP
L=json.load(open('loc.json')); OUT='new/'; os.makedirs(OUT,exist_ok=True)
MAXG=170
FORCE_ERASE={'g2-115-18.png'}
FORCE_EXPAND={'g2-115-6-3.png','g2-115-6-o1.png'}
SKIP={'g6-115-23.png','g2-114-15-3.png','g2-112-19-4.png','g3-113-1-o1.png','g3-113-1-o2.png','g3-113-1-o3.png','g3-113-1-o4.png'}
_rgb={}
def rgbpage(g,y,k,pi):
    key=(g,y,k,pi)
    if key not in _rgb:
        p=pymupdf.open(f'{PAP}g{g}-{y}-{k}.pdf')[pi]; pm=p.get_pixmap(dpi=200,alpha=False)
        _rgb[key]=np.frombuffer(pm.samples,np.uint8).reshape(pm.height,pm.width,3)
    return _rgb[key]
_M={}
def analyse(r):
    pg=pages(r['g'],r['y'],r['k'])[r['pg']]; H,W=pg.shape
    ink=pg<175
    emask=np.zeros(pg.shape,bool)
    x0,y0,x1,y1=r['x']-4,r['y0']-4,r['x']+r['w']+4,r['y0']+r['h']+4
    x0=max(0,x0);y0=max(0,y0)
    ox=(x0,y0,x1,y1); erase=[]; changed=False; note=[]
    for it in range(12):
        sides={'T':ink[y0:y0+2,x0:x1],'B':ink[y1-2:y1,x0:x1],'L':ink[y0:y1,x0:x0+2],'R':ink[y0:y1,x1-2:x1]}
        hit=[s for s,a in sides.items() if a.any()]
        if not hit: break
        wx0,wy0,wx1,wy1=max(0,x0-MAXG),max(0,y0-MAXG),min(W,x1+MAXG),min(H,y1+MAXG)
        lab,n=ndimage.label(ink[wy0:wy1,wx0:wx1],structure=np.ones((3,3)))
        bx0,by0,bx1,by1=x0-wx0,y0-wy0,x1-wx0,y1-wy0
        edge=np.zeros(lab.shape,bool)
        if 'T' in hit: edge[by0:by0+2,bx0:bx1]=True
        if 'B' in hit: edge[by1-2:by1,bx0:bx1]=True
        if 'L' in hit: edge[by0:by1,bx0:bx0+2]=True
        if 'R' in hit: edge[by0:by1,bx1-2:bx1]=True
        ids=[i for i in np.unique(lab[edge]) if i]
        inside=np.zeros(lab.shape,bool); inside[by0:by1,bx0:bx1]=True
        progress=False
        for i in ids:
            m=lab==i; tot=m.sum(); inn=(m&inside).sum()
            ys,xs=np.where(m); cb=(xs.min()+wx0,ys.min()+wy0,xs.max()+1+wx0,ys.max()+1+wy0)
            touch_win=cb[0]<=wx0 or cb[1]<=wy0 or cb[2]>=wx1 or cb[3]>=wy1
            if (inn>=0.35*tot or r['name'] in FORCE_EXPAND) and not touch_win and r['name'] not in FORCE_ERASE:
                nx0,ny0,nx1,ny1=min(x0,cb[0]-6),min(y0,cb[1]-6),max(x1,cb[2]+6),max(y1,cb[3]+6)
                if (nx0,ny0,nx1,ny1)!=(x0,y0,x1,y1): x0,y0,x1,y1=max(0,nx0),max(0,ny0),min(W,nx1),min(H,ny1); progress=True; changed=True
            elif touch_win and inn>=0.35*tot: note.append('BIG')
            else:
                erase.append(cb); sub=m[cb[1]-wy0:cb[3]-wy0,cb[0]-wx0:cb[2]-wx0]; ink[cb[1]:cb[3],cb[0]:cb[2]][sub]=False; emask[cb[1]:cb[3],cb[0]:cb[2]][sub]=True; progress=True; changed=True
        if not progress: break
    _M[r['name']]=emask
    return dict(r,box=[int(v) for v in (x0,y0,x1,y1)],obox=[int(v) for v in ox],erase=[[int(v) for v in e] for e in erase],changed=changed,note=note)
def render(a):
    pg=rgbpage(a['g'],a['y'],a['k'],a['pg']).copy(); x0,y0,x1,y1=a['box']
    m=ndimage.binary_dilation(_M[a['name']],iterations=3); pg[m]=255
    im=Image.fromarray(pg[y0:y1,x0:x1])
    g=np.array(im.convert('L'))<235; ys,xs=np.where(g)
    if not len(xs): return None
    return im.crop((max(0,xs.min()-6),max(0,ys.min()-6),min(im.width,xs.max()+7),min(im.height,ys.max()+7)))
if __name__=='__main__':
    res=[]
    for r in L:
        if r['name'] in SKIP: continue
        if r['score']<0.6: print('skip low',r['name'],r['score']); continue
        a=analyse(r)
        if a['changed'] or a['note']:
            im=render(a)
            if im is None: print('BLANK',a['name']); continue
            old=Image.open(IMG+a['name'])
            if im.width<old.width*0.7 or im.height<old.height*0.7: print('SHRUNK',a['name'],old.size,im.size)
            im.save(OUT+a['name']); res.append(a)
    json.dump(res,open('fix.json','w'))
    print(len(res),'changed'); print([a['name'] for a in res if a['note']])
