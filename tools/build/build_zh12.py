"""國語一、二年級（114 年，官方答案卷）：題目用原卷裁圖，接在 build_zh.py 之後執行。"""
import json,importlib.util
OUT='/home/claude/repo-xuefu/chinese/'
IM=json.load(open('/home/claude/work/zh/zh12_imgs.json'))
def load(g,y):
    s=importlib.util.spec_from_file_location(f'z{g}{y}',f'/home/claude/work/zh/src/g{g}_{y}.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def main():
    Q=json.load(open(OUT+'data/questions.json')); P=json.load(open(OUT+'data/passages.json'))
    Q=[q for q in Q if q['grade']>2]; P={k:v for k,v in P.items() if not k.startswith(('g1-','g2-'))}
    for g in (1,2):
      for y in ('114','113','112','111'):
        m=load(g,y); SELF=getattr(m,'SELF',False)
        a,b,text=m.PSG; pid=f'g{g}-{y}-p{a}'; key=(lambda k:f'{g}-{k}' if y=='114' else f'{g}-{y}-{k}'); pi=IM[key('psg')]
        P[pid]=dict(id=pid,a=a,b=b,intro=f'請閱讀以下故事，並回答 {a}～{b} 題：',text=text,img=pi[0],w=pi[1],h=pi[2])
        for n in range(1,26):
            nm,w,h=IM[key(n)]
            if n in m.FILL:
                tag,stem,ans,ex=m.FILL[n]
                zy=ans[0] in 'ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕㄖㄗㄘㄙㄧㄨㄩㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦ'
                if zy and ans[-1] not in 'ˊˇˋ˙': ans=ans+'|'+ans+'ˉ'
                q=dict(id=f'g{g}-{y}-{n}',grade=g,year=y,no=n,type='fill',stem=stem,blanks=[ans],options=None,answer=None,ex=ex)
            else:
                tag,stem,opts,ans,ex=m.Q[n]
                q=dict(id=f'g{g}-{y}-{n}',grade=g,year=y,no=n,type='choice',stem=stem,options=opts,answer=ans,ex=ex+[f"所以選 {'①②③'[ans-1]} {opts[ans-1]}"])
            q.update(img=nm,iw=w,ih=h,xf=[f'{tag[0]}-{g}-{tag[1:]}'])
            if SELF: q['ansSrc']='self'
            if a<=n<=b: q['psg']=pid
            Q.append(q)
    json.dump(Q,open(OUT+'data/questions.json','w'),ensure_ascii=False,indent=1)
    json.dump(P,open(OUT+'data/passages.json','w'),ensure_ascii=False,indent=1)
    C=json.load(open(OUT+'data/codes.json'))
    LAB={'A1':'字音','A2':'字形（國字）','A3':'部首','B1':'詞義','B2':'詞語運用','C1':'句意理解','C2':'段落重點','C3':'語句銜接與排序','C4':'刪除多餘語詞','C5':'標點符號','D1':'閱讀：故事','D2':'閱讀：說明文與圖表'}
    for g in (1,2):
        for k,v in LAB.items(): C['xuefu'][f'{k[0]}-{g}-{k[1:]}']={'label':v,'summary':''}
    json.dump(C,open(OUT+'data/codes.json','w'),ensure_ascii=False,indent=1)
    from collections import Counter; print(Counter((q['grade'],q['year']) for q in Q if q['grade']<=2))
if __name__=='__main__': main()
