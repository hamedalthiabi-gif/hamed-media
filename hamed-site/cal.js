// Seasonal touch for the calendar page: each month gets its own palette, motif and line. usage: node cal.js file.html
const fs = require('fs'); const { JSDOM } = require(require.resolve('jsdom', { paths: ['/home/claude/hamed-tools/node_modules'] }));
const f = process.argv[2]; const dom = new JSDOM(fs.readFileSync(f, 'utf8')); const d = dom.window.document;
const $ = s => { const e = d.querySelector(s); if (!e) throw new Error('missing ' + s); return e; };

// hook into the existing calendar renderer
const calScript = [...d.querySelectorAll('script')].find(s => s.textContent.includes("document.getElementById('cal-days-h').textContent="));
if (!calScript) throw new Error('calendar script');
calScript.textContent = calScript.textContent.replace("document.getElementById('cal-days-h').textContent=", "if(window.__season)window.__season(sel.m,sel.y);document.getElementById('cal-days-h').textContent=");

// banner slot above the month tabs
$('#month-tabs').insertAdjacentHTML('beforebegin', '<div class="season" id="season" aria-live="polite"><div class="ss-text"><small id="ss-tag"></small><h3 id="ss-title"></h3><p id="ss-line"></p></div><div class="ss-art" id="ss-art" aria-hidden="true"></div></div>');

const sc = d.createElement('script');
sc.textContent = `(function(){
var M=["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"];
var AR=function(n){return String(n).replace(/\\d/g,function(x){return "٠١٢٣٤٥٦٧٨٩"[x]})};
// motifs (simple flat shapes, drawn in the theme colours via currentColor / CSS vars)
var A={
cup:'<svg viewBox="0 0 200 160"><path d="M60 70h70v34a30 30 0 0 1-30 30h-10a30 30 0 0 1-30-30z" fill="var(--a1)"/><path d="M130 80h10a14 14 0 0 1 0 28h-12" fill="none" stroke="var(--a1)" stroke-width="8"/><rect x="44" y="134" width="112" height="8" rx="4" fill="var(--a2)"/><path d="M78 58c-8-10 8-16 0-28M96 58c-8-10 8-16 0-28M114 58c-8-10 8-16 0-28" fill="none" stroke="var(--a3)" stroke-width="5" stroke-linecap="round"/></svg>',
dallah:'<svg viewBox="0 0 200 160"><path d="M92 34h16l4 10h-24z" fill="var(--a2)"/><path d="M86 46h28c6 22 18 40 18 64 0 16-12 26-32 26s-32-10-32-26c0-24 12-42 18-64z" fill="var(--a1)"/><path d="M68 92c-20-8-34-30-40-44l10-4c8 14 18 30 32 36z" fill="var(--a1)"/><path d="M132 80c14 0 22 10 22 22s-8 20-18 22" fill="none" stroke="var(--a1)" stroke-width="7"/><circle cx="100" cy="28" r="6" fill="var(--a2)"/><path d="M150 42c-6-8 6-12 0-22M164 46c-6-8 6-12 0-22" fill="none" stroke="var(--a3)" stroke-width="4" stroke-linecap="round"/></svg>',
blossom:'<svg viewBox="0 0 200 160"><path d="M20 140C70 120 110 80 180 30" fill="none" stroke="var(--a2)" stroke-width="5"/>'+[[70,112],[118,76],[160,44]].map(function(p){var c="";for(var i=0;i<5;i++){var a=i*72*Math.PI/180;c+='<circle cx="'+(p[0]+Math.cos(a)*11)+'" cy="'+(p[1]+Math.sin(a)*11)+'" r="10" fill="var(--a1)"/>'}return c+'<circle cx="'+p[0]+'" cy="'+p[1]+'" r="6" fill="var(--a3)"/>'}).join('')+'<ellipse cx="96" cy="104" rx="14" ry="6" transform="rotate(-35 96 104)" fill="var(--a2)"/><ellipse cx="140" cy="68" rx="14" ry="6" transform="rotate(-35 140 68)" fill="var(--a2)"/></svg>',
rain:'<svg viewBox="0 0 200 160"><path d="M56 92a26 26 0 0 1 8-50 34 34 0 0 1 64-6 28 28 0 0 1 22 56z" fill="var(--a1)"/>'+[[66,112],[92,124],[118,110],[144,124],[80,140],[130,142]].map(function(p){return '<path d="M'+p[0]+' '+p[1]+'c-5 8-5 12 0 14 5-2 5-6 0-14z" fill="var(--a3)"/>'}).join('')+'</svg>',
sun:'<svg viewBox="0 0 200 160"><circle cx="100" cy="80" r="34" fill="var(--a1)"/>'+Array.from({length:12}).map(function(_,i){var a=i*30*Math.PI/180;return '<line x1="'+(100+Math.cos(a)*46)+'" y1="'+(80+Math.sin(a)*46)+'" x2="'+(100+Math.cos(a)*60)+'" y2="'+(80+Math.sin(a)*60)+'" stroke="var(--a3)" stroke-width="6" stroke-linecap="round"/>'}).join('')+'</svg>',
melon:'<svg viewBox="0 0 200 160"><path d="M30 60a70 70 0 0 0 140 0z" fill="var(--a2)"/><path d="M40 60a60 60 0 0 0 120 0z" fill="#fff" opacity=".85"/><path d="M46 60a54 54 0 0 0 108 0z" fill="var(--a1)"/>'+[[78,78],[100,90],[122,78],[90,104],[112,104]].map(function(p){return '<ellipse cx="'+p[0]+'" cy="'+p[1]+'" rx="3" ry="5" fill="#222" opacity=".75"/>'}).join('')+'<circle cx="160" cy="118" r="18" fill="var(--a3)"/><path d="M160 100v-10" stroke="var(--a2)" stroke-width="4"/></svg>',
citrus:'<svg viewBox="0 0 200 160"><circle cx="78" cy="84" r="46" fill="var(--a2)"/><circle cx="78" cy="84" r="40" fill="var(--a1)"/>'+Array.from({length:8}).map(function(_,i){var a=i*45*Math.PI/180;return '<line x1="78" y1="84" x2="'+(78+Math.cos(a)*38)+'" y2="'+(84+Math.sin(a)*38)+'" stroke="#fff" stroke-width="3" opacity=".8"/>'}).join('')+'<circle cx="78" cy="84" r="5" fill="#fff"/><ellipse cx="146" cy="96" rx="30" ry="22" fill="var(--a3)"/><path d="M150 72c6-10 16-12 22-10-4 8-12 12-22 10z" fill="var(--a2)"/></svg>',
drink:'<svg viewBox="0 0 200 160"><path d="M66 36h68l-8 108H74z" fill="var(--a1)" opacity=".9"/><path d="M70 64h60l-6 80H76z" fill="var(--a3)"/><rect x="82" y="74" width="16" height="16" rx="3" fill="#fff" opacity=".7" transform="rotate(12 90 82)"/><rect x="104" y="90" width="16" height="16" rx="3" fill="#fff" opacity=".7" transform="rotate(-10 112 98)"/><path d="M116 36l14-26h10" fill="none" stroke="var(--a2)" stroke-width="6" stroke-linecap="round"/><circle cx="132" cy="44" r="14" fill="var(--a2)"/><circle cx="132" cy="44" r="9" fill="#fff" opacity=".6"/></svg>',
palm:'<svg viewBox="0 0 200 160"><path d="M100 150c4-40 2-70-4-92" fill="none" stroke="var(--a2)" stroke-width="8" stroke-linecap="round"/><path d="M96 58c-20-18-48-20-70-8 24-2 46 4 70 8zM96 58c-10-24-34-36-56-34 22 8 40 18 56 34zM96 58c8-24 32-38 56-36-22 8-40 20-56 36zM96 58c20-16 50-16 70-2-24-2-46 0-70 2z" fill="var(--a1)"/>'+[[84,74],[92,82],[80,86],[100,78],[88,94],[96,90]].map(function(p){return '<ellipse cx="'+p[0]+'" cy="'+p[1]+'" rx="5" ry="7" fill="var(--a3)"/>'}).join('')+'</svg>',
leaves:'<svg viewBox="0 0 200 160">'+[[60,60,-30,"a1"],[120,50,20,"a3"],[90,110,10,"a2"],[150,110,-40,"a1"]].map(function(p){return '<g transform="translate('+p[0]+' '+p[1]+') rotate('+p[2]+')"><path d="M0-34C22-20 22 20 0 34-22 20-22-20 0-34z" fill="var(--'+p[3]+')"/><path d="M0-30V40" stroke="#fff" stroke-width="2.5" opacity=".7"/></g>'}).join('')+'</svg>',
cloud:'<svg viewBox="0 0 200 160"><path d="M50 88a24 24 0 0 1 8-46 32 32 0 0 1 60-6 26 26 0 0 1 20 52z" fill="var(--a1)"/><path d="M110 150v-44" stroke="var(--a2)" stroke-width="5"/><path d="M70 106a40 40 0 0 1 80 0z" fill="var(--a3)"/><path d="M110 150c0 6-10 6-10 0" fill="none" stroke="var(--a2)" stroke-width="5" stroke-linecap="round"/></svg>',
fire:'<svg viewBox="0 0 200 160"><path d="M100 22c10 26 40 40 40 74a40 40 0 0 1-80 0c0-18 10-26 16-38 4 12 10 16 16 18-6-22 0-38 8-54z" fill="var(--a1)"/><path d="M100 70c6 14 20 22 20 40a20 20 0 0 1-40 0c0-14 12-22 20-40z" fill="var(--a3)"/><rect x="50" y="138" width="100" height="10" rx="5" fill="var(--a2)" transform="rotate(-8 100 143)"/><rect x="50" y="138" width="100" height="10" rx="5" fill="var(--a2)" transform="rotate(8 100 143)"/></svg>'
};
// palette: bg, ink, a1, a2, a3
var T=[
["شتاء","بداية عام جديد، وقت مناسب لرسم خطة العطاء.","cup",["#3B2A2A","#F6E7D8","#C77D4A","#8A5A3B","#F2C9A1"]],
["شتاء","شهر يوم التأسيس، والدفء في المجالس.","dallah",["#2F2420","#F6E7D8","#B8863B","#7A5230","#F0D9A8"]],
["ربيع","الأرض تخضرّ، والمبادرات تنمو.","blossom",["#EAF3E6","#24412B","#E79AA8","#5C8A4F","#F6D365"]],
["ربيع","مطر الربيع يذكّرنا بأن الأثر يبدأ بقطرة.","rain",["#E4EEF5","#1F3A52","#9CC0DA","#5B88A8","#4B8BC0"]],
["أواخر الربيع","الأيام تطول، والفرص أيضًا.","sun",["#FFF4DC","#5A3B12","#F4B63F","#E08E2B","#F7C873"]],
["صيف","صيف منعش، ومبادرات تبقى حاضرة.","melon",["#E8F6EE","#1E4A35","#E8576B","#3E9A63","#9ED9A8"]],
["صيف","انتعاش الصيف في كل خطة.","citrus",["#FFF7D6","#4E3D07","#F5C93A","#8BB43C","#F29D38"]],
["صيف","في ذروة الصيف، يحلّ اليوم العالمي للعمل الإنساني.","drink",["#E3F5F7","#12454D","#7FD1DB","#E86A4F","#2FA6B5"]],
["خريف","موسم التمور واليوم الوطني.","palm",["#F6EEDC","#3D2E14","#6E9A4E","#7C5A2F","#9C4A2A"]],
["خريف","الأوراق تتبدّل، والخطط تُراجع.","leaves",["#FBEBDD","#4A2614","#D9733B","#9A4A22","#E9A23B"]],
["بدايات الشتاء","مع أولى غيوم الشتاء، تكثر ملتقيات القطاع غير الربحي.","cloud",["#E9EDF3","#1E2C44","#9AA9C2","#4C5D7C","#C46A4A"]],
["شتاء","ليالي الشتاء الطويلة، ونار تجمع الناس.","fire",["#2A1E1A","#F7E3D0","#E6863A","#6B3F28","#F6C35B"]]];
var box=document.getElementById('season');
window.__season=function(m,y){var t=T[m],p=t[3];if(!box)return;
box.style.setProperty('--sb',p[0]);box.style.setProperty('--si',p[1]);box.style.setProperty('--a1',p[2]);box.style.setProperty('--a2',p[3]);box.style.setProperty('--a3',p[4]);
document.getElementById('ss-tag').textContent=t[0];document.getElementById('ss-title').textContent=M[m]+' '+AR(y);document.getElementById('ss-line').textContent=t[1];
document.getElementById('ss-art').innerHTML=A[t[2]];box.classList.remove('in');void box.offsetWidth;box.classList.add('in')};
})();`;
// must run before the calendar script renders
calScript.parentNode.insertBefore(sc, calScript);

[...d.querySelectorAll('style')].pop().textContent += `
/* ===== calendar seasonal banner ===== */
.season{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-top:28px;padding:22px 30px;border-radius:8px;background:var(--sb,#eee);color:var(--si,#222);overflow:hidden;position:relative;min-height:150px;transition:background .5s,color .5s}
.season::after{content:"";position:absolute;width:240px;height:240px;border-radius:50%;background:var(--a3);opacity:.14;left:-60px;top:-80px}
.ss-text{position:relative;z-index:1;min-width:0}
.ss-text small{font-weight:600;font-size:14px;opacity:.8}
.ss-text h3{font-size:clamp(26px,3.4vw,38px);margin:2px 0 4px}
.ss-text p{font-size:16px;opacity:.9}
.ss-art{position:relative;z-index:1;width:190px;flex:none}
.ss-art svg{display:block;width:100%;height:auto}
.season.in .ss-art{animation:ssin .7s ease both}.season.in .ss-text{animation:ssin .5s ease both}
@keyframes ssin{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@media (max-width:560px){.season{padding:18px}.ss-art{width:110px}}
@media (prefers-reduced-motion:reduce){.season.in .ss-art,.season.in .ss-text{animation:none}}
`;
fs.writeFileSync(f, '<!doctype html>\n' + d.documentElement.outerHTML); console.log('ok');
