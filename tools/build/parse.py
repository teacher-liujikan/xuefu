import re, json, sys, pymupdf, os
from ext import load
QRE=re.compile(r'^(\d ?\d?)\s?\.\s*(.*)$')
PRE=re.compile(r'請閱讀.*回答\s*(\d+)\s*[〜~～\-－至到]\s*(\d+)\s*題')
def mk(real):
    """chars -> marked text"""
    s='';st=None
    def close():
        nonlocal s,st
        if st=='u': s+='</u>'
        elif st=='b': s+='</b>'
        elif st=='z': s+='}'
        st=None
    prev=None
    for c in real:
        if c['c']==' ':
            continue
        want='z' if c['k']=='Z' else ('b' if (c['u']>=2 or c.get('bi')) else ('u' if c['u']==1 else None))
        gap = prev is not None and c['x0']-prev['x1']>c['sz']*0.45
        if want!=st or (gap and st in('u','b')):
            close()
            if gap: s+=' '
            if want=='u': s+='<u>'
            elif want=='b': s+='<b>'
            elif want=='z': s+='{'
            st=want
        elif gap: s+=' '
        s+=c['c']; prev=c
    close()
    return s
def parse(name):
    d,ls=load(name)
    W=d[0].rect.width; mid=W/2
    ls=[L for L in ls]
    ls.sort(key=lambda L:(L['pg'],L['col'],L['yc']))
    # column right edges
    edge={}
    for L in ls:
        if '評量測驗' in L['txt'] or re.search(r'第\s*\d+\s*頁',L['txt']): L['skip']=1; continue
        k=(L['pg'],L['col']); edge[k]=max(edge.get(k,0),L['x1'])
    blocks=[]; cur=None; nextq=1; started=False
    hy=[L['yc'] for L in ls if L['pg']==0 and '單題' in L['txt']]
    hy=hy[0] if hy else 0
    for L in ls:
        if L.get('skip'): continue
        if L['pg']==0 and L['yc']<hy-2: continue
        t=L['txt']
        real=L['real']
        if not started:
            if '單題' in t: started=True
            continue
        if re.match(r'^[（(]\s*\d+\s*[〜~～]',t) or re.match(r'^[一二三]、',t): 
            continue
        ans=None; body=real; tt=t
        m=None
        # answer digit (colored) glued before number
        m=QRE.match(tt.strip())
        isred=lambda c:(c['col']>>16)>150 and ((c['col']>>8)&255)<110
        if real[0]['c'] in '1234' and isred(real[0]):
            ans=int(real[0]['c']); body=real[1:]; tt=''.join(c['c'] for c in body)
            m=QRE.match(tt.strip())
        colx=0 if L['col']==0 else mid
        if m and int(m.group(1).replace(' ',''))==nextq and L['x0']-colx<115:
            # strip number chars from body
            k=0; seen=''
            bb=[c for c in body if c['c']!=' ']
            while not seen.endswith('.'): seen+=bb[k]['c']; k+=1
            cur=dict(kind='q',no=nextq,ans=ans,nx=bb[0]['x0'],sx=(bb[k]['x0'] if k<len(bb) else bb[k-1]['x1']+4),ny=(min(c['y0'] for c in bb[:k]),max(c['y1'] for c in bb[:k])),lines=[dict(L=L,chars=bb[k:])]); blocks.append(cur); nextq+=1
            continue
        pm=PRE.search(t)
        if pm:
            cur=dict(kind='p',a=int(pm.group(1)),b=int(pm.group(2)),intro=t,lines=[],L0=L); blocks.append(cur); continue
        if cur is None: continue
        cur['lines'].append(dict(L=L,chars=[c for c in real if c['c']!=' ']))
    foot={}
    for L in ls:
        if L.get('skip'): foot[L['pg']]=min(foot.get(L['pg'],1e9),L['y0'])
    out=[]
    for bi,b in enumerate(blocks):
        Ls=[x['L'] for x in b['lines']]
        if b['kind']=='p': Ls=[b['L0']]+Ls
        # crop rects grouped by (pg,col)
        rects={}
        for L in Ls:
            k=(L['pg'],L['col']); r=rects.get(k)
            y0,y1=L['y0'],L['y1']
            rects[k]=[min(r[0],y0),max(r[1],y1)] if r else [y0,y1]
        b['rects']=[dict(pg=k[0],col=k[1],y0=v[0],y1=v[1]) for k,v in sorted(rects.items())]
        last=b['rects'][-1]; nb=blocks[bi+1] if bi+1<len(blocks) else None
        ny=None
        if nb:
            nL=(nb['L0'] if nb['kind']=='p' else nb['lines'][0]['L'])
            if nL['pg']==last['pg'] and nL['col']==last['col'] and nL['y0']>last['y1']: ny=nL['y0']-9
        if ny is None: ny=min(foot.get(last['pg'],1e9),d[last['pg']].rect.height-50)-10
        b['ynext']=max(ny,last['y1'])
        if b['kind']=='q':
            stem=[];opts={};curo=None
            for x in b['lines']:
                L=x['L']; s=mk(x['chars'])
                wrap = L['x1']>edge[(L['pg'],L['col'])]-22 and not re.search(r'[？。！：」]$',L['txt'])
                parts=re.split(r'\(([1-4])\)\s*',s)
                if len(parts)>1 and parts[0].strip()=='' :
                    for i in range(1,len(parts),2):
                        curo=int(parts[i]); opts[curo]=parts[i+1].strip()
                    x['wrap']=wrap
                elif curo:
                    opts[curo]+=s
                else:
                    stem.append((s,wrap))
            txt=''
            for i,(s,w) in enumerate(stem):
                txt+=s
                if i<len(stem)-1: txt+= '' if w else '\n'
            out.append(dict(kind='q',no=b['no'],ans=b['ans'],nx=b['nx'],sx=b['sx'],ny=b['ny'],ynext=b['ynext'],stem=txt,options=[opts.get(i,'') for i in (1,2,3,4)],rects=b['rects']))
        else:
            txt=''
            x0s=[x['L']['x0']-(0 if x['L']['col']==0 else mid) for x in b['lines']]
            base=min(x0s) if x0s else 0
            pedge={}
            for x in b['lines']:
                k=(x['L']['pg'],x['L']['col']); pedge[k]=max(pedge.get(k,0),x['L']['x1'])
            for i,x in enumerate(b['lines']):
                L=x['L']; s=mk(x['chars'])
                ind=(x0s[i]-base)>12
                if i>0: 
                    prevL=b['lines'][i-1]['L']
                    pw=prevL['x1']>pedge[(prevL['pg'],prevL['col'])]-22
                    txt+= '' if (pw and not ind) else '\n'
                txt+=s
            out.append(dict(kind='p',a=b['a'],b=b['b'],intro=b['intro'],text=txt,rects=b['rects'],nimg=0))
    return d,out
if __name__=='__main__':
    name=sys.argv[1]
    d,out=parse(name)
    for o in out:
        if o['kind']=='q':
            print(f"Q{o['no']} [{o['ans']}] {o['stem']}")
            for i,x in enumerate(o['options']): print(f"   ({i+1}) {x}")
        else:
            print(f"--- PASSAGE {o['a']}-{o['b']} ---\n{o['text']}\n---")
