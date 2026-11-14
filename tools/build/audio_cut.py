import json,re,subprocess,sys,os
CN={'零':0,'一':1,'二':2,'兩':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}
def cnum(s):
    s=s.strip()
    if s.isdigit(): return int(s)
    if not s or any(c not in CN for c in s): return None
    if '十' in s:
        a,_,b=s.partition('十'); return (CN[a] if a else 1)*10+(CN[b] if b else 0)
    return CN[s[0]] if len(s)==1 else None
cjk=lambda t:bool(re.search(r'[一-鿿]',t))
def items(segs):
    """回傳 [(題號, 開始, 結束, [內容])]"""
    out=[]
    for i,s in enumerate(segs):
        m=re.search(r'第\s*([0-9零一二兩三四五六七八九十]+)\s*[題题體体期提其]',s['t'])
        if not m or len(re.sub(r'[\s。，,.!！?？]','',s['t']))>8: continue
        n=cnum(m.group(1))
        if n is None: continue
        j=i+1; body=[]
        isann=lambda t:bool(re.search(r'第\s*[0-9零一二兩三四五六七八九十]+\s*[題题體体期提其]',t)) and len(re.sub(r'[\s。，,.!！?？]','',t))<=8
        while j<len(segs) and not isann(segs[j]['t']) and not (cjk(segs[j]['t']) and len(re.sub(r'[^\u4e00-\u9fff]','',segs[j]['t']))>=3): body.append(segs[j]['t']); j+=1
        end=segs[j]['a'] if j<len(segs) else segs[-1]['b']+1
        out.append((n,s['a'],end,body))
    return out
def cut(src,a,b,dst):
    tmp=dst+'.tmp.mp3'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{max(0,a-0.25):.2f}','-to',f'{b-0.2:.2f}','-i',src,'-ac','1','-ar','22050','-b:a','40k','-af','afade=t=out:st=%.2f:d=0.25'%max(0,b-a-0.5),tmp],check=True)
    os.replace(tmp,dst)
if __name__=='__main__':
    for it in items(json.load(open(sys.argv[1]))): print(it[0],round(it[1],1),round(it[2],1),it[3])
