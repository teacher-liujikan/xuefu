def W(desc,ans,opts,gloss,extra=None):
    """辨識單字：desc=圖的描述, gloss={word:中文}"""
    o=opts[ans-1]; others='，'.join(f'{w} 是{gloss[w]}' for i,w in enumerate(opts) if i!=ans-1 and w in gloss)
    ex=[desc,f'{gloss.get(o,"")}是 {o}。'+(others+'。' if others else '')]
    if extra: ex.append(extra)
    return ex+[f"所以選 {'①②③'[ans-1]} {o}"]
def S(lines,ans,optlabel):
    return lines+[f"所以選 {'①②③'[ans-1]} {optlabel}"]
