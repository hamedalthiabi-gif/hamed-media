// Adds the NCSS study to the publications. usage: node study.js in.html out.html
const fs=require('fs');const {JSDOM}=require(require.resolve('jsdom',{paths:['/home/claude/hamed-tools/node_modules']}));
const [, , src, dst]=process.argv;const dom=new JSDOM(fs.readFileSync(src,'utf8'));const doc=dom.window.document;
const $=s=>{const e=doc.querySelector(s);if(!e)throw new Error('missing '+s);return e};
const T='تطوير أدوات تمويل مبتكرة لتعزيز الاستدامة المالية للمنظمات غير الربحية';
const URL='https://rssj.ncss.gov.sa/index.php/rssj/article/view/257';
const card=cls=>`<article class="pub${cls}"><img src="pubs/cover16.webp" alt="غلاف: ${T}" width="900" height="1200" loading="lazy"><div class="pub-body"><span class="pub-tag">دراسة محكّمة · ٢٠٢٦</span><h3>${T}</h3><p>دراسة منشورة في مجلة البحوث والدراسات الاجتماعية، تقترح إطارًا عمليًا لتطبيق أدوات التمويل المبتكرة في السياق السعودي.</p></div><a class="btn btn-coral" href="${URL}" target="_blank" rel="noopener">قراءة الدراسة</a></article>`;
const own=$('#sec-own').nextElementSibling; if(!own.classList.contains('pub-grid'))throw new Error('grid');
own.insertAdjacentHTML('afterbegin',card(' tall'));
const hp=$('.hp-grid'); hp.lastElementChild.remove(); hp.insertAdjacentHTML('afterbegin',card(''));
const st=$('.start .st h3'); st.textContent='١٦ إصدارًا معرفيًا';
fs.writeFileSync(dst,'<!doctype html>\n'+doc.documentElement.outerHTML);console.log('ok');
