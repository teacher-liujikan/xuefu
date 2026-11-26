import json,sys
from PIL import Image, ImageDraw
SP='/tmp/claude-0/-home-claude/b964d65a-5edb-5fce-8e3b-206c85541d8d/scratchpad/'
def pairsheet(items,name,olddir,newdir,cw=280,per=14):
    cells=[]
    for n in items:
        ims=[]
        for d in (olddir,newdir):
            im=Image.open(d+n).convert('RGB'); s=min(1,(cw-14)/im.width,240/im.height); ims.append(im.resize((max(1,int(im.width*s)),max(1,int(im.height*s)))))
        h=max(i.height for i in ims)+24
        c=Image.new('RGB',(cw*2,h),'#f5c542'); ImageDraw.Draw(c).text((3,2),n[:-4],fill='black'); c.paste(ims[0],(6,18)); c.paste(ims[1],(cw+6,18)); cells.append(c)
    rows=[cells[i:i+2] for i in range(0,len(cells),2)]
    H=sum(max(c.height for c in r) for r in rows); C=Image.new('RGB',(cw*4,H),'#f5c542'); y=0
    for r in rows:
        x=0
        for c in r: C.paste(c,(x,y)); x+=cw*2
        y+=max(c.height for c in r)
    C.save(SP+name); print(name,C.size)
if __name__=='__main__':
    res=[a['name'] for a in json.load(open('fix.json'))]
    for i in range(0,len(res),16): pairsheet(res[i:i+16],f'pair{i//16}.png','/home/claude/repo-xuefu/math/img/','new/')
