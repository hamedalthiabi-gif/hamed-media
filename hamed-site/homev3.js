// Home v3: Wahaj-style corporate look. Order: حامد ← الخدمات (+ أرقام + طريقة العمل) ← الإصدارات ← الإثبات ← التواصل
// usage: node homev3.js in.html out.html   (in = index.v1.html)
const fs = require('fs'); const { JSDOM } = require(require.resolve('jsdom', { paths: ['/home/claude/hamed-tools/node_modules'] }));
const [, , src, dst] = process.argv; const dom = new JSDOM(fs.readFileSync(src, 'utf8')); const doc = dom.window.document;
const $ = s => { const e = doc.querySelector(s); if (!e) throw new Error('missing ' + s); return e; };
const $$ = s => [...doc.querySelectorAll(s)];
const H = html => { const t = doc.createElement('template'); t.innerHTML = html.trim(); return t.content.firstElementChild; };

// nav
const NAV = [['home', 'الرئيسية'], ['about', 'من حامد'], ['store', 'الخدمات'], ['pubs', 'الإصدارات'], ['cal', 'التقويم'], ['contact', 'تواصل معنا']];
$('.nav ul').innerHTML = NAV.map(([k, t]) => `<li><a href="#${k}" data-nav="${k}">${t}</a></li>`).join('');
$('#mnav').innerHTML = NAV.map(([k, t]) => `<a href="#${k}" data-nav="${k}">${t}</a>`).join('');
const arrow = $('.f2 ul li a svg').outerHTML;
$('.f2 .cols > div:nth-child(2) ul').innerHTML = NAV.map(([k, t]) => `<li><a href="#${k}">${arrow}${t}</a></li>`).join('');
const ph = (id, t) => { const e = $(`#${id} .phead`); e.querySelector('h1').textContent = t; e.querySelector('nav').lastChild.textContent = t; };
ph('about', 'من حامد'); ph('store', 'الخدمات'); $('#store .eyebrow').textContent = 'الخدمات';
doc.title = 'حامد الذيابي | مستشار التسويق والاستدامة المالية للمنظمات غير الربحية';
$('meta[property="og:title"]').content = doc.title;

// top contact bar (from footer icons)
const soc = $('.f2 .soc').innerHTML;
$('header.nav').insertAdjacentHTML('beforebegin', `<div class="topbar"><div class="wrap"><div class="tb-info"><a href="https://wa.me/966554070212" target="_blank" rel="noopener" dir="ltr">+966 55 407 0212</a><a href="mailto:hamedalthiabi@gmail.com">hamedalthiabi@gmail.com</a></div><div class="tb-soc">${soc}</div></div></div>`);

// home sections
const home = $('#home');
const sec = c => $('#home > section.' + c);
const slider = sec('slider'), ab = sec('ab-split'), svc = sec('svc2'), cnt = sec('cnt-band'), why = sec('why'), nl = sec('nl-band'), clients = sec('clients'), awards = sec('awards');

// 1) slider: about Hamed, services, publications — real photos
const S = [
  ['img/n-hero1.webp', 'مستشار التسويق والاستدامة المالية', 'حامد الذيابي', 'أكثر من عشرين عامًا في تنمية موارد المنظمات غير الربحية وبناء استدامتها المالية.', '#about', 'تعرّف على حامد'],
  ['img/n-hero3.webp', 'الخدمات', 'خطط ودورات واستشارات لمنظمتك', 'من التشخيص إلى القياس، نبني مع منظمتك مصادر دخل مستقرة ومتنوعة.', '#store', 'اطلب الخدمة'],
  ['img/n-about.webp', 'الإصدارات', 'معرفة من الميدان، متاحة للجميع', 'كتاب وبحوث وأدلة في التسويق والاستدامة المالية للقطاع غير الربحي.', '#pubs', 'تصفّح الإصدارات'],
];
$$('.slide').forEach((s, i) => { const [img, sm, h, p, href, b] = S[i]; s.querySelector('img').setAttribute('src', img); s.querySelector('.cap').innerHTML = `<small>${sm}</small><h2>${h}</h2><p>${p}</p><a class="btn btn-coral" href="${href}">${b}</a>`; });
slider.querySelector('.scroll-ind')?.remove();

// 2) about Hamed
ab.querySelector('.ab-txt').innerHTML = `<small>من حامد</small><h2>حامد الذيابي</h2>
<p>مستشار في التسويق والاستدامة المالية للمنظمات غير الربحية. أدرك من عمله الميداني أن التحدي الحقيقي للمنظمات ليس جمع المال فقط، بل بناء استدامة تحررها من الطوارئ المالية.</p>
<p>حوّل خبرته الممتدة لأكثر من عشرين عامًا إلى منهجيات عملية تساعد المنظمات على خدمة قضاياها وتعظيم أثرها.</p>
<ul class="ab-facts"><li><b>مستشار لبرامج رائدة</b>مسرعة مسك، وبرنامج سند محمد بن سلمان، وحاضنة جدارة</li><li><b>رئيس مجلس أمناء مؤسسة درب</b>مؤسسة غير ربحية</li><li><b>تأهيل أكاديمي</b>جامعة مانشستر ٢٠٢٥، جامعة غرناطة ٢٠٢٤، ماجستير جامعة حائل ٢٠٢٢</li></ul>
<a class="btn btn-navy" href="#about">السيرة الكاملة</a>`;

// 3) services
svc.querySelector('.sec-head').innerHTML = '<small>الخدمات</small><h2>ما نقدّمه للمنظمات غير الربحية</h2>';
svc.querySelector('.home-cta')?.remove();
svc.querySelector('.wrap').appendChild(H(`<div class="more-c"><a class="btn btn-coral" href="#store">اطلب الخدمة</a></div>`));
// how we work
why.querySelector('.sec-head').innerHTML = '<small>كيف نعمل</small><h2>نبدأ من واقع منظمتك</h2><p>لا نقدّم إجابات جاهزة، بل نساعدك على رؤية الصورة كاملة واتخاذ قرار أفضل.</p>';

// 4) publications (our own only)
const ownGrid = $('#sec-own').nextElementSibling, guideGrid = $('#sec-guides .pub-grid');
const pick = (g, t) => [...g.children].filter(a => t(a.querySelector('img').getAttribute('src'))).map(a => { const c = a.cloneNode(true); c.classList.remove('tall'); return c; });
const products = [...pick(ownGrid, s => /cover16|book|cover10|cover09|cover11|cover12/.test(s)), ...pick(guideGrid, s => /cover13|cover14/.test(s))];
if (products.length !== 8) throw new Error('products ' + products.length);
const prods = H(`<section class="prods"><div class="wrap"><div class="sec-head rv"><small>الإصدارات</small><h2>من إعداد حامد الذيابي</h2><p>كتاب وبحوث وأدلة في التسويق والاستدامة المالية للقطاع غير الربحي.</p></div><div class="pub-grid prod-pubs"></div><div class="more-c"><a class="btn btn-navy" href="#pubs">كل الإصدارات</a></div></div></section>`);
products.forEach(p => prods.querySelector('.prod-pubs').appendChild(p));

// 5) proof
clients.querySelector('.eyebrow').textContent = 'عملاء وشركاء';
clients.querySelector('.h2').textContent = 'جهات وثقت بنا';

// 6) contact
const contact = H(`<section class="cta-end"><div class="wrap"><h2>لنبدأ من واقع منظمتك</h2><p>أخبرنا بما تحتاجه منظمتك، ونقترح عليك المسار الأنسب لتنمية مواردها واستدامتها.</p>
<div class="ct-cards">
<a class="ct" href="https://wa.me/966554070212" target="_blank" rel="noopener"><small>واتساب الأعمال</small><b dir="ltr">+966 55 407 0212</b><span>افتح المحادثة</span></a>
<a class="ct" href="mailto:hamedalthiabi@gmail.com"><small>البريد الإلكتروني</small><b dir="ltr">hamedalthiabi@gmail.com</b><span>أرسل رسالة</span></a>
<a class="ct" href="https://www.linkedin.com/in/HAMEDALTHIABI" target="_blank" rel="noopener"><small>لينكدإن</small><b dir="ltr">HAMEDALTHIABI</b><span>زيارة الحساب</span></a>
</div></div></section>`);

const wa = H(`<section class="wa-band"><div class="wrap"><div class="wa-text"><small>قناة واتساب</small><h2>تابع «درب الاستدامة المالية»</h2><p>محتوى في الاستدامة المالية وتنمية موارد القطاع غير الربحي، يصلك على واتساب.</p></div><a class="btn btn-coral" href="https://whatsapp.com/channel/0029VaDG6R49Gv7Okjpy860R" target="_blank" rel="noopener">متابعة القناة</a></div></section>`);
home.innerHTML = '';
[slider, ab, svc, cnt, why, prods, nl, wa, clients, awards, contact].forEach(s => home.appendChild(s));
home.appendChild(H(`<div hidden><span id="m-eyebrow"></span><ul id="home-days"></ul><ul id="home-events"></ul></div>`));

// styles: drop decorative "AI" tells, use a calm corporate look
$$('style').pop().textContent += `
/* ===== home v3 (corporate) ===== */
.topbar{background:var(--navy);color:#C9D1DC;font-size:13.5px}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px;padding-block:7px}
.tb-info{display:flex;gap:22px;flex-wrap:wrap}
.tb-info a{color:#C9D1DC;text-decoration:none}.tb-info a:hover{color:#fff}
.tb-soc{display:flex;gap:6px}
.tb-soc a{width:28px;height:28px;display:grid;place-items:center;background:var(--coral);color:#fff}
.tb-soc a svg{width:14px;fill:currentColor}
@media (max-width:700px){.tb-soc{display:none}.tb-info{gap:14px;font-size:12.5px}}
.dotgrid,.scroll-ind{display:none!important}
.track img{filter:none!important;opacity:1!important}
.sec-head h2::after,.h2::after{display:none!important}
.ab-pics::before,.why-pic::before,.card .ic::after{display:none!important}
.cnt b::after{display:none}
.sec-head{margin-bottom:40px}
.sec-head small,.ab-txt small{color:var(--coral);font-size:15px;font-weight:600}
.sec-head h2{font-size:clamp(28px,3.4vw,44px)}
.slide::after{background:linear-gradient(rgba(0,37,68,.25),rgba(0,22,41,.65))}
.slide h2{font-size:clamp(34px,5.4vw,64px)}
.ab-pics{padding:0 0 50px 50px}
.ab-pics img,.why-pic img{border-radius:6px}
.ab-pics .p2{border-radius:6px}
.ab-txt h2{margin:4px 0 16px}
.ab-facts{list-style:none;padding:0;margin:20px 0 4px;display:grid;gap:10px}
.ab-facts li{display:grid;gap:2px;font-size:14.5px;color:var(--muted);padding-inline-start:16px;border-inline-start:3px solid var(--coral)}
.ab-facts b{color:var(--navy);font-size:16px}
.card,.pub,.aw-list li,.aw-photos figure{border-radius:6px}
.card .ic{border-radius:6px}
.svc2 .more-c,.prods .more-c{text-align:center;margin-top:36px}
.why .sec-head{margin-bottom:0}
.why-pic .badge{border-radius:4px}
.prods{background:#fff}
.prod-pubs{grid-template-columns:repeat(4,1fr)!important}
.prod-pubs .pub img{aspect-ratio:3/4;object-fit:cover;object-position:top;background:#F1ECE3}
@media (max-width:1000px){.prod-pubs{grid-template-columns:repeat(3,1fr)!important}}
@media (max-width:760px){.prod-pubs{grid-template-columns:1fr 1fr!important}}
@media (max-width:440px){.prod-pubs{grid-template-columns:1fr!important}}
.awards .aw-list{grid-template-columns:repeat(4,1fr);gap:18px}
.awards .aw-list li{padding:26px 16px 22px}
.awards .aw-list li::before{border-radius:6px}
@media (max-width:900px){.awards .aw-list{grid-template-columns:1fr 1fr}}
@media (max-width:480px){.awards .aw-list{grid-template-columns:1fr}}
.wa-band{background:var(--navy-2);color:#fff;padding-block:40px}
.wa-band .wrap{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap}
.wa-text{display:grid;gap:6px;flex:1 1 380px;min-width:0}
.wa-text small{color:#E9A57F;font-weight:600;font-size:13.5px}
.wa-text h2{font-size:clamp(22px,3vw,28px)}
.wa-text p{color:#C9D1DC;max-width:36em}
.ct-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:980px;margin:30px auto 0}
.ct{display:grid;gap:4px;padding:22px;border:1px solid rgba(255,255,255,.2);border-radius:6px;text-decoration:none;color:#fff;transition:border-color .2s,background .2s;min-width:0}
.ct:hover{border-color:var(--coral);background:rgba(255,255,255,.05)}
.ct small{color:#E9A57F;font-weight:600;font-size:13px}
.ct b{font-size:17px;overflow-wrap:anywhere}
.ct span{font-size:13.5px;color:#C9D1DC}
@media (max-width:760px){.ct-cards{grid-template-columns:1fr}}
`;
fs.writeFileSync(dst, '<!doctype html>\n' + doc.documentElement.outerHTML); console.log('ok');
