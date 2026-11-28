# تقويم الشهر على قالب الهوية (agent/brand/identity-kit/identity-templates.pdf، الصفحة ٦، النسخة الفاتحة بطلب تغريد ٢٨ نوفمبر).
# python3 agent/tools/month_calendar_tpl.py data.json out.png
# data.json: {"month_label": "ديسمبر 2026م",
#   "events": [{"date": "ديسمبر 1–2", "name": "...", "place": "..."}],  (١–٣)
#   "days":   [{"date": "ديسمبر 5", "name": "..."}]}                    (حتى ٦)
# التاريخ بصيغة القالب: الشهر ثم الرقم. لا زخارف إضافية على القالب.
import json, sys, os, base64, re
from playwright.sync_api import sync_playwright
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brand')
KIT = os.path.join(R, 'identity-kit')
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
NAVY, COP = '#002544', '#b96740'
DS = 322  # قطر المعيّن


def dots(n=4):
    return '<span class="dots">' + '<i class="ci"></i>' * (n - 1) + '<i class="dm"></i></span>'


def diamond(it, x, y):
    pl = f'<div class="pl">{it["place"]}</div>' if it.get('place') else ''
    return (f'<div class="dw" style="left:{x - DS / 2}px;top:{y - DS / 2}px"><div class="d"></div>'
            f'<div class="t"><b>{re.sub(r"([0-9][0-9–]*)", r"<span dir=ltr>\1</span>", it["date"])}</b><div class="nm">{it["name"]}</div>{pl}</div></div>')


def row(items, y):
    step = DS + 4; n = len(items); x0 = 540 + (n - 1) * step / 2
    return ''.join(diamond(it, x0 - i * step, y) for i, it in enumerate(items))  # من اليمين


def html(d):
    ev, days = d.get('events', []), d.get('days', [])
    body = f'<h2 style="top:455px">{dots()}<span>أبرز ملتقيات القطاع غير الربحي</span>{dots()}</h2>'
    body += row(ev, 755)
    body += f'<h2 style="top:1010px">{dots()}<span>الأيام العالمية للقطاع غير الربحي</span>{dots()}</h2>'
    for k in range(0, len(days), 3):
        body += row(days[k:k + 3], 1310 + (k // 3) * 330)
    f = lambda w, fn: f"@font-face{{font-family:P;font-weight:{w};src:url(data:font/ttf;base64,{b64(os.path.join(KIT, fn))})}}"
    return f'''<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:L;unicode-range:U+0020-007F,U+2013;src:url(data:font/ttf;base64,{b64(os.path.join(KIT, 'avenir-800.ttf'))})}}
{f(400, 'IBMPlexArabic-Regular.ttf')}{f(600, 'IBMPlexArabic-SemiBold.ttf')}{f(700, 'IBMPlexArabic-Bold.ttf')}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{width:1080px;height:1920px;overflow:hidden}}
body{{width:1080px;height:1920px;background:#fff;font-family:L,P;color:{NAVY};position:relative;overflow:hidden}}
.frame{{position:absolute;inset:0;border:3px solid {NAVY}}}
.corner{{position:absolute;left:0;top:0;width:330px;height:360px;background:{COP};clip-path:polygon(0 0,100% 0,100% 30%,22% 100%,0 100%)}}
.corner{{clip-path:polygon(0 0,74% 0,100% 33%,24% 100%,0 72%)}}
.ml{{position:absolute;left:22px;top:118px;width:250px;white-space:nowrap;text-align:center;font-weight:700;font-size:36px;color:#fff}}
.logo{{position:absolute;right:62px;top:66px;width:360px}}
h2{{position:absolute;left:0;right:0;display:flex;align-items:center;justify-content:center;gap:30px;font-weight:700;font-size:44px;line-height:1}}
.dots{{display:inline-flex;align-items:center;gap:9px}} .dots i{{display:block;background:{COP}}}
.dm{{width:20px;height:20px;transform:rotate(45deg)}} .ci{{width:25px;height:25px;border-radius:50%}}
.dw{{position:absolute;width:{DS}px;height:{DS}px;display:flex;align-items:center;justify-content:center}}
.d{{position:absolute;inset:14.6%;background:{COP};transform:rotate(45deg)}}
.t{{position:relative;text-align:center;width:58%;line-height:1.28;color:#fff}}
.t b{{display:block;font-size:33px;font-weight:700;margin-bottom:3px}}
.nm{{font-size:23px;font-weight:400}} .pl{{font-size:19px;margin-top:3px;font-weight:600}}
.foot{{position:absolute;bottom:64px;left:62px;right:62px;display:flex;justify-content:space-between;align-items:center;font-size:25px;font-weight:600;direction:ltr}}
.foot .c{{display:flex;gap:34px}} .foot .c span{{display:flex;align-items:center;gap:10px}}
.foot .c i{{width:22px;height:22px;border-radius:50%;background:{COP};display:block}}
</style></head><body><div class="frame"></div>
<div class="corner"></div><div class="ml">{d['month_label']}</div>
<img class="logo" src="data:image/png;base64,{b64(os.path.join(R, 'logo_navy.png'))}">
{body}
<div class="foot"><div class="c"><span><i></i>hamedalthiabi.com</span><span><i></i>@hamedalthiabi</span></div>{dots(10)}</div>
</body></html>'''


if __name__ == '__main__':
    d = json.load(open(sys.argv[1], encoding='utf-8'))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.set_content(html(d)); pg.wait_for_timeout(400); pg.screenshot(path=sys.argv[2]); b.close()
