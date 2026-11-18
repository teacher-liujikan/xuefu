# -*- coding: utf-8 -*-
"""Build review/<NN>/index.html for each 數與量 worksheet, plus review/index.html.
Run: python3 tools/build/review/build.py   (from the repo root)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data import W

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BASE = 'https://teacher-liujikan.github.io/xuefu/review/'
rd = lambda f: open(os.path.join(HERE, f), encoding='utf-8').read()
CSS, VERT, STEPS, ENGINE = rd('style.css'), rd('vert.js'), rd('steps.js'), rd('engine.js')

def page(no, title, code, S, Q):
    url = f'{BASE}{no}/'
    data = dict(KEY=f'xuefu-review-ws{no}-v1', URL=url, S=[dict(id=f's{i+1}', name=n) for i, n in enumerate(S)], Q=Q)
    return f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} 檢討</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Iansui&family=Huninn&family=Bpmf+Huninn&family=Noto+Sans+TC:wght@400;700&display=swap">
<style>body{{margin:0}}[hidden]{{display:none!important}}img{{max-width:100%}}
{CSS}</style></head><body>
<div class="wrap">
  <header class="top"><button type="button" class="qrthumb" id="qrOpen" aria-label="放大 QR code，讓學生用平板掃描"><span id="qrSmall"></span><small>學生掃我</small></button>
    <div class="school">學習扶助・二年級數學・學習單 {no}（{code}）</div>
    <h1>{title} 自己來檢討</h1>
    <p class="lead">拿出寫好的作答單，一關一關檢討。每題點「我寫對了」或「我寫錯了／不會」，就會看到正確答案；寫錯的題目看詳解，再在作答單上訂正。有寫錯的關卡先給老師批改，全部寫對的關卡可以直接往下做。三關都完成後，會出現錯題測驗。</p>
    <div class="tools">
      <button class="btn" id="bpmfBtn" type="button">注音：開</button>
      <span id="resetZone"><button class="btn" id="resetBtn" type="button">從頭開始</button></span>
    </div>
  </header>
  <nav class="steps" id="steps" aria-label="檢討進度"></nav>
  <main id="main"></main>
  <div class="qrmodal" id="qrModal" hidden><div class="qrcard" role="dialog" aria-modal="true" aria-labelledby="qrTitle"><h2 id="qrTitle">拿平板掃這裡，開始檢討</h2><div id="qrBig"></div><p class="qrurl" id="qrUrl"></p><button type="button" class="btn primary" id="qrClose">關閉</button></div></div>
  <footer>學習扶助・二年級數學・學習單 {no}　<a class="back" href="../">所有學習單</a><br>記錄只存在這台裝置的瀏覽器裡。</footer>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<script>
(function(){{
const DATA={json.dumps(data, ensure_ascii=False)};
{VERT}
{STEPS}
{ENGINE}
}})();
</script>
</body></html>
'''

def index(items):
    rows = ''.join(f'<a class="card" href="{no}/"><b>{no}</b><span>{t}</span><small>{c}・{n} 題</small></a>' for no, t, c, n in items)
    return f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>學習單檢討</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Iansui&family=Huninn&display=swap">
<style>
:root{{--paper:#f5f7fb;--card:#fff;--ink:#1d2742;--muted:#5a647a;--line:#cfd7e4;--pen:#2753c9}}
@media (prefers-color-scheme:dark){{:root{{--paper:#11161f;--card:#18202c;--ink:#e5e9f1;--muted:#9ba4b6;--line:#2e3849;--pen:#86a2ff}}}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Huninn","Noto Sans TC",sans-serif}}
.wrap{{max-width:760px;margin:0 auto;padding:24px 16px 60px}}
h1{{font-family:"Iansui","Huninn",sans-serif;font-weight:400;font-size:34px;margin:0 0 6px}}
p{{color:var(--muted);margin:0 0 18px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}}
.card{{display:flex;flex-direction:column;gap:2px;background:var(--card);border:1.5px solid var(--line);border-radius:12px;padding:12px 14px;text-decoration:none;color:var(--ink)}}
.card:hover{{border-color:var(--pen)}}
.card b{{color:var(--pen);font-size:20px}} .card small{{color:var(--muted)}}
</style></head><body><div class="wrap">
<h1>學習單 自己來檢討</h1>
<p>學習扶助・二年級數學・數與量。掃作答單右上角的 QR code，就會直接打開那一份。</p>
<div class="grid">{rows}</div></div></body></html>
'''

if __name__ == '__main__':
    out = os.path.join(ROOT, 'review'); items = []
    for no in sorted(W):
        title, code, S, Q = W[no]()
        d = os.path.join(out, no); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page(no, title, code, S, Q))
        items.append((no, title, code, len(Q)))
        print(no, title, len(Q), 'Q')
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(index(items))
