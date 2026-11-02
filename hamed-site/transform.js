// Restructures hamedalthiabi.com: content first, then services, "we" voice.
// usage: node transform.js live/index.html out/index.html
const fs = require('fs');
const { JSDOM } = require(require.resolve('jsdom', { paths: ['/home/claude/hamed-tools/node_modules'] }));
const [, , src, dst] = process.argv;
const dom = new JSDOM(fs.readFileSync(src, 'utf8'));
const doc = dom.window.document;
const $ = s => { const e = doc.querySelector(s); if (!e) throw new Error('missing ' + s); return e; };
const $$ = s => [...doc.querySelectorAll(s)];
const H = html => { const t = doc.createElement('template'); t.innerHTML = html.trim(); return t.content.firstElementChild; };

// head
doc.title = 'حامد الذيابي | معرفة وخدمات لاستدامة القطاع غير الربحي';
$('meta[name=description]').content = 'إصدارات مجانية وتقويم للقطاع غير الربحي، وخدمات استشارية وتدريبية في التسويق والاستدامة المالية للمنظمات غير الربحية.';
$('meta[property="og:title"]').content = doc.title;
$('meta[property="og:description"]').content = 'اقرأ مجانًا، وتابع مناسبات القطاع، واطلب الخدمة التي تناسب منظمتك.';

// nav + footer
const NAV = [['home', 'الرئيسية'], ['pubs', 'الإصدارات'], ['cal', 'التقويم'], ['store', 'خدماتنا'], ['about', 'من نحن'], ['contact', 'تواصل معنا']];
$('.nav ul').innerHTML = NAV.map(([k, t]) => `<li><a href="#${k}" data-nav="${k}">${t}</a></li>`).join('');
$('#mnav').innerHTML = NAV.map(([k, t]) => `<a href="#${k}" data-nav="${k}">${t}</a>`).join('');
const nb = $('.nav .wrap > a.btn'); nb.href = '#store'; nb.textContent = 'اطلب الخدمة';
const arrow = $('.f2 ul li a svg').outerHTML;
$('.f2 .cols > div:nth-child(2) ul').innerHTML = NAV.map(([k, t]) => `<li><a href="#${k}">${arrow}${t}</a></li>`).join('');
$('.f2 .about-f p').textContent = 'معرفة وخدمات في التسويق والاستدامة المالية للمنظمات غير الربحية. نساعد المنظمات على تنمية مواردها وبناء استدامتها؛ لتتفرغ لخدمة قضاياها وتعظيم أثرها.';

// hero slides: content first
const CAP = [
  `<small>مكتبة مجانية للقطاع غير الربحي</small><h2>معرفة عملية تنمّي موارد منظمتك</h2><p>أدلة وترجمات وتقارير في جمع التبرعات والسرد القصصي والاستدامة المالية، اقرأها الآن مجانًا.</p><div><a class="btn btn-coral" href="#pubs">اقرأ مجانًا</a><a class="btn btn-ghost" href="#store">خدماتنا</a></div>`,
  `<small>تقويم القطاع غير الربحي</small><h2>مناسبات القطاع وفعالياته في مكان واحد</h2><p>الأيام العالمية ومواسم العطاء وملتقيات القطاع في المملكة، محدّثة كل شهر لتخطط حملاتك مبكرًا.</p><div><a class="btn btn-coral" href="#cal">افتح التقويم</a></div>`,
  `<small>خدماتنا للمنظمات غير الربحية</small><h2>استدامة العطاء، وأثرٌ يمتد</h2><p>نساعد المنظمات غير الربحية على تنمية مواردها، وتنويع مصادر دخلها، وبناء استدامة مالية تحررها من الطوارئ.</p><div><a class="btn btn-coral" href="#store">اطلب الخدمة</a></div>`];
$$('.slide .cap').forEach((c, i) => { if (CAP[i]) c.innerHTML = CAP[i]; });
const simg = $$('.slide > img');
simg[0].setAttribute('src', 'img/panel.webp');
simg[2].setAttribute('src', 'img/prince.webp');

// home order
const home = $('#home');
const sec = c => $('#home > section.' + c);
const slider = sec('slider'), ab = sec('ab-split'), svc = sec('svc2'), cnt = sec('cnt-band'), quote = sec('quote-band'),
  why = sec('why'), pubs = sec('home-pubs'), nl = sec('nl-band'), month = sec('month-sec'), clients = sec('clients'), awards = sec('awards');
const start = H(`<section class="start"><div class="wrap"><div class="start-grid">
<a class="st" href="#pubs"><small>اقرأ مجانًا</small><h3>١٥ إصدارًا معرفيًا</h3><p>أدلة وترجمات وتقارير جاهزة للقراءة والتطبيق.</p><span class="go">تصفّح الإصدارات ←</span></a>
<a class="st" href="#cal"><small>خطّط مبكرًا</small><h3>تقويم القطاع</h3><p>الأيام العالمية ومواسم العطاء وفعاليات المملكة.</p><span class="go">افتح التقويم ←</span></a>
<a class="st" href="#pubs" data-sec="media"><small>شاهد واستمع</small><h3>بودكاست ولقاءات</h3><p>حوارات عن تجارب القطاع غير الربحي ومستقبله.</p><span class="go">شاهد الآن ←</span></a>
<a class="st hl" href="#store"><small>لمنظمتك</small><h3>اطلب الخدمة</h3><p>خطط ودورات وجلسات استشارية وتقييم.</p><span class="go">اختر خدمتك ←</span></a>
</div></div></section>`);
const media = H(`<section class="media-home"><div class="wrap"><div class="eyebrow">شاهد واستمع</div><h2 class="h2">حوارات عن القطاع غير الربحي</h2>
<ul class="link-list"><li><div><b>بودكاست «حكاية القطاع»</b><span>الموسم الثاني</span></div><a href="https://youtube.com/playlist?list=PLAo-jF-fp49E9FgPTL12OkFwTjiPrUwtw" target="_blank" rel="noopener">مشاهدة</a></li><li><div><b>بودكاست «سبر»</b><span>توثيق تجارب القطاع غير الربحي</span></div><a href="https://youtube.com/@user-sb2gs6rx7l" target="_blank" rel="noopener">مشاهدة</a></li><li><div><b>بودكاست «اكتفاء»</b><span>حلقة حوارية</span></div><a href="https://youtu.be/XbSVe_wosPU" target="_blank" rel="noopener">مشاهدة</a></li><li><div><b>ذا ستيج</b><span>مشاركة</span></div><a href="https://youtu.be/-byebEAYGnk" target="_blank" rel="noopener">مشاهدة</a></li></ul>
<div class="more-c"><a class="btn btn-navy" href="#pubs" data-sec="media">كل المشاركات الإعلامية</a></div></div></section>`);
const ctaEnd = H(`<section class="cta-end"><div class="wrap"><h2>لنبدأ من واقع منظمتك</h2><p>أخبرنا بما تحتاجه منظمتك، ونقترح عليك المسار الأنسب لتنمية مواردها واستدامتها.</p><div class="ctas"><a class="btn btn-coral" href="#store">اطلب الخدمة</a><a class="btn btn-ghost" href="https://wa.me/966554070212" target="_blank" rel="noopener">راسلنا على واتساب</a></div></div></section>`);
quote.remove();
[slider, start, pubs, month, media, nl, svc, cnt, why, clients, awards, ab, ctaEnd].forEach(s => home.appendChild(s));

pubs.querySelector('.eyebrow').textContent = 'مكتبة مجانية';
pubs.querySelector('.h2').textContent = 'اقرأ مجانًا، وطبّق في منظمتك';
pubs.querySelector('.hp-top .btn').textContent = 'كل الإصدارات';
month.querySelector('.h2').textContent = 'مناسبات القطاع وفعالياته';
svc.querySelector('.wrap').appendChild(H(`<div class="home-cta"><p>تحتاج خدمة لمنظمتك؟ اختر ما يناسبك واطلبه مباشرة.</p><a class="btn btn-coral" href="#store">اطلب الخدمة</a></div>`));
const cntH = [...cnt.querySelectorAll('.cnt h3')];
cntH[1].textContent = 'دورة تدريبية قدّمناها'; cntH[2].textContent = 'جهة وثقت بنا'; cntH[3].textContent = 'مستفيد من برامجنا';
why.querySelector('.sec-head h2').textContent = 'لماذا نحن؟';
clients.querySelector('.h2').textContent = 'جهات وثقت بنا';
ab.querySelector('.ab-txt').innerHTML = `<small>من نحن</small><h2>خبرة ميدانية تحوّلت إلى منهجيات عملية</h2><p>خلف هذا المحتوى خبرة تمتد أكثر من عشرين عامًا يقودها أ. حامد الذيابي في تنمية موارد المنظمات غير الربحية وبناء استدامتها المالية.</p><p>تعلّمنا من الميدان أن التحدي الحقيقي ليس جمع المال فقط، بل بناء استدامة تحرر المنظمة من الطوارئ المالية؛ ولذلك نحوّل الخبرة إلى أدوات ومنهجيات تساعد المنظمات على خدمة قضاياها وتعظيم أثرها.</p><a class="btn btn-navy" href="#about">تعرّف علينا</a>`;

// inner pages
const about = $('#about .phead'); about.querySelector('h1').textContent = 'من نحن'; about.querySelector('nav').lastChild.textContent = 'من نحن';
const store = $('#store .phead'); store.querySelector('h1').textContent = 'خدماتنا'; store.querySelector('nav').lastChild.textContent = 'خدماتنا';
$('#store .eyebrow').textContent = 'خدماتنا';
$('#pubs .pubs-top .h2').textContent = 'مكتبة الإصدارات';
$('#pubs .pubs-top .intro').textContent = 'كتاب وأدلة وبحوث وتقارير ونماذج في التسويق والاستدامة المالية للقطاع غير الربحي، إلى جانب مشاركاتنا الإعلامية.';

// styles
$$('style').pop().textContent += `
/* ===== content-first restructure ===== */
.start{padding-block:44px 8px}
.start-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.st{display:grid;gap:6px;align-content:start;padding:22px;background:#fff;box-shadow:var(--shadow);text-decoration:none;color:inherit;border-top:3px solid var(--navy);transition:transform .3s,border-color .3s;min-width:0}
.st:hover{transform:translateY(-4px);border-color:var(--coral)}
.st small{color:var(--coral);font-weight:600;font-size:13.5px}
.st h3{font-size:19px;color:var(--navy)}
.st p{font-size:14.5px;color:var(--muted);line-height:1.7}
.st .go{font-size:14px;font-weight:600;color:var(--navy);margin-top:4px}
.st.hl{background:var(--navy);border-color:var(--coral)}.st.hl h3,.st.hl .go{color:#fff}.st.hl p{color:#C9D1DC}.st.hl small{color:#E9A57F}
@media (max-width:900px){.start-grid{grid-template-columns:1fr 1fr}}
@media (max-width:480px){.start-grid{grid-template-columns:1fr}}
.media-home{background:var(--cream)}
.media-home .link-list{max-width:900px;margin:32px auto 0}
.media-home .more-c{text-align:center;margin-top:26px}
.cta-end{background:var(--navy);color:#fff;text-align:center;padding-block:72px}
.cta-end h2{font-size:clamp(26px,3.4vw,38px)}
.cta-end p{color:#C9D1DC;margin:12px auto 0;max-width:34em}
.cta-end .ctas{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:26px}
.slide .cap div{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:30px}
.slide .cap div .btn{margin-top:0}
.btn-ghost{color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.7)}
.btn-ghost:hover{box-shadow:inset 0 0 0 1px #fff;background:rgba(255,255,255,.08)}
`;

// order buttons -> WhatsApp with the service name
const sc = doc.createElement('script');
sc.textContent = `document.querySelectorAll('.prod .btn').forEach(function(a){var n=a.closest('.prod').querySelector('h3').textContent;a.href='https://wa.me/966554070212?text='+encodeURIComponent('السلام عليكم، أرغب في طلب خدمة: '+n);a.target='_blank';a.rel='noopener'});`;
doc.body.appendChild(sc);

fs.mkdirSync(require('path').dirname(dst), { recursive: true });
fs.writeFileSync(dst, '<!doctype html>\n' + doc.documentElement.outerHTML);
console.log('written', dst);
