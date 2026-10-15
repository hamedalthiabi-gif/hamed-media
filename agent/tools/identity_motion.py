# موشن إطلاق الهوية: بناء الشعار، نقاط تتجمع، كتابة الشعار، الألوان، النمط، النماذج، الختام
# هادئ، بلا موسيقى، ٣٣ ثانية. الاستخدام: python3 identity_motion.py W H out.mp4 ASSETS_DIR
import os, sys, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
T=os.path.dirname(os.path.abspath(__file__)); B=os.path.join(T,'..','brand')+'/'
W,H=int(sys.argv[1]),int(sys.argv[2]); OUT=sys.argv[3]; A=sys.argv[4] if len(sys.argv)>4 else '/home/claude/x'
FPS=30; DUR=33
NAVY=(0,37,68); NAVY2=(11,51,88); CORAL=(187,104,65); CREAM=(248,245,239); INK=(27,36,51); MUT=(170,182,198); GUIDE=(46,82,120)
F=lambda w,s: ImageFont.truetype(B+f'plex-{w}.ttf',int(s),layout_engine=ImageFont.Layout.RAQM)
FL=lambda s: ImageFont.truetype(B+'plex-latin-400.ttf',int(s))
S=min(W,H)/1080; cx,cy=W/2,H/2
def e(x): x=max(0.,min(1.,x)); return 1-(1-x)**3
def eio(x): x=max(0.,min(1.,x)); return x*x*(3-2*x)
def win(t,a,b,c=None,d=None):
    v=e((t-a)/(b-a))
    if c is not None: v*=1-e((t-c)/(d-c))
    return v
_tc={}
def txt(t,f,c=CREAM,rtl=True,pad=0,bg=None,key=None):
    k=(t,id(f),c,rtl,pad,bg)
    if k in _tc: return _tc[k]
    d=ImageDraw.Draw(Image.new('RGB',(1,1))); bb=d.textbbox((0,0),t,font=f,direction='rtl' if rtl else None)
    w,h=bb[2]-bb[0]+2*pad,bb[3]-bb[1]+2*pad
    im=Image.new('RGBA',(max(w,1),max(h,1)),(0,0,0,0)); dd=ImageDraw.Draw(im)
    if bg: dd.rounded_rectangle([0,0,w-1,h-1],radius=int(10*S),fill=bg)
    dd.text((pad-bb[0],pad-bb[1]),t,font=f,fill=c,direction='rtl' if rtl else None); _tc[k]=im; return im
def put(fr,im,x,y,a=1.,anchor='c'):
    if a<=0.003: return
    if a<1: im=im.copy(); im.putalpha(im.getchannel('A').point(lambda p:int(p*a)))
    if anchor=='c': x,y=x-im.width/2,y-im.height/2
    elif anchor=='r': x,y=x-im.width,y-im.height/2
    fr.alpha_composite(im,(int(x),int(y)))
def scale(im,k): return im.resize((max(1,int(im.width*k)),max(1,int(im.height*k))),Image.LANCZOS)
def rounded(im,r):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,im.width-1,im.height-1],radius=r,fill=255)
    o=im.convert('RGBA'); o.putalpha(m); return o
def shadowed(im,r=18):
    pad=int(40*S); sh=Image.new('RGBA',(im.width+2*pad,im.height+2*pad),(0,0,0,0))
    m=Image.new('L',sh.size,0); ImageDraw.Draw(m).rounded_rectangle([pad,pad+int(10*S),pad+im.width,pad+im.height+int(10*S)],radius=r,fill=110)
    m=m.filter(ImageFilter.GaussianBlur(int(18*S))); sh.putalpha(m); sh.alpha_composite(im,(pad,pad)); return sh
# ---------- الأصول ----------
LW=Image.open(B+'logo_white.png').convert('RGBA'); LN=Image.open(B+'logo_navy.png').convert('RGBA')
big=scale(LW,620*S/LW.width)
# نقاط من الشعار
random.seed(7)
mask=big.getchannel('A'); px=mask.load(); pts=[]
for y in range(0,big.height,int(max(3,7*S))):
    for x in range(0,big.width,int(max(3,7*S))):
        if px[x,y]>140: pts.append((x,y))
random.shuffle(pts); pts=pts[:900]
ox,oy=cx-big.width/2,cy-big.height/2
P=[(ox+x,oy+y,random.uniform(0,W),random.uniform(0,H),random.uniform(0,0.6)) for x,y in pts]
links=[]
for i in range(0,len(P),3):
    best=None;bd=1e9
    for j in range(len(P)):
        if j==i: continue
        dd=(P[i][0]-P[j][0])**2+(P[i][1]-P[j][1])**2
        if 30*S<dd<bd: bd=dd;best=j
    if best is not None and bd<(40*S)**2: links.append((i,best))
# نماذج
site=Image.open(A+'/site_full.png').convert('RGB')
bw=int(640*S); bh=int(430*S); site_s=scale(site,bw/site.width)
covers=[rounded(scale(Image.open(A+f'/dist/pubs/{c}').convert('RGB'),int(230*S)/Image.open(A+f'/dist/pubs/{c}').width),int(12*S)) for c in ['cover15.webp','cover01.webp','cover14.webp']]
yt=rounded(scale(Image.open(A+'/yt_banner.png').convert('RGB'),int(520*S)/2560),int(14*S))
# نمط
def pattern(off,col,size=int(70*S)):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=int(9*S)
    for j,y in enumerate(range(-size,H+size,size)):
        for i,x in enumerate(range(-size,W+size,size)):
            X=x+(size/2 if j%2 else 0)+off; Y=y+off*0.5
            if (i+j)%2: d.polygon([(X,Y-r),(X+r,Y),(X,Y+r),(X-r,Y)],outline=col,width=max(1,int(2*S)))
            else: d.ellipse([X-r*0.7,Y-r*0.7,X+r*0.7,Y+r*0.7],outline=col,width=max(1,int(2*S)))
    return im
PAT=[pattern(o,(200,186,165,255)) for o in range(0,int(70*S),2)]
F_big=F(600,150*S); F_mid=F(600,84*S); F_small=F(400,34*S); F_hex=FL(30*S); F_lab=F(600,40*S)
L1='استدامة العطاء'; L2='وأثر يمتد'
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
  '-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart',OUT],stdin=subprocess.PIPE)
for n in range(FPS*DUR):
    t=n/FPS
    # الخلفية: كحلي، ثم كريمي في مشهدي الألوان والنمط
    light=win(t,13.8,14.6,21.6,22.4)
    bg=tuple(int(NAVY[i]+(CREAM[i]-NAVY[i])*light) for i in range(3))
    fr=Image.new('RGBA',(W,H),bg+(255,)); d=ImageDraw.Draw(fr)
    # ١) بناء الشعار بالخطوط الإرشادية
    if t<5.4:
        g=win(t,0.2,1.6,4.0,4.8)
        if g>0:
            col=GUIDE+(int(255*g),); x0,x1=ox,ox+big.width; y0,y1=oy,oy+big.height
            L=e((t-0.2)/1.4)
            for yy in [y0,y1,(y0+y1)/2]: d.line([(cx-(W/2)*L,yy),(cx+(W/2)*L,yy)],fill=col,width=1)
            for xx in [x0,x1,cx]: d.line([(xx,cy-(H/2)*L),(xx,cy+(H/2)*L)],fill=col,width=1)
            R=big.width*0.55*L; d.ellipse([cx-R,cy-R,cx+R,cy+R],outline=col,width=1)
            d.line([(x0,y0),(x1,y1)],fill=col,width=1); d.line([(x0,y1),(x1,y0)],fill=col,width=1)
        rv=eio((t-1.2)/2.0)
        if rv>0:
            w=int(big.width*rv); crop=big.crop((big.width-w,0,big.width,big.height))
            a=1-e((t-4.6)/0.8)
            put(fr,crop,ox+big.width-w,oy,a,anchor='tl')
    # ٢) نقاط تتجمع لتكوين الشعار
    if 4.6<t<9.8:
        k=eio((t-4.9)/2.6); fa=win(t,4.6,5.2,9.2,9.8)
        for i,(tx,ty,sx,sy,dl) in enumerate(P):
            kk=eio((t-4.9-dl)/2.4)
            X=sx+(tx-sx)*kk; Y=sy+(ty-sy)*kk
            a=int(220*fa*(1-0.75*win(t,7.9,8.6)))
            r=1.6*S+0.6*S
            d.ellipse([X-r,Y-r,X+r,Y+r],fill=CREAM+(a,))
        la=win(t,7.2,7.9,8.6,9.2)
        if la>0:
            for i,j in links: d.line([P[i][:2],P[j][:2]],fill=MUT+(int(140*la),),width=1)
        put(fr,big,cx,cy,win(t,7.9,8.7,9.2,9.8))
    # ٣) كتابة الشعار حرفًا حرفًا
    if 9.8<t<14.2:
        fa=1-e((t-13.6)/0.6)
        n1=min(len(L1),int(max(0,(t-10.0))*len(L1)/1.6)); n2=min(len(L2),int(max(0,(t-11.9))*len(L2)/1.1))
        if n1>0:
            im=txt(L1[:n1],F_mid); put(fr,im,cx+txt(L1,F_mid).width/2,cy-int(60*S),fa,anchor='r')
            if n1<len(L1) or n2==0:
                if int(t*2)%2==0 or n1<len(L1): d.rectangle([cx+txt(L1,F_mid).width/2-im.width-int(14*S),cy-int(110*S),cx+txt(L1,F_mid).width/2-im.width-int(9*S),cy-int(10*S)],fill=CORAL+(int(255*fa),))
        if n2>0:
            im2=txt(L2[:n2],F_mid,CORAL); put(fr,im2,cx+txt(L2,F_mid).width/2,cy+int(70*S),fa,anchor='r')
    # ٤) الألوان والخط
    if 14.0<t<18.9:
        fa=1-e((t-18.3)/0.6)
        cards=[(NAVY,'#002544','كحلي'),(CORAL,'#BB6841','نحاسي'),(CREAM,'#F8F5EF','كريمي'),(INK,'#1B2433','حبر')]
        cw,chh=int(205*S),int(300*S); gap=int(22*S); total=4*cw+3*gap; x0=cx+total/2
        for i,(c,hx,nm) in enumerate(cards):
            k=e((t-14.4-i*0.25)/0.9); y=cy-int(40*S)+int((1-k)*120*S)
            x=x0-(i+1)*cw-i*gap
            card=Image.new('RGBA',(cw,chh),c+(255,)); dc=ImageDraw.Draw(card)
            if c==CREAM: dc.rounded_rectangle([0,0,cw-1,chh-1],radius=int(14*S),outline=(214,205,190),width=2)
            tc=INK if c==CREAM else CREAM
            dc.text((cw-int(20*S),chh-int(80*S)),nm,font=F_lab,fill=tc,anchor='rs',direction='rtl')
            dc.text((int(20*S),chh-int(28*S)),hx,font=F_hex,fill=tc,anchor='ls')
            put(fr,rounded(card,int(14*S)),x+cw/2,y,k*fa)
        fk=win(t,15.8,16.6)
        put(fr,txt('IBM Plex Sans Arabic',FL(40*S),INK,rtl=False),cx,cy+int(210*S),fk*fa)
        put(fr,txt('أ ب ت ث ج ح خ',F(400,46*S),(94,102,115)),cx,cy+int(270*S),fk*fa)
    # ٥) النمط + أثر يمتد
    if 18.6<t<22.6:
        fa=win(t,18.6,19.3,21.8,22.5)
        pat=PAT[int((t-18.6)*8)%len(PAT)]; put(fr,pat,0,0,fa*0.9,anchor='tl')
        k1=win(t,19.0,19.9); k2=win(t,19.7,20.6)
        put(fr,scale(txt('أثر',F(600,170*S),NAVY),0.9+0.1*k1),cx,cy-int(90*S),k1*fa)
        put(fr,scale(txt('يمتد',F(600,170*S),CORAL),0.9+0.1*k2),cx,cy+int(110*S),k2*fa)
    # ٦) النماذج: الموقع والإصدارات
    if 22.2<t<28.2:
        fa=1-e((t-27.6)/0.6)
        k=e((t-22.4)/1.1); sc=e((t-23.2)/3.6)
        top=int((site_s.height-bh)*0.10*sc)
        shot=site_s.crop((0,top,bw,top+bh))
        bar=int(34*S); frame=Image.new('RGBA',(bw,bh+bar),(230,226,218,255)); df=ImageDraw.Draw(frame)
        for i,c in enumerate([(232,106,94),(240,190,80),(110,190,110)]): df.ellipse([int((16+i*22)*S),int(11*S),int((28+i*22)*S),int(23*S)],fill=c)
        frame.paste(shot,(0,bar)); frame=shadowed(rounded(frame,int(14*S)),int(14*S))
        bx=cx+int(150*S)*(1 if W>=H else 0); by=cy-int(70*S) if W>=H else cy-int(330*S)
        put(fr,frame,bx+int((1-k)*200*S),by,k*fa)
        for i,cv in enumerate(covers):
            kc=e((t-23.6-i*0.35)/1.0)
            if W>=H: x=cx-int(370*S)+i*int(30*S); y=cy+int(150*S)-i*int(120*S)
            else: x=cx-int(250*S)+i*int(250*S); y=cy+int(330*S)
            put(fr,shadowed(cv,int(12*S)),x,y+int((1-kc)*100*S),kc*fa)
        ky=e((t-25.0)/1.0)
        if W<H: put(fr,shadowed(yt,int(14*S)),cx,cy+int(700*S)+int((1-ky)*80*S),ky*fa)
    # ٧) الختام
    if t>27.8:
        k=win(t,27.9,28.9); tt=int(300*S*e((t-27.9)/1.2))
        d.polygon([(0,0),(tt,0),(0,tt)],fill=CORAL); d.polygon([(W,H),(W,H-tt),(W-tt,H)],fill=CORAL)
        put(fr,scale(LW,460*S/LW.width),cx,cy-int(110*S),k)
        put(fr,txt('استدامة العطاء وأثر يمتد',F(400,44*S),MUT),cx,cy+int(35*S),win(t,28.7,29.6))
        put(fr,txt('hamedalthiabi.com',FL(44*S),CREAM,rtl=False,pad=int(24*S),bg=CORAL),cx,cy+int(150*S),win(t,29.4,30.3))
    p.stdin.write(fr.convert('RGB').tobytes())
p.stdin.close(); p.wait(); print(OUT)
