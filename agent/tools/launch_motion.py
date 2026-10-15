# موشن جرافيك يوم الإطلاق: هادئ، بلا موسيقى، ٣٠ ثانية، بهوية حامد
import os, sys, subprocess, math
from PIL import Image, ImageDraw, ImageFont
B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','brand')+'/'
W,H=(int(sys.argv[1]),int(sys.argv[2])) if len(sys.argv)>2 else (1080,1920)
OUT=sys.argv[3] if len(sys.argv)>3 else 'launch_motion.mp4'
FPS=30; DUR=30
NAVY=(0,37,68); CORAL=(187,104,65); CREAM=(248,245,239); MUT=(170,182,198)
F=lambda w,s: ImageFont.truetype(B+f'plex-{w}.ttf',s,layout_engine=ImageFont.Layout.RAQM)
FL=lambda s: ImageFont.truetype(B+'plex-latin-400.ttf',s)
def txt(t,f,c=CREAM,rtl=True,pad=0,bg=None):
    d=ImageDraw.Draw(Image.new('RGB',(1,1))); bb=d.textbbox((0,0),t,font=f,direction='rtl' if rtl else None)
    w,h=bb[2]-bb[0]+2*pad,bb[3]-bb[1]+2*pad
    im=Image.new('RGBA',(w,h),(0,0,0,0)); dd=ImageDraw.Draw(im)
    if bg: dd.rectangle([0,0,w,h],fill=bg)
    dd.text((pad-bb[0],pad-bb[1]),t,font=f,fill=c,direction='rtl' if rtl else None); return im
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def fade(t,a,b,out_a=None,out_b=None):
    v=ease((t-a)/(b-a))
    if out_a is not None: v*=1-ease((t-out_a)/(out_b-out_a))
    return v
s=W/1080
lg=Image.open(B+'logo_white.png').convert('RGBA'); lw=int(460*s); logo=lg.resize((lw,int(lg.height*lw/lg.width)),Image.LANCZOS)
lw2=int(300*s); logo_s=lg.resize((lw2,int(lg.height*lw2/lg.width)),Image.LANCZOS)
L={'a':txt('استدامة العطاء',F(600,int(92*s))),'b':txt('وأثر يمتد',F(600,int(92*s)),CORAL),
   'go':txt('انطلقنا',F(600,int(170*s))),'sub':txt('الموقع الرسمي متاح الآن',F(600,int(58*s))),
   'url':txt('hamedalthiabi.com',FL(int(50*s)),rtl=False,pad=int(26*s),bg=CORAL),
   'tag':txt('استدامة العطاء وأثر يمتد',F(400,int(40*s)),MUT),'head':txt('تجدون في الموقع',F(400,int(44*s)),MUT)}
items=[txt(x,F(600,int(60*s))) for x in ['الخدمات','المتجر','الإصدارات','التقويم']]
def paste(fr,im,cx,cy,alpha,dy=0):
    if alpha<=0: return
    a=im.copy(); a.putalpha(a.getchannel('A').point(lambda p:int(p*alpha)))
    fr.alpha_composite(a,(int(cx-a.width/2),int(cy-a.height/2+dy)))
tri=int(300*s)
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
  '-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart',OUT],stdin=subprocess.PIPE)
for i in range(FPS*DUR):
    t=i/FPS; fr=Image.new('RGBA',(W,H),NAVY+(255,)); d=ImageDraw.Draw(fr)
    k=ease(t/2.5); tt=int(tri*k)
    d.polygon([(0,0),(tt,0),(0,tt)],fill=CORAL); d.polygon([(W,H),(W,H-tt),(W-tt,H)],fill=CORAL)
    cy=H/2
    # ١: الشعار
    paste(fr,logo,W/2,cy,fade(t,0.8,2.6,5.0,6.2),dy=int(20*s*(1-ease((t-0.8)/1.8))))
    # ٢: استدامة العطاء وأثر يمتد
    paste(fr,L['a'],W/2,cy-int(60*s),fade(t,6.4,7.8,11.2,12.2),dy=int(24*s*(1-ease((t-6.4)/1.4))))
    paste(fr,L['b'],W/2,cy+int(70*s),fade(t,7.6,9.0,11.2,12.2),dy=int(24*s*(1-ease((t-7.6)/1.4))))
    # ٣: انطلقنا + الموقع
    a3=fade(t,12.6,14.2,21.0,22.0)
    paste(fr,L['go'],W/2,cy-int(150*s),a3,dy=int(30*s*(1-ease((t-12.6)/1.6))))
    paste(fr,L['sub'],W/2,cy+int(20*s),fade(t,14.4,15.8,21.0,22.0))
    paste(fr,L['url'],W/2,cy+int(150*s),fade(t,15.6,17.0,21.0,22.0))
    # ٤: ما في الموقع
    paste(fr,L['head'],W/2,cy-int(250*s),fade(t,22.0,23.0,26.0,26.8))
    for j,im in enumerate(items):
        a=fade(t,22.4+j*0.6,23.6+j*0.6,26.0,26.8); y=cy+int((-120+j*110)*s)
        paste(fr,im,W/2,y,a)
        if a>0: dd=ImageDraw.Draw(fr); x0=W/2+im.width/2+int(36*s); r=int(9*s); dd.polygon([(x0,y-r),(x0+r,y),(x0,y+r),(x0-r,y)],fill=CORAL+(int(255*a),))
    # ٥: الخاتمة
    a5=fade(t,26.8,28.0)
    paste(fr,logo_s,W/2,cy-int(110*s),a5); paste(fr,L['url'],W/2,cy+int(40*s),a5); paste(fr,L['tag'],W/2,cy+int(150*s),a5)
    p.stdin.write(fr.convert('RGB').tobytes())
p.stdin.close(); p.wait(); print(OUT)
