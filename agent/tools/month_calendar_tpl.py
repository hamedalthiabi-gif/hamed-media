# تقويم الشهر على قالب الهوية (agent/brand/identity-kit/identity-templates.pdf، الصفحة ٦): خلفية كحلية ومعيّنات نحاسية.
# python3 agent/tools/month_calendar_tpl.py data.json out.png
# data.json: {"month_label": "ديسمبر 2026م", "touch": "autumn"|"winter"|"none",
#   "events": [{"date": "1–2 ديسمبر", "name": "...", "place": "..."}],  (حتى ٣)
#   "days":   [{"date": "5 ديسمبر", "name": "..."}]}                    (حتى ٦)
import json, sys, os, base64, random, math
from playwright.sync_api import sync_playwright
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brand')
KIT = os.path.join(R, 'identity-kit')
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
NAVY, COP = '#002544', '#b96740'


def leaf(x, y, s, rot, col, op):
    return (f'<svg class="lf" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;transform:rotate({rot}deg);opacity:{op}" viewBox="0 0 100 100">'
            f'<path d="M50 4 C78 22 84 58 50 96 C16 58 22 22 50 4Z" fill="{col}"/>'
            f'<path d="M50 10 L50 94 M50 34 L64 24 M50 34 L36 24 M50 52 L67 40 M50 52 L33 40 M50 70 L64 60 M50 70 L36 60" stroke="{NAVY}" stroke-opacity=".35" stroke-width="2.2" fill="none"/></svg>')


def flake(x, y, s, op):
    arms = ''.join(f'<g transform="rotate({k*60} 50 50)"><path d="M50 50 L50 6 M50 22 L40 12 M50 22 L60 12 M50 36 L42 28 M50 36 L58 28" stroke="#cfdbe6" stroke-width="3" fill="none"/></g>' for k in range(6))
    return f'<svg class="lf" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:{op}" viewBox="0 0 100 100">{arms}</svg>'


def touches(kind):
    rnd = random.Random(7); out = ''
    spots = [(-30, 250, 150), (930, 520, 130), (-40, 1120, 140), (960, 1300, 120), (40, 1640, 110), (900, 1700, 150), (420, 1810, 90)]
    for x, y, s in spots:
        if kind == 'autumn':
            col = rnd.choice(['#c9783f', '#d99a4e', '#a85a33', '#e0b067'])
            out += leaf(x, y, s, rnd.randint(-70, 70), col, round(rnd.uniform(.6, .8), 2))
        elif kind == 'winter':
            out += flake(x, y, s, round(rnd.uniform(.18, .3), 2))
    return out


def dots(n=4):
    return '<span class="dots">' + '<i class="dm"></i>' + '<i class="ci"></i>' * (n - 2) + '<i class="dm"></i></span>'


def diamond(it, size):
    place = f'<div class="pl">{it["place"]}</div>' if it.get('place') else ''
    return (f'<div class="dw" style="width:{size}px;height:{size}px"><div class="d"></div>'
            f'<div class="t"><b>{it["date"]}</b><div class="nm">{it["name"]}</div>{place}</div></div>')


def html(d):
    ev = ''.join(diamond(e, 370) for e in d.get('events', []))
    days = d.get('days', [])
    rows = [days[i:i + 3] for i in range(0, len(days), 3)]
    dy = ''.join('<div class="row">' + ''.join(diamond(x, 310) for x in r) + '</div>' for r in rows)
    f = lambda w, fn: f"@font-face{{font-family:P;font-weight:{w};src:url(data:font/ttf;base64,{b64(os.path.join(KIT, fn))})}}"
    return f'''<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:L;font-weight:400 900;unicode-range:U+0020-007F,U+2013;src:url(data:font/ttf;base64,{b64(os.path.join(KIT,'avenir-800.ttf'))})}}
{f(400,'IBMPlexArabic-Regular.ttf')}{f(600,'IBMPlexArabic-SemiBold.ttf')}{f(700,'IBMPlexArabic-Bold.ttf')}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{width:1080px;height:1920px;overflow:hidden}}
body{{width:1080px;height:1920px;background:{NAVY};font-family:L,P;color:#fff;position:relative;overflow:hidden}}
.lf{{position:absolute;z-index:0}}
.corner{{position:absolute;left:-190px;top:-190px;width:440px;height:440px;background:{COP};transform:rotate(45deg);z-index:2}}
.ml{{position:absolute;left:28px;top:70px;font-weight:700;font-size:38px;z-index:3;direction:rtl}}
.logo{{position:absolute;right:70px;top:70px;width:400px;z-index:3}}
h2{{display:flex;align-items:center;justify-content:center;gap:26px;font-weight:700;font-size:50px;position:relative;z-index:3}}
.dots{{display:inline-flex;align-items:center;gap:12px}}
.dots i{{display:block;background:{COP}}} .dm{{width:24px;height:24px;transform:rotate(45deg)}} .ci{{width:30px;height:30px;border-radius:50%}}
.sec{{position:absolute;left:0;right:0;z-index:3}}
.row{{display:flex;justify-content:center;gap:34px;margin-top:-4px}}
.dw{{position:relative;display:flex;align-items:center;justify-content:center}}
.d{{position:absolute;inset:15%;background:{COP};transform:rotate(45deg);box-shadow:0 10px 28px rgba(0,0,0,.25)}}
.t{{position:relative;text-align:center;width:62%;line-height:1.3}}
.t b{{display:block;font-size:36px;font-weight:700;margin-bottom:4px}}
.nm{{font-size:26px;font-weight:600}} .pl{{font-size:22px;margin-top:4px;opacity:.9}}
.foot{{position:absolute;bottom:62px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:center;z-index:3;font-size:30px;font-weight:600;direction:ltr}}
</style></head><body>
{touches(d.get('touch','none'))}
<div class="corner"></div><div class="ml">{d['month_label']}</div>
<img class="logo" src="data:image/png;base64,{b64(os.path.join(R,'logo_white.png'))}">
<div class="sec" style="top:420px"><h2>{dots()}<span>أبرز ملتقيات القطاع غير الربحي</span>{dots()}</h2>
<div class="row" style="margin-top:30px">{ev}</div></div>
<div class="sec" style="top:{940 if d.get('events') else 420}px"><h2>{dots()}<span>الأيام العالمية للقطاع غير الربحي</span>{dots()}</h2>
<div style="margin-top:36px">{dy}</div></div>
<div class="foot">{dots(10)}<span>hamedalthiabi.com</span></div>
</body></html>'''


if __name__ == '__main__':
    d = json.load(open(sys.argv[1], encoding='utf-8'))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.set_content(html(d)); pg.wait_for_timeout(400); pg.screenshot(path=sys.argv[2]); b.close()
