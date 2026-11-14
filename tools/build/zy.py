"""把文字加上注音字型（ㄅ字嗨 Bpmf）的破音選字碼。{字}＝不顯示注音。"""
import re,collections,importlib.util
D='/home/claude/work/zh/mcb/Source/Data/'
VAR={};READ=collections.defaultdict(list);DEF={}
for ln in open(D+'bpmfvs-variants.txt',encoding='utf8'):
    if ln.startswith('#') or '-' not in ln: continue
    k,v=ln.rstrip('\n').split(' ',1); ch,rd=k.split('-',1)
    VAR[(ch,rd)]=v
    if rd!='na':
        READ[ch].append(rd)
        if v==ch: DEF[ch]=rd
PH=collections.defaultdict(list)
for ln in open(D+'BPMFMappings.txt',encoding='utf8'):
    p=ln.split()
    if len(p)>=3 and len(p[0])==len(p)-1 and len(p[0])>1: PH[p[0]].append(p[1:])
def best(word):
    c=PH.get(word)
    if not c: return None
    def bad(rs): return sum(1 for ch,r in zip(word,rs) if (ch=='一' and r!='ㄧ') or (ch=='不' and r!='ㄅㄨˋ'))
    return sorted(c,key=bad)[0]
def readings(text,over=None,force=None):
    """回傳 [(char, reading or None)]；over: {片語: [讀音…]} 人工指定（優先）；force: {字: 讀音} 其餘位置一律用這個讀音"""
    over=over or {}; force=force or {}
    n=len(text); out=[None]*n; fixed=[False]*n
    for w in sorted(over,key=len,reverse=True):
        st=0
        while True:
            i=text.find(w,st)
            if i<0: break
            if not any(fixed[i:i+len(w)]):
                for k,r in enumerate(over[w]): out[i+k]=(text[i+k],r); fixed[i+k]=True
            st=i+1
    i=0
    while i<n:
        if fixed[i]: i+=1; continue
        hit=None
        for L in range(min(6,n-i),1,-1):
            if any(fixed[i:i+L]): continue
            w=text[i:i+L]; b_=best(w)
            if b_ and all('\u4e00'<=c<='\u9fff' for c in w): hit=(w,b_);break
        if hit:
            for k,(ch,r) in enumerate(zip(*hit)): out[i+k]=(ch,force.get(ch,r))
            i+=len(hit[0])
        else:
            ch=text[i]; out[i]=(ch,force.get(ch,DEF.get(ch)) if ch in READ else None); i+=1
    return out
def annotate(text,over=None,report=None,force=None):
    parts=re.split(r'(\{[^{}]*\}|<[^>]+>)',text); res=''
    for p in parts:
        if not p: continue
        if p.startswith('<'): res+=p; continue
        if p.startswith('{'):
            res+=''.join(VAR.get((c,'na'),c) for c in p[1:-1]); continue
        rs=readings(p,over,force)
        for k,(ch,r) in enumerate(rs):
            if r is None or ch not in READ: res+=ch; continue
            v=VAR.get((ch,r))
            if v is None: v=ch; print('!! no variant',ch,r)
            res+=v
            if report is not None and len(READ[ch])>1:
                ctx=''.join(c for c,_ in rs[max(0,k-3):k+4]); report.append((ch,r,ctx))
    return res
