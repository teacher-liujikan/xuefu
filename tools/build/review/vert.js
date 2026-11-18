function vert(a,op,b,r){
  a=String(a);b=String(b);r=String(r);
  const w=Math.max(a.length,b.length+1,r.length);
  const rows=[a.padStart(w),op+b.padStart(w-1),r.padStart(w)];
  let h='';
  rows.forEach((row,i)=>{[...row].forEach(ch=>{h+=`<span class="${i===1?'l':''}${i===2?'r':''}">${ch===' '?'':ch}</span>`})});
  return `<div class="vert" style="--c:${w}">${h}</div>`;
}
