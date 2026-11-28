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


def leaf(x, y, s, rot, col, op=1):
    return (f'<svg class="lf" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;transform:rotate({rot}deg);opacity:{op}" viewBox="0 0 100 100">'
            f'<path d="M50 3 C80 20 86 60 50 97 C14 60 20 20 50 3Z" fill="{col}"/>'
            f'<path d="M50 8 L50 97 M50 32 L63 22 M50 32 L37 22 M50 50 L66 38 M50 50 L34 38 M50 68 L63 58 M50 68 L37 58" stroke="#fff" stroke-opacity=".55" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>')


def touches(kind):
    # لمسة نوفمبر: غصن خريفي يتدلّى من مثلث الشهر، وأوراق تتساقط على الهامشين حتى التذييل
    if kind != 'autumn': return ''
    C1, C2, C3, C4 = '#c46a3a', '#e0a35a', '#9a4a28', '#d4893f'
    br = ('<svg class="lf" style="left:170px;top:225px;width:300px;height:200px" viewBox="0 0 300 200">'
          '<path d="M10 10 C70 30 120 60 170 100 C200 125 235 140 280 150" stroke="#002544" stroke-width="3" fill="none" stroke-linecap="round" opacity=".55"/></svg>')
    L = [(186, 222, 56, 70, C2), (240, 258, 50, -20, C1), (296, 296, 60, 115, C3), (356, 322, 48, 30, C4), (416, 350, 40, 150, C1),
         (20, 1040, 78, -25, C1), (88, 1150, 50, 50, C4), (14, 1290, 62, 160, C3), (70, 1420, 44, -70, C2), (24, 1560, 70, 20, C4),
         (978, 1060, 58, 35, C2), (940, 1200, 80, -60, C1), (996, 1350, 46, 80, C3), (950, 1500, 64, 130, C4),
         (860, 1640, 96, -35, C1), (950, 1680, 70, 40, C2), (900, 1760, 52, 110, C3), (800, 1720, 44, -80, C4),
         (520, 1752, 34, 120, C2), (450, 1776, 28, -40, C1)]
    wm = '<svg class="wm" style="left:250px;top:1080px;width:580px;height:580px;transform:rotate(-20deg)" viewBox="0 0 100 100"><path d="M50 3 C80 20 86 60 50 97 C14 60 20 20 50 3Z" fill="#b96740"/></svg>'
    return wm + br + ''.join(leaf(x, y, sz, r, c) for x, y, sz, r, c in L)


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
body{{width:1080px;height:1920px;background:radial-gradient(ellipse 70% 40% at 88% 6%,#f9e2c6 0,rgba(249,226,198,0) 70%),radial-gradient(ellipse 80% 45% at 8% 100%,#f5d6b4 0,rgba(245,214,180,0) 70%),#fbf5ec;font-family:L,P;color:{NAVY};position:relative;overflow:hidden}}
.frame{{position:absolute;inset:0;border:3px solid {NAVY};z-index:5;pointer-events:none}}
.wm{{position:absolute;opacity:.08}}
.corner{{position:absolute;left:0;top:0;width:330px;height:360px;background:{COP};clip-path:polygon(0 0,100% 0,100% 30%,22% 100%,0 100%)}}
.corner{{clip-path:polygon(0 0,74% 0,100% 33%,24% 100%,0 72%);background:linear-gradient(150deg,#cf8352,#a9562d);box-shadow:inset 0 0 0 1px rgba(255,255,255,.2)}}
.ml{{position:absolute;left:22px;top:118px;width:250px;white-space:nowrap;text-align:center;font-weight:700;font-size:36px;color:#fff}}
.logo{{position:absolute;right:62px;top:66px;width:360px}}
h2{{position:absolute;left:0;right:0;display:flex;align-items:center;justify-content:center;gap:30px;font-weight:700;font-size:44px;line-height:1}}
.dots{{display:inline-flex;align-items:center;gap:9px}} .dots i{{display:block;background:{COP}}}
.dm{{width:20px;height:20px;transform:rotate(45deg)}} .ci{{width:25px;height:25px;border-radius:50%}}
.lf{{position:absolute}}\n.dw{{position:absolute;display:flex;align-items:center;justify-content:center}}
.d{{position:absolute;inset:14.6%;background:linear-gradient(135deg,#d08350 0%,#b96740 55%,#9e5230 100%);transform:rotate(45deg);box-shadow:0 16px 30px rgba(140,70,35,.28);outline:2px solid rgba(255,240,222,.55);outline-offset:-10px}}
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
