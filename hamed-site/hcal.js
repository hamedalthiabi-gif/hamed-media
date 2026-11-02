// «تقويم حامد»: scheduled courses read live from the Google Sheet tab "courses". usage: node hcal.js file.html
const fs = require('fs'); const { JSDOM } = require(require.resolve('jsdom', { paths: ['/home/claude/hamed-tools/node_modules'] }));
const f = process.argv[2]; const dom = new JSDOM(fs.readFileSync(f, 'utf8')); const d = dom.window.document;
const cal = d.querySelector('#cal section.cal-sec'); if (!cal) throw new Error('cal');
cal.insertAdjacentHTML('beforebegin', `<section class="hc-sec" id="hamed-cal"><div class="wrap">
<div class="sec-head"><small>تقويم حامد</small><h2>دورات قادمة</h2><p>الدورات والبرامج التدريبية المجدولة مع أ. حامد الذيابي، وسجّل مباشرة في الدورة المتاحة.</p></div>
<div class="hc-list" id="hc-list"><p class="hc-empty">جارٍ تحميل الدورات…</p></div>
</div></section>`);
const sc = d.createElement('script');
sc.textContent = `(function(){
var SHEET='1QEPXJI6Nz61nZ71HS_TW8T-gORuCsboVayOFjT5el14';
var M=["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"],DY=["الأحد","الاثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت"];
var AR=function(n){return String(n).replace(/\\d/g,function(x){return "٠١٢٣٤٥٦٧٨٩"[x]})};
var box=document.getElementById('hc-list');
function iso(v){if(v==null)return null;if(typeof v==='string'){var m=v.match(/^Date\\((\\d+),(\\d+),(\\d+)/);if(m)return m[1]+'-'+String(+m[2]+1).padStart(2,'0')+'-'+m[3].padStart(2,'0');var t=v.trim();if(/^\\d{4}-\\d{2}-\\d{2}$/.test(t))return t}return null}
function esc(s){return String(s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function empty(){box.innerHTML='<div class="hc-none"><p>لا توجد دورات مجدولة حاليًا.</p><p class="sm">تابع قناة «درب الاستدامة المالية» ليصلك موعد الدورة القادمة، أو اطلب دورة لفريق منظمتك.</p><div class="hc-act"><a class="btn btn-coral" href="https://whatsapp.com/channel/0029VaDG6R49Gv7Okjpy860R" target="_blank" rel="noopener">متابعة القناة</a><a class="btn btn-navy" href="#store">اطلب دورة لمنظمتك</a></div></div>'}
function card(c){var a=new Date(c.from+'T00:00'),b=new Date(c.to+'T00:00');var full=/مكتمل|مغلق/.test(c.status);
var when=c.from===c.to?DY[a.getDay()]+' '+AR(a.getDate())+' '+M[a.getMonth()]+' '+AR(a.getFullYear()):AR(a.getDate())+(a.getMonth()!==b.getMonth()?' '+M[a.getMonth()]:'')+' – '+AR(b.getDate())+' '+M[b.getMonth()]+' '+AR(b.getFullYear());
var reg=/^https?:/.test(c.url)?c.url:'https://wa.me/966554070212?text='+encodeURIComponent('السلام عليكم، أرغب في التسجيل في دورة: '+c.name+' ('+c.from+')');
return '<article class="hc'+(full?' full':'')+'"><div class="hc-date"><b>'+AR(a.getDate())+'</b><span>'+M[a.getMonth()]+'</span></div><div class="hc-body"><div class="hc-tags">'+(c.mode?'<span>'+esc(c.mode)+'</span>':'')+'<span class="st">'+(full?'اكتملت المقاعد':'التسجيل متاح')+'</span></div><h3>'+esc(c.name)+'</h3>'+(c.desc?'<p>'+esc(c.desc)+'</p>':'')+'<div class="hc-meta"><span>'+when+'</span>'+(c.time?'<span>'+esc(c.time)+'</span>':'')+(c.place?'<span>'+esc(c.place)+'</span>':'')+'</div></div><div class="hc-go">'+(full?'<span class="btn hc-off" aria-disabled="true">مكتملة</span>':'<a class="btn btn-coral" href="'+esc(reg)+'" target="_blank" rel="noopener">سجّل الآن</a>')+'</div></article>'}
fetch('https://docs.google.com/spreadsheets/d/'+SHEET+'/gviz/tq?tqx=out:json&headers=1&sheet=courses').then(function(r){return r.text()}).then(function(t){
var j=JSON.parse(t.slice(t.indexOf('{'),t.lastIndexOf('}')+1));var cols=j.table.cols.map(function(c){return (c.label||'').trim().toLowerCase()});var ix=function(k){return cols.indexOf(k)};
var today=new Date();today.setHours(0,0,0,0);var out=[];
(j.table.rows||[]).forEach(function(r){var g=function(k){var c=r.c[ix(k)];return c?(c.v!=null?c.v:c.f):null};var name=g('name'),from=iso(g('from')),to=iso(g('to'))||from;
if(name&&from&&new Date(to+'T23:59')>=today)out.push({name:String(name),desc:String(g('desc')||''),from:from,to:to,time:String(g('time')||''),place:String(g('place')||''),mode:String(g('mode')||''),status:String(g('status')||''),url:String(g('url')||'')})});
out.sort(function(a,b){return a.from.localeCompare(b.from)});
if(!out.length)return empty();box.innerHTML=out.map(card).join('')}).catch(empty);
})();`;
d.body.appendChild(sc);
[...d.querySelectorAll('style')].pop().textContent += `
/* ===== تقويم حامد ===== */
.hc-sec{background:#fff}
.hc-list{display:grid;gap:16px;max-width:980px;margin-inline:auto}
.hc{display:grid;grid-template-columns:90px 1fr auto;gap:20px;align-items:center;background:#fff;border-radius:8px;box-shadow:var(--shadow);padding:20px 22px;border-inline-start:4px solid var(--coral)}
.hc.full{border-color:var(--line);opacity:.8}
.hc-date{background:var(--navy);color:#fff;border-radius:6px;text-align:center;padding:10px 6px;line-height:1.2}
.hc-date b{display:block;font-size:30px}
.hc-date span{font-size:13px;color:#E9A57F}
.hc-tags{display:flex;gap:8px;flex-wrap:wrap}
.hc-tags span{font-size:12.5px;background:var(--cream);color:var(--navy);padding:2px 10px;border-radius:30px}
.hc-tags .st{background:#E6F3EA;color:#2F7A55;font-weight:600}
.hc.full .hc-tags .st{background:#F3E6E6;color:#9A3A3A}
.hc h3{color:var(--navy);font-size:20px;margin:6px 0 2px}
.hc p{color:var(--muted);font-size:14.5px}
.hc-meta{display:flex;gap:14px;flex-wrap:wrap;font-size:14px;color:var(--ink);margin-top:6px}
.hc-meta span+span::before{content:"·";margin-inline-end:14px;color:var(--muted)}
.hc-off{background:var(--line);color:var(--muted);cursor:default}
.hc-none{text-align:center;background:var(--cream);border-radius:8px;padding:30px 20px}
.hc-none p{color:var(--navy);font-size:18px;font-weight:600}
.hc-none p.sm{font-size:15px;font-weight:400;color:var(--muted);margin-top:6px}
.hc-act{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px}
.hc-empty{text-align:center;color:var(--muted)}
@media (max-width:640px){.hc{grid-template-columns:70px 1fr}.hc-go{grid-column:1/-1}.hc-go .btn{width:100%;justify-content:center}}
`;
fs.writeFileSync(f, '<!doctype html>\n' + d.documentElement.outerHTML); console.log('ok');
