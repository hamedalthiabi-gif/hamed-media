// Home v2: من حامد ← الخدمات ← الإصدارات (منتجاتنا) ← الإثبات ← التواصل. No repeated sections.
// usage: node homev2.js in.html out.html
const fs = require('fs'); const { JSDOM } = require(require.resolve('jsdom', { paths: ['/home/claude/hamed-tools/node_modules'] }));
const [, , src, dst] = process.argv; const dom = new JSDOM(fs.readFileSync(src, 'utf8')); const doc = dom.window.document;
const $ = s => { const e = doc.querySelector(s); if (!e) throw new Error('missing ' + s); return e; };
const $$ = s => [...doc.querySelectorAll(s)];
const H = html => { const t = doc.createElement('template'); t.innerHTML = html.trim(); return t.content.firstElementChild; };

// ---------- nav labels ----------
const NAV = [['home', 'الرئيسية'], ['about', 'من حامد'], ['store', 'الخدمات'], ['pubs', 'الإصدارات'], ['cal', 'التقويم'], ['contact', 'تواصل معنا']];
$('.nav ul').innerHTML = NAV.map(([k, t]) => `<li><a href="#${k}" data-nav="${k}">${t}</a></li>`).join('');
$('#mnav').innerHTML = NAV.map(([k, t]) => `<a href="#${k}" data-nav="${k}">${t}</a>`).join('');
const arrow = $('.f2 ul li a svg').outerHTML;
$('.f2 .cols > div:nth-child(2) ul').innerHTML = NAV.map(([k, t]) => `<li><a href="#${k}">${arrow}${t}</a></li>`).join('');
const ph = (id, t) => { const e = $(`#${id} .phead`); e.querySelector('h1').textContent = t; e.querySelector('nav').lastChild.textContent = t; };
ph('about', 'من حامد'); ph('store', 'الخدمات');
$('#store .eyebrow').textContent = 'الخدمات';
doc.title = 'حامد الذيابي | مستشار التسويق والاستدامة المالية للمنظمات غير الربحية';
$('meta[property="og:title"]').content = doc.title;

// ---------- keep pieces we reuse ----------
const home = $('#home');
const svcCards = $('#home .svc2 .cards');
const clients = $('#home > section.clients');
const awardsList = $('#home .awards .aw-list');
const nl = $('#home > section.nl-band');
const ownGrid = $('#sec-own').nextElementSibling;
const guideGrid = $('#sec-guides .pub-grid');
const pick = (grid, test) => [...grid.children].filter(a => test(a.querySelector('img').getAttribute('src'))).map(a => { const c = a.cloneNode(true); c.classList.remove('tall'); return c; });
const products = [
  ...pick(ownGrid, s => /cover16|book|cover10|cover09|cover11|cover12/.test(s)),
  ...pick(guideGrid, s => /cover13|cover14/.test(s)),
];
if (products.length !== 8) throw new Error('products ' + products.length);

home.innerHTML = '';

// 1) Hero — who is Hamed
home.appendChild(H(`<section class="hx"><div class="wrap hx-grid">
<div class="hx-txt rv">
<small class="hx-hi">أهلًا بك، أنا</small>
<h1>حامد الذيابي</h1>
<p class="hx-role">مستشار التسويق والاستدامة المالية للمنظمات غير الربحية</p>
<p class="hx-lede">أساعد المنظمات غير الربحية على تنمية مواردها وتنويع مصادر دخلها، وبناء استدامة مالية تحررها من الطوارئ؛ بخطط عملية تُنفَّذ وتُقاس.</p>
<div class="hx-ctas"><a class="btn btn-coral" href="#store">اطلب الخدمة</a><a class="btn btn-ghost" href="#pubs">تصفّح الإصدارات</a></div>
<ul class="hx-tags"><li>ماجستير إدارة المنظمات غير الربحية</li><li>زمالة جامعة مانشستر</li><li>مستشار مسرعة مسك</li></ul>
</div>
<div class="hx-pic"><img src="hamed.webp" alt="أ. حامد الذيابي" width="700" height="933" fetchpriority="high"></div>
</div>
<div class="wrap"><div class="hx-stats">
<div><b data-n="20">+٢٠</b><span>عامًا في تنمية الموارد</span></div>
<div><b data-n="118">+١١٨</b><span>دورة تدريبية</span></div>
<div><b data-n="60">+٦٠</b><span>جهة وثقت بنا</span></div>
<div><b data-n="15000">+١٥٬٠٠٠</b><span>مستفيد من برامجنا</span></div>
</div></div></section>`));

// 2) من حامد
home.appendChild(H(`<section class="who"><div class="wrap who-grid">
<div class="who-pics rv"><img class="w1" src="img/n-consult.webp" alt="أ. حامد الذيابي في جلسة استشارية مع فريق إحدى المنظمات" loading="lazy"><img class="w2" src="img/n-why.webp" alt="أ. حامد الذيابي يقدّم ورشة عمل" loading="lazy"></div>
<div class="who-txt rv">
<div class="eyebrow">من حامد</div>
<h2>من قلب الميدان إلى منهجيات عملية</h2>
<p>أدرك حامد الذيابي من عمله الميداني أن التحدي الحقيقي للمنظمات غير الربحية ليس جمع المال فقط، بل بناء استدامة تحررها من الطوارئ المالية.</p>
<p>ومن خلال أكثر من عشرين عامًا من الخبرة والتعلم المتخصص، حوّل خبرته إلى منهجيات عملية تساعد المنظمات على خدمة قضاياها وتعظيم أثرها.</p>
<ul class="who-facts">
<li><b>مستشار لبرامج رائدة</b><span>مسرعة مسك، وبرنامج سند محمد بن سلمان، وحاضنة جدارة</span></li>
<li><b>رئيس مجلس أمناء مؤسسة درب</b><span>مؤسسة غير ربحية لتمكين العاملين في القطاع</span></li>
<li><b>تأهيل أكاديمي دولي</b><span>جامعة مانشستر ٢٠٢٥، جامعة غرناطة ٢٠٢٤، جامعة حائل ٢٠٢٢</span></li>
</ul>
<a class="btn btn-navy" href="#about">السيرة الكاملة</a>
</div></div></section>`));

// 3) الخدمات + طريقة العمل
const svc = H(`<section class="svc2"><div class="wrap">
<div class="sec-head rv"><small>الخدمات</small><h2>كيف نخدم منظمتك</h2><p>أربعة مسارات تبدأ من فهم واقع منظمتك، وتنتهي بنتائج تُقاس.</p></div>
<div class="svc-slot"></div>
<ol class="flow rv">
<li><b>٠١</b><h3>التشخيص</h3><p>نقرأ واقع المنظمة: مصادر الدخل، ونقاط القوة، والمخاطر.</p></li>
<li><b>٠٢</b><h3>التصميم</h3><p>نختار مصادر الدخل الأنسب ونبني خطة واضحة.</p></li>
<li><b>٠٣</b><h3>التمكين</h3><p>نسلّم الفريق الأدوات، وندرّبه على التطبيق.</p></li>
<li><b>٠٤</b><h3>القياس</h3><p>نتابع النتائج بالمؤشرات، ونحسّن المسار.</p></li>
</ol>
<div class="home-cta"><p>تحتاج خدمة لمنظمتك؟ اختر ما يناسبك واطلبه مباشرة.</p><a class="btn btn-coral" href="#store">اطلب الخدمة</a></div>
</div></section>`);
svc.querySelector('.svc-slot').replaceWith(svcCards);
home.appendChild(svc);

// 4) الإصدارات (منتجاتنا)
const prod = H(`<section class="prods"><div class="wrap">
<div class="sec-head rv"><small>الإصدارات</small><h2>من إعداد حامد الذيابي</h2><p>كتاب وبحوث وأدلة في التسويق والاستدامة المالية للقطاع غير الربحي، أغلبها متاح للقراءة مجانًا.</p></div>
<div class="pub-grid prod-pubs"></div>
<div class="more-c"><a class="btn btn-navy" href="#pubs">كل الإصدارات</a></div>
</div></section>`);
products.forEach(p => prod.querySelector('.prod-pubs').appendChild(p));
home.appendChild(prod);
home.appendChild(nl);

// 5) الإثبات: جهات + من الميدان + جوائز
clients.querySelector('.eyebrow').textContent = 'عملاء وشركاء';
clients.querySelector('.h2').textContent = 'جهات وثقت بنا';
home.appendChild(clients);
const field = H(`<section class="field"><div class="wrap">
<div class="sec-head rv"><small>من الميدان</small><h2>أثر حظي بالتقدير</h2></div>
<div class="gal rv">
<figure class="g-big"><img src="img/n-hero1.webp" alt="أ. حامد الذيابي يقدّم برنامجًا تدريبيًا" loading="lazy"></figure>
<figure><img src="img/n-aw1.webp" alt="تكريم من المركز الوطني لتنمية القطاع غير الربحي" loading="lazy"><figcaption>تكريم من المركز الوطني لتنمية القطاع غير الربحي</figcaption></figure>
<figure><img src="img/n-aw2.webp" alt="الجائزة الوطنية للعمل التطوعي" loading="lazy"><figcaption>الجائزة الوطنية للعمل التطوعي</figcaption></figure>
<figure><img src="img/n-hero3.webp" alt="أ. حامد الذيابي متحدثًا في إحدى الفعاليات" loading="lazy"></figure>
<figure><img src="img/n-services.webp" alt="أ. حامد الذيابي في ورشة عمل" loading="lazy"></figure>
</div>
<div class="aw-slot"></div>
</div></section>`);
field.querySelector('.aw-slot').replaceWith(awardsList);
home.appendChild(field);

// stubs for the calendar script (home month widgets were removed)
home.appendChild(H(`<div hidden><span id="m-eyebrow"></span><ul id="home-days"></ul><ul id="home-events"></ul></div>`));

// 6) تواصل
home.appendChild(H(`<section class="cta-end"><div class="wrap">
<h2>لنبدأ من واقع منظمتك</h2><p>أخبرنا بما تحتاجه منظمتك، ونقترح عليك المسار الأنسب لتنمية مواردها واستدامتها.</p>
<div class="ct-cards">
<a class="ct" href="https://wa.me/966554070212" target="_blank" rel="noopener"><small>واتساب الأعمال</small><b dir="ltr">+966 55 407 0212</b><span>افتح المحادثة</span></a>
<a class="ct" href="mailto:hamedalthiabi@gmail.com"><small>البريد الإلكتروني</small><b dir="ltr">hamedalthiabi@gmail.com</b><span>أرسل رسالة</span></a>
<a class="ct" href="https://www.linkedin.com/in/HAMEDALTHIABI" target="_blank" rel="noopener"><small>لينكدإن</small><b dir="ltr">HAMEDALTHIABI</b><span>زيارة الحساب</span></a>
</div></div></section>`));

// ---------- styles ----------
$$('style').pop().textContent += `
/* ===== home v2 ===== */
.hx{background:var(--navy);color:#fff;position:relative;overflow:hidden;padding:0!important}
.hx::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(233,165,127,.16) 1.5px,transparent 2px);background-size:26px 26px;mask-image:linear-gradient(90deg,#000,transparent 60%);-webkit-mask-image:linear-gradient(90deg,#000,transparent 60%)}
.hx-grid{position:relative;display:grid;grid-template-columns:1.15fr .85fr;gap:24px;align-items:end;padding-top:56px}
.hx-txt{padding-bottom:56px;min-width:0}
.hx-hi{color:#E9A57F;font-weight:600;font-size:16px}
.hx h1{font-size:clamp(40px,6vw,72px);font-weight:700;margin:6px 0 4px}
.hx-role{font-size:clamp(17px,2vw,22px);font-weight:500;color:#E9A57F}
.hx-lede{margin-top:18px;max-width:34em;font-size:18px;font-weight:300;color:#D9DEE6}
.hx-ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
.hx-tags{list-style:none;padding:0;margin:26px 0 0;display:flex;flex-wrap:wrap;gap:8px}
.hx-tags li{border:1px solid rgba(255,255,255,.25);padding:4px 12px;font-size:13.5px;color:#D9DEE6}
.hx-pic{position:relative;justify-self:center;width:min(420px,100%);align-self:end}
.hx-pic::before{content:"";position:absolute;width:74%;aspect-ratio:1;background:var(--coral);transform:rotate(45deg);left:13%;top:20%}
.hx-pic img{position:relative;display:block;width:100%;height:auto}
.hx-stats{position:relative;display:grid;grid-template-columns:repeat(4,1fr);background:#fff;color:var(--navy);box-shadow:0 18px 40px rgba(0,0,0,.18);margin-bottom:-1px}
.hx-stats div{padding:22px 18px;text-align:center;border-inline-start:1px solid var(--line);min-width:0}
.hx-stats div:first-child{border-inline-start:0}
.hx-stats b{display:block;font-size:30px;font-weight:700;font-variant-numeric:tabular-nums}
.hx-stats span{font-size:14px;color:var(--muted)}
@media (max-width:820px){.hx-grid{grid-template-columns:1fr;padding-top:36px}.hx-txt{padding-bottom:0}.hx-pic{width:min(320px,80%)}.hx-stats{grid-template-columns:1fr 1fr}.hx-stats div:nth-child(3){border-inline-start:0}.hx-stats div{border-top:1px solid var(--line)}}
.who{background:#fff}
.who-grid{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.who-pics{position:relative;padding:0 0 70px 70px}
.who-pics .w1{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.who-pics .w2{position:absolute;left:0;bottom:0;width:50%;aspect-ratio:1;object-fit:cover;border:8px solid #fff;box-shadow:var(--shadow)}
.who-pics::before{content:"";position:absolute;right:-16px;top:-16px;width:110px;height:110px;background:var(--coral);z-index:0}
.who-pics .w1{position:relative}
.who-txt .eyebrow{justify-content:flex-start}
.who-txt h2{font-size:clamp(26px,3.2vw,38px);color:var(--navy);margin:4px 0 16px}
.who-txt p{color:var(--muted)}
.who-txt p+p{margin-top:10px}
.who-facts{list-style:none;padding:0;margin:22px 0 26px;display:grid;gap:12px}
.who-facts li{display:grid;gap:2px;padding:12px 16px;border-inline-start:3px solid var(--coral);background:var(--cream)}
.who-facts b{color:var(--navy);font-size:16px}
.who-facts span{color:var(--muted);font-size:14.5px}
@media (max-width:860px){.who-grid{grid-template-columns:1fr;gap:32px}}
.flow{list-style:none;padding:0;margin:40px 0 0;display:grid;grid-template-columns:repeat(4,1fr);gap:0;background:var(--navy);color:#fff}
.flow li{padding:24px 22px;border-inline-start:1px solid rgba(255,255,255,.14);min-width:0}
.flow li:first-child{border-inline-start:0}
.flow b{color:#E9A57F;font-size:14px}
.flow h3{font-size:19px;margin:6px 0}
.flow p{font-size:14.5px;color:#C9D1DC;font-weight:300}
@media (max-width:820px){.flow{grid-template-columns:1fr 1fr}.flow li:nth-child(3){border-inline-start:0}}
@media (max-width:480px){.flow{grid-template-columns:1fr}.flow li{border-inline-start:0;border-top:1px solid rgba(255,255,255,.14)}}
.prods{background:#fff}
.prod-pubs{grid-template-columns:repeat(4,1fr)!important}
.prod-pubs .pub img{aspect-ratio:3/4;object-fit:cover;object-position:top;background:#F1ECE3}
.prods .more-c{text-align:center;margin-top:30px}
@media (max-width:1000px){.prod-pubs{grid-template-columns:repeat(3,1fr)!important}}
@media (max-width:760px){.prod-pubs{grid-template-columns:1fr 1fr!important}}
@media (max-width:440px){.prod-pubs{grid-template-columns:1fr!important}}
.field{background:var(--cream)}
.gal{display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:repeat(2,220px);gap:14px}
.gal figure{margin:0;position:relative;overflow:hidden;background:var(--navy)}
.gal .g-big{grid-row:span 2}
.gal img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s}
.gal figure:hover img{transform:scale(1.05)}
.gal figcaption{position:absolute;inset:auto 0 0 0;padding:26px 14px 12px;background:linear-gradient(transparent,rgba(0,22,41,.85));color:#fff;font-size:14px;font-weight:600}
@media (max-width:820px){.gal{grid-template-columns:1fr 1fr;grid-template-rows:none;grid-auto-rows:170px}.gal .g-big{grid-column:span 2;grid-row:span 1;height:240px}}
.field .aw-list{margin-top:40px;grid-template-columns:repeat(4,1fr);gap:18px}
.field .aw-list li{padding:26px 16px 22px}
@media (max-width:900px){.field .aw-list{grid-template-columns:1fr 1fr}}
@media (max-width:480px){.field .aw-list{grid-template-columns:1fr}}
.ct-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:980px;margin:30px auto 0}
.ct{display:grid;gap:4px;padding:22px;border:1px solid rgba(255,255,255,.2);text-decoration:none;color:#fff;transition:border-color .2s,background .2s;min-width:0}
.ct:hover{border-color:var(--coral);background:rgba(255,255,255,.05)}
.ct small{color:#E9A57F;font-weight:600;font-size:13px}
.ct b{font-size:17px;overflow-wrap:anywhere}
.ct span{font-size:13.5px;color:#C9D1DC}
@media (max-width:760px){.ct-cards{grid-template-columns:1fr}}
`;
fs.writeFileSync(dst, '<!doctype html>\n' + doc.documentElement.outerHTML); console.log('ok');
