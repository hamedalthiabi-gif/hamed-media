# تصاميم الهوية السابقة (تُستخدم حتى ١٠ نوفمبر ٢٠٢٦ فقط؛ من ١١ نوفمبر تُستخدم الهوية الجديدة)
# بطاقة:  python3 agent/tools/old_identity.py card "العنوان" "الوسم" img/out.png
# موشن:   python3 agent/tools/old_identity.py motion img/out.mp4 "شريحة ١" "شريحة ٢" ... [--tag "الوسم"]
#   كل شريحة نص قصير (سطر إلى ثلاثة أسطر)، ٥ ثوانٍ لكل شريحة، هادئ وبلا صوت، أقل من دقيقة.
import sys, os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brand') + '/'
TEAL = (15, 104, 111); BG = (246, 247, 246); INK = (36, 52, 56); MUT = (110, 128, 131); WHITE = (255, 255, 255)
F = lambda w, s: ImageFont.truetype(B + f'plex-{w}.ttf', int(s), layout_engine=ImageFont.Layout.RAQM)


def wrap(d, t, f, mw):
    out, cur = [], ''
    for w in t.split():
        c = (cur + ' ' + w).strip()
        if d.textlength(c, font=f, direction='rtl') <= mw: cur = c
        else: out.append(cur); cur = w
    return out + [cur]


def logo(w):
    lg = Image.open(B + 'old_logo.png').convert('RGBA')
    return lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS)


def fit(d, text, maxw, maxl, s0, smin):
    s = s0
    while True:
        f = F(600, s); L = [l for part in text.split('|') for l in wrap(d, part.strip(), f, maxw)]
        if len(L) <= maxl or s <= smin: return f, L, s
        s -= 4


def base(W, H):
    im = Image.new('RGB', (W, H), BG)
    deco = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(deco)
    dd.ellipse([W - 260, -260, W + 260, 260], fill=TEAL + (18,)); dd.ellipse([-300, H - 520, 300, H + 80], fill=TEAL + (14,))
    dd.ellipse([W - 170, H - 330, W - 90, H - 250], fill=TEAL + (28,))
    im.paste(deco, (0, 0), deco); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=TEAL); d.rectangle([0, H - 110, W, H], fill=TEAL)
    d.text((W // 2, H - 55), 'استدامة العطاء وأثرٌ يمتد', font=F(400, 34), fill=WHITE, anchor='mm', direction='rtl')
    lg = logo(380); im.paste(lg, ((W - 380) // 2, 110), lg)
    return im, d


def card(title, tag, out, W=1080, H=1350):
    im, d = base(W, H)
    f, L, s = fit(d, title, 880, 4, 80, 52)
    lh = int(s * 1.6); total = len(L) * lh; y0 = (H - total) // 2 + 30
    d.rectangle([W // 2 - 40, y0 - 60, W // 2 + 40, y0 - 54], fill=TEAL)
    for i, l in enumerate(L):
        d.text((W // 2, y0 + i * lh), l, font=f, fill=TEAL, anchor='mt', direction='rtl')
    if tag:
        ft = F(600, 38); tw = d.textlength(tag, font=ft, direction='rtl'); by = y0 + total + 50
        d.rounded_rectangle([W // 2 - tw / 2 - 34, by, W // 2 + tw / 2 + 34, by + 74], radius=37, fill=TEAL)
        d.text((W // 2, by + 37), tag, font=ft, fill=WHITE, anchor='mm', direction='rtl')
    im.save(out)


def motion(out, slides, tag='', W=1080, H=1920, FPS=30, SEC=5.0):
    slides = slides[:11]  # حد أقصى ٥٥ ثانية
    tmp = tempfile.mkdtemp(); n = 0
    bgim, _ = base(W, H)
    for k, s in enumerate(slides):
        d0 = ImageDraw.Draw(bgim.copy())
        f, L, sz = fit(d0, s, 900, 4, 84, 56)
        lh = int(sz * 1.6); total = len(L) * lh; y0 = (H - total) // 2
        for i in range(int(SEC * FPS)):
            t = i / FPS
            a = min(1, t / 1.2) * min(1, (SEC - t) / 0.9)  # ظهور واختفاء هادئ
            a = max(0, a); dy = int((1 - min(1, t / 1.2)) ** 3 * 30)
            fr = bgim.copy(); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            for j, l in enumerate(L):
                d.text((W // 2, y0 + j * lh + dy), l, font=f, fill=TEAL + (int(255 * a),), anchor='mt', direction='rtl')
            if tag:
                ft = F(600, 36); tw = d.textlength(tag, font=ft, direction='rtl'); by = H - 330
                d.rounded_rectangle([W // 2 - tw / 2 - 30, by, W // 2 + tw / 2 + 30, by + 70], radius=35, fill=TEAL)
                d.text((W // 2, by + 35), tag, font=ft, fill=WHITE, anchor='mm', direction='rtl')
            n_ = len(slides); gx = W // 2 + (n_ - 1) * 15
            for m in range(n_):  # نقاط تقدم من اليمين إلى اليسار
                x = gx - m * 30; r = 7 if m == k else 5
                d.ellipse([x - r, H - 200 - r, x + r, H - 200 + r], fill=TEAL + ((255 if m <= k else 70),))
            fr.paste(lay, (0, 0), lay); fr.save(f'{tmp}/{n:05d}.png'); n += 1
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{tmp}/%05d.png',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-an', out], check=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'card': card(a[1], a[2], a[3])
    else:
        tag = ''
        if '--tag' in a: i = a.index('--tag'); tag = a[i + 1]; a = a[:i] + a[i + 2:]
        motion(a[1], a[2:], tag)
