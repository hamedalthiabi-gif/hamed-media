// Inner pages in the same corporate (Wahaj-like) look as the home page. usage: node inner.js file.html
const fs = require('fs'); const { JSDOM } = require(require.resolve('jsdom', { paths: ['/home/claude/hamed-tools/node_modules'] }));
const f = process.argv[2]; const dom = new JSDOM(fs.readFileSync(f, 'utf8')); const d = dom.window.document;
const $ = s => { const e = d.querySelector(s); if (!e) throw new Error('missing ' + s); return e; };

// About: portrait beside the bio, message card under it
const q = $('#about .about .quote');
const side = d.createElement('div'); side.className = 'ab-side';
side.innerHTML = '<img src="img/n-portrait.webp" alt="أ. حامد الذيابي" loading="lazy">';
q.replaceWith(side); side.appendChild(q);
$('#about .about .eyebrow').textContent = 'من هو حامد الذيابي';

// Contact: three info cards + social row (no dark block, no dot ornament)
const ct = $('#contact section.contact');
const socials = [...ct.querySelectorAll('.soc-list a')].map(a => `<a href="${a.href}" target="_blank" rel="noopener">${a.querySelector('b').textContent}</a>`).join('');
const ic = p => `<span class="ci-ic"><svg viewBox="0 0 24 24"><path d="${p}"/></svg></span>`;
ct.innerHTML = `<div class="wrap">
<div class="sec-head"><small>تواصل معنا</small><h2>لنبدأ من واقع منظمتك</h2><p>يسعدنا تواصلك للاستفسار عن خدماتنا، أو لنتعرّف على واقع منظمتك ونقترح المسار الأنسب لها.</p></div>
<div class="ci-grid">
<div class="cinfo">${ic('M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z')}<small>واتساب الأعمال</small><span dir="ltr">+966 55 407 0212</span><div class="ci-act"><a class="btn btn-coral" href="https://wa.me/966554070212" target="_blank" rel="noopener">مراسلة</a></div></div>
<div class="cinfo">${ic('M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm9 7.2L4.4 7H4v.4l8 5.6 8-5.6V7h-.4L12 12.2z')}<small>البريد الإلكتروني</small><span dir="ltr">hamedalthiabi@gmail.com</span><div class="ci-act"><a class="btn btn-navy" href="mailto:hamedalthiabi@gmail.com">إرسال</a><button class="copy" data-t="hamedalthiabi@gmail.com">نسخ</button></div></div>
<div class="cinfo">${ic('M4 4h16v12H5.2L4 17.2V4zm3 4v2h10V8H7zm0 3v2h7v-2H7z')}<small>قناة واتساب</small><span>درب الاستدامة المالية</span><div class="ci-act"><a class="btn btn-coral" href="https://whatsapp.com/channel/0029VaDG6R49Gv7Okjpy860R" target="_blank" rel="noopener">متابعة القناة</a></div></div>
<div class="cinfo">${ic('M12 2a7 7 0 0 1 7 7c0 5.2-7 13-7 13S5 14.2 5 9a7 7 0 0 1 7-7zm0 4.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z')}<small>الموقع</small><span>الرياض، المملكة العربية السعودية</span></div>
</div>
<div class="ci-soc"><b>تابعنا</b>${socials}</div>
</div>`;

[...d.querySelectorAll('style')].pop().textContent += `
/* ===== inner pages: corporate look ===== */
.phead{padding:86px 20px 78px}
.phead::before{background:linear-gradient(rgba(0,37,68,.78),rgba(0,22,41,.86))}
.phead nav{font-size:14.5px}
section .eyebrow{color:var(--coral);font-weight:600;font-size:15px}
.prod::after,.cover::after,.about .quote::after{display:none!important}
.dots{display:none!important}
.prod,.pub,.link-list li,.aud,.contact-card,.panel,.kn,.svc{border-radius:6px}
.btn{border-radius:4px}
/* about */
.about .wrap{grid-template-columns:1.1fr .9fr;align-items:center}
.about .h2,.about .eyebrow,.creds .h2,.creds .eyebrow{text-align:start;justify-content:flex-start}
.about p{color:var(--muted)}
.ab-side{position:relative;padding-bottom:70px}
.ab-side img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;object-position:top;border-radius:6px}
.ab-side .quote{position:absolute;inset-inline:28px;bottom:0;padding:22px 24px;border-radius:6px;box-shadow:0 14px 30px rgba(0,37,68,.25)}
.ab-side .quote p{font-size:18px}
.ab-side .quote .alt{display:none}
.creds{background:var(--cream)}
.cr-list{gap:12px}
.cr-list li{background:#fff;border:0;border-inline-start:3px solid var(--coral);border-radius:6px;padding:14px 18px;box-shadow:var(--shadow)}
.method .steps{gap:16px}
.method .step,.method .step:first-child{background:rgba(255,255,255,.06);border:0;border-radius:6px;padding:24px 22px}
.method .step .n{display:inline-grid;place-items:center;width:40px;height:40px;border-radius:50%;background:var(--coral);color:#fff}
.aud-grid{background:none;border:0;gap:20px}
.aud{background:#fff;box-shadow:var(--shadow);border-top:3px solid var(--coral)}
/* services */
.fchips{justify-content:center}
.fchip{border-radius:30px;padding:8px 18px}
.prod{border:0;box-shadow:var(--shadow);transition:transform .3s,box-shadow .3s}
.prod:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(0,37,68,.14)}
.prod .cat{display:inline-block;justify-self:start;background:var(--cream);padding:2px 10px;border-radius:30px}
/* publications */
.pub-head{border-bottom:0;padding-bottom:0}
.pub-head::before{display:none}
.h3x{font-size:clamp(22px,2.6vw,30px)}
.pub-head::after{content:"";flex:1;height:1px;background:var(--line);margin-inline-start:16px}
.pub-jump{justify-content:center}
.pub-jump a{border-radius:30px;padding:7px 16px}
#sec-trans{background:var(--cream);border:0}
.link-list li{background:#fff;border:0;box-shadow:var(--shadow)}
.link-list a{border-radius:4px}
.media-sec{background:var(--cream)}
.media-sec .link-list li{background:#fff}
/* calendar */
.month-tabs{justify-content:center}
.month-tabs button{border-radius:30px;padding:6px 14px}
.month-tabs button.now{box-shadow:inset 0 0 0 2px var(--coral)}
.month-grid .mg-col{background:#fff;border-radius:6px;box-shadow:var(--shadow);padding:22px}
.mg-h{border-bottom:1px solid var(--line)}
.d-date{border-radius:6px}
.cal-sec{background:var(--cream)}
/* contact */
.contact .wrap{display:block}
.ci-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.cinfo{background:#fff;border-radius:6px;box-shadow:var(--shadow);padding:30px 24px;text-align:center;display:grid;justify-items:center;gap:6px;align-content:start}
.ci-ic{width:64px;height:64px;border-radius:50%;background:var(--cream);display:grid;place-items:center;margin-bottom:8px}
.ci-ic svg{width:28px;fill:var(--coral)}
.cinfo small{color:var(--muted);font-size:14px}
.cinfo span{color:var(--navy);font-weight:600;font-size:17px;overflow-wrap:anywhere}
.ci-act{display:flex;gap:8px;margin-top:12px}
.ci-act .btn{padding:9px 20px}
.cinfo .copy{background:#fff;color:var(--navy);border:1px solid var(--line);border-radius:4px;padding:8px 16px}
.ci-soc{display:flex;justify-content:center;align-items:center;gap:10px;flex-wrap:wrap;margin-top:34px}
.ci-soc b{color:var(--navy);margin-inline-end:6px}
.ci-soc a{padding:7px 16px;border-radius:30px;background:var(--navy);color:#fff;text-decoration:none;font-size:14px}
.ci-soc a:hover{background:var(--coral)}
.contact{background:var(--cream)}
@media (max-width:1000px){.ci-grid{grid-template-columns:1fr 1fr}}
@media (max-width:820px){.about .wrap{grid-template-columns:1fr}}
@media (max-width:520px){.ci-grid{grid-template-columns:1fr}}
`;
fs.writeFileSync(f, '<!doctype html>\n' + d.documentElement.outerHTML); console.log('ok');
