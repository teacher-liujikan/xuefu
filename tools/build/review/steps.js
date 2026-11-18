/* step-by-step vertical calculation for 五、 */
const PL=['個位','十位','百位','千位','萬位'];
const SV=[];
const digs=(n,w)=>[...String(n).padStart(w,' ')].map(c=>c===' '?'':c);
const snap=o=>JSON.parse(JSON.stringify(o));
function frame(op,a,b,w){const f={top:digs(a,w),bot:digs(b,w),small:Array(w).fill(''),cross:Array(w).fill(false),res:Array(w).fill(''),hl:-1};f.bot[0]=op;return f}
function addSteps(a,b,unit=''){
  const A=String(a),B=String(b),w=Math.max(A.length,B.length+1,String(a+b).length),f=frame('＋',a,b,w);
  const st=[{f:snap(f),t:'先把數字對齊：個位對個位、十位對十位。從<b>個位</b>開始加。'}];
  let carry=0;const n=Math.max(A.length,B.length);
  for(let c=0;c<n;c++){
    const i=w-1-c,da=+(f.top[i]||0),hasB=c<B.length,db=hasB?+f.bot[i]:0,s=da+db+carry,last=c===n-1;let t=`<b>${PL[c]}</b>：`;
    if(!hasB&&!carry){f.res[i]=String(da);t+=`下面沒有數字，${da} 直接寫下來。`}
    else{t+=(hasB?`${da}＋${db}`:`${da}`)+(carry?`＋進位 ${carry}`:'')+`＝${s}`;
      if(s>=10){f.res[i]=String(s%10);if(last){f.res[i-1]='1';t+=`，寫 ${s%10}，再把 1 寫在${PL[c+1]}。`;carry=0}else{f.small[i-1]='1';carry=1;t+=`，寫 ${s%10}，<b class="cr">進 1</b> 到${PL[c+1]}。`}}
      else{f.res[i]=String(s);carry=0;t+=`，寫 ${s}。`}}
    f.hl=i;st.push({f:snap(f),t});
  }
  f.hl=-1;st.push({f:snap(f),t:`算完了！答案是 <b>${a+b}${unit}</b>。`});return st;
}
function subSteps(a,b,unit=''){
  const A=String(a),B=String(b),w=Math.max(A.length,B.length+1),f=frame('－',a,b,w),cur=f.top.map(x=>+x||0);
  const mark=(j,v)=>{cur[j]=v;f.small[j]=String(v);f.cross[j]=true};
  const st=[{f:snap(f),t:'先把數字對齊：個位對個位、十位對十位。從<b>個位</b>開始減。'}];
  for(let c=0;c<A.length;c++){
    const i=w-1-c,hasB=c<B.length,db=hasB?+f.bot[i]:0;
    if(cur[i]<db){
      let k=i-1;while(cur[k]===0)k--;
      let t=`<b>${PL[c]}</b>：${cur[i]} 不夠減 ${db}，要向${PL[c+1]}借 1。`;
      if(k<i-1)t+=`可是${PL[c+1]}是 0，沒辦法借，要再往前向${PL[w-1-k]}借。`;
      t+=`${PL[w-1-k]} ${cur[k]} 變成 ${cur[k]-1}；`;mark(k,cur[k]-1);
      for(let j=k+1;j<i;j++){t+=`${PL[w-1-j]} 0 先變成 10，再借 1 給右邊，剩下 9；`;mark(j,9)}
      t+=`${PL[c]}變成 ${cur[i]+10}。`;mark(i,cur[i]+10);
      f.hl=i;st.push({f:snap(f),t});
    }
    const r=cur[i]-db,lead=c===A.length-1&&c>0&&r===0;
    let t=`<b>${PL[c]}</b>：`+(hasB?`${cur[i]}－${db}＝${r}`:`下面沒有數字，${cur[i]} 直接寫下來`);
    if(lead)t+='，最前面的 0 不用寫。';else{f.res[i]=String(r);t+=hasB?`，寫 ${r}。`:'。'}
    f.hl=i;st.push({f:snap(f),t});
  }
  f.hl=-1;st.push({f:snap(f),t:`算完了！答案是 <b>${a-b}${unit}</b>。`});return st;
}
function mulSteps(a,b){
  const A=String(a),P=a*b,w=Math.max(A.length,2,String(P).length),f=frame('×',a,b,w);
  const st=[{f:snap(f),t:`把 ${b} 對齊個位。用 ${b} 去乘上面的每一位，從<b>個位</b>開始。`}];
  let carry=0;
  for(let c=0;c<A.length;c++){
    const i=w-1-c,da=+f.top[i],p=da*b,s=p+carry,last=c===A.length-1;
    let t=`<b>${PL[c]}</b>：${da}×${b}＝${p}`+(carry?`，再加進位 ${carry}，${p}＋${carry}＝${s}`:'');
    if(last&&s>=10){f.res[i]=String(s%10);f.res[i-1]=String(Math.floor(s/10));t+=`，前面沒有數字了，直接寫 ${s}。`;carry=0}
    else if(s>=10){f.res[i]=String(s%10);carry=Math.floor(s/10);f.small[i-1]=String(carry);t+=`，寫 ${s%10}，<b class="cr">進 ${carry}</b> 到${PL[c+1]}。`}
    else{f.res[i]=String(s);carry=0;t+=`，寫 ${s}。`}
    f.hl=i;st.push({f:snap(f),t});
  }
  f.hl=-1;st.push({f:snap(f),t:`算完了！答案是 <b>${P}</b>。`});return st;
}
function frameHTML(f){
  const w=f.top.length;let h='';
  const cell=(i,cls,v)=>`<span class="${cls}${i===f.hl?' hl':''}">${v}</span>`;
  for(let i=0;i<w;i++)h+=cell(i,'sm',f.small[i]);
  for(let i=0;i<w;i++)h+=cell(i,f.cross[i]?'x':'',f.top[i]);
  for(let i=0;i<w;i++)h+=cell(i,'ul',f.bot[i]);
  for(let i=0;i<w;i++)h+=cell(i,'rs',f.res[i]);
  return `<div class="svf" style="--c:${w}">${h}</div>`;
}
function unitHTML(o){
  const hl=k=>o.hl===k?' hl':'';
  return `<div class="ug">
  <span></span><span class="sm${hl('cm')}">${o.carry||''}</span><span></span><span class="sm${hl('mm')}"></span><span></span>
  <span></span><span class="${hl('cm')}">23</span><span class="u">公分</span><span class="${hl('mm')}">6</span><span class="u">毫米</span>
  <span class="ul">＋</span><span class="ul${hl('cm')}">6</span><span class="ul u">公分</span><span class="ul${hl('mm')}">5</span><span class="ul u">毫米</span>
  <span></span><span class="rs${hl('cm')}">${o.cm||''}</span><span class="u">${o.cm?'公分':''}</span><span class="rs${hl('mm')}">${o.mm||''}</span><span class="u">${o.mm?'毫米':''}</span></div>`;
}
function unitSteps(){
  return [
    {html:unitHTML({}),t:'公分對公分、毫米對毫米。先算<b>毫米</b>。'},
    {html:unitHTML({hl:'mm',mm:'11'}),t:'<b>毫米</b>：6＋5＝11 毫米。'},
    {html:unitHTML({hl:'mm',mm:'1',carry:'1'}),t:'11 毫米超過 10 毫米了。10 毫米＝1 公分，所以毫米寫 1，把 <b class="cr">1 公分進到公分</b>。'},
    {html:unitHTML({hl:'cm',mm:'1',carry:'1',cm:'30'}),t:'<b>公分</b>：23＋6＋進位 1＝30 公分。'},
    {html:unitHTML({mm:'1',carry:'1',cm:'30'}),t:'算完了！答案是 <b>30 公分 1 毫米</b>。'}
  ];
}
function calcStepper(steps){
  const id=SV.push(steps)-1;
  return `<div class="stepper" data-sv="${id}" data-i="0">${svInner(id,0)}</div>`;
}
function svInner(id,i){
  const s=SV[id][i],n=SV[id].length,last=i===n-1;
  return `<div class="svbox">${s.html||frameHTML(s.f)}</div><p class="svtext" aria-live="polite">${s.t}</p>
  <div class="svnav"><button type="button" class="btn" data-svgo="prev" ${i?'':'disabled'}>◀ 上一步</button><span class="svcount">第 ${i+1}／${n} 步</span><button type="button" class="btn primary" data-svgo="next">${last?'↺ 再看一次':'下一步 ▶'}</button></div>`;
}
function svGo(t){
  const box=t.closest('.stepper'),id=+box.dataset.sv,n=SV[id].length;let i=+box.dataset.i;
  if(t.dataset.svgo==='prev')i=Math.max(0,i-1);else i=i===n-1?0:i+1;
  box.dataset.i=i;box.innerHTML=svInner(id,i);
  const b=box.querySelector(`[data-svgo="${t.dataset.svgo}"]`);if(b&&!b.disabled)b.focus();
}
