// Swaps in photos from Hamed's «الصور المهنية» folder. usage: node images.js in.html out.html
const fs = require('fs'); const { JSDOM } = require(require.resolve('jsdom', { paths: ['/home/claude/hamed-tools/node_modules'] }));
const [, , src, dst] = process.argv; const dom = new JSDOM(fs.readFileSync(src, 'utf8')); const doc = dom.window.document;
const $ = s => { const e = doc.querySelector(s); if (!e) throw new Error('missing ' + s); return e; };
const $$ = s => [...doc.querySelectorAll(s)];

const sl = $$('.slide > img');
sl[0].src = 'img/n-hero1.webp'; sl[1].src = 'img/n-hero2.webp'; sl[2].src = 'img/n-hero3.webp';
const p1 = $('.ab-pics .p1'); p1.src = 'img/n-consult.webp'; p1.alt = 'أ. حامد الذيابي في جلسة استشارية مع فريق إحدى المنظمات';
const p2 = $('.ab-pics .p2'); p2.src = 'img/n-portrait.webp'; p2.alt = 'أ. حامد الذيابي';
const wp = $('.why-pic img'); wp.src = 'img/n-why.webp'; wp.alt = 'أ. حامد الذيابي يقدّم ورشة عمل';
const ph = (page, img) => { const e = $(`#${page} .phead`); e.style.backgroundImage = `url(img/${img})`; };
ph('about', 'n-about.webp'); ph('store', 'n-services.webp'); ph('pubs', 'n-pubs.webp');

const st = $$('style').map(s => s).find(s => s.textContent.includes('.cnt-band{background:var(--navy) url(img/panel.webp)'));
st.textContent = st.textContent.replace('.cnt-band{background:var(--navy) url(img/panel.webp)', '.cnt-band{background:var(--navy) url(img/n-board.webp)');

const AW = [['n-aw1.webp', 'تكريم من المركز الوطني لتنمية القطاع غير الربحي'], ['n-aw2.webp', 'الجائزة الوطنية للعمل التطوعي'], ['n-aw3.webp', 'تكريم في مبادرة «مجتمع نسق»']];
$('.awards .aw-list').insertAdjacentHTML('beforebegin', `<div class="aw-photos">${AW.map(([f, c]) => `<figure><img src="img/${f}" alt="${c}" loading="lazy"><figcaption>${c}</figcaption></figure>`).join('')}</div>`);
$$('style').pop().textContent += `
.aw-photos{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:44px}
.aw-photos figure{margin:0;background:#fff;box-shadow:var(--shadow);overflow:hidden}
.aw-photos img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;transition:transform .6s}
.aw-photos figure:hover img{transform:scale(1.04)}
.aw-photos figcaption{padding:14px 16px;font-size:15px;font-weight:600;color:var(--navy)}
@media (max-width:820px){.aw-photos{grid-template-columns:1fr 1fr}}
@media (max-width:480px){.aw-photos{grid-template-columns:1fr}}
`;
fs.writeFileSync(dst, '<!doctype html>\n' + doc.documentElement.outerHTML); console.log('ok');
