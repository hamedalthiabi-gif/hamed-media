# تصميم «تقويم الشهر» للقطاع غير الربحي: الملتقيات والمؤتمرات والمعارض + الأيام العالمية، بلمسة موسمية للشهر.
# python3 agent/tools/month_calendar.py data.json out.png
# data.json: {"month": 11, "year": 2026, "identity": "old"|"new", "ramadan": false,
#   "events": [{"date": "٢ نوفمبر", "from": 2, "to": 2, "name": "ملتقى ...", "place": "الرياض، ..."}],   (حتى ٨)
#   "days":   [{"date": "١٦ نوفمبر", "from": 16, "name": "اليوم الدولي للتسامح"}]}                       (حتى ٦)
# from/to أرقام لاتينية لتلوين الأيام في التقويم المصغر.
# الهوية: old حتى أكتوبر/نوفمبر ٢٠٢٦، new من ديسمبر ٢٠٢٦. الخط لا يدعم الأرقام اللاتينية و«-»: اكتب الأرقام عربية و«إلى».
import json, sys, os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brand') + '/'
F = lambda w, s: ImageFont.truetype(B + f'plex-{w}.ttf', int(s), layout_engine=ImageFont.Layout.RAQM)
AR = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
MONTHS = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
ID = {
 'old': dict(main=(15, 104, 111), accent=(15, 104, 111), bg=(244, 242, 237), ink=(28, 52, 58), card=(255, 255, 255), logo='old_logo.png'),
 'new': dict(main=(0, 37, 68), accent=(187, 104, 65), bg=(248, 245, 239), ink=(0, 37, 68), card=(255, 255, 255), logo='logo_navy.png'),
}
SEASON = {12: 'winter', 1: 'winter', 2: 'winter', 3: 'spring', 4: 'spring', 5: 'spring',
          6: 'summer', 7: 'summer', 8: 'summer', 9: 'autumn', 10: 'autumn', 11: 'autumn'}


def clean(t):
    for c in '«»:.-–—()': t = t.replace(c, ' ')
    return ' '.join(t.translate(AR).split())


def wrap(d, t, f, mw):
    out, cur = [], ''
    for w in clean(t).split():
        c = (cur + ' ' + w).strip()
        if d.textlength(c, font=f, direction='rtl') <= mw: cur = c
        else: out.append(cur); cur = w
    return out + [cur]


# ---------- اللمسات الموسمية (رسم متجهي هادئ) ----------
def leaf(size, col, rot):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = size / 2; L = size * 0.46; Wd = size * 0.2; pts = []
    for i in range(61):  # ورقة لوزية بطرف مدبب
        t = i / 60 * math.pi * 2; y = -L * math.cos(t); x = Wd * math.sin(t) * (1 - 0.35 * math.cos(t)) ** 1.2
        pts.append((c + x, c + y))
    d.polygon(pts, fill=col)
    vein = tuple(max(0, v - 45) for v in col[:3]) + (min(255, col[3] + 20),)
    d.line([(c, c - L * 0.9), (c, c + L + size * 0.04)], fill=vein, width=max(2, size // 50))
    for k in range(1, 5):
        yy = c - L * 0.6 + k * L * 0.32
        for sgn in (1, -1): d.line([(c, yy), (c + sgn * Wd * 0.7, yy - L * 0.18)], fill=vein, width=max(1, size // 80))
    return im.rotate(rot, resample=Image.BICUBIC, expand=False)


def flake(size, col):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size / 2; w = max(2, size // 28)
    for k in range(6):
        a = math.radians(k * 60); x, y = c + c * 0.9 * math.cos(a), c + c * 0.9 * math.sin(a)
        d.line([(c, c), (x, y)], fill=col, width=w)
        for s in (0.45, 0.68):
            bx, by = c + c * s * math.cos(a), c + c * s * math.sin(a)
            for da in (35, -35):
                b = a + math.radians(da); d.line([(bx, by), (bx + c * 0.22 * math.cos(b), by + c * 0.22 * math.sin(b))], fill=col, width=w)
    return im


def blossom(size, col):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size / 2; r = size * 0.22
    for k in range(5):
        a = math.radians(k * 72 - 90); x, y = c + r * math.cos(a), c + r * math.sin(a)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    d.ellipse([c - r * 0.45, c - r * 0.45, c + r * 0.45, c + r * 0.45], fill=(235, 196, 92, col[3]))
    return im


def sun(size, col):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size / 2
    d.ellipse([c - size * 0.2, c - size * 0.2, c + size * 0.2, c + size * 0.2], outline=col, width=max(2, size // 30))
    for k in range(12):
        a = math.radians(k * 30); d.line([(c + size * 0.28 * math.cos(a), c + size * 0.28 * math.sin(a)),
                                         (c + size * 0.45 * math.cos(a), c + size * 0.45 * math.sin(a))], fill=col, width=max(2, size // 30))
    return im


def crescent(size, col, bg):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([0, 0, size, size], fill=col); d.ellipse([size * 0.28, -size * 0.05, size * 1.18, size * 0.95], fill=(0, 0, 0, 0))
    return im


def decorate(im, month, ident, ramadan):
    W, H = im.size; rnd = random.Random(month * 31 + (1 if ident == 'new' else 0))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    s = SEASON[month]
    spots = [(-40, 330), (W - 150, 300), (W - 120, 900), (-50, 1250), (W - 170, 1560), (30, 1700), (W // 2 + 260, 60), (60, 60)]
    for i, (x, y) in enumerate(spots):
        sz = rnd.randint(110, 190)
        if s == 'autumn':
            col = rnd.choice([(196, 112, 52), (214, 146, 62), (170, 86, 46), (222, 170, 90)]) + (rnd.randint(170, 225),)
            el = leaf(sz, col, rnd.randint(-80, 80))
        elif s == 'winter':
            el = flake(sz, (150, 185, 205, rnd.randint(110, 170)))
        elif s == 'spring':
            el = blossom(int(sz * 0.8), rnd.choice([(232, 168, 176), (240, 196, 200), (214, 140, 150)]) + (rnd.randint(150, 210),))
        else:
            el = sun(sz, (226, 170, 80, rnd.randint(110, 160)))
        lay.alpha_composite(el, (int(x), int(y)))
    if ramadan:
        c = ID[ident]['accent']; lay.alpha_composite(crescent(150, c + (200,), None), (W - 230, 1640))
    sh = lay.filter(ImageFilter.GaussianBlur(6)); sh2 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh2.putalpha(sh.getchannel('A').point(lambda a: a // 4))
    im.alpha_composite(sh2, (6, 10)); im.alpha_composite(lay)


# ---------- التصميم ----------
def card(im, box, r, fill):
    x0, y0, x1, y1 = box
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([x0 + 4, y0 + 8, x1 + 4, y1 + 8], r, fill=(0, 0, 0, 40))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(im).rounded_rectangle(box, r, fill=fill + (255,))


def minical(im, data, C, y0, y1):
    # تقويم الشهر مصغرًا، وتُلوَّن فيه أيام الفعاليات والمناسبات
    import calendar as cal
    W = im.size[0]; month, year = int(data['month']), int(data['year'])
    marked = set()
    for it in data.get('events', []) + data.get('days', []):
        a = it.get('from'); b = it.get('to', a)
        if a: marked.update(range(int(a), int(b) + 1))
    first, n = cal.monthrange(year, month); first = (first + 1) % 7  # الأحد أولًا
    rows = math.ceil((first + n) / 7); cw = 110; ch = min(78, (y1 - y0 - 140) / (rows + 1))
    if ch < 46: return
    gw = cw * 7; x0 = (W - gw) / 2; top = y0 + max(0, (y1 - y0 - 120 - ch * (rows + 1)) / 2)
    card(im, [x0 - 30, top, x0 + gw + 30, top + 110 + ch * (rows + 1)], 26, (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.text((W / 2, top + 50), MONTHS[month - 1] + ' ' + str(year).translate(AR), font=F(600, 40), fill=C['main'], anchor='mm', direction='rtl')
    names = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
    for k, nm in enumerate(names):
        d.text((x0 + gw - (k + 0.5) * cw, top + 100), nm, font=F(400, 24), fill=(130, 140, 145), anchor='mm', direction='rtl')
    for day in range(1, n + 1):
        i = first + day - 1; r, c = divmod(i, 7)
        cx = x0 + gw - (c + 0.5) * cw; cy = top + 100 + (r + 1) * ch
        if day in marked:
            d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=C['accent'])
            d.text((cx, cy), str(day).translate(AR), font=F(600, 32), fill=(255, 255, 255), anchor='mm')
        else:
            d.text((cx, cy), str(day).translate(AR), font=F(400, 32), fill=C['ink'], anchor='mm')


def make(data, out, W=1080, H=1920):
    ident = data.get('identity', 'old'); C = ID[ident]; month = int(data['month'])
    im = Image.new('RGBA', (W, H), C['bg'] + (255,))
    decorate(im, month, ident, data.get('ramadan', False))
    d = ImageDraw.Draw(im)
    # الترويسة: الشعار يسارًا وشارة الشهر يمينًا
    lg = Image.open(B + C['logo']).convert('RGBA'); lw = 330 if ident == 'old' else 360
    lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
    card(im, [50, 60, 50 + lw + 40, 60 + lg.height + 40], 22, (255, 255, 255)); im.alpha_composite(lg, (70, 80))
    bw, bh = 230, 210; bx = W - 60 - bw
    ImageDraw.Draw(im).rounded_rectangle([bx, 0, bx + bw, bh], 26, fill=C['main'] + (255,))
    d = ImageDraw.Draw(im)
    d.text((bx + bw / 2, 75), MONTHS[month - 1], font=F(600, 52), fill=(255, 255, 255), anchor='mm', direction='rtl')
    d.text((bx + bw / 2, 145), str(data['year']).translate(AR), font=F(600, 52), fill=(255, 255, 255), anchor='mm')

    def section(y, title, items, cols, ch):
        ft = F(600, 44); tw = d.textlength(title, font=ft, direction='rtl')
        n = len(items); rows = max(1, math.ceil(n / cols)); gap = 26; px = 70
        top = y + 40; hgt = 60 + rows * ch + (rows - 1) * gap + 40
        ImageDraw.Draw(im).rounded_rectangle([px - 20, top, W - px + 20, top + hgt], 34, outline=C['main'] + (255,), width=3)
        ImageDraw.Draw(im).rounded_rectangle([W / 2 - tw / 2 - 40, y + 8, W / 2 + tw / 2 + 40, y + 72], 32, fill=(232, 238, 238, 255) if ident == 'old' else (236, 230, 220, 255))
        d2 = ImageDraw.Draw(im); d2.text((W / 2, y + 40), clean(title), font=ft, fill=C['main'], anchor='mm', direction='rtl')
        cw = (W - 2 * px - (cols - 1) * gap) / cols
        for i, it in enumerate(items):
            r_, c_ = divmod(i, cols)
            if r_ == rows - 1 and n % cols: c_ += (cols - n % cols) / 2  # توسيط الصف الأخير
            x1 = W - px - c_ * (cw + gap); x0 = x1 - cw; y0 = top + 60 + r_ * (ch + gap)
            card(im, [x0, y0, x1, y0 + ch], 18, C['card'])
            dd = ImageDraw.Draw(im)
            dd.rectangle([x0 + cw / 2 - 45, y0 - 14, x0 + cw / 2 + 45, y0 + 14], fill=C['accent'] + (255,))  # شريط لاصق
            dd.text(((x0 + x1) / 2, y0 + 52), clean(it['date']), font=F(600, 38), fill=C['main'], anchor='mm', direction='rtl')
            fn = F(400, 32 if cols == 2 else 30)
            L = wrap(dd, it['name'], fn, cw - 40)[:3]
            for j, l in enumerate(L):
                dd.text(((x0 + x1) / 2, y0 + 98 + j * 44), l, font=fn, fill=C['ink'], anchor='mm', direction='rtl')
            if it.get('place'):
                fp = F(400, 24); pl = wrap(dd, it['place'], fp, cw - 70)[0]
                dd.rounded_rectangle([x0 + 22, y0 + ch - 66, x1 - 22, y0 + ch - 20], 12, fill=C['main'] + (255,))
                dd.text(((x0 + x1) / 2, y0 + ch - 43), pl, font=fp, fill=(255, 255, 255), anchor='mm', direction='rtl')
        return top + hgt

    y = 330
    if data.get('events'):
        y = section(y, 'أبرز ملتقيات ومؤتمرات القطاع غير الربحي', data['events'][:8], 2, 250) + 50
    if data.get('days'):
        y = section(y, 'الأيام العالمية للقطاع غير الربحي', data['days'][:6], 3, 170) + 50
    minical(im, data, C, y, H - 110)
    d = ImageDraw.Draw(im)
    if ident == 'new':
        d.text((W / 2, H - 50), 'hamedalthiabi.com', font=ImageFont.truetype(B + 'plex-latin-400.ttf', 30), fill=C['main'], anchor='mm')
    im.convert('RGB').save(out)


if __name__ == '__main__':
    make(json.load(open(sys.argv[1], encoding='utf-8')), sys.argv[2])
