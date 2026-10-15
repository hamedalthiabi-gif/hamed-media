import sys, textwrap
from PIL import Image, ImageDraw, ImageFont
import os; B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','brand')+'/'
W,H=1080,1920
NAVY=(0,37,68); CORAL=(187,104,65); CREAM=(248,245,239)
def font(w,s): return ImageFont.truetype(B+f'plex-{w}.ttf',s,layout_engine=ImageFont.Layout.RAQM)
def wrap(d,t,f,maxw):
    words=t.split(); lines=[]; cur=''
    for w in words:
        c=(cur+' '+w).strip()
        if d.textlength(c,font=f,direction='rtl')<=maxw: cur=c
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
def make(title, tag='استدامة العطاء', out='cover.png'):
    im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
    d.polygon([(0,0),(330,0),(0,330)],fill=CORAL)
    d.polygon([(W,H),(W,H-330),(W-330,H)],fill=CORAL)
    lg=Image.open(B+'logo_white.png').convert('RGBA'); r=420/lg.width
    lg=lg.resize((420,int(lg.height*r)),Image.LANCZOS); im.paste(lg,((W-420)//2,400),lg)
    # dots
    y=400+lg.height+60
    for i,x in enumerate(range(W//2-75,W//2+90,50)):
        if i%2: d.polygon([(x,y-9),(x+9,y),(x,y+9),(x-9,y)],fill=CORAL)
        else: d.ellipse([x-8,y-8,x+8,y+8],fill=CORAL)
    # title
    size=92
    while True:
        f=font(600,size); lines=wrap(d,title,f,860)
        if len(lines)<=4 or size<=60: break
        size-=6
    lh=int(size*1.55); ty=y+110
    for i,l in enumerate(lines):
        d.text((W//2,ty+i*lh),l,font=f,fill=CREAM,anchor='mt',direction='rtl')
    # tag
    ft=font(600,46); tw=d.textlength(tag,font=ft,direction='rtl')
    by=ty+len(lines)*lh+60
    d.rectangle([W//2-tw/2-34,by,W//2+tw/2+34,by+86],fill=CORAL)
    d.text((W//2,by+43),tag,font=ft,fill=CREAM,anchor='mm',direction='rtl')
    fl=ImageFont.truetype(B+'plex-latin-400.ttf',38)
    d.text((W//2,H-330),'@hamedalthiabi',font=fl,fill=(200,205,215),anchor='mm')
    im.save(out); return out
if __name__=='__main__':
    make(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else 'استدامة العطاء', sys.argv[3] if len(sys.argv)>3 else 'cover.png')
