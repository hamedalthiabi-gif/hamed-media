# موشن إطلاق الهوية «أثرٌ يمتد»: قطرة تتسع دوائرها فتكشف الشعار، ثم تتحول نقاطه إلى «وأثرٌ يمتد»
# فتمتد الكلمة، ثم ألوان الهوية ونقوشها، ثم جولة في الموقع، ثم الختام. هادئ بلا موسيقى (٤٠ ثانية)
import os, sys, subprocess, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
T=os.path.dirname(os.path.abspath(__file__)); B=os.path.join(T,'..','brand')+'/'
W,H=int(sys.argv[1]),int(sys.argv[2]); OUT=sys.argv[3]; A=sys.argv[4] if len(sys.argv)>4 else '/home/claude/x'
FPS=30; DUR=40
NAVY=(0,37,68); CORAL=(187,104,65); CREAM=(248,245,239); INK=(27,36,51); MUT=(170,182,198); GUIDE=(40,74,112); SAND=(232,224,210)
F=lambda w,s: ImageFont.truetype(B+f'plex-{w}.ttf',int(s),layout_engine=ImageFont.Layout.RAQM)
FL=lambda s: ImageFont.truetype(B+'plex-latin-400.ttf',int(s))
S=min(W,H)/1080; cx,cy=W/2,H/2; TALL=H>W
def e(x): x=max(0.,min(1.,x)); return 1-(1-x)**3
def eio(x): x=max(0.,min(1.,x)); return x*x*(3-2*x)
def win(t,a,b,c=None,d=None):
    v=e((t-a)/(b-a))
    if c is not None: v*=1-e((t-c)/(d-c))
    return v
_c={}
def txt(t,f,c=CREAM,rtl=True,pad=0,bg=None):
    k=(t,id(f),c,rtl,pad,bg)
    if k in _c: return _c[k]
    d=ImageDraw.Draw(Image.new('RGB',(1,1))); bb=d.textbbox((0,0),t,font=f,direction='rtl' if rtl else None)
    w,h=bb[2]-bb[0]+2*pad,bb[3]-bb[1]+2*pad
    im=Image.new('RGBA',(max(w,1),max(h,1)),(0,0,0,0)); dd=ImageDraw.Draw(im)
    if bg: dd.rounded_rectangle([0,0,w-1,h-1],radius=int(10*S),fill=bg)
    dd.text((pad-bb[0],pad-bb[1]),t,font=f,fill=c,direction='rtl' if rtl else None); _c[k]=im; return im
def put(fr,im,x,y,a=1.,anchor='c'):
    if a<=0.003: return
    if a<1: im=im.copy(); im.putalpha(im.getchannel('A').point(lambda p:int(p*a)))
    if anchor=='c': x,y=x-im.width/2,y-im.height/2
    elif anchor=='r': x,y=x-im.width,y-im.height/2
    fr.alpha_composite(im,(int(x),int(y)))
def sc(im,k): return im.resize((max(1,int(im.width*k)),max(1,int(im.height*k))),Image.LANCZOS)
def rnd(im,r):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,im.width-1,im.height-1],radius=r,fill=255)
    o=im.convert('RGBA'); o.putalpha(m); return o
def shadow(im,r):
    pad=int(40*S); sh=Image.new('RGBA',(im.width+2*pad,im.height+2*pad),(0,0,0,0))
    m=Image.new('L',sh.size,0); ImageDraw.Draw(m).rounded_rectangle([pad,pad+int(12*S),pad+im.width,pad+im.height+int(12*S)],radius=r,fill=120)
    sh.putalpha(m.filter(ImageFilter.GaussianBlur(int(20*S)))); sh.alpha_composite(im,(pad,pad)); return sh
def orn(d,x,y,col,a=255,n=4,step=None,r=None):
    step=step or 34*S; r=r or 7*S
    for i in range(n):
        X=x-(n-1)*step/2+i*step
        if i%2: d.polygon([(X,y-r),(X+r,y),(X,y+r),(X-r,y)],fill=col+(a,))
        else: d.ellipse([X-r*0.85,y-r*0.85,X+r*0.85,y+r*0.85],fill=col+(a,))
# ---------- الأصول ----------
LW=Image.open(B+'logo_white.png').convert('RGBA'); LN=Image.open(B+'logo_navy.png').convert('RGBA')
big=sc(LW,620*S/LW.width); ox,oy=cx-big.width/2,cy-big.height/2-int(20*S)
LINE='وأثرٌ يمتد'; FT=F(600,150*S)
def stretched(k):  # «يمتد» تمتد بالكشيدة
    return 'وأثرٌ يمـ'+'ـ'*k+'تد' if k>0 else LINE
def two_tone(s,a=1.):
    w1=txt('وأثرٌ',FT,CREAM); w2=txt(s.split(' ',1)[1],FT,CORAL); g=int(34*S)
    im=Image.new('RGBA',(w1.width+g+w2.width,max(w1.height,w2.height)),(0,0,0,0))
    im.alpha_composite(w1,(w2.width+g,im.height-w1.height)); im.alpha_composite(w2,(0,im.height-w2.height)); return im
TXT0=two_tone(LINE); tx0,ty0=cx-TXT0.width/2,cy-TXT0.height/2+int(40*S)
random.seed(11)
def sample(im,ox,oy,n,step):
    m=im.getchannel('A').load(); pts=[(ox+x,oy+y) for y in range(0,im.height,step) for x in range(0,im.width,step) if m[x,y]>150]
    random.shuffle(pts); return [pts[i%len(pts)] for i in range(n)]
N=1100; st=max(2,int(5*S))
PA=sample(big,ox,oy,N,st); PB=sample(TXT0,tx0,ty0,N,st)
PM=[(random.uniform(0,W),random.uniform(0,H)) for _ in range(N)]; DL=[random.uniform(0,0.7) for _ in range(N)]
LK=[]
for i in range(0,N,4):
    best=None;bd=1e18
    for j in range(N):
        if j!=i:
            dd=(PB[i][0]-PB[j][0])**2+(PB[i][1]-PB[j][1])**2
            if 20*S*S<dd<bd: bd=dd;best=j
    if best is not None and bd<(36*S)**2: LK.append((i,best))
# صفحات الموقع
pages=[('pg_home','الرئيسية'),('pg_store','المتجر والخدمات'),('pg_pubs','الإصدارات'),('pg_cal','تقويم القطاع')]
BW=int((980 if TALL else 820)*S); BH=int(BW*0.62); BAR=int(30*S)
PG=[(sc(Image.open(f'{A}/{f}.png').convert('RGB'),BW/1280),lab) for f,lab in pages]
mob=Image.open(f'{A}/m_home.png').convert('RGB'); PWd=int((300 if TALL else 230)*S); mob=sc(mob,PWd/mob.width); PHt=int(PWd*2.05)
def pattern(off):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); s=int(64*S); r=int(8*S)
    for j,y in enumerate(range(-s,H+s,s)):
        for i,x in enumerate(range(-s,W+s,s)):
            X=x+(s/2 if j%2 else 0)+off; Y=y
            if (i+j)%2: d.polygon([(X,Y-r),(X+r,Y),(X,Y+r),(X-r,Y)],outline=(205,190,168),width=max(1,int(2*S)))
            else: d.ellipse([X-r*0.7,Y-r*0.7,X+r*0.7,Y+r*0.7],outline=(205,190,168),width=max(1,int(2*S)))
    return im
PAT=[pattern(o) for o in range(0,int(64*S),2)]
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
  '-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart',OUT],stdin=subprocess.PIPE)
for n in range(FPS*DUR):
    t=n/FPS
    light=win(t,15.6,16.4,22.6,23.4)
    bg=tuple(int(NAVY[i]+(CREAM[i]-NAVY[i])*light) for i in range(3))
    fr=Image.new('RGBA',(W,H),bg+(255,)); d=ImageDraw.Draw(fr)
    # ١) قطرة ودوائر تتسع فتكشف الشعار
    if t<6.6:
        fo=1-e((t-5.8)/0.8)
        if t<0.9:
            y=-30*S+(cy-(-30*S))*eio(t/0.9); r=12*S; d.ellipse([cx-r,y-r,cx+r,y+r],fill=CORAL)
        for i in range(6):
            k=(t-0.9-i*0.38)/3.4
            if 0<k<1:
                R=max(W,H)*0.62*e(k); a=int(255*(1-k)*0.9*fo)
                col=CORAL if i==0 else GUIDE
                d.ellipse([cx-R,cy-R,cx+R,cy+R],outline=col+(a,),width=max(1,int((3 if i==0 else 2)*S)))
        if t>=0.9:
            R=max(W,H)*0.62*e((t-1.6)/3.0)
            if R>2:
                m=Image.new('L',big.size,0); ImageDraw.Draw(m).ellipse([cx-ox-R,cy-oy-R,cx-ox+R,cy-oy+R],fill=255)
                lg=big.copy(); a=lg.getchannel('A'); from PIL import ImageChops; lg.putalpha(ImageChops.multiply(a,m))
                put(fr,lg,ox,oy,fo,anchor='tl')
        tt=int(260*S*win(t,3.4,4.8,5.8,6.6)); 
        d.polygon([(0,0),(tt,0),(0,tt)],fill=CORAL); d.polygon([(W,H),(W,H-tt),(W-tt,H)],fill=CORAL)
        orn(d,cx,oy+big.height+int(60*S),CORAL,int(255*win(t,4.0,4.8,5.8,6.4)))
    # ٢) نقاط الشعار تتحول إلى «وأثرٌ يمتد» ثم تمتد الكلمة
    if 6.2<t<16.2:
        fa=win(t,6.2,6.6)
        for i in range(N):
            a1=eio((t-6.4-DL[i]*0.5)/1.2); a2=eio((t-7.6-DL[i])/2.0)
            x=PA[i][0]+(PM[i][0]-PA[i][0])*a1; y=PA[i][1]+(PM[i][1]-PA[i][1])*a1
            x=x+(PB[i][0]-x)*a2; y=y+(PB[i][1]-y)*a2
            al=int(230*fa*(1-win(t,10.6,11.4)))
            if al>3: r=1.9*S; d.ellipse([x-r,y-r,x+r,y+r],fill=CREAM+(al,))
        la=win(t,9.6,10.4,10.8,11.4)
        if la>0:
            for i,j in LK: d.line([PB[i],PB[j]],fill=MUT+(int(150*la),),width=1)
        if t>10.4:
            k=int(min(7,max(0,(t-11.6)*5)))
            im=two_tone(stretched(k)); fo=1-e((t-15.4)/0.8)
            put(fr,im,cx,cy+int(40*S),win(t,10.4,11.2)*fo)
            put(fr,txt('استدامة العطاء',F(600,110*S)),cx,cy-int(150*S),win(t,13.0,14.0)*fo,)
    # ٣) ألوان الهوية ونقوشها (بلا نصوص)
    if 15.6<t<20.4:
        fo=1-e((t-19.6)/0.8); g=int(18*S); cs=int(150*S)
        cols=[NAVY,CORAL,SAND,INK,CORAL,NAVY,SAND,NAVY,CORAL]
        for i,c in enumerate(cols):
            r_,c_=divmod(i,3); k=e((t-16.0-i*0.12)/0.9)
            x=cx+(1-c_)*(cs+g); y=cy+(r_-1)*(cs+g)+int((1-k)*80*S)
            tile=Image.new('RGBA',(cs,cs),c+(255,)); dt=ImageDraw.Draw(tile)
            ic=CREAM if c!=SAND else NAVY
            if i in (0,4,8):
                rr=int(26*S); mx=my=cs//2; dt.polygon([(mx,my-rr),(mx+rr,my),(mx,my+rr),(mx-rr,my)],fill=ic); dt.ellipse([mx-8*S,my-8*S,mx+8*S,my+8*S],fill=c)
            elif i in (2,6):
                rr=int(16*S); dt.ellipse([cs/2-rr,cs/2-rr,cs/2+rr,cs/2+rr],fill=ic)
            put(fr,rnd(tile,int(16*S)),x,y,k*fo)
        kk=win(t,18.0,18.8)
        if kk>0:
            plate=Image.new('RGBA',(int(3*cs+2*g+40*S),int(cs+g)),CREAM+(255,)); pl=rnd(plate,int(18*S)); put(fr,pl,cx,cy,kk*fo)
            put(fr,sc(LN,380*S/LN.width),cx,cy,kk*fo)
    # ٤) النقوش + الشعار
    if 20.0<t<23.6:
        fo=win(t,20.0,20.7,22.8,23.5)
        put(fr,PAT[int((t-20)*10)%len(PAT)],0,0,fo,anchor='tl')
        plate=rnd(Image.new('RGBA',(int(640*S),int(300*S)),CREAM+(255,)),int(24*S)); put(fr,plate,cx,cy,fo)
        put(fr,sc(LN,440*S/LN.width),cx,cy-int(30*S),win(t,20.4,21.2,22.8,23.5))
        put(fr,txt('مستشار التسويق والاستدامة المالية',F(400,36*S),(94,102,115)),cx,cy+int(90*S),win(t,21.0,21.8,22.8,23.5))
    # ٥) جولة في الموقع
    if 23.2<t<35.6:
        fo=win(t,23.2,24.0,34.8,35.6)
        put(fr,txt('الموقع الرسمي',F(600,60*S)),cx,int((150 if not TALL else 260)*S),win(t,23.4,24.2,34.8,35.6))
        frame=Image.new('RGBA',(BW,BH+BAR),(232,228,220,255)); df=ImageDraw.Draw(frame)
        for i,c in enumerate([(232,106,94),(240,190,80),(110,190,110)]): df.ellipse([int((14+i*20)*S),int(10*S),int((25+i*20)*S),int(21*S)],fill=c)
        df.rounded_rectangle([int(90*S),int(6*S),BW-int(90*S),BAR-int(6*S)],radius=int(8*S),fill=(250,248,244))
        df.text((BW/2,BAR/2),'hamedalthiabi.com',font=FL(15*S),fill=(110,110,110),anchor='mm')
        seg=2.8; i=int(min(3,max(0,(t-24.0)//seg))); lt=(t-24.0)-i*seg
        pg,lab=PG[i]; top=int(min(pg.height-BH,max(0,(pg.height-BH)*0.25))*eio(lt/seg))
        frame.paste(pg.crop((0,top,BW,top+BH)),(0,BAR))
        if lt<0.5 and i>0:
            pp,_=PG[i-1]; old=pp.crop((0,int(min(pp.height-BH,(pp.height-BH)*0.25)),BW,int(min(pp.height-BH,(pp.height-BH)*0.25))+BH)).convert('RGBA')
            old.putalpha(int(255*(1-lt/0.5))); frame.alpha_composite(old,(0,BAR))
        k=e((t-23.6)/1.2); by=cy+(int(10*S) if not TALL else -int(120*S))
        put(fr,shadow(rnd(frame,int(14*S)),int(14*S)),cx+int((1-k)*120*S),by,k*fo)
        put(fr,txt(lab,F(600,34*S),CREAM,pad=int(16*S),bg=CORAL),cx,by+(BH+BAR)/2+int(60*S),fo*min(1,lt/0.4+ (1 if i==0 and t>24.4 else 0)))
        # الجوال
        kp=e((t-25.0)/1.2)
        ph=Image.new('RGBA',(PWd+int(16*S),PHt+int(16*S)),(18,22,30,255)); ph=rnd(ph,int(34*S))
        mt=int((mob.height-PHt)*0.3*eio((t-25.5)/9)); scr=rnd(mob.crop((0,mt,PWd,mt+PHt)),int(28*S)); ph.alpha_composite(scr,(int(8*S),int(8*S)))
        if TALL: px_,py_=cx+int(250*S),by+(BH+BAR)/2+int(560*S)
        else: px_,py_=cx-BW/2+int(30*S),by+int(170*S)
        put(fr,shadow(ph,int(34*S)),px_,py_+int((1-kp)*120*S),kp*fo)
        if TALL:
            for j,cv in enumerate(['cover15.webp','cover01.webp']):
                kc=e((t-26.0-j*0.4)/1.0); im=Image.open(f'{A}/dist/pubs/{cv}').convert('RGB'); im=rnd(sc(im,int(250*S)/im.width),int(12*S))
                put(fr,shadow(im,int(12*S)),cx-int(330*S)+j*int(60*S),by+(BH+BAR)/2+int(420*S)+j*int(260*S),kc*fo)
    # ٦) الختام
    if t>35.2:
        k=win(t,35.3,36.3); tt=int(300*S*e((t-35.3)/1.2))
        d.polygon([(0,0),(tt,0),(0,tt)],fill=CORAL); d.polygon([(W,H),(W,H-tt),(W-tt,H)],fill=CORAL)
        put(fr,sc(LW,460*S/LW.width),cx,cy-int(130*S),k)
        orn(d,cx,cy-int(20*S),CORAL,int(255*win(t,35.8,36.6)))
        put(fr,txt('استدامة العطاء وأثرٌ يمتد',F(400,46*S),MUT),cx,cy+int(50*S),win(t,36.1,37.0))
        put(fr,txt('hamedalthiabi.com',FL(44*S),CREAM,rtl=False,pad=int(24*S),bg=CORAL),cx,cy+int(165*S),win(t,36.8,37.7))
    p.stdin.write(fr.convert('RGB').tobytes())
p.stdin.close(); p.wait(); print(OUT)
