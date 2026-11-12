import re,sys
src=open('/home/claude/repo-xuefu/math/index.html').read()
s=src
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c<n or (n==1 and c!=1): print('!! count',c,'for',a[:70]); 
    s=s.replace(a,b)
def rex(pat,b,flags=0):
    global s
    s2,c=re.subn(pat,lambda m:b,s,flags=flags)
    if c!=1: print('!! regex count',c,pat[:60])
    s=s2
rep('學習扶助篩選測驗數學考古題：依年度整卷線上作答，或由老師依版本單元、學扶細目挑題；','學習扶助篩選測驗國語考古題：依年度整卷線上作答，或由老師依題型挑題；')
rep('</a>・數學</div>','</a>・國語</div>')
rep('<script src="viz.js?v=7"></script>\n','')
s=s.replace('數學　共','國語　共')
rep("const YEARS=['115','114','113','112','111','mA'];","const YEARS=['114','113','112','111'];")
rep("const NS='xuefu-kaoti:';","const NS='xuefu-zh:';")
rep("const GROUPS=[['NC','數與量'],['SC','空間與形狀'],['RC','關係'],['DC','資料與不確定性']];","const GROUPS=[['A','字音字形'],['B','詞語'],['C','句子與標點'],['D','閱讀理解']];")
rep("let PK=Object.assign({mode:'unit',","let PK=Object.assign({mode:'code',")
rep("delete PK.noPaper;","delete PK.noPaper;PK.mode='code';")
# rich text
n=s.count('fracify(esc(')
s=s.replace('fracify(esc(','rich((')
print('rich replaced',n)
rep("const WARN=/^小心[：:]\\s*/;","const rich=s=>esc(s).replace(/&lt;(\\/?[ub])&gt;/g,'<$1>');\nconst plain=s=>String(s==null?'':s).replace(/<\\/?[ub]>/g,'');\nconst WARN=/^小心[：:]\\s*/;")
rep("const exText=s=>rich((s)).replace(/\\n/g,'<br>');","const exText=s=>rich(s).replace(/\\{([^{}]+)\\}/g,'<span class=\"nz\">$1</span>').replace(/\\n/g,'<br>');")
# explanation: static, everything shown
rep("const lis=L.map((s,k)=>{const hid=k>0?' hidden':'';","const lis=L.map((s,k)=>{const hid='';")
rex(r"const ctl=L\.length>1\?`<div class=\"exctl\">.*?:'';","const ctl='';")
rep('<div class="exbox" data-n="${L.length}" data-shown="1"','<div class="exbox${q.grade===3?\' bp\':\'\'}" data-n="${L.length}" data-shown="${L.length}"')
# stem with image
rep("function stemHTML(q,mode,num){\n","function stemHTML(q,mode,num){\n  if(q.img)return {html:qimgTag(q),rest:[]};\n")
rep("const BL='（　）';","const BL='（　）';\nconst qimgTag=q=>`<img class=\"qimg\" src=\"${esc(q.img)}\" width=\"${q.iw}\" height=\"${q.ih}\" style=\"max-width:min(100%,${Math.round(q.iw/1.55)}px)\" alt=\"${esc(plain(q.stem)+' '+(q.options||[]).map((t,j)=>'('+(j+1)+')'+plain(t)).join(' '))}\" decoding=\"async\">`;\n/* 題組文章：同一篇文章連續出現時，只在第一題前面放一次（作答時一次一題，每題都放） */\nfunction psgHTML(q,prev,always){\n  const p=q.psg&&PSG[q.psg];if(!p)return '';\n  if(!always&&prev&&prev.psg===q.psg)return '';\n  const pic=!!p.img;\n  const body=pic?`<img class=\"pimg\" src=\"${esc(p.img)}\" width=\"${p.w}\" height=\"${p.h}\" style=\"max-width:min(100%,${Math.round(p.w/1.55)}px)\" alt=\"${esc(plain(p.text))}\" decoding=\"async\">`:p.text.split('\\n').map(t=>`<p>${rich(t)}</p>`).join('');\n  return `<div class=\"psg${pic?' pic':''}\"><p class=\"psgi\">📖 請先閱讀下面的${/圖文/.test(p.intro)?'圖文':'文章'}，再回答問題：</p>${body}</div>`;\n}")
# options: number-only when the picture already has the options
rep("  const dis=isPaper(q)?'disabled':'';\n","  const dis=isPaper(q)?'disabled':'';\n  if(q.img)return `<div class=\"opts numonly\" role=\"radiogroup\" aria-label=\"第 ${num} 題的選項\">${texts.map((t,j)=>`<button type=\"button\" class=\"opt\" role=\"radio\" aria-checked=\"false\" data-c=\"${j+1}\" aria-label=\"選項 ${j+1}：${esc(plain(t))}\"><span class=\"k\">${j+1}</span></button>`).join('')}</div>`;\n")
# card with passage
rep("  let L=`<div class=\"stem\"><span class=\"qn\">${num}.</span>${st.html}</div>${figsHTML(st.rest)}`,R='';\n  if(q.type==='choice')R+=optsHTML(q,num);",
    "  const pg=psgHTML(q,k>0?SET.qs[k-1]:null,one);\n  const stemBox=`<div class=\"stem${q.img?' hasimg':''}\"><span class=\"qn\">${num}.</span>${st.html}</div>${figsHTML(st.rest)}`;\n  let L=one&&pg?pg:pg+stemBox,R=one&&pg?stemBox:'';\n  if(q.type==='choice')R+=optsHTML(q,num);")
# print sheet
rep("    const st=stemHTML(q,'print');\n    let opts='';\n    if(q.type==='choice'){","    const st=stemHTML(q,'print');\n    let opts='';const pg=psgHTML(q,k>0?qs[k-1]:null,false);\n    if(q.type==='choice'&&!q.img){")
rep("return `<div class=\"pq\"><p class=\"pstem\">","return `${pg}<div class=\"pq\"><p class=\"pstem\">")
# word export
rep("    const {seq,rest}=figPlan(q);\n    const out=[];let cur=[T((k+1)+'. ',{bold:true})];",
    "    const P0=q.psg&&PSG[q.psg]&&!(k>0&&qs[k-1].psg===q.psg)?PSG[q.psg]:null;\n    if(P0){children.push(para([T(`請先閱讀下面的${/圖文/.test(P0.intro)?'圖文':'文章'}，再回答問題：`,{bold:true})],{spacing:{before:120,after:80}}));\n      if(P0.img)children.push(new D.Paragraph({alignment:D.AlignmentType.CENTER,spacing:{after:120},children:[await IMG(P0.img,Math.min(MAXW,Math.round(P0.w/1.7)))]}));\n      else P0.text.split('\\n').forEach(t=>children.push(para(RUNS('　　'+t),{spacing:{after:40,line:380},border:undefined})));\n      children.push(new D.Paragraph({spacing:{after:80},children:[]}))}\n    const {seq,rest}=q.img?{seq:[],rest:[]}:figPlan(q);\n    const out=[];let cur=[T((k+1)+'. ',{bold:true})];\n    if(q.img){cur.push(T(`（${srcOf(q,mixed)}）`,{size:20,color:'777777'}));out.push(para(cur));cur=[];out.push(new D.Paragraph({indent:{left:240},spacing:{after:60},children:[await IMG(q.img,Math.min(MAXW-20,Math.round(q.iw/1.7)))]}))}")
rep("lines.forEach((ln,i)=>{if(i>0)flush();if(ln)cur.push(T(ln))});","lines.forEach((ln,i)=>{if(i>0)flush();if(ln)RUNS(ln).forEach(r=>cur.push(r))});")
rep("    cur.push(src);flush();","    if(!q.img){cur.push(src);flush()}")
rep("    if(q.type==='choice'){\n      const im=q.optImgs||[];const ts=q.options||[];","    if(q.type==='choice'&&!q.img){\n      const im=q.optImgs||[];const ts=(q.options||[]).map(plain);")
rep("  const isSmall=async src=>","  const RUNS=(text,x)=>String(text).split(/(<u>.*?<\\/u>|<b>.*?<\\/b>)/).filter(Boolean).map(t=>/^<u>/.test(t)?T(plain(t),Object.assign({underline:{}},x||{})):/^<b>/.test(t)?T(plain(t),Object.assign({bold:true,underline:{type:'double'}},x||{})):T(t,x));\n  const isSmall=async src=>")
rep("const runs=[T(`${k+1}. `,{bold:true}),T(ansText(q))];","const runs=[T(`${k+1}. `,{bold:true}),T(plain(ansText(q)))];")
rep("[T(`(${++sn}) `+s,{size:22})]","[T(`(${++sn}) `+plain(s).replace(/[{}]/g,''),{size:22})]")
# picker
rep("${[['unit','📚 依版本單元'],['code','🧩 依學扶細目']].map(","${[['code','🧩 依題型挑題']].map(")
rep("一併列出前一年級的${PK.mode==='unit'?'單元':'細目'}（先備概念）","一併列出前一年級的題目")
rep("依課本單元或學扶細目挑題，做成紙本練習卷","依題型挑題，做成紙本練習卷")
rep("依課本單元或學扶細目挑題，產生練習給學生掃 QR code","依題型挑題，產生練習給學生掃 QR code")
rep("還沒有選到題目，請先勾選單元或細目","還沒有選到題目，請先勾選題型")
rex(r"單元對照依各版本課程整理，各校進度可能不同，請以實際教學為準。","題型是依題目內容自行分類，方便老師挑題，不是官方的學扶細目。")
rep("`<span class=\"cd\">${c}</span>${esc(XF[c].label)}`","esc(XF[c].label)")
rep("${CN[g]}年級的細目${g<GRADE?'（先備）':''}","${CN[g]}年級${g<GRADE?'（前一年級）':''}")
rep("<b>${name}（${k}）</b>","<b>${name}</b>")
# loader
rep("Promise.all(['questions','units','codes'].map(","Promise.all(['questions','passages','codes'].map(")
rep("  UNITS=u;\n","  UNITS={};PSG=u;\n")
rep("let QS=[],BY={},UNITS={},XF={},DUP={};","let QS=[],BY={},UNITS={},XF={},DUP={},PSG={};")
rep("o.xf=[...new Set((o.xuefu||[]).map(normCode))]","o.xf=o.xf||[]")
rep("  if(!UNITS[PK.ver])PK.ver=Object.keys(UNITS)[0];\n","")
# tabs: only grades that have questions
rep("t.innerHTML=[1,2,3,4,5,6].map(","t.innerHTML=[1,2,3,4,5,6].filter(g=>QS.some(q=>q.grade===g)).map(")
rep("function bpmfOn(g){return g in pref.bpmf?!!pref.bpmf[g]:g<=2}","function bpmfOn(g){return false}")
rep('var P=["/xuefu/","/xuefu/math/"]','var P=["/xuefu/","/xuefu/math/","/xuefu/chinese/"]')
rep("<p>115 年三～六年級官方未公布答案，答案為自行解題，如有疑義請以官方為準。</p>","<p>113、114 年用官方答案卷；111、112 年沒有取得官方答案卷，答案為自行解題（題目旁會標「非官方答案」），如有疑義請以官方為準。</p>")
rep("<p>「模擬卷」是照考古題的命題架構自編的題目，不是官方試題。</p>","<p>三年級題目有注音，直接用原卷的樣子呈現；一、二年級是紙筆手寫卷，目前還沒有放。</p>")
rep("const body=pic?","const ttl=p.title?`<p class=\"psgt\">${esc(p.title)}</p>`:'';\n  const body=ttl+(pic?")
rep(".join('');\n  return `<div class=\"psg${pic?' pic':''}\">",".join(''));\n  return `<div class=\"psg${pic?' pic':''}\">")
css='''
/* ---- 國語 ---- */
#padBtn,[data-bpmf],.tools{display:none!important}
.stem u,.opt u,.psg u,.pstem u,.popts u,.pans u{text-decoration:underline;text-underline-offset:.22em;text-decoration-thickness:1.5px}
.stem b,.psg b,.pstem b{font-weight:700;text-decoration:underline double;text-underline-offset:.2em}
.psg b{text-decoration:none}
.qimg,.pimg{display:block;height:auto;background:#fff;border-radius:8px;padding:6px;box-sizing:border-box;max-width:100%}
.stem.hasimg{display:flex;gap:4px;align-items:flex-start}
.stem.hasimg>.qn{white-space:nowrap;padding-top:6px}
.stem.hasimg .qimg{min-width:0;flex:0 1 auto}
.stem.hasimg .qimg{flex:0 1 auto;min-width:0}
.psg{border:1.5px solid var(--line);border-radius:12px;background:var(--card);padding:10px 14px;margin:0 0 12px;line-height:1.95}
.psg p{margin:0 0 .35em;text-indent:2em}
.psg p.psgi{text-indent:0;font-weight:700;color:var(--main);font-size:.92em;margin-bottom:.5em}
.psg.pic{padding:8px}
.psg p.psgt{text-indent:0;text-align:center;font-weight:700;font-size:1.05em}
.opts.numonly{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.opts.numonly .opt{justify-content:center;min-height:64px}
.opts.numonly .opt .k{display:inline-grid;place-items:center;line-height:1;padding:0}
.exbox.bp{font-family:"Bpmf Huninn","Huninn","Noto Sans TC",sans-serif;line-height:2.3}
.exbox .nz,.exbox.bp .nz{font-family:"Huninn","Noto Sans TC",sans-serif}
.psheet .psg{border:1px solid #000;border-radius:0;background:#fff;color:#000;break-inside:avoid-page;margin:10px 0}
.psheet .qimg,.psheet .pimg{padding:0}
'''
rep("</style>\n</head>",css+"</style>\n</head>")
n=s.count('String(t).length<=8'); s=s.replace('String(t).length<=8','plain(String(t)).length<=4'); print('short',n)
open('index.html','w').write(s)
print('done',len(s))
