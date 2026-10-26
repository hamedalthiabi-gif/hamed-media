# انفوجرافيك خطوات/عناصر بالهوية الصحيحة للتاريخ
# python3 agent/tools/infographic.py old|new "العنوان" "الوسم" img/out.png "خطوة ١|وصفها" "خطوة ٢|وصفها" ...
#   ٣–٦ عناصر، العنوان قصير، والوصف سطر أو سطران. الخط لا يدعم « » : . ( ) فلا تستخدمها. يصلح غلافًا للينكدإن وصورة لإكس.
import sys, os
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from old_identity import clean, wrap, F, B

THEMES = {
    'old': dict(main=(15, 104, 111), bg=(246, 247, 246), ink=(36, 52, 56), mut=(96, 114, 117), soft=(15, 104, 111, 22),
                logo='old_logo.png', on=(255, 255, 255), line=(205, 222, 223)),
    'new': dict(main=(0, 37, 68), bg=(248, 246, 242), ink=(0, 37, 68), mut=(98, 108, 120), soft=(187, 104, 65, 26),
                logo='logo_navy.png', on=(255, 255, 255), accent=(187, 104, 65), line=(226, 214, 204)),
}


def make(theme, title, tag, out, items, W=1080, H=1350):
    T = THEMES[theme]; M = T['main']; A = T.get('accent', M)
    im = Image.new('RGB', (W, H), T['bg']); deco = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(deco)
    dd.ellipse([W - 230, -230, W + 230, 230], fill=T['soft']); dd.ellipse([-260, H - 420, 260, H + 100], fill=T['soft'])
    im.paste(deco, (0, 0), deco); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=M); d.rectangle([0, H - 36, W, H], fill=M)
    lg = Image.open(B + T['logo']).convert('RGBA'); lw = 250; lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
    im.paste(lg, ((W - lw) // 2, 60), lg)
    y = 60 + lg.height + 50
    ft = F(600, 62)
    for l in wrap(d, title, ft, 900):
        d.text((W // 2, y), l, font=ft, fill=M, anchor='mt', direction='rtl'); y += 86
    d.rectangle([W // 2 - 40, y + 8, W // 2 + 40, y + 14], fill=A); y += 50
    n = len(items); bottom = H - 200
    gap = 22; ch = min(190, (bottom - y - gap * (n - 1)) // n)
    fh, fd, fn = F(600, 42), F(400, 32), F(600, 46)
    x0, x1 = 70, W - 70
    for i, it in enumerate(items):
        head, _, desc = it.partition('|'); cy = y + i * (ch + gap)
        d.rounded_rectangle([x0, cy, x1, cy + ch], radius=28, fill=(255, 255, 255), outline=T['line'], width=2)
        cx, r = x1 - 80, 40
        d.ellipse([cx - r, cy + ch // 2 - r, cx + r, cy + ch // 2 + r], fill=M)
        d.text((cx, cy + ch // 2), '١٢٣٤٥٦٧٨٩'[i], font=fn, fill=T['on'], anchor='mm')
        if i < n - 1:  # خط يصل الدوائر
            d.line([cx, cy + ch // 2 + r, cx, cy + ch + gap + ch // 2 - r], fill=A, width=4)
        tx = cx - r - 34; lines = wrap(d, desc, fd, tx - x0 - 40) if desc else []
        block = 56 + len(lines) * 44; ty = cy + (ch - block) // 2
        d.text((tx, ty), clean(head), font=fh, fill=M, anchor='ra', direction='rtl')
        for j, l in enumerate(lines):
            d.text((tx, ty + 60 + j * 44), l, font=fd, fill=T['ink'], anchor='ra', direction='rtl')
    tag = clean(tag)
    if tag:
        f2 = F(600, 34); tw = d.textlength(tag, font=f2, direction='rtl'); by = H - 150
        d.rounded_rectangle([W // 2 - tw / 2 - 30, by, W // 2 + tw / 2 + 30, by + 66], radius=33, fill=M)
        d.text((W // 2, by + 33), tag, font=f2, fill=T['on'], anchor='mm', direction='rtl')
    im.save(out)


if __name__ == '__main__':
    a = sys.argv[1:]
    make(a[0], a[1], a[2], a[3], a[4:])
