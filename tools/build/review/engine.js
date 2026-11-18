/* ---------- helpers ---------- */
const $=s=>document.querySelector(s);
const norm=s=>String(s??'').replace(/[０-９]/g,c=>String.fromCharCode(c.charCodeAt(0)-65248))
  .replace(/>/g,'＞').replace(/</g,'＜').replace(/=/g,'＝').replace(/\+/g,'＋').replace(/-/g,'－').replace(/[*xX]/g,'×')
  .replace(/[,，、\s]/g,'').trim();
const okAns=(v,a)=>String(a).split('||').some(x=>norm(v)===norm(x));
const showAns=a=>String(a).split('||').join(' 或 ');
const {KEY,URL,S,Q}=DATA;
let state={bpmf:true};
try{const s=JSON.parse(localStorage.getItem(KEY)||'null'); if(s) state=Object.assign(state,s);}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){}};
Q.forEach((q,i)=>q.id='q'+i);

/* ex tokens: {{add:a|b|unit}} {{sub:a|b|unit}} {{mul:a|b}} {{vert:a|op|b|r}} */
function expand(h){
  return String(h||'').replace(/\{\{(\w+):([^}]*)\}\}/g,(m,k,arg)=>{
    const a=arg.split('|');
    if(k==='add') return calcStepper(addSteps(+a[0],+a[1],a[2]||''));
    if(k==='sub') return calcStepper(subSteps(+a[0],+a[1],a[2]||''));
    if(k==='mul') return calcStepper(mulSteps(+a[0],+a[1]));
    if(k==='vert') return vert(a[0],a[1],a[2],a[3]);
    return m;
  });
}
Q.forEach(q=>{q.exHTML=null});
const exOf=q=>q.exHTML||(q.exHTML=expand(q.ex));

/* ---------- state ---------- */
function blankState(){return {mark:{},sec:{},cur:0,view:'review',v:{},test:{round:1,ids:null,done:false,res:{}},bpmf:state.bpmf}}
if(!state.mark){state=Object.assign(blankState(),{bpmf:state.bpmf!==false})}
const secQs=sid=>Q.filter(q=>q.s===sid);
const byId=id=>Q.find(q=>q.id===id);
const allDone=()=>S.every(s=>state.sec[s.id]==='done');
const short=s=>s.name.split('、')[0];
const long=s=>s.name.split('、')[1]||s.name;

/* ---------- review rendering (answers shown in red after marking) ---------- */
function slots(src,q,start,show){
  let i=start;
  const html=src.replace(/\[\[(.*?)\]\]/g,(m,spec)=>{const idx=i++;const a=show?showAns(q.ans[idx]):'';return `<span class="slot${spec.startsWith('s:')?' txt':''}">${a}</span>`});
  return {html,next:i};
}
const figHTML=q=>q.fig?`<div class="figbox">${q.fig}</div>`:'';
function reviewBody(q,show){
  if(q.type==='choice'){
    return `<p class="stem"><span class="qn">${q.n}</span>${q.stem}</p>${figHTML(q)}<div class="opts">${q.opts.map((o,i)=>`<div class="opt ro${show&&i===q.ans?' ansopt':''}"><span class="k">${i+1}</span><span>${o}</span></div>`).join('')}</div>${show?`<p class="ansline">正確答案：<b>${q.opts[q.ans]}</b></p>`:''}`;
  }
  if(q.type==='fill'){
    const a=slots(q.stem,q,0,show);
    return `<p class="stem"><span class="qn">${q.n}</span>${q.ask||''}</p>${figHTML(q)}<div class="stem">${a.html}</div>`;
  }
  if(q.type==='word') return `<p class="stem"><span class="qn">${q.n}</span>${q.stem}</p>${figHTML(q)}<p class="ansline">算式：<span class="slot wide">${show?q.f:''}</span>　答：<span class="slot">${show?q.ans:''}</span> ${q.unit}</p>`;
  if(q.type==='word2') return `<p class="stem"><span class="qn">${q.n}</span>${q.stem}</p>${figHTML(q)}<p class="ansline">先算：<span class="slot wide">${show?q.f1:''}</span></p><p class="ansline">再算：<span class="slot wide">${show?q.f2:''}</span></p><p class="ansline">答：<span class="slot">${show?q.ans:''}</span> ${q.unit}</p>`;
  if(q.type==='open') return `<p class="stem"><span class="qn">${q.n}</span>${q.stem}<span class="opentag">自己畫／自己說</span></p>${figHTML(q)}${show?`<div class="ansbox">參考答案：<b>${q.ansText}</b></div>`:''}`;
}
function reviewCard(q,locked){
  const m=state.mark[q.id];
  return `<article class="q${m?' marked '+m:''}" id="${q.id}">
    <span class="mark" aria-hidden="true">${m==='right'?'○':m==='wrong'?'✗':''}</span>
    ${reviewBody(q,!!m)}
    ${locked?'':`<div class="selfmark" role="group" aria-label="這題你寫對還是寫錯">
      <span class="ask">作答單上這題：</span>
      <button type="button" class="mk ok${m==='right'?' on':''}" data-mark="right" data-q="${q.id}" aria-pressed="${m==='right'}">○ 我寫對了</button>
      <button type="button" class="mk no${m==='wrong'?' on':''}" data-mark="wrong" data-q="${q.id}" aria-pressed="${m==='wrong'}">✗ 我寫錯了／不會</button>
    </div>`}
    ${m?`<details class="explain"${m==='wrong'?' open':''}><summary>${m==='wrong'?'詳解（看懂後在作答單上訂正）':'看說明'}</summary><p><b>提示：</b>${q.hint}</p>${exOf(q)}</details>`:''}
  </article>`;
}

/* ---------- stepper ---------- */
function firstOpen(){const i=S.findIndex(s=>state.sec[s.id]!=='done');return i<0?S.length:i}
function stepper(){
  const items=S.map((s,i)=>{const st=state.sec[s.id];const qs=secQs(s.id);const marked=qs.filter(q=>state.mark[q.id]).length;
    const isCur=state.view==='review'&&state.cur===i;
    const reach=st==='done'||i<=firstOpen();
    return `<button type="button" class="step${st==='done'?' done':''}${isCur?' cur':''}" data-step="${i}" ${reach?'':'disabled'} aria-current="${isCur}"><b>${short(s)}</b><small>${st==='done'?'✔ 完成':st==='teacher'?'等老師':marked+'/'+qs.length}</small></button>`}).join('');
  const t=`<button type="button" class="step test${state.view!=='review'?' cur':''}" data-step="test" ${allDone()?'':'disabled'}><b>錯題測驗</b><small>${allDone()?(state.test.done&&!pendingIds().length?'✔ 完成':'可以做了'):'最後解鎖'}</small></button>`;
  $('#steps').innerHTML=items+t;
}

/* ---------- views ---------- */
const doneLabel=(left,wrong)=>(!left&&!wrong)?'全部寫對！直接做下一關 →':'這一關檢討好了';
const leftText=(left,wrong)=>left?`還有 <b>${left}</b> 題還沒點喔。`:wrong?`有 ${wrong} 題寫錯，都在作答單上訂正好了嗎？`:'這一關全部寫對，太棒了！不用給老師批改，可以直接做下一關。';
function renderReview(){
  const s=S[state.cur];const st=state.sec[s.id];const qs=secQs(s.id);
  const locked=st==='done';
  if(st==='teacher'){
    $('#main').innerHTML=`<section class="teacher" aria-live="polite">
      <div class="stamp">${short(s).replace('第','').replace('關','')}</div>
      <h2>${short(s)} 檢討好了！</h2>
      <p class="big">請把作答單拿給老師，<br>先批改這一關。</p>
      <p class="muted">老師看過以後，請老師按住下面的按鈕。</p>
      <button type="button" class="hold" id="holdBtn"><span class="fill"></span><span class="lbl">老師確認：按住 2 秒</span></button>
      <button type="button" class="btn" id="backBtn">回去再看一下</button>
    </section>`;
    bindHold(s);return;
  }
  const left=qs.filter(q=>!state.mark[q.id]).length;
  const wrong=qs.filter(q=>state.mark[q.id]==='wrong').length;
  $('#main').innerHTML=`<section class="sec">
    <div class="sec-h"><h2>${short(s)}</h2><small>${long(s)}・共 ${qs.length} 題</small></div>
    ${locked?'<p class="muted">這一關已經檢討完成，老師也確認過了。</p>':`<p class="muted">對照作答單，每一題點「我寫對了」或「我寫錯了／不會」。點了以後會出現正確答案；寫錯的題目會打開詳解，看懂後在作答單上訂正。</p><div class="allright"><button type="button" class="mk ok big2" id="allRight">○ 這一關我全部寫對了</button><span class="muted">按了以後，每一題都會標成寫對，並顯示正確答案讓你再對一次。</span></div>`}
    <div class="cards">${qs.map(q=>reviewCard(q,locked)).join('')}</div>
    ${locked?`<div class="finish"><button type="button" class="btn primary" data-goto="${firstOpen()<S.length?firstOpen():'test'}">${firstOpen()<S.length?'到現在要檢討的關卡':'去做錯題測驗'}</button></div>`
    :`<div class="finish"><p id="leftMsg">${leftText(left,wrong)}</p><button type="button" class="btn primary big" id="secDone" ${left?'disabled':''}>${doneLabel(left,wrong)}</button></div>`}
  </section>`;
}
function pendingIds(){
  if(state.test.ids) return state.test.ids;
  return Q.filter(q=>state.mark[q.id]==='wrong'&&q.type!=='open').map(q=>q.id);
}
function renderTest(){
  const ids=pendingIds();
  if(!ids.length){
    const anyOpen=Q.some(q=>q.type==='open'&&state.mark[q.id]==='wrong');
    $('#main').innerHTML=`<section class="teacher"><div class="stamp">○</div><h2>${state.test.round>1?'錯題全部都會了！':'沒有要測驗的錯題！'}</h2><p class="big">${state.test.round>1?'你把寫錯的題目都學會了，<br>給自己拍拍手！':'給自己拍拍手！'}</p>${anyOpen?'<p class="muted">要自己畫或自己說的題目不會出在測驗裡，請拿作答單給老師看。</p>':''}<p class="muted">可以把結果給老師看。</p></section>`;
    return;
  }
  const done=state.test.done,res=state.test.res;
  const right=done?ids.filter(id=>res[id]).length:0;
  $('#main').innerHTML=`<section class="sec">
    <div class="sec-h"><h2>錯題測驗${state.test.round>1?` 第 ${state.test.round} 次`:''}</h2><small>共 ${ids.length} 題</small></div>
    ${done?`<div class="result"><b>${right}</b> ／ ${ids.length} 題答對 ${right===ids.length?'<span>全部答對了！</span>':'<span>錯的題目看一下詳解，再挑戰一次。</span>'}</div>`
          :'<p class="muted">這些是你寫錯的題目。不要看作答單，自己再做一遍，全部寫完再按「交卷」。</p>'}
    <fieldset id="testFs" ${done?'disabled':''}><legend class="sr">錯題</legend><div class="cards">${ids.map(id=>cardHTML(byId(id))).join('')}</div></fieldset>
    <div class="finish">${done?(right===ids.length?`<button type="button" class="btn primary big" id="testFinish">完成</button>`:`<button type="button" class="btn primary big" id="testAgain">錯的再做一次（${ids.length-right} 題）</button>`):`<p id="testLeft" class="muted"></p><button type="button" class="btn primary big" id="submitTest">交卷</button>`}</div>
  </section>`;
  if(done) ids.forEach(id=>markTestCard(byId(id),res[id]));
}
function render(){stepper();if(state.view==='review')renderReview();else renderTest()}

/* ---------- test: interactive cards ---------- */
function blanksHTML(src,q,startIdx){
  let i=startIdx;
  const html=src.replace(/\[\[(.*?)\]\]/g,(m,spec)=>{
    const idx=i++,id=`${q.id}_${idx}`,val=(state.v[q.id]||{})[idx]??'';
    if(spec.startsWith('s:')){const o=spec.slice(2).split('|');return `<select class="blank" id="${id}" data-q="${q.id}" data-i="${idx}" aria-label="第 ${idx+1} 格"><option value="">選</option>${o.map(x=>`<option${x===val?' selected':''}>${x}</option>`).join('')}</select>`}
    const cls=spec==='w'?'w':spec==='s'?'s':'';
    return `<input class="blank ${cls}" id="${id}" data-q="${q.id}" data-i="${idx}" inputmode="${spec==='w'?'text':'numeric'}" autocomplete="off" value="${String(val).replace(/"/g,'')}" aria-label="第 ${idx+1} 格">`;
  });
  return {html,next:i};
}
function cardHTML(q){
  let body='';const v=state.v[q.id]||{};const esc=x=>String(x||'').replace(/"/g,'');
  if(q.type==='choice'){
    body=`<p class="stem"><span class="qn">${q.n}</span>${q.stem}</p>${figHTML(q)}<div class="opts" role="radiogroup">${q.opts.map((o,i)=>`<button type="button" class="opt${v.c===i?' sel':''}" data-q="${q.id}" data-c="${i}" role="radio" aria-checked="${v.c===i}"><span class="k">${i+1}</span><span>${o}</span></button>`).join('')}</div>`;
  } else if(q.type==='fill'){
    body=`<p class="stem"><span class="qn">${q.n}</span>${q.ask||''}</p>${figHTML(q)}<div class="stem">${blanksHTML(q.stem,q,0).html}</div>`;
  } else if(q.type==='word'){
    body=`<p class="stem"><span class="qn">${q.n}</span>${q.stem}</p>${figHTML(q)}<div class="row"><label>算式：<input class="blank" style="width:12em;text-align:left" id="${q.id}_f" data-q="${q.id}" data-i="f" autocomplete="off" placeholder="例如 5×3＝15" value="${esc(v.f)}"></label><label>答：<input class="blank w" id="${q.id}_a" data-q="${q.id}" data-i="a" inputmode="numeric" autocomplete="off" value="${esc(v.a)}"> ${q.unit}</label></div>`;
  } else if(q.type==='word2'){
    body=`<p class="stem"><span class="qn">${q.n}</span>${q.stem}</p>${figHTML(q)}<div class="w2"><label>先算：<input class="blank" style="width:11em;text-align:left" data-q="${q.id}" data-i="f1" autocomplete="off" value="${esc(v.f1)}"></label><label>再算：<input class="blank" style="width:11em;text-align:left" data-q="${q.id}" data-i="f2" autocomplete="off" value="${esc(v.f2)}"></label><label>答：<input class="blank w" id="${q.id}_a" data-q="${q.id}" data-i="a" inputmode="numeric" autocomplete="off" value="${esc(v.a)}"> ${q.unit}</label></div>`;
  }
  return `<article class="q" id="${q.id}"><span class="mark" aria-hidden="true"></span><p class="from">${short(S.find(s=>s.id===q.s))}</p>${body}<div class="fbzone" id="fb_${q.id}"></div></article>`;
}
function check(q){
  const v=state.v[q.id]||{};
  if(q.type==='choice') return {ok:v.c===q.ans,empty:v.c==null};
  if(q.type==='fill'){const per=q.ans.map((a,i)=>okAns(v[i],a));return {ok:per.every(Boolean),per,empty:q.ans.every((a,i)=>!norm(v[i]))}}
  if(q.type==='word'||q.type==='word2') return {ok:norm(v.a)!==''&&Number(norm(v.a))===Number(q.ans),empty:!norm(v.a)};
  return {ok:true,empty:false};
}
function markTestCard(q,ok){
  const card=document.getElementById(q.id);if(!card)return;
  card.classList.add(ok?'right':'wrong');
  card.querySelector('.mark').textContent=ok?'○':'✗';
  const r=check(q);
  if(q.type==='fill'&&r.per) r.per.forEach((k,i)=>{const el=document.getElementById(`${q.id}_${i}`);if(el)el.classList.add(k?'ok':'no')});
  if(q.type==='choice') card.querySelectorAll('.opt').forEach(b=>{const c=+b.dataset.c;if(c===(state.v[q.id]||{}).c)b.classList.add(ok?'good':'bad');if(!ok&&c===q.ans)b.classList.add('ansopt')});
  document.getElementById('fb_'+q.id).innerHTML=ok?'<div class="fb ok"><strong>答對了！</strong></div>'
    :`<div class="fb no"><strong>還是錯了，再看一次詳解</strong><div class="explain">${reviewBody(q,true).replace(/class="qn"/g,'class="qn sr"')}<hr>${exOf(q)}</div></div>`;
}

/* ---------- teacher hold button ---------- */
function bindHold(s){
  const b=$('#holdBtn');let t=null;
  const start=e=>{if(e.type==='keydown'&&!(e.key===' '||e.key==='Enter'))return;if(e.repeat)return;e.preventDefault();b.classList.add('holding');t=setTimeout(()=>{state.sec[s.id]='done';const n=firstOpen();if(n<S.length){state.cur=n}else{state.view='test'}save();render();window.scrollTo(0,0)},2000)};
  const stop=()=>{b.classList.remove('holding');clearTimeout(t)};
  b.addEventListener('pointerdown',start);b.addEventListener('keydown',start);
  ['pointerup','pointerleave','pointercancel','keyup','blur'].forEach(ev=>b.addEventListener(ev,stop));
  b.addEventListener('contextmenu',e=>e.preventDefault());
  $('#backBtn').addEventListener('click',()=>{delete state.sec[s.id];save();render()});
}

/* ---------- events ---------- */
const onVal=e=>{const t=e.target;if(!t.dataset||!t.dataset.q||t.dataset.i==null)return;
  state.v[t.dataset.q]=state.v[t.dataset.q]||{};state.v[t.dataset.q][t.dataset.i]=t.value;save()};
document.addEventListener('input',onVal);document.addEventListener('change',onVal);
document.addEventListener('click',e=>{
  const t=e.target.closest('button');if(!t)return;
  if(t.dataset.svgo){svGo(t);return}
  if(t.dataset.step!=null){if(t.dataset.step==='test'){state.view='test'}else{state.view='review';state.cur=+t.dataset.step}save();render();window.scrollTo(0,0);return}
  if(t.dataset.goto!=null){if(t.dataset.goto==='test')state.view='test';else{state.view='review';state.cur=+t.dataset.goto}save();render();window.scrollTo(0,0);return}
  if(t.dataset.mark){
    const q=byId(t.dataset.q);state.mark[q.id]=t.dataset.mark;save();
    document.getElementById(q.id).outerHTML=reviewCard(q,false);
    const s=S[state.cur],qs=secQs(s.id),left=qs.filter(x=>!state.mark[x.id]).length,wrong=qs.filter(x=>state.mark[x.id]==='wrong').length;
    $('#leftMsg').innerHTML=leftText(left,wrong);
    $('#secDone').disabled=!!left;$('#secDone').textContent=doneLabel(left,wrong);stepper();return}
  if(t.id==='allRight'){secQs(S[state.cur].id).forEach(q=>state.mark[q.id]='right');save();render();const f=document.getElementById('secDone');if(f)f.scrollIntoView({block:'center'});return}
  if(t.id==='secDone'){
    const sid=S[state.cur].id;
    if(secQs(sid).every(q=>state.mark[q.id]==='right')){state.sec[sid]='done';const n=firstOpen();if(n<S.length)state.cur=n;else state.view='test'}
    else state.sec[sid]='teacher';
    save();render();window.scrollTo(0,0);return}
  if(t.id==='submitTest'){
    const ids=pendingIds();const blank=ids.filter(id=>check(byId(id)).empty);
    if(blank.length&&!t.dataset.sure){t.dataset.sure='1';$('#testLeft').textContent=`還有 ${blank.length} 題沒寫，確定要交卷嗎？再按一次「交卷」。`;return}
    state.test.ids=ids;state.test.res={};ids.forEach(id=>state.test.res[id]=check(byId(id)).ok);state.test.done=true;save();render();window.scrollTo(0,0);return}
  if(t.id==='testAgain'){
    const ids=state.test.ids.filter(id=>!state.test.res[id]);ids.forEach(id=>delete state.v[id]);
    state.test={round:state.test.round+1,ids,done:false,res:{}};save();render();window.scrollTo(0,0);return}
  if(t.id==='testFinish'){state.test={round:state.test.round+1,ids:[],done:true,res:{}};save();render();window.scrollTo(0,0);return}
  if(t.dataset.c!=null&&t.classList.contains('opt')){
    const q=byId(t.dataset.q);state.v[q.id]={c:+t.dataset.c};
    t.parentNode.querySelectorAll('.opt').forEach(b=>{const on=b===t;b.classList.toggle('sel',on);b.setAttribute('aria-checked',on)});save();return}
});

/* zhuyin toggle */
function applyBpmf(){document.body.classList.toggle('bpmf',!!state.bpmf);$('#bpmfBtn').textContent='注音：'+(state.bpmf?'開':'關')}
$('#bpmfBtn').addEventListener('click',()=>{state.bpmf=!state.bpmf;applyBpmf();save()});

/* reset with in-page confirm */
const rz=$('#resetZone');
rz.addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b)return;
  if(b.id==='resetBtn'){rz.innerHTML='<span class="confirm">確定要從頭開始嗎？<button class="btn primary" id="yesReset" type="button">從頭開始</button><button class="btn" id="noReset" type="button">不要</button></span>';return}
  if(b.id==='yesReset'){state=blankState();save();render();window.scrollTo(0,0)}
  rz.innerHTML='<button class="btn" id="resetBtn" type="button">從頭開始</button>';
});

/* QR code for students */
(function(){
  const url=/github\.io$/.test(location.hostname)?location.origin+location.pathname:URL;
  const make=(el,size)=>{try{new QRCode(el,{text:url,width:size,height:size,colorDark:'#1d2742',colorLight:'#ffffff',correctLevel:QRCode.CorrectLevel.M})}catch(e){}};
  if(window.QRCode){make($('#qrSmall'),144);make($('#qrBig'),420)}else{$('#qrOpen').hidden=true}
  $('#qrUrl').textContent=url;
  const m=$('#qrModal');
  $('#qrOpen').addEventListener('click',()=>{m.hidden=false;$('#qrClose').focus()});
  $('#qrClose').addEventListener('click',()=>{m.hidden=true});
  m.addEventListener('click',e=>{if(e.target===m)m.hidden=true});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')m.hidden=true});
})();
window.__Q=Object.fromEntries(Q.map(q=>[q.id,q]));
applyBpmf();render();
