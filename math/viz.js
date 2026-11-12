/* 學扶考古題：詳解的圖解元件（直式、數線、分數、定位板、複名數）。
   XFViz.frames(spec) 回傳 [{h:畫面 HTML, c:說明文字}]；XFViz.mount(el,spec) 放上可以按「下一步」的播放器。 */
(function(){
'use strict';
const PL=['個位','十位','百位','千位','萬位','十萬位'];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const dg=n=>String(n).split('').map(Number);
const OPS={'+':'＋','-':'−','x':'×','/':'÷'};

/* ---------- 直式：用表格排 ---------- */
// rows: [{cells:[{t,cls}], cls}]，每列的 cells 數量相同
function grid(rows,cls){
  return `<table class="vz ${cls||''}" role="img" aria-label="直式">${rows.map(r=>`<tr class="${r.cls||''}">${r.cells.map(c=>`<td class="${c&&c.cls||''}">${c&&c.t!=null?esc(c.t):''}</td>`).join('')}</tr>`).join('')}</table>`;
}
function addFrames(a,b){
  const sum=a+b,W=String(sum).length,A=dg(a),B=dg(b);
  const at=(D,col)=>{const i=D.length-(W-col);return i>=0?D[i]:null};
  const res=Array(W).fill(null),car=Array(W).fill(null),F=[];
  const draw=(hi)=>grid([
    {cls:'ann',cells:[{}].concat(car.map((c,i)=>({t:c,cls:'car'+(i===hi?' hi':'')})))},
    {cells:[{}].concat([...Array(W)].map((_,i)=>({t:at(A,i),cls:i===hi?'hi':''})))},
    {cls:'line',cells:[{t:'＋',cls:'op'}].concat([...Array(W)].map((_,i)=>({t:at(B,i),cls:i===hi?'hi':''})))},
    {cells:[{}].concat(res.map((r,i)=>({t:r,cls:'res'+(i===hi?' hi':'')})))}]);
  F.push({h:draw(-1),c:`${a} ＋ ${b}：把位數對齊，從個位開始算。`});
  let c=0;
  for(let col=W-1;col>=0;col--){
    const p=W-1-col,x=at(A,col),y=at(B,col);
    if(x==null&&y==null){if(c){res[col]=c;F.push({h:draw(col),c:`把進位的 ${c} 寫在${PL[p]}。`})}c=0;continue}
    const s=(x||0)+(y||0)+c;
    let cap=`${PL[p]}：${x==null?0:x} ＋ ${y==null?0:y}${c?` ＋ 進位的 ${c}`:''} ＝ ${s}，`;
    res[col]=s%10;
    if(s>=10){if(col>0)car[col-1]=1;cap+=`寫 ${s%10}，進 1 到${PL[p+1]}。`}else cap+=`寫 ${s}。`;
    c=s>=10?1:0;F.push({h:draw(col),c:cap});
  }
  F.push({h:draw(-1),c:`${a} ＋ ${b} ＝ ${sum}`,end:1});
  return F;
}
function subFrames(a,b){
  const W=String(a).length,A=dg(a),B=dg(b),cur=A.slice(),ann=Array(W).fill(null),cut=Array(W).fill(false),res=Array(W).fill(null),F=[];
  const bt=col=>{const i=B.length-(W-col);return i>=0?B[i]:null};
  const draw=(hi,hs)=>grid([
    {cls:'ann',cells:[{}].concat(ann.map((v,i)=>({t:v,cls:'bor'+(hs&&hs.includes(i)?' hi':'')})))},
    {cells:[{}].concat(A.map((v,i)=>({t:v,cls:(cut[i]?'cut ':'')+(i===hi?'hi':'')})))},
    {cls:'line',cells:[{t:'−',cls:'op'}].concat([...Array(W)].map((_,i)=>({t:bt(i),cls:i===hi?'hi':''})))},
    {cells:[{}].concat(res.map((r,i)=>({t:r,cls:'res'+(i===hi?' hi':'')})))}]);
  F.push({h:draw(-1),c:`${a} − ${b}：把位數對齊，從個位開始算。`});
  for(let col=W-1;col>=0;col--){
    const p=W-1-col,y=bt(col)||0;
    if(cur[col]<y){
      let j=col-1;while(j>=0&&cur[j]===0)j--;
      const old=cur[col],mid=[];
      cur[j]--;ann[j]=cur[j];cut[j]=true;
      for(let k=j+1;k<col;k++){cur[k]=9;ann[k]=9;cut[k]=true;mid.push(PL[W-1-k])}
      cur[col]+=10;ann[col]=cur[col];cut[col]=true;
      const hs=[];for(let k=j;k<=col;k++)hs.push(k);
      F.push({h:draw(col,hs),c:`${PL[p]}的 ${old} 不夠減 ${y}，向${PL[W-1-j]}借 1。`+(mid.length?`${mid.join('、')}是 0，要一路往前借，借過以後變成 9。`:'')+`${PL[p]}變成 ${cur[col]}。`});
    }
    if(bt(col)==null&&col<W-1&&cur.slice(0,col+1).every(v=>v===0)){continue}
    res[col]=cur[col]-y;
    F.push({h:draw(col),c:`${PL[p]}：${cur[col]} − ${y} ＝ ${res[col]}，寫 ${res[col]}。`});
  }
  let k=0;while(k<W-1&&(res[k]===0||res[k]==null)){res[k]=null;k++}
  F.push({h:draw(-1),c:`${a} − ${b} ＝ ${a-b}`,end:1});
  return F;
}
function mulFrames(a,m){
  const prod=a*m,A=dg(a),W=Math.max(String(prod).length,A.length),off=W-A.length;
  const res=Array(W).fill(null),car=Array(W).fill(null),F=[];
  const draw=hi=>grid([
    {cls:'ann',cells:[{}].concat(car.map((c,i)=>({t:c,cls:'car'+(i===hi?' hi':'')})))},
    {cells:[{}].concat([...Array(W)].map((_,i)=>({t:i>=off?A[i-off]:null,cls:i===hi?'hi':''})))},
    {cls:'line',cells:[{t:'×',cls:'op'}].concat([...Array(W)].map((_,i)=>({t:i===W-1?m:null,cls:hi>=0&&i===W-1?'hi2':''})))},
    {cells:[{}].concat(res.map((r,i)=>({t:r,cls:'res'+(i===hi?' hi':'')})))}]);
  F.push({h:draw(-1),c:`${a} × ${m}：用 ${m} 從個位開始，一位一位乘。`});
  let c=0;
  for(let i=A.length-1;i>=0;i--){
    const col=i+off,p=A.length-1-i,q=A[i]*m,s=q+c;
    let cap=`${PL[p]}：${A[i]} × ${m} ＝ ${q}`+(c?`，加上進位的 ${c} 是 ${s}`:'')+'，';
    if(i>0){res[col]=s%10;if(s>=10){car[col-1]=Math.floor(s/10);cap+=`寫 ${s%10}，進 ${Math.floor(s/10)} 到${PL[p+1]}。`}else cap+=`寫 ${s}。`;c=Math.floor(s/10)}
    else{const ds=dg(s);ds.forEach((d,k)=>{res[col-(ds.length-1)+k]=d});cap+=`寫 ${s}。`}
    F.push({h:draw(col),c:cap});
  }
  F.push({h:draw(-1),c:`${a} × ${m} ＝ ${prod}`,end:1});
  return F;
}
function divFrames(a,d){
  const D=dg(a),W=D.length,q=Array(W).fill(null),work=[],F=[];
  const draw=(hi)=>{
    const rows=[{cls:'quo',cells:[{},{}].concat(q.map((v,i)=>({t:v,cls:'res'+(i===hi?' hi':'')})))},
      {cls:'dvd',cells:[{t:d,cls:'dsr'},{t:')',cls:'par'}].concat(D.map((v,i)=>({t:v,cls:'top'+(i===hi?' hi':'')})))}];
    work.forEach(w=>{const cells=[{},{}].concat(Array(W).fill(null).map(()=>({})));const s=String(w.t);
      for(let k=0;k<s.length;k++){const ci=w.end-(s.length-1)+k;if(ci>=0)cells[ci+2]={t:s[k],cls:(w.line?'ul ':'')+(w.hi?'hi':'')}}
      rows.push({cells})});
    return grid(rows,'vdiv');
  };
  F.push({h:draw(-1),c:`${a} ÷ ${d}：從最高位開始，一位一位除。`});
  let cur=0,started=false;
  for(let i=0;i<W;i++){
    cur=cur*10+D[i];const p=W-1-i;
    work.forEach(w=>w.hi=0);
    if(!started&&cur<d&&i<W-1){F.push({h:draw(i),c:`${PL[p]}的 ${cur} 比 ${d} 小，不夠除，和下一位合起來看。`});continue}
    const qd=Math.floor(cur/d),pr=qd*d,rem=cur-pr;
    if(qd===0&&started){
      q[i]=0;
      F.push({h:draw(i),c:`${cur} 比 ${d} 小，不夠除，商的${PL[p]}要寫 0。`,warn:1});
    }else{
      started=true;q[i]=qd;work.push({t:pr,end:i,line:1,hi:1});
      F.push({h:draw(i),c:`${cur} ÷ ${d}：${d} × ${qd} ＝ ${pr}，商的${PL[p]}寫 ${qd}。`});
      work.forEach(w=>w.hi=0);
      work.push({t:rem,end:i,hi:1});
      F.push({h:draw(i),c:`${cur} − ${pr} ＝ ${rem}${i<W-1?'':rem?`，剩下 ${rem}。`:'，剛好除完。'}`});
    }
    if(i<W-1){
      const last=work[work.length-1];
      if(last&&!last.line){last.t=(rem===0&&!(qd===0)?'':String(last.t)==='0'?'':String(last.t))+String(D[i+1]);last.end=i+1;last.hi=1}
      else work.push({t:String(cur)+String(D[i+1]),end:i+1,hi:1});
      if(qd===0&&started){/* 商 0：直接把下一位拉下來 */}
      F.push({h:draw(i+1),c:`把${PL[p-1]}的 ${D[i+1]} 拉下來，變成 ${rem*10+D[i+1]}。`});
    }
    cur=rem;
  }
  work.forEach(w=>w.hi=0);
  const Q=Math.floor(a/d),R=a%d;
  F.push({h:draw(-1),c:`${a} ÷ ${d} ＝ ${Q}`+(R?` …… ${R}（商是 ${Q}，餘數是 ${R}）`:`（商是 ${Q}，餘數是 0）`),end:1});
  return F;
}

/* ---------- SVG 小工具 ---------- */
const svg=(w,h,body,label)=>`<svg class="vsvg" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(label||'圖解')}">${body}</svg>`;
const tx=(x,y,s,cls,anchor)=>`<text x="${x}" y="${y}" class="${cls||''}" text-anchor="${anchor||'middle'}">${esc(s)}</text>`;

/* 數線：{t:'nl',min,max,step,every,start,hops（正往右、負往左）,blank,unit} */
function nlFrames(s){
  const W=600,H=150,L=40,R=560,n=Math.round((s.max-s.min)/s.step),X=v=>L+(v-s.min)/(s.max-s.min)*(R-L),ev=s.every||1;
  const hops=s.hops||0,dir=hops<0?-1:1,N=Math.abs(hops),F=[];
  const base=k=>{
    let b=`<line x1="${L-18}" y1="96" x2="${R+18}" y2="96" class="ax"/>`;
    for(let i=0;i<=n;i++){const v=s.min+i*s.step,x=X(v),lab=(s.labels?s.labels.includes(v):i%ev===0)&&!(s.hide||[]).includes(v);
      b+=`<line x1="${x}" y1="${lab?84:89}" x2="${x}" y2="${lab?108:103}" class="tk"/>`;
      if(lab)b+=tx(x,130,v,'nlab');
      else if((s.hide||[]).includes(v))b+=tx(x,130,k>=N&&v===s.start+hops*s.step?v:'（ ）',k>=N&&v===s.start+hops*s.step?'nlab ans':'nlab');
    }
    for(let i=1;i<=k;i++){const x1=X(s.start+dir*(i-1)*s.step),x2=X(s.start+dir*i*s.step),mx=(x1+x2)/2;
      b+=`<path d="M${x1} 80 Q${mx} ${80-Math.min(46,Math.abs(x2-x1)*.9)} ${x2} 80" class="hop${i===k?' hi':''}"/>`+tx(mx,80-Math.min(46,Math.abs(x2-x1)*.9)/2-10,i,'hopn');}
    const cx=X(s.start+dir*k*s.step);
    b+=`<circle cx="${X(s.start)}" cy="96" r="7" class="pt0"/><circle cx="${cx}" cy="96" r="9" class="pt"/>`;
    return svg(W,H,b,'數線');
  };
  F.push({h:base(0),c:s.c0||`數線上每一格是 ${s.step}${s.unit||''}。從 ${s.start} 開始。`});
  for(let k=1;k<=N;k++)F.push({h:base(k),c:`往${dir>0?'右':'左'}跳 ${k} 格，到 ${s.start+dir*k*s.step}。`});
  F.push({h:base(N),c:s.end||`${s.start} 往${dir>0?'右':'左'} ${N} 格是 ${s.start+hops*s.step}。`,end:1});
  return F;
}
/* 估算：{t:'rd',items:[{n,lo,hi}],expr:'5000 − 1000 ＝ 4000'} */
function rdFrames(s){
  const W=600,rowH=92,F=[],L=70,R=530;
  const draw=k=>{let b='';
    s.items.forEach((it,i)=>{if(i>k)return;const y=i*rowH+52,X=v=>L+(v-it.lo)/(it.hi-it.lo)*(R-L),to=(it.n-it.lo)<(it.hi-it.n)?it.lo:it.hi,x=X(it.n);
      b+=`<line x1="${L}" y1="${y}" x2="${R}" y2="${y}" class="ax"/>`;
      for(let j=0;j<=10;j++){const xx=L+(R-L)*j/10;b+=`<line x1="${xx}" y1="${y-(j%5?5:10)}" x2="${xx}" y2="${y+(j%5?5:10)}" class="tk"/>`}
      b+=tx(L,y+34,it.lo,'nlab'+(to===it.lo?' ans':''))+tx(R,y+34,it.hi,'nlab'+(to===it.hi?' ans':''))+tx((L+R)/2,y+34,(it.lo+it.hi)/2,'nsm');
      b+=`<circle cx="${x}" cy="${y}" r="8" class="pt"/>`+tx(Math.min(Math.max(x,L+30),R-30),y-18,it.n,'nlab hi');
      b+=`<path d="M${x} ${y+12} Q${(x+X(to))/2} ${y+26} ${X(to)} ${y+12}" class="hop${i===k?' hi':''}"/>`;
    });
    return svg(W,s.items.length*rowH+10,b,'估算');};
  s.items.forEach((it,i)=>{const to=(it.n-it.lo)<(it.hi-it.n)?it.lo:it.hi;
    F.push({h:draw(i),c:`${it.n} 在 ${it.lo} 和 ${it.hi} 中間，離 ${to} 比較近，把 ${it.n} 看成 ${to}。`})});
  F.push({h:draw(s.items.length-1),c:s.expr,end:1});
  return F;
}
/* 分數：{t:'fr',den,a,b,op:'+'|'-'|'show',unit:'盒',per:每份代表幾個（離散量）,item:'顆',end} */
function frFrames(s){
  const den=s.den,a=s.a,b=s.b||0,op=s.op||'show',tot=op==='+'?a+b:a,bars=Math.max(1,Math.ceil(tot/den)),u=s.unit||'',F=[];
  const cw=Math.min(56,Math.floor(520/den)),bw=cw*den,W=600,x0=(W-bw)/2,bh=54,gap=22;
  const draw=(na,nb,cross)=>{let o='';
    for(let r=0;r<bars;r++){const y=14+r*(bh+gap);
      for(let i=0;i<den;i++){const k=r*den+i;let cls='fc';
        if(k<na)cls+=' fa';else if(k<na+nb)cls+=' fb';
        o+=`<rect x="${x0+i*cw}" y="${y}" width="${cw}" height="${bh}" class="${cls}"/>`;
        if(cross&&k>=na-cross&&k<na)o+=`<path d="M${x0+i*cw+8} ${y+8} L${x0+(i+1)*cw-8} ${y+bh-8} M${x0+(i+1)*cw-8} ${y+8} L${x0+i*cw+8} ${y+bh-8}" class="fx"/>`;
      }
      o+=tx(x0+bw+10,y+bh/2+7,`1 ${u}`,'nsm','start');}
    return svg(W,14+bars*(bh+gap),o,'分數圖');};
  const f=n=>`${n}/${den}`;
  F.push({h:draw(0,0),c:`1 ${u}平分成 ${den} 份，1 份是 ${f(1)} ${u}${s.per?`，也就是 ${s.per} ${s.item}`:''}。`});
  if(op==='show'){
    F.push({h:draw(a,0),c:s.rev?`${a*s.per} ${s.item}是 ${a} 份，${a} 份就是 ${f(a)} ${u}。`:`${f(a)} ${u}是 ${a} 份${s.per?`，${a} 份是 ${a*s.per} ${s.item}`:''}。`});
  }else if(op==='+'){
    F.push({h:draw(a,0),c:`${f(a)} ${u}是 ${a} 份，先塗 ${a} 份。`});
    F.push({h:draw(a,b),c:`${f(b)} ${u}是 ${b} 份，再塗 ${b} 份。${a+b>den?`第 1 個塗滿了，就塗到第 2 個。`:''}`});
    F.push({h:draw(a,b),c:`${a} 份 ＋ ${b} 份 ＝ ${a+b} 份，分母不變，是 ${f(a+b)} ${u}。`});
  }else{
    F.push({h:draw(a,0),c:`${f(a)} ${u}是 ${a} 份，先塗 ${a} 份。`});
    F.push({h:draw(a,0,b),c:`拿走 ${f(b)} ${u}，就是劃掉 ${b} 份。`});
    F.push({h:draw(a,0,b),c:`${a} 份 − ${b} 份 ＝ ${a-b} 份，分母不變，是 ${f(a-b)} ${u}。`});
  }
  if(s.end)F.push({h:F[F.length-1].h,c:s.end});
  F[F.length-1].end=1;return F;
}
/* 定位板：{t:'pv',cols:['千','百','十','個'],put:[['千',4],['百',12],['十',8]]} */
function pvFrames(s){
  const cols=s.cols,val=cols.map(()=>null),F=[],nm=c=>c==='個'?'一':c;
  const draw=(hi,note)=>`<table class="vpv" role="img" aria-label="定位板"><tr>${cols.map(c=>`<th>${esc(c)}</th>`).join('')}</tr><tr>${val.map((v,i)=>`<td class="${i===hi||(Array.isArray(hi)&&hi.includes(i))?'hi':''}${v!=null&&v>=10?' over':''}">${v==null?'':v}</td>`).join('')}</tr></table>`;
  F.push({h:draw(-1),c:`畫一個定位板：${cols.join('、')}。`});
  s.put.forEach(([c,n])=>{const i=cols.indexOf(c);val[i]=(val[i]||0)+n;F.push({h:draw(i),c:`${n} 個${c==='個'?'一':c}，在「${c}」的格子寫 ${n}。`})});
  for(let i=cols.length-1;i>0;i--){if(val[i]!=null&&val[i]>=10){const k=Math.floor(val[i]/10),old=val[i];val[i]=old%10;val[i-1]=(val[i-1]||0)+k;
    F.push({h:draw([i,i-1]),c:`${old} 個${nm(cols[i])}：每 10 個${nm(cols[i])}換成 1 個${cols[i-1]}，所以是 ${k} 個${cols[i-1]}和 ${old%10} 個${nm(cols[i])}。「${cols[i-1]}」變成 ${val[i-1]}。`})}}
  for(let i=0;i<cols.length;i++)if(val[i]==null&&val.slice(0,i).some(v=>v!=null))val[i]=0;
  const num=val.filter(v=>v!=null).join('');
  F.push({h:draw(-1),c:s.end||`沒有的位數補 0，合起來是 ${num}。`,end:1});
  return F;
}
/* 單位換算：{t:'uc',big:'公升',small:'毫升',base:1000,B:8,S:4,dir:'small'（換成小單位）|'big'（換成大單位）} */
function ucFrames(s){
  const k=String(s.base).length-1,F=[],sm=String(s.S).padStart(k,'0').split(''),names=k===3?['百','十','個']:k===2?['十','個']:['個'];
  const draw=(showB,nS,hi)=>`<table class="vpv vuc" role="img" aria-label="單位換算表"><tr><th rowspan="2">${esc(s.big)}</th><th colspan="${k}">${esc(s.small)}</th></tr><tr>${names.map(n=>`<th class="sub">${n}</th>`).join('')}</tr><tr><td class="${hi==='B'?'hi':''}">${showB?s.B:''}</td>${sm.map((d,i)=>`<td class="${hi==='S'?'hi':''}${nS===2&&i<k-String(s.S).length?' zero':''}">${nS&&(nS===2||i>=k-String(s.S).length)?d:''}</td>`).join('')}</tr></table>`;
  const tot=s.B*s.base+s.S;
  F.push({h:draw(0,0),c:`1 ${s.big} ＝ ${s.base} ${s.small}，所以「${s.small}」有 ${k} 個位置。`});
  if(s.dir==='big'){
    F.push({h:draw(1,2,'B'),c:`把 ${tot} 從右邊對齊放進去：超過 ${k} 位的 ${s.B} 就是 ${s.B} ${s.big}。`});
    F.push({h:draw(1,2,'S'),c:`剩下的 ${sm.join('')} 就是 ${s.S} ${s.small}。`});
    F.push({h:draw(1,2),c:`${tot} ${s.small} ＝ ${s.B} ${s.big}${s.S?` ${s.S} ${s.small}`:''}`,end:1});
  }else{
    F.push({h:draw(1,0,'B'),c:`${s.B} ${s.big}寫在「${s.big}」的格子。`});
    if(s.S===0)F.push({h:draw(1,2,'S'),c:`後面沒有零頭，「${s.small}」的 ${k} 個格子都要補 0。`,warn:1});
    else{F.push({h:draw(1,1,'S'),c:`${s.S} ${s.small}從最右邊對齊寫。`});
      if(String(s.S).length<k)F.push({h:draw(1,2,'S'),c:`空的格子要補 0。`,warn:1})}
    F.push({h:draw(1,2),c:`${s.B} ${s.big}${s.S?` ${s.S} ${s.small}`:''} ＝ ${tot} ${s.small}`,end:1});
  }
  return F;
}
/* 複名數加減：{t:'cu',units:['公斤','公克'],base:1000,a:[5,40],b:[0,1380],op:'+'} */
function cuFrames(s){
  const [U,u]=s.units,base=s.base,F=[];let [A,a]=s.a,[B,b]=s.b;const op=s.op==='-'?'-':'+';
  const row=(x,y,cls)=>`<td class="${cls||''}">${x==null?'':x}</td><td class="${cls||''}">${y==null?'':y}</td>`;
  let top=[A,a],bot=[B,b],res=[null,null],note='';
  const draw=(hi)=>`<table class="vpv vcu" role="img" aria-label="${U}和${u}分開算"><tr><th></th><th>${U}</th><th>${u}</th></tr><tr><td></td>${top.map((v,i)=>`<td class="${hi===i?'hi':''}">${v}</td>`).join('')}</tr><tr class="line"><td class="op">${op==='+'?'＋':'−'}</td>${bot.map((v,i)=>`<td class="${hi===i?'hi':''}">${v}</td>`).join('')}</tr><tr>${'<td></td>'}${res.map((v,i)=>`<td class="res ${hi===i?'hi':''}">${v==null?'':v}</td>`).join('')}</tr></table>`;
  F.push({h:draw(-1),c:`${U}和${u}分開，同樣的單位對齊。`});
  if(b>=base){const k=Math.floor(b/base);F.push({h:draw(-1),c:`${b} ${u}先換一下：${b} ${u} ＝ ${k} ${U} ${b%base} ${u}。`});B+=k;b%=base;bot=[B,b];F.push({h:draw(-1),c:`換好了，下面寫成 ${B} ${U} ${b} ${u}。`})}
  if(a>=base){const k=Math.floor(a/base);A+=k;a%=base;top=[A,a];F.push({h:draw(-1),c:`上面也換成 ${A} ${U} ${a} ${u}。`})}
  if(op==='+'){
    const sm=a+b;res[1]=sm;F.push({h:draw(1),c:`先算${u}：${a} ＋ ${b} ＝ ${sm}。`});
    let c=0;if(sm>=base){c=Math.floor(sm/base);res[1]=sm%base;F.push({h:draw(1),c:`${sm} ${u}滿 ${base} 了，${base} ${u}換成 1 ${U}，剩下 ${sm%base} ${u}。`,warn:1})}
    res[0]=A+B+c;F.push({h:draw(0),c:`再算${U}：${A} ＋ ${B}${c?` ＋ 換過來的 ${c}`:''} ＝ ${A+B+c}。`});
  }else{
    if(a<b){F.push({h:draw(1),c:`${u}：${a} 不夠減 ${b}，向${U}借 1，1 ${U}換成 ${base} ${u}。`,warn:1});A-=1;a+=base;top=[A,a];F.push({h:draw(-1),c:`上面變成 ${A} ${U} ${a} ${u}。`})}
    res[1]=a-b;F.push({h:draw(1),c:`先算${u}：${a} − ${b} ＝ ${a-b}。`});
    res[0]=A-B;F.push({h:draw(0),c:`再算${U}：${A} − ${B} ＝ ${A-B}。`});
  }
  F.push({h:draw(-1),c:`答案是 ${res[0]?`${res[0]} ${U}`:''}${res[1]?` ${res[1]} ${u}`:''}`.replace('是  ','是 '),end:1});
  return F;
}

function frames(s){
  try{
    if(s.t==='v'){const a=s.a,b=s.b;
      if(s.op==='+')return addFrames(a,b);
      if(s.op==='-')return subFrames(a,b);
      if(s.op==='x')return mulFrames(a,b);
      if(s.op==='/')return divFrames(a,b);}
    if(s.t==='nl')return nlFrames(s);
    if(s.t==='rd')return rdFrames(s);
    if(s.t==='fr')return frFrames(s);
    if(s.t==='pv')return pvFrames(s);
    if(s.t==='uc')return ucFrames(s);
    if(s.t==='cu')return cuFrames(s);
  }catch(e){console.warn('viz',e)}
  return [];
}
function title(s){
  if(s.title)return s.title;
  if(s.t==='v')return `直式：${s.a} ${OPS[s.op]} ${s.b}`;
  return {nl:'在數線上跳跳看',rd:'在數線上看接近誰',fr:'用圖看分數',pv:'用定位板看',uc:'用換算表看',cu:'單位分開算'}[s.t]||'圖解';
}
function mount(el,spec){
  const F=frames(spec);if(!F.length){el.hidden=true;return}
  let i=0;
  el.classList.add('vizbox');
  el.innerHTML=`<p class="vzt">${esc(title(spec))}</p><div class="vzfig"></div><p class="vzcap" aria-live="polite"></p><div class="vzbtns"><button type="button" class="btn" data-vz="prev">← 上一步</button><span class="vzn"></span><button type="button" class="btn primary" data-vz="next">下一步 →</button><button type="button" class="btn" data-vz="again" hidden>↺ 再看一次</button></div>`;
  const fig=el.querySelector('.vzfig'),cap=el.querySelector('.vzcap'),n=el.querySelector('.vzn'),bp=el.querySelector('[data-vz=prev]'),bn=el.querySelector('[data-vz=next]'),ba=el.querySelector('[data-vz=again]');
  const show=()=>{const f=F[i];fig.innerHTML=f.h;cap.innerHTML=(window.XFfrac?window.XFfrac(esc(f.c)):esc(f.c));cap.className='vzcap'+(f.warn?' warn':'')+(f.end?' end':'');n.textContent=`${i+1}／${F.length}`;bp.disabled=i===0;bn.hidden=i===F.length-1;ba.hidden=i!==F.length-1};
  el.addEventListener('click',e=>{const b=e.target.closest('[data-vz]');if(!b)return;
    if(b.dataset.vz==='next'&&i<F.length-1)i++;else if(b.dataset.vz==='prev'&&i>0)i--;else if(b.dataset.vz==='again')i=0;show()});
  show();
}
const CSS=`
.vizbox{margin:8px 0 10px;padding:10px 12px 12px;background:var(--card,#fff);border:2px solid var(--pen,#1d4ed8);border-radius:14px;max-width:660px}
.vzt{margin:0 0 4px;font-weight:700;color:var(--pen,#1d4ed8);font-size:17px}
.vzfig{display:flex;justify-content:center;align-items:center;min-height:150px;overflow-x:auto}
.vzcap{margin:8px 0;padding:8px 12px;min-height:3.4em;background:var(--pen-soft,#eef2ff);border-radius:10px;font-size:18px;line-height:1.6}
.vzcap.warn{background:var(--warn-soft,#fff3d1);outline:1.5px solid var(--warn,#b97400)}
.vzcap.end{background:var(--ok-soft,#e5f5ec);font-weight:700}
.vzbtns{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.vzbtns .btn{min-height:46px;font-size:17px}
.vzbtns .btn[disabled]{opacity:.4}
.vzn{font-size:14px;color:var(--muted,#555);min-width:3.2em;text-align:center}
table.vz{border-collapse:collapse;font-family:var(--f-num,ui-monospace,monospace);font-variant-numeric:tabular-nums;margin:4px auto}
table.vz td{width:1.5em;height:1.5em;text-align:center;font-size:30px;line-height:1.5em;padding:0;position:relative;color:var(--ink,#111)}
table.vz tr.ann td{font-size:17px;height:1.5em;line-height:1.5em;width:auto;color:#c2410c;font-weight:700}
table.vz tr.line td{border-bottom:3px solid var(--ink,#111)}
table.vz td.op{color:var(--muted,#555)}
table.vz td.hi{background:#fde68a;border-radius:6px;color:#111}
table.vz td.hi2{background:#bfdbfe;border-radius:6px;color:#111}
table.vz td.res{color:var(--pen,#1d4ed8);font-weight:700}
table.vz td.res.hi{color:#1e3a8a}
table.vz td.cut{color:var(--shade,#999)}
table.vz td.cut::after{content:"";position:absolute;left:12%;right:12%;top:50%;border-top:3px solid #dc2626;transform:rotate(-55deg)}
table.vz.vdiv tr.dvd td.top{border-top:3px solid var(--ink,#111)}
table.vz.vdiv td.par{width:.7em;font-size:34px;font-weight:300;line-height:1.3em}
table.vz.vdiv td.dsr{padding-right:2px}
table.vz.vdiv td.ul{border-bottom:3px solid var(--ink,#111)}
svg.vsvg{width:100%;max-width:600px;height:auto}
svg.vsvg .ax{stroke:var(--ink,#111);stroke-width:3}
svg.vsvg .tk{stroke:var(--ink,#111);stroke-width:2}
svg.vsvg text{font-family:var(--f-num,sans-serif);fill:var(--ink,#111)}
svg.vsvg .nlab{font-size:20px}
svg.vsvg .nsm{font-size:15px;fill:var(--muted,#555)}
svg.vsvg .nlab.ans,svg.vsvg .nlab.hi{fill:#c2410c;font-weight:700}
svg.vsvg .hop{fill:none;stroke:var(--pen,#1d4ed8);stroke-width:3;opacity:.55}
svg.vsvg .hop.hi{stroke:#ea580c;opacity:1;stroke-width:4}
svg.vsvg .hopn{font-size:14px;fill:var(--pen,#1d4ed8)}
svg.vsvg .pt{fill:#ea580c}
svg.vsvg .pt0{fill:var(--pen,#1d4ed8);opacity:.5}
svg.vsvg .fc{fill:var(--card,#fff);stroke:var(--ink,#111);stroke-width:2}
svg.vsvg .fc.fa{fill:#93c5fd}
svg.vsvg .fc.fb{fill:#fdba74}
svg.vsvg .fx{stroke:#dc2626;stroke-width:4;fill:none}
table.vpv{border-collapse:collapse;margin:6px auto;font-family:var(--f-num,sans-serif)}
table.vpv th,table.vpv td{border:2px solid var(--ink,#111);min-width:64px;height:48px;text-align:center;font-size:20px;padding:2px 8px;color:var(--ink,#111)}
table.vpv th{background:var(--main-soft,#e4f2ea);font-weight:700}
table.vpv th.sub{font-size:15px;height:30px;font-weight:400}
table.vpv td{font-size:28px;font-weight:700}
table.vpv td.hi{background:#fde68a;color:#111}
table.vpv td.over{color:#c2410c}
table.vpv td.zero{color:#c2410c}
table.vpv.vcu td.op,table.vpv.vcu th:first-child,table.vpv.vcu td:first-child{border:none;background:none;min-width:36px}
table.vpv.vcu tr.line td{border-bottom:4px solid var(--ink,#111)}
table.vpv.vcu td.res{color:var(--pen,#1d4ed8)}
@media print{.vizbox{display:none}}
`;
if(typeof document!=='undefined'){const st=document.createElement('style');st.textContent=CSS;document.head.appendChild(st)}
const api={frames,mount,title};
if(typeof window!=='undefined')window.XFViz=api;
if(typeof module!=='undefined')module.exports=api;
})();
