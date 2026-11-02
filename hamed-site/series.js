// Makes «سلسلة القطاع الجديد» an interactive episode picker (YouTube shorts). usage: node series.js file.html
const fs=require('fs');const {JSDOM}=require(require.resolve('jsdom',{paths:['/home/claude/hamed-tools/node_modules']}));
const f=process.argv[2];const dom=new JSDOM(fs.readFileSync(f,'utf8'));const d=dom.window.document;
const EP=[['مقدمة وتعريف','43YCmPw_OUU',685,1049],['الشركات غير الربحية','pmYVmBpLEEs',418,1049],['التعليم غير الربحي','J_Xl9wlomyk',151,1049],['الصناديق العائلية','vv4LjQkQe7o',685,589],['الجمعيات الأهلية','Ay5vihgoEAk',418,589],['المؤسسات الأهلية','H2M-XqO0dmI',151,589]];
const pct=(v,t)=>(v/t*100).toFixed(2)+'%';
const hot=EP.map(([t,id,x,y],i)=>`<a class="sr-hot" href="https://www.youtube.com/shorts/${id}" target="_blank" rel="noopener" aria-label="الحلقة ${i+1}: ${t}" style="left:${pct(x,1080)};top:${pct(1920-y,1920)};width:${pct(244,1080)};height:${pct(444,1920)}"></a>`).join('');
const list=EP.map(([t,id],i)=>`<li><a href="https://www.youtube.com/shorts/${id}" target="_blank" rel="noopener"><b>الحلقة ${['الأولى','الثانية','الثالثة','الرابعة','الخامسة','السادسة'][i]}</b>${t}</a></li>`).join('');
let n=0;
d.querySelectorAll('.pub').forEach(card=>{const img=card.querySelector('img');if(!img||!/cover14/.test(img.getAttribute('src')))return;n++;
  card.classList.add('series-card');card.querySelector('.pub-tag').textContent='سلسلة مرئية · ٦ حلقات';
  const a=card.querySelector('a.btn');a.className='btn btn-coral series-open';a.removeAttribute('data-pdf');a.href='https://www.youtube.com/shorts/43YCmPw_OUU';a.textContent='شاهد الحلقات';
  img.classList.add('series-open');img.style.cursor='pointer';});
if(!n)throw 'no series card';
d.body.insertAdjacentHTML('beforeend',`<div class="sr-modal" id="sr-modal" hidden role="dialog" aria-modal="true" aria-label="سلسلة القطاع الجديد"><div class="sr-box"><button class="sr-x" type="button" aria-label="إغلاق">✕</button><div class="sr-img"><img src="pubs/cover14.webp" alt="سلسلة القطاع الجديد، تقديم أ. حامد الذيابي">${hot}</div><div class="sr-side"><h3>سلسلة القطاع الجديد</h3><p>حلقات قصيرة تعرّف بالقطاع غير الربحي وأشكاله المختلفة، تقديم أ. حامد الذيابي.</p><ol>${list}</ol></div></div></div>`);
const sc=d.createElement('script');sc.textContent=`(function(){var m=document.getElementById('sr-modal');function o(e){e.preventDefault();m.hidden=false;document.body.style.overflow='hidden'}function c(){m.hidden=true;document.body.style.overflow=''}document.querySelectorAll('.series-open').forEach(function(x){x.addEventListener('click',o)});m.querySelector('.sr-x').addEventListener('click',c);m.addEventListener('click',function(e){if(e.target===m)c()});document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!m.hidden)c()})})();`;
d.body.appendChild(sc);
[...d.querySelectorAll('style')].pop().textContent+=`
.sr-modal{position:fixed;inset:0;z-index:60;background:rgba(0,18,34,.82);display:grid;place-items:center;padding:16px}
.sr-modal[hidden]{display:none!important}
.sr-box{position:relative;background:#fff;border-radius:8px;display:grid;grid-template-columns:auto 300px;max-height:92vh;overflow:auto;max-width:860px;width:auto}
.sr-img{position:relative;align-self:start;width:fit-content;line-height:0}
.sr-img img{display:block;height:min(86vh,900px);width:auto;max-width:100%}
.sr-hot{position:absolute;border-radius:6px;outline:2px solid transparent;transition:outline-color .2s,background .2s}
.sr-hot:hover,.sr-hot:focus-visible{outline-color:var(--coral);background:rgba(187,104,65,.12)}
.sr-side{padding:26px 22px}
.sr-side h3{color:var(--navy);font-size:21px}
.sr-side p{color:var(--muted);font-size:14.5px;margin-top:6px}
.sr-side ol{list-style:none;padding:0;margin:16px 0 0;display:grid;gap:8px}
.sr-side li a{display:grid;padding:10px 12px;border:1px solid var(--line);border-radius:6px;text-decoration:none;color:var(--ink);font-size:14.5px}
.sr-side li a:hover{border-color:var(--coral)}
.sr-side li b{color:var(--coral);font-size:12.5px}
.sr-x{position:absolute;top:8px;left:8px;z-index:2;width:36px;height:36px;border:0;border-radius:50%;background:var(--navy);color:#fff;cursor:pointer;font-size:16px}
@media (max-width:760px){.sr-box{grid-template-columns:1fr}.sr-img img{height:auto;width:100%}}
`;
fs.writeFileSync(f,'<!doctype html>\n'+d.documentElement.outerHTML);console.log('cards',n);
