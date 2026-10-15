import sys
from PIL import Image, ImageDraw, ImageFont
import os; B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','brand')+'/'
NAVY=(0,37,68); CORAL=(187,104,65); CREAM=(248,245,239)
F=lambda w,s: ImageFont.truetype(B+f'plex-{w}.ttf',s,layout_engine=ImageFont.Layout.RAQM)
def wrap(d,t,f,mw):
    out=[];cur=''
    for w in t.split():
        c=(cur+' '+w).strip()
        if d.textlength(c,font=f,direction='rtl')<=mw: cur=c
        else: out.append(cur);cur=w
    return out+[cur]
def make(title,tag,out,W=1080,H=1350):
    im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
    d.polygon([(0,0),(260,0),(0,260)],fill=CORAL); d.polygon([(W,H),(W,H-260),(W-260,H)],fill=CORAL)
    lg=Image.open(B+'logo_white.png').convert('RGBA'); lw=360
    lg=lg.resize((lw,int(lg.height*lw/lg.width)),Image.LANCZOS); im.paste(lg,((W-lw)//2,170),lg)
    s=84
    while True:
        f=F(600,s); L=wrap(d,title,f,860)
        if len(L)<=4 or s<=56: break
        s-=6
    lh=int(s*1.55); total=len(L)*lh; y0=(H-total)//2+40
    for i,l in enumerate(L): d.text((W//2,y0+i*lh),l,font=f,fill=CREAM,anchor='mt',direction='rtl')
    ft=F(600,40); tw=d.textlength(tag,font=ft,direction='rtl'); by=y0+total+50
    d.rectangle([W//2-tw/2-30,by,W//2+tw/2+30,by+76],fill=CORAL)
    d.text((W//2,by+38),tag,font=ft,fill=CREAM,anchor='mm',direction='rtl')
    fl=ImageFont.truetype(B+'plex-latin-400.ttf',32)
    d.text((W//2,H-150),'hamedalthiabi.com',font=fl,fill=(200,205,215),anchor='mm')
    im.save(out)
if __name__=='__main__': make(sys.argv[1],sys.argv[2],sys.argv[3])
