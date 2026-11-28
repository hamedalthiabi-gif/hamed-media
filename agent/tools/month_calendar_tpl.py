# تقويم الشهر على قالب الهوية (agent/brand/identity-kit/identity-templates.pdf، الصفحة ٦، النسخة الفاتحة بطلب تغريد ٢٨ نوفمبر).
# python3 agent/tools/month_calendar_tpl.py data.json out.png
# data.json: {"month_label": "ديسمبر 2026م",
#   "events": [{"date": "ديسمبر 1–2", "name": "...", "place": "..."}],  (١–٣)
#   "days":   [{"date": "ديسمبر 5", "name": "..."}]}                    (حتى ٦)
# "touch": "autumn" لمسة خريفية (غصن وأوراق على الهامش)؛ ٤ أيام تُرتّب خلية معيّنات ١-٢-١.
# التاريخ بصيغة القالب: الشهر ثم الرقم. 
import json, sys, os, base64, re
from playwright.sync_api import sync_playwright
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brand')
KIT = os.path.join(R, 'identity-kit')
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
NAVY, COP = '#002544', '#b96740'
DS = 322  # قطر المعيّن


MAPLE = ('M50 97 L50 80 C41 83 31 85 21 87 L25 77 L7 67 L15 62 L5 45 L20 47 L23 38 L36 51 L32 22 L42 28 L50 5 '
         'L58 28 L68 22 L64 51 L77 38 L80 47 L95 45 L85 62 L93 67 L75 77 L79 87 C69 85 59 83 50 80 Z')
OAK = ('M50 97 L50 86 C44 86 40 82 41 77 C34 79 29 75 32 69 C25 69 22 63 27 58 C20 56 20 49 26 46 C21 41 24 34 31 34 '
       'C29 27 34 22 40 25 C40 17 46 12 50 6 C54 12 60 17 60 25 C66 22 71 27 69 34 C76 34 79 41 74 46 C80 49 80 56 73 58 '
       'C78 63 75 69 68 69 C71 75 66 79 59 77 C60 82 56 86 50 86 Z')
SHADES = [('#cf8a5c', '#b96740', '#8a4526'), ('#c47548', '#a85a35', '#7a3b20'), ('#d99a6c', '#b96740', '#94502c'), ('#b96740', '#9a5130', '#6e341c')]
DEFS = (
    '<svg width="0" height="0" style="position:absolute"><defs>'
    '<filter id="tex" x="-10%" y="-10%" width="120%" height="120%">'
    '<feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="3" seed="4" result="n"/>'
    '<feDiffuseLighting in="n" surfaceScale="1.2" lighting-color="#fff" result="l"><feDistantLight azimuth="235" elevation="55"/></feDiffuseLighting>'
    '<feComposite in="l" in2="SourceGraphic" operator="in" result="li"/>'
    '<feBlend in="SourceGraphic" in2="li" mode="multiply" result="m"/>'
    '<feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="9" result="w"/>'
    '<feDisplacementMap in="m" in2="w" scale="3.5" xChannelSelector="R" yChannelSelector="G" result="d"/>'
    '<feDropShadow dx="3" dy="7" stdDeviation="5" flood-color="#3a1f10" flood-opacity=".28"/></filter>'
    + ''.join(f'<radialGradient id="g{i}" cx="38%" cy="35%" r="75%"><stop offset="0" stop-color="{a}"/><stop offset=".55" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></radialGradient>' for i, (a, b, c) in enumerate(SHADES))
    + '</defs></svg>')


def leaf(x, y, s, rot, k, kind='maple', blur=0):
    path = MAPLE if kind == 'maple' else OAK
    a, b, c = SHADES[k % len(SHADES)]
    veins = ('M50 96 L50 9 M50 79 L23 40 M50 79 L77 40 M50 79 L12 64 M50 79 L88 64 M36 60 L30 50 M64 60 L70 50' if kind == 'maple'
             else 'M50 96 L50 9 M50 70 L33 63 M50 70 L67 63 M50 55 L29 46 M50 55 L71 46 M50 40 L34 31 M50 40 L66 31 M50 27 L43 20 M50 27 L57 20')
    bl = f';filter:blur({blur}px)' if blur else ''
    return (f'<svg class="lf" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;transform:rotate({rot}deg){bl}" viewBox="0 0 100 100">'
            f'<g filter="url(#tex)"><path d="{path}" fill="url(#g{k % len(SHADES)})"/>'
            f'<path d="{veins}" stroke="{c}" stroke-opacity=".75" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
            f'<path d="{veins}" stroke="{a}" stroke-opacity=".5" stroke-width=".5" fill="none" transform="translate(.7 .3)"/>'
            f'<path d="M50 97 L50 100" stroke="{c}" stroke-width="2"/></g></svg>')


def touches(kind):
    # لمسة نوفمبر: أوراق خريف واقعية بدرجات النحاسي من الهوية، على الهوامش فقط
    if kind != 'autumn': return ''
    L = [  # x, y, size, rot, shade, kind, blur
        (196, 236, 92, 25, 0, 'maple', 0), (276, 300, 64, -40, 1, 'oak', 0), (150, 330, 54, 75, 2, 'maple', 1.2),
        (-34, 1010, 150, -20, 1, 'maple', 0), (40, 1200, 70, 60, 2, 'oak', 0), (-20, 1370, 96, 140, 3, 'maple', 0),
        (60, 1530, 56, -70, 0, 'oak', 1.5), (-10, 1640, 110, 15, 2, 'maple', 0),
        (960, 1000, 120, 40, 0, 'maple', 0), (990, 1190, 66, -30, 3, 'oak', 1), (930, 1330, 92, 110, 1, 'maple', 0),
        (980, 1500, 70, -80, 2, 'oak', 0), (850, 1600, 150, -25, 0, 'maple', 0), (970, 1700, 96, 60, 3, 'maple', 0),
        (760, 1720, 60, 130, 1, 'oak', 1.5), (520, 1760, 42, -20, 2, 'maple', 2)]
    return DEFS + ''.join(leaf(*l) for l in L)


def dots(n=4):
    return '<span class="dots">' + '<i class="ci"></i>' * (n - 1) + '<i class="dm"></i></span>'


def diamond(it, x, y, ds=None):
    ds = ds or DS
    pl = f'<div class="pl">{it["place"]}</div>' if it.get('place') else ''
    return (f'<div class="dw" style="left:{x - ds / 2}px;top:{y - ds / 2}px;width:{ds}px;height:{ds}px"><div class="d"></div>'
            f'<div class="t"><b>{re.sub(r"([0-9][0-9–]*)", r"<span dir=ltr>\1</span>", it["date"])}</b><div class="nm" style="font-size:{20 if len(it['name']) > 40 else 22}px">{it["name"]}</div>{pl}</div></div>')


def row(items, y, ds=None):
    ds = ds or DS; step = ds + 6; n = len(items); x0 = 540 + (n - 1) * step / 2
    return ''.join(diamond(it, x0 - i * step, y, ds) for i, it in enumerate(items))  # من اليمين


def cluster(items, y0):
    # معيّنات متداخلة كخلية: ١ ثم ٢ ثم ١ (أو ١ ثم ٢ ثم ٢…)، من اليمين
    h = DS / 2 + 3; out = ''; y = y0; i = 0; pattern = [1, 2] * 4
    for k in pattern:
        if i >= len(items): break
        grp = items[i:i + k]; i += k
        xs = [540] if len(grp) == 1 else [540 + h, 540 - h]
        out += ''.join(diamond(it, x, y) for it, x in zip(grp, xs)); y += h
    return out, y - h


def html(d):
    ev, days = d.get('events', []), d.get('days', [])
    body = f'<h2 style="top:440px">{dots()}<span>أبرز ملتقيات القطاع غير الربحي</span>{dots()}</h2>'
    body += row(ev, 720, 350 if len(ev) <= 2 else DS)
    body += f'<h2 style="top:975px">{dots()}<span>الأيام العالمية للقطاع غير الربحي</span>{dots()}</h2>'
    if len(days) == 4:
        c, _ = cluster(days, 1215); body += c
    else:
        for k in range(0, len(days), 3):
            body += row(days[k:k + 3], 1240 + (k // 3) * 330)
    body = touches(d.get('touch')) + body
    f = lambda w, fn: f"@font-face{{font-family:P;font-weight:{w};src:url(data:font/ttf;base64,{b64(os.path.join(KIT, fn))})}}"
    return f'''<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:L;unicode-range:U+0020-007F,U+2013;src:url(data:font/ttf;base64,{b64(os.path.join(KIT, 'avenir-800.ttf'))})}}
{f(400, 'IBMPlexArabic-Regular.ttf')}{f(600, 'IBMPlexArabic-SemiBold.ttf')}{f(700, 'IBMPlexArabic-Bold.ttf')}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{width:1080px;height:1920px;overflow:hidden}}
body{{width:1080px;height:1920px;background:#f8f5ef;font-family:L,P;color:{NAVY};position:relative;overflow:hidden}}
.frame{{position:absolute;inset:0;border:3px solid {NAVY};z-index:5;pointer-events:none}}
.wm{{position:absolute;opacity:.08}}
.corner{{position:absolute;left:0;top:0;width:330px;height:360px;background:{COP};clip-path:polygon(0 0,100% 0,100% 30%,22% 100%,0 100%)}}
.corner{{clip-path:polygon(0 0,74% 0,100% 33%,24% 100%,0 72%);background:{COP}}}
.ml{{position:absolute;left:22px;top:118px;width:250px;white-space:nowrap;text-align:center;font-weight:700;font-size:36px;color:#fff}}
.logo{{position:absolute;right:62px;top:66px;width:360px}}
h2{{position:absolute;left:0;right:0;display:flex;align-items:center;justify-content:center;gap:30px;font-weight:700;font-size:44px;line-height:1}}
.dots{{display:inline-flex;align-items:center;gap:9px}} .dots i{{display:block;background:{COP}}}
.dm{{width:20px;height:20px;transform:rotate(45deg)}} .ci{{width:25px;height:25px;border-radius:50%}}
.lf{{position:absolute}}\n.dw{{position:absolute;display:flex;align-items:center;justify-content:center}}
.d{{position:absolute;inset:14.6%;background:{COP};transform:rotate(45deg);box-shadow:0 16px 30px rgba(140,70,35,.28);outline:2px solid rgba(248,245,239,.6);outline-offset:-10px}}
.t{{position:relative;text-align:center;width:60%;line-height:1.26;color:#fff}}
.t b{{display:block;font-size:33px;font-weight:700;margin-bottom:3px}}
.nm{{font-size:22px;font-weight:400}} .pl{{font-size:19px;margin-top:3px;font-weight:600}}
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
