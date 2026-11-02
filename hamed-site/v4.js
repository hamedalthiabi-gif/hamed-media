// v4 (Hamed's notes): home = من حامد ← الدورات ← الإصدارات (٦) ← الجوائز (٦) ← الخدمات; full CV on «من حامد»;
// pubs page gets المقالات + الدورات; contact for requests = email + phone. usage: node v4.js file.html
const fs = require('fs'); const { JSDOM } = require(require.resolve('jsdom', { paths: ['/home/claude/hamed-tools/node_modules'] }));
const f = process.argv[2]; const dom = new JSDOM(fs.readFileSync(f, 'utf8')); const d = dom.window.document;
const $ = s => { const e = d.querySelector(s); if (!e) throw new Error('missing ' + s); return e; };
const $$ = s => [...d.querySelectorAll(s)];
const H = html => { const t = d.createElement('template'); t.innerHTML = html.trim(); return t.content.firstElementChild; };
const WA = n => 'https://wa.me/966554070212?text=' + encodeURIComponent('السلام عليكم، أرغب في طلب ' + n);

// ---------- data ----------
const COURSES = [
  ['التسويق الخيري', 'أسس تسويق الجهات غير الربحية وبناء علاقتها بالداعمين.'],
  ['صناعة الخطة التسويقية', 'دورة تطبيقية يخرج منها المتدرب بخطة تسويقية لجهته.'],
  ['تصميم تجربة المتبرع', 'تحسين تجربة المتبرع لرفع رضاه وولائه.'],
  ['الاستدامة المالية', 'بناء الاستدامة المالية وتنويع مصادر الدخل.'],
  ['خطة تنمية الموارد المالية', 'دورة تطبيقية في إعداد خطة تنمية موارد متكاملة.'],
  ['برنامج تدريبي حسب احتياجك', 'نصمّم برنامجًا تدريبيًا يناسب فريق منظمتك وأهدافها.'],
];
const AWARDS6 = [
  ['img/aw-stevie.webp', 'جائزة Stevie الدولية', 'المستوى الذهبي لأفضل مشروع إنساني شارك في إنتاجه'],
  [null, 'موسوعة جينيس', 'أكبر صف تبرعات في العالم، حملة «أواني الخير»'],
  ['img/aw-prince.webp', 'تكريم أمير المنطقة الشرقية', 'تكريم من صاحب السمو الملكي أمير المنطقة الشرقية'],
  ['img/n-aw2.webp', 'جائزة العمل التطوعي ٢٠٢٥', 'الجائزة الوطنية للعمل التطوعي'],
  ['img/n-aw1.webp', 'تطوع احترافي', 'المركز الوطني لتنمية القطاع غير الربحي'],
  ['img/aw-linkedin.webp', 'من أبرز ١٠ مؤثرين', 'على منصة لينكدإن'],
];
const AWARDS_ALL = [
  ['جائزة Stevie الدولية', 'المستوى الذهبي لأفضل مشروع إنساني شارك في إنتاجه'],
  ['موسوعة جينيس', 'أكبر صف تبرعات في العالم، حملة «أواني الخير»'],
  ['تكريم أمير المنطقة الشرقية', 'تكريم من صاحب السمو الملكي أمير المنطقة الشرقية'],
  ['جائزة العمل التطوعي ٢٠٢٥', 'الجائزة الوطنية للعمل التطوعي'],
  ['تطوع احترافي', 'المركز الوطني لتنمية القطاع غير الربحي'],
  ['من أبرز ١٠ مؤثرين', 'على منصة لينكدإن'],
  ['جائزة رواد التسويق', 'المركز الثاني على مستوى المملكة'],
  ['أبطال العدالة الاجتماعية', 'مؤسسة الملك خالد'],
  ['هاكثون التنمية الاجتماعية الأول', 'المركز الثاني، مشروع «تعزيز»'],
];

// ---------- HOME ----------
const home = $('#home');
const sec = c => $('#home > section.' + c);
const slider = sec('slider'), ab = sec('ab-split'), svc = sec('svc2'), cnt = sec('cnt-band'), why = sec('why'), prods = sec('prods'),
  nl = sec('nl-band'), wa = sec('wa-band'), clients = sec('clients'), awards = sec('awards'), contact = sec('cta-end');

// no repeated "20 years"
slider.querySelector('.slide .cap p').textContent = 'مستشار في تنمية موارد المنظمات غير الربحية وبناء استدامتها المالية.';
const abp = ab.querySelectorAll('.ab-txt p');
abp[1].textContent = 'حوّل خبرته الميدانية إلى منهجيات عملية تساعد المنظمات على خدمة قضاياها وتعظيم أثرها.';

// courses
const courses = H(`<section class="crs-sec"><div class="wrap"><div class="sec-head rv"><small>الدورات التدريبية</small><h2>دورات نقدّمها للعاملين في القطاع</h2><p>برامج تطبيقية في التسويق والاستدامة المالية وتنمية الموارد، حضوريًا أو عن بُعد.</p></div>
<div class="crs-grid">${COURSES.map(([t, p], i) => `<article class="crs"><span class="crs-n">${['٠١','٠٢','٠٣','٠٤','٠٥','٠٦'][i]}</span><h3>${t}</h3><p>${p}</p><a class="crs-go" href="${WA(i === 5 ? 'برنامج تدريبي لمنظمتنا' : 'دورة: ' + t)}" target="_blank" rel="noopener">اطلب الدورة</a></article>`).join('')}</div>
<div class="more-c"><a class="btn btn-navy" href="#pubs" data-sec="courses">مقاطع من الدورات</a></div></div></section>`);

// publications: 6 only
[...prods.querySelectorAll('.pub')].forEach(p => { if (/cover13|cover14/.test(p.querySelector('img').getAttribute('src'))) p.remove(); });
prods.querySelector('.prod-pubs').classList.add('six');

// awards: 6 with photos
const aw = H(`<section class="aw6"><div class="wrap"><div class="sec-head rv"><small>جوائز وتكريمات</small><h2>أثر حظي بالتقدير</h2></div>
<div class="aw6-grid">${AWARDS6.map(([img, t, s]) => `<figure class="aw6-c">${img ? `<img src="${img}" alt="${t}" loading="lazy">` : `<div class="aw6-ph"><svg viewBox="0 0 24 24"><path d="M7 2h10v2h4v3a5 5 0 0 1-4.6 5A5 5 0 0 1 13 14.9V18h3v2H8v-2h3v-3.1A5 5 0 0 1 7.6 12 5 5 0 0 1 3 7V4h4V2zm0 4H5v1a3 3 0 0 0 2 2.8V6zm10 0v3.8A3 3 0 0 0 19 7V6h-2z"/></svg></div>`}<figcaption><b>${t}</b><span>${s}</span></figcaption></figure>`).join('')}</div>
<div class="more-c"><a class="btn btn-navy" href="#about">كل الجوائز في السيرة الكاملة</a></div></div></section>`);

// services title
svc.querySelector('.sec-head').innerHTML = '<small>الخدمات</small><h2>ماذا نقدّم</h2><p>خدمات للمنظمات غير الربحية من التخطيط إلى التدريب والتقييم.</p>';

// contact for requests: email + phone only
contact.querySelectorAll('.ct').forEach(a => { if (/linkedin/.test(a.href)) a.remove(); });

home.innerHTML = '';
[slider, ab, cnt, courses, prods, nl, wa, aw, svc, clients, contact].forEach(s => home.appendChild(s));
home.appendChild(H(`<div hidden><span id="m-eyebrow"></span><ul id="home-days"></ul><ul id="home-events"></ul></div>`));
// why (+٢٠ badge) and the old awards block are dropped

// ---------- PUBLICATIONS PAGE ----------
const ownGrid = $('#sec-own').nextElementSibling;
// newsletter card moves to articles
const nlCard = [...ownGrid.children].find(a => /newsletter/.test(a.querySelector('img').getAttribute('src')));
nlCard.remove();
ownGrid.appendChild(H(`<article class="pub tall"><img src="pubs/cover17.webp" alt="غلاف: تقرير حملات رمضان ٢٠٢٤" width="900" height="1200" loading="lazy"><div class="pub-body"><span class="pub-tag">تقرير · ٢٠٢٤</span><h3>تقرير حملات رمضان ٢٠٢٤</h3><p>قراءة في حملات القطاع غير الربحي خلال رمضان، صادر عن مؤسسة درب.</p></div><a class="btn btn-navy" href="https://darb-hub.com/pdf-files/%d8%aa%d9%82%d8%b1%d9%8a%d8%b1-%d8%ad%d9%85%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2024/" target="_blank" rel="noopener">قراءة التقرير</a></article>`));
// contributions list fixes
$$('#sec-contrib .link-list li').forEach(li => {
  const b = li.querySelector('b').textContent;
  if (/تقرير حملات رمضان/.test(b)) li.remove();
  if (/دليل التخصص/.test(b)) li.querySelector('span').textContent = 'مع المركز الوطني لتنمية القطاع غير الربحي';
});
// articles + courses sections
const nlUrl = nlCard.querySelector('a').href;
$('#sec-trans').insertAdjacentHTML('beforebegin', `
<section class="pubs-sec" id="sec-articles"><div class="wrap"><div class="pub-head"><h2 class="h3x">المقالات</h2></div>
<p class="intro sm">مقالات أ. حامد الذيابي في الاستدامة المالية والتسويق والتحول الرقمي للقطاع غير الربحي.</p>
<div class="art-grid" id="art-grid"></div>
<div class="nl-card"><img src="pubs/newsletter.webp" alt="نشرة الاستدامة المالية" loading="lazy"><div><small>النشرة البريدية على لينكدإن</small><h3>نشرة «الاستدامة المالية»</h3><p>نشرة دورية بأكثر من ٢٨٠٠ مشترك، تصلك فيها المقالات الجديدة أولًا بأول.</p><a class="btn btn-coral" href="${nlUrl}" target="_blank" rel="noopener">اشترك في النشرة</a></div></div>
</div></section>
<section class="pubs-sec" id="sec-courses"><div class="wrap"><div class="pub-head"><h2 class="h3x">الدورات</h2></div>
<p class="intro sm">الدورات التدريبية التي يقدّمها أ. حامد الذيابي، ومقاطع منها.</p>
<div class="crs-grid">${COURSES.slice(0, 5).map(([t, p], i) => `<article class="crs"><span class="crs-n">${['٠١','٠٢','٠٣','٠٤','٠٥'][i]}</span><h3>${t}</h3><p>${p}</p><a class="crs-go" href="${WA('دورة: ' + t)}" target="_blank" rel="noopener">اطلب الدورة</a></article>`).join('')}</div>
<div class="vid-grid" id="vid-grid"></div>
</div></section>`);
$('#pubs .pub-jump').innerHTML = [['own', 'الإصدارات'], ['articles', 'المقالات'], ['courses', 'الدورات'], ['trans', 'ترجمات الاستدامة'], ['guides', 'أدلة مصوّرة'], ['contrib', 'إصدارات شارك فيها'], ['media', 'الإعلام والمشاركات']].map(([k, t]) => `<a href="#pubs" data-jump="${k}">${t}</a>`).join('');
// hide empty article/video grids until links are added
// (cards are added later as <a class="art"> / <a class="vid">)

// ---------- ABOUT (السيرة الكاملة) ----------
['creds', 'method', 'aud-sec'].forEach(c => { const e = d.querySelector('#about section.' + c); if (e) e.remove(); });
const li = (b, s) => `<li><b>${b}</b>${s ? `<span>${s}</span>` : ''}</li>`;
$('#about section.about').insertAdjacentHTML('afterend', `
<section class="cv-exp"><div class="wrap"><div class="sec-head"><small>الخبرات</small><h2>المسيرة المهنية</h2></div>
<ol class="tl">
<li><span class="yr">٢٠٢٤ – الآن</span><div><h3>لجنة حكومية</h3><p>قيادة حملات جمع التبرعات وتنمية الموارد، وبناء الشراكات مع الجهات الحكومية والخاصة وغير الربحية.</p></div></li>
<li><span class="yr">٢٠٢٣ – ٢٠٢٥</span><div><h3>وزارة البلديات والإسكان · مدير علاقات الشركاء</h3><p>إدارة شبكة الشركاء والمانحين، وتطوير مبادرات المسؤولية الاجتماعية وتجربة المانحين.</p></div></li>
<li><span class="yr">٢٠٢٢ – ٢٠٢٣</span><div><h3>اللجنة الوطنية لرعاية السجناء والمفرج عنهم وأسرهم (تراحم) · مدير التسويق وتنمية الموارد والشراكات</h3><p>قاد حملة رمضان التي حققت <b>أكثر من ٣٣ مليون ريال</b>، وأسهم في تأسيس وقف تراحم.</p></div></li>
<li><span class="yr">٢٠٢٠ – ٢٠٢٢</span><div><h3>مركز الأثر · مدير الشراكات والخدمات المساندة</h3><p>بناء شراكات ذات أثر مرتفع، وتمكين المنظمات غير الربحية، والإشراف على مبادرات الحوكمة والاستدامة.</p></div></li>
<li><span class="yr">٢٠١٧ – ٢٠٢٠</span><div><h3>جمعية البر الخيرية بأم الدوم · المدير التنفيذي</h3><p>رفع الإيرادات السنوية من <b>٦٠٠ ألف إلى ٦ ملايين ريال</b>، وأبرم أكثر من ٣٠ شراكة مع جهات داعمة.</p></div></li>
<li><span class="yr">٢٠١٣ – ٢٠١٧</span><div><h3>جمعية البر الخيرية بأم الدوم · رئيس العلاقات العامة والإعلام</h3><p>إعداد أول خطة استراتيجية للجمعية، وبناء الهيكل المؤسسي.</p></div></li>
</ol></div></section>
<section class="cv-q"><div class="wrap cv-2">
<div><div class="sec-head"><small>المؤهلات</small><h2>الشهادات الدراسية</h2></div><ul class="cv-list">
${li('زمالة قيادة العمل التشاركي', 'جامعة مانشستر، ٢٠٢٥')}${li('الزمالة العربية الأوروبية في الاقتصاد الاجتماعي', 'جامعة غرناطة، ٢٠٢٤')}${li('ماجستير إدارة المنظمات غير الربحية التنفيذي', 'جامعة حائل، ٢٠٢٢، بتقدير ممتاز مع مرتبة الشرف الأولى')}${li('بكالوريوس الشريعة', 'جامعة الإمام محمد بن سعود الإسلامية، ٢٠١٧')}${li('زمالة الاستثمار', '')}
</ul></div>
<div><div class="sec-head"><small>الشهادات المهنية</small><h2>تأهيل مهني</h2></div><ul class="cv-list">
${li('إدارة المشاريع الاحترافية (PMP)', 'معهد إدارة المشاريع PMI، الولايات المتحدة')}${li('برنامج القيادة المرنة للمنظمات غير الربحية', 'جامعة باث، بريطانيا')}${li('دبلوم القيادة الوسطى للمنظمات غير الربحية', 'جامعة برثاي، بريطانيا')}${li('دبلوم التقييم التنموي', 'جامعة إيناب الكندية')}${li('القيادة للرؤساء التنفيذيين في القطاع غير الربحي', 'جامعة الملك فهد للبترول والمعادن')}${li('الدبلوم التطبيقي المصغر للمنظمات غير الربحية', 'مؤسسة الأميرة العنود')}${li('بيمرا لتصميم تجارب العملاء المحترفين', 'معهد بيمرا، ٢٠٢٥')}${li('أساسيات المشاركة المجتمعية', 'الرابطة الدولية للمشاركة العامة، ٢٠٢٥')}${li('شهادة محترف مؤشرات الأداء', 'معهد مؤشرات الأداء')}${li('شهادة الأيزو في إدارة الشراكات والتعاونيات', '')}${li('قيادة الريادة نحو المستقبل', 'أكاديمية تأهيل القيادات، لندن')}${li('دبلوم ربان للقيادات الشابة للقطاع الخيري', 'المركز العالمي الكندي')}${li('برنامج تمكين القيادة', 'GOOSTA')}${li('برنامج MDLP', 'معهد SAP')}
</ul></div></div></section>
<section class="cv-aw"><div class="wrap"><div class="sec-head"><small>الجوائز</small><h2>جوائز وتكريمات</h2></div>
<ul class="cv-awl">${AWARDS_ALL.map(([b, s]) => li(b, s)).join('')}</ul></div></section>
<section class="cv-roles"><div class="wrap cv-3">
<div><h3 class="cv-h">الاستشارات</h3><ul class="cv-list sm">${li('مستشار مسرعة مسك في الاستدامة المالية', '')}${li('مستشار برنامج سند محمد بن سلمان في التسويق الخيري', '')}${li('مستشار حاضنة جدارة', '')}${li('مستشار لعدد من الجهات غير الربحية', '')}</ul></div>
<div><h3 class="cv-h">الكيانات المؤسسة</h3><ul class="cv-list sm">${li('مؤسسة درب غير الربحية', 'رئيس مجلس الأمناء')}${li('شركة ذا فورث أتش', 'شريك مؤسس')}${li('جمعية أصالة الجوان الأهلية', 'رئيس مجلس الإدارة')}${li('جمعية ضفاف الأهلية', 'عضو مؤسس')}${li('جمعية الخدمات الاجتماعية بنمران', 'عضو مؤسس')}${li('صندوق عون لنا العائلي', 'عضو مؤسس')}</ul></div>
<div><h3 class="cv-h">العضويات</h3><ul class="cv-list sm">${li('عضو هيئة تدريس', 'جامعة المجمعة، وجامعة الحدود الشمالية')}${li('عضو ممارس مهني', 'جامعة الأميرة نورة')}${li('عضو مجلس أثر الشباب', 'مجتمع مسك')}${li('عضو لجنة الاستثمار وتنمية الموارد', 'جمعية أجواد')}${li('عضو لجنة التسويق', 'جمعية زمزم الصحية')}${li('عضو جمعيات', 'الاستشارات التسويقية، تجربة العميل، الادخار، تطوير القطاع غير الربحي')}</ul></div>
</div></section>
<section class="cv-more"><div class="wrap cv-2">
<div><h3 class="cv-h">مشاركات وأعمال</h3><ul class="cv-list sm">${li('المشاركة في تأسيس منصة تعزيز', 'أول منصة تمويل اجتماعي قائم على المكافآت')}${li('تصميم تجربة العميل لإحدى جوائز التميز', '')}${li('تصميم وثيقة الإعلام الرقمي لمؤسسة مانحة', '')}${li('تطوير تجربة المتبرع لمجموعة من متاجر الجمعيات', '')}${li('تحكيم مبادرات حاضنة مسك، ومرشد برنامج مسك ١٠', '')}</ul></div>
<div><h3 class="cv-h">ملتقيات شارك فيها</h3><ul class="cv-chips"><li>ملتقى القطاع الثقافي غير الربحي</li><li>ملتقى المتاجر الإلكترونية</li><li>ملتقى التسويق الخيري</li><li>ملتقى تنمية الموارد المالية، الخبر</li><li>ميسّر ملتقى أثر الشباب، مسك</li><li>قمة Next Gen</li><li>منتدى تجربة المستفيد</li></ul>
<div class="cv-vol"><b>٨٥٥</b><span>ساعة تطوعية مع ٢٠ جهة</span></div></div>
</div></section>`);

// ---------- styles ----------
$$('style').pop().textContent += `
/* ===== v4 ===== */
.crs-sec{background:#fff}
.crs-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.crs{background:#fff;border-radius:6px;box-shadow:var(--shadow);padding:26px 24px;display:grid;gap:8px;align-content:start;border-top:3px solid var(--navy);transition:transform .3s,border-color .3s}
.crs:hover{transform:translateY(-4px);border-color:var(--coral)}
.crs-n{color:var(--coral);font-weight:700;font-size:15px}
.crs h3{font-size:20px;color:var(--navy)}
.crs p{color:var(--muted);font-size:15px}
.crs-go{justify-self:start;margin-top:6px;color:var(--navy);font-weight:600;font-size:14.5px;text-decoration:none;border-bottom:2px solid var(--coral)}
.crs-sec .more-c,.aw6 .more-c{text-align:center;margin-top:34px}
.prod-pubs.six{grid-template-columns:repeat(3,1fr)!important}
.aw6{background:var(--cream)}
.aw6-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.aw6-c{margin:0;background:#fff;border-radius:6px;box-shadow:var(--shadow);overflow:hidden}
.aw6-c img,.aw6-ph{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.aw6-ph{background:var(--navy);display:grid;place-items:center}
.aw6-ph svg{width:72px;fill:#E9A57F}
.aw6-c figcaption{padding:16px 18px;display:grid;gap:2px}
.aw6-c b{color:var(--navy);font-size:17px}
.aw6-c span{color:var(--muted);font-size:14px}
@media (max-width:900px){.crs-grid,.aw6-grid,.prod-pubs.six{grid-template-columns:1fr 1fr!important}}
@media (max-width:520px){.crs-grid,.aw6-grid,.prod-pubs.six{grid-template-columns:1fr!important}}
.ct-cards{grid-template-columns:repeat(2,1fr)!important;max-width:680px!important}
@media (max-width:560px){.ct-cards{grid-template-columns:1fr!important}}
/* pubs: articles + courses */
.art-grid:empty,.vid-grid:empty{display:none}
.art-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:22px}
.nl-card{display:grid;grid-template-columns:180px 1fr;gap:24px;align-items:center;margin-top:24px;background:#fff;border-radius:6px;box-shadow:var(--shadow);padding:20px}
.nl-card img{width:100%;border-radius:6px}
.nl-card small{color:var(--coral);font-weight:600;font-size:13.5px}
.nl-card h3{color:var(--navy);font-size:21px;margin:2px 0 6px}
.nl-card p{color:var(--muted);font-size:15px;margin-bottom:14px}
@media (max-width:600px){.nl-card{grid-template-columns:1fr}.nl-card img{max-width:200px}}
#sec-courses .crs-grid{margin-top:22px}
.vid-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:22px}
#sec-articles{background:#fff}
#sec-courses{background:var(--cream)}
/* about: full CV */
.cv-exp,.cv-aw,.cv-more{background:#fff}
.cv-q,.cv-roles{background:var(--cream)}
.cv-exp .sec-head,.cv-q .sec-head,.cv-aw .sec-head{text-align:start;margin-inline:0;margin-bottom:26px}
.cv-exp .tl{margin-top:0}
.cv-exp .tl h3{font-size:18px}
.cv-2{display:grid;grid-template-columns:1fr 1fr;gap:44px}
.cv-3{display:grid;grid-template-columns:repeat(3,1fr);gap:30px}
.cv-list{list-style:none;padding:0;margin:0;display:grid;gap:10px}
.cv-list li{background:#fff;border-radius:6px;box-shadow:var(--shadow);border-inline-start:3px solid var(--coral);padding:12px 16px;display:grid;gap:2px}
.cv-list b{color:var(--navy);font-size:15.5px}
.cv-list span{color:var(--muted);font-size:13.5px}
.cv-list.sm li{padding:10px 14px}
.cv-h{color:var(--navy);font-size:22px;margin-bottom:16px}
.cv-awl{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.cv-awl li{background:var(--cream);border-radius:6px;padding:16px 18px;display:grid;gap:2px}
.cv-awl b{color:var(--navy)}.cv-awl span{color:var(--muted);font-size:14px}
.cv-chips{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}
.cv-chips li{background:var(--cream);border-radius:30px;padding:7px 14px;font-size:14px;color:var(--navy)}
.cv-vol{margin-top:22px;background:var(--navy);color:#fff;border-radius:6px;padding:18px 22px;display:flex;align-items:baseline;gap:12px}
.cv-vol b{font-size:34px;color:#E9A57F}
@media (max-width:900px){.cv-3,.cv-awl{grid-template-columns:1fr 1fr}}
@media (max-width:700px){.cv-2,.cv-3,.cv-awl{grid-template-columns:1fr}}
`;
fs.writeFileSync(f, '<!doctype html>\n' + d.documentElement.outerHTML); console.log('ok');
