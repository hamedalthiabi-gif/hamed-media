# موشن إطلاق الهوية (دقيقة): الهوية السابقة والأرقام ← التحول ← الهوية الجديدة ← المتجر ← الإصدارات ← التقويم ← الشركاء ← الختام
import os, sys, subprocess, random, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
T=os.path.dirname(os.path.abspath(__file__)); B=os.path.join(T,'..','brand')+'/'
W,H=int(sys.argv[1]),int(sys.argv[2]); OUT=sys.argv[3]; A=sys.argv[4] if len(sys.argv)>4 else '/home/claude/x'
FPS=30; DUR=60
NAVY=(0,37,68); CORAL=(187,104,65); CREAM=(248,245,239); INK=(27,36,51); MUT=(170,182,198); GUIDE=(40,74,112); SAND=(232,224,210)
OLD=(246,247,246); OLDT=(92,112,115); TEAL=(15,103,111)
F=lambda w,s: ImageFont.truetype(B+f'plex-{w}.ttf',int(s),layout_engine=ImageFont.Layout.RAQM)
FL=lambda s: ImageFont.truetype(B+'plex-latin-400.ttf',int(s))
S=min(W,H)/1080; cx,cy=W/2,H/2; TALL=H>W
AR=str.maketrans('0123456789','٠١٢٣٤٥٦٧٨٩')
def e(x): x=max(0.,min(1.,x)); return 1-(1-x)**3
def eio(x): x=max(0.,min(1.,x)); return x*x*(3-2*x)
def win(t,a,b,c=None,d=None):
    v=e((t-a)/(b-a))
    if c is not None: v*=1-e((t-c)/(d-c))
    return v
_c={}
def txt(t,f,c=CREAM,rtl=True,pad=0,bg=None,r=10):
    k=(t,id(f),c,rtl,pad,bg)
    if k in _c: return _c[k]
    d=ImageDraw.Draw(Image.new('RGB',(1,1))); bb=d.textbbox((0,0),t,font=f,direction='rtl' if rtl else None)
    w,h=bb[2]-bb[0]+2*pad,bb[3]-bb[1]+2*pad
    im=Image.new('RGBA',(max(w,1),max(h,1)),(0,0,0,0)); dd=ImageDraw.Draw(im)
    if bg: dd.rounded_rectangle([0,0,w-1,h-1],radius=int(r*S),fill=bg)
    dd.text((pad-bb[0],pad-bb[1]),t,font=f,fill=c,direction='rtl' if rtl else None)
    if len(_c)<4000: _c[k]=im
    return im
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
    pad=int(36*S); sh=Image.new('RGBA',(im.width+2*pad,im.height+2*pad),(0,0,0,0))
    m=Image.new('L',sh.size,0); ImageDraw.Draw(m).rounded_rectangle([pad,pad+int(12*S),pad+im.width,pad+im.height+int(12*S)],radius=r,fill=120)
    sh.putalpha(m.filter(ImageFilter.GaussianBlur(int(18*S)))); sh.alpha_composite(im,(pad,pad)); return sh
def orn(d,x,y,col,a=255,n=4):
    st=34*S; r=7*S
    for i in range(n):
        X=x-(n-1)*st/2+i*st
        if i%2: d.polygon([(X,y-r),(X+r,y),(X,y+r),(X-r,y)],fill=col+(a,))
        else: d.ellipse([X-r*0.85,y-r*0.85,X+r*0.85,y+r*0.85],fill=col+(a,))
def tri(d,k):
    tt=int(260*S*k); d.polygon([(0,0),(tt,0),(0,tt)],fill=CORAL); d.polygon([(W,H),(W,H-tt),(W-tt,H)],fill=CORAL)
def browser(img,top,bw,bh):
    bar=int(30*S); fr=Image.new('RGBA',(bw,bh+bar),(232,228,220,255)); df=ImageDraw.Draw(fr)
    for i,c in enumerate([(232,106,94),(240,190,80),(110,190,110)]): df.ellipse([int((14+i*20)*S),int(10*S),int((25+i*20)*S),int(21*S)],fill=c)
    df.rounded_rectangle([int(90*S),int(6*S),bw-int(90*S),bar-int(6*S)],radius=int(8*S),fill=(250,248,244))
    df.text((bw/2,bar/2),'hamedalthiabi.com',font=FL(15*S),fill=(110,110,110),anchor='mm')
    if img.height<bh:
        pad_=Image.new('RGB',(img.width,bh),(247,245,240)); pad_.paste(img,(0,0)); img=pad_
    top=int(max(0,min(img.height-bh,top))); fr.paste(img.crop((0,top,bw,top+bh)),(0,bar)); return shadow(rnd(fr,int(14*S)),int(14*S))
# ---------- الأصول ----------
OLDL=Image.open(B+'old_logo.png').convert('RGBA')
LW=Image.open(B+'logo_white.png').convert('RGBA'); LN=Image.open(B+'logo_navy.png').convert('RGBA')
big=sc(LW,620*S/LW.width); ox,oy=cx-big.width/2,cy-big.height/2-int(20*S)
FT=F(600,140*S)
def two_tone(k):
    s2='يمـ'+'ـ'*k+'تد' if k>0 else 'يمتد'
    w1=txt('وأثرٌ',FT,CREAM); w2=txt(s2,FT,CORAL); g=int(34*S)
    im=Image.new('RGBA',(w1.width+g+w2.width,max(w1.height,w2.height)),(0,0,0,0))
    im.alpha_composite(w1,(w2.width+g,im.height-w1.height)); im.alpha_composite(w2,(0,im.height-w2.height)); return im
TXT0=txt('استدامة العطاء',F(600,125*S)); tx0,ty0=cx-TXT0.width/2,cy-TXT0.height/2-int(85*S)
random.seed(11)
def sample(im,ox,oy,n,step):
    m=im.getchannel('A').load(); pts=[(ox+x,oy+y) for y in range(0,im.height,step) for x in range(0,im.width,step) if m[x,y]>150]
    random.shuffle(pts); return [pts[i%len(pts)] for i in range(n)]
N=1000; stp=max(2,int(5*S))
PA=sample(big,ox,oy,N,stp); PB=sample(TXT0,tx0,ty0,N,stp)
PM=[(random.uniform(0,W),random.uniform(0,H)) for _ in range(N)]; DL=[random.uniform(0,0.5) for _ in range(N)]
BW=int((980 if TALL else 860)*S); BH=int(BW*(0.95 if TALL else 0.6))
def pg(n): im=Image.open(f'{A}/pg_{n}.png').convert('RGB'); return sc(im,BW/1280)
PST,PPB,PCL=pg('store'),pg('pubs'),pg('cal')
COV=[]
for f in sorted(glob.glob(f'{A}/dist/pubs/cover*.webp')):
    im=Image.open(f).convert('RGB'); s=int((170 if not TALL else 190)*S); im=im.resize((s,int(s*min(1.4,im.height/im.width)))); COV.append(rnd(im,int(10*S)))
CL=[]
for f in sorted(glob.glob(f'{A}/dist/clients/*.webp')):
    im=Image.open(f).convert('RGBA'); card=Image.new('RGBA',(int(230*S),int(115*S)),(255,255,255,255)); im.thumbnail((int(190*S),int(90*S)))
    card.alpha_composite(im,((card.width-im.width)//2,(card.height-im.height)//2)); CL.append(rnd(card,int(12*S)))
def count(v,k):
    x=int(v*e(k)); return f'{x:,}'.replace(',','٬').translate(AR)
def stat(numstr,col):
    a=txt(numstr,F(600,96*S),col); p_=txt('+',FL(80*S),col,rtl=False)
    im=Image.new('RGBA',(a.width+p_.width+int(6*S),a.height),(0,0,0,0)); im.alpha_composite(a,(0,0)); im.alpha_composite(p_,(a.width+int(6*S),(a.height-p_.height)//2)); return im
STATS=[(20,'عامًا من الخبرة الميدانية'),(118,'دورة تدريبية'),(60,'جهة شريكة'),(15000,'مستفيد من برامجه')]
def icon(kind,col,s_):
    im=Image.new('RGBA',(s_,s_),(0,0,0,0)); d=ImageDraw.Draw(im); w=max(2,int(4*S)); m=int(s_*0.18)
    if kind=='web': d.rounded_rectangle([m,m,s_-m,s_-m],radius=int(8*S),outline=col,width=w); d.line([m,m+int(s_*0.18),s_-m,m+int(s_*0.18)],fill=col,width=w)
    if kind=='bag': d.rounded_rectangle([m,int(s_*0.35),s_-m,s_-m],radius=int(8*S),outline=col,width=w); d.arc([int(s_*0.32),int(s_*0.15),int(s_*0.68),int(s_*0.55)],180,360,fill=col,width=w)
    if kind=='book': d.rectangle([m,m,s_/2,s_-m],outline=col,width=w); d.rectangle([s_/2,m,s_-m,s_-m],outline=col,width=w)
    if kind=='cal':
        d.rounded_rectangle([m,int(s_*0.25),s_-m,s_-m],radius=int(8*S),outline=col,width=w); d.line([m,int(s_*0.42),s_-m,int(s_*0.42)],fill=col,width=w)
        for xx in (0.38,0.62): d.line([s_*xx,int(s_*0.15),s_*xx,int(s_*0.32)],fill=col,width=w)
    return im
TILES=[('web','موقع رسمي','كل ما يقدّمه حامد في مكان واحد'),('bag','١٨ خدمة ودورة','متجر للخطط والدورات والجلسات'),('book','١٥ إصدارًا','معرفة متاحة للجميع'),('cal','تقويم القطاع','الأيام العالمية والمواسم والفعاليات')]
CATS=['تصميم الخطط والنماذج','الدورات التدريبية','الجلسات الاستشارية','التقييم والتحكيم']
DAYS=[('٢٠ نوفمبر','اليوم العالمي للطفل'),('٥ ديسمبر','اليوم الدولي للمتطوعين'),('١٨ ديسمبر','اليوم العالمي للغة العربية'),('٢٠ ديسمبر','اليوم الدولي للتضامن الإنساني')]
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
  '-c:v','libx264','-pix_fmt','yuv420p','-crf','19','-preset','medium','-movflags','+faststart',OUT],stdin=subprocess.PIPE)
for n in range(FPS*DUR):
    t=n/FPS
    # الخلفية
    if t<8.6:
        fr=Image.new('RGBA',(W,H),OLD+(255,))
    else:
        light=win(t,33.6,34.2,41.6,42.2)+win(t,48.6,49.2,53.6,54.2)
        bg=tuple(int(NAVY[i]+(CREAM[i]-NAVY[i])*light) for i in range(3)); fr=Image.new('RGBA',(W,H),bg+(255,))
    d=ImageDraw.Draw(fr)
    # أ) الهوية السابقة والأرقام
    if t<8.4:
        fo=1-e((t-7.6)/0.5)
        for gx in range(0,W,int(90*S)): d.line([gx,0,gx,H],fill=(232,238,238))
        for gy in range(0,H,int(90*S)): d.line([0,gy,W,gy],fill=(232,238,238))
        lgw=int((430 if not TALL else 640)*S); ol=sc(OLDL,lgw/OLDL.width)
        ly=int((190 if not TALL else 380)*S)
        put(fr,ol,cx,ly+int((1-e(t/0.9))*30*S),win(t,0.0,0.8)*fo)
        put(fr,txt('الهوية السابقة',F(400,30*S),OLDT),cx,ly+ol.height/2+int(40*S),win(t,0.4,1.0)*fo)
        for i,(v,lab) in enumerate(STATS):
            r_,c_=divmod(i,2)
            if TALL: x=cx; y=int((820+i*240)*S)
            else: x=cx+(1 if c_==0 else -1)*int(230*S); y=cy+int((60+r_*210)*S)
            k=(t-1.2-i*0.45)/1.3; a=win(t,1.2+i*0.45,1.7+i*0.45)*fo
            put(fr,stat(count(v,k),TEAL),x,y,a)
            put(fr,txt(lab,F(400,30*S),OLDT),x,y+int(78*S),a)
        put(fr,txt('وتستحق هوية تليق بها',F(600,52*S),CORAL),cx,H-int((80 if not TALL else 150)*S),win(t,5.6,6.4)*fo)
        if t>7.9:  # مسح باللون الكحلي من اليمين
            k=eio((t-7.9)/0.7); xw=int(W*(1-k)); d.rectangle([xw,0,W,H],fill=NAVY); d.rectangle([xw-int(8*S),0,xw,H],fill=CORAL)
    # ب+ج) قطرة ودوائر تكشف الشعار
    if 8.4<t<13.6:
        fo=1-e((t-13.0)/0.6); lt=t-8.6
        if 0<lt<0.6:
            y=-30*S+(cy-(-30*S))*eio(lt/0.6); r=12*S; d.ellipse([cx-r,y-r,cx+r,y+r],fill=CORAL)
        for i in range(5):
            k=(lt-0.6-i*0.28)/2.4
            if 0<k<1:
                R=max(W,H)*0.62*e(k); a=int(255*(1-k)*0.9*fo); d.ellipse([cx-R,cy-R,cx+R,cy+R],outline=(CORAL if i==0 else GUIDE)+(a,),width=max(1,int((3 if i==0 else 2)*S)))
        R=max(W,H)*0.62*e((lt-1.0)/2.0)
        if R>2:
            m=Image.new('L',big.size,0); ImageDraw.Draw(m).ellipse([cx-ox-R,cy-oy-R,cx-ox+R,cy-oy+R],fill=255)
            lg=big.copy(); lg.putalpha(ImageChops.multiply(lg.getchannel('A'),m)); put(fr,lg,ox,oy,fo,anchor='tl')
        tri(d,win(t,10.6,11.6,12.8,13.6)); orn(d,cx,oy+big.height+int(60*S),CORAL,int(255*win(t,11.2,11.8,12.8,13.4)))
    # د) النقاط تكتب الشعار اللفظي
    if 13.0<t<19.4:
        fa=win(t,13.0,13.3)
        for i in range(N):
            a1=eio((t-13.1-DL[i]*0.4)/0.8); a2=eio((t-14.0-DL[i])/1.4)
            x=PA[i][0]+(PM[i][0]-PA[i][0])*a1; y=PA[i][1]+(PM[i][1]-PA[i][1])*a1
            x=x+(PB[i][0]-x)*a2; y=y+(PB[i][1]-y)*a2
            al=int(230*fa*(1-win(t,15.6,16.2)))
            if al>3: r=1.9*S; d.ellipse([x-r,y-r,x+r,y+r],fill=CREAM+(al,))
        if t>15.4:
            fo=1-e((t-18.8)/0.6)
            put(fr,TXT0,tx0,ty0,win(t,15.4,16.0)*fo,anchor='tl')
            k=int(min(7,max(0,(t-16.9)*9)))
            put(fr,two_tone(k),cx,cy+int(115*S),win(t,16.1,16.7)*fo)
    # هـ) التحول
    if 19.2<t<24.8:
        fo=1-e((t-24.2)/0.6)
        put(fr,txt('التحول',F(600,34*S),CORAL),cx,int((150 if not TALL else 330)*S),win(t,19.3,19.8)*fo)
        put(fr,txt('من حضور متفرق إلى منظومة متكاملة',F(600,54*S)),cx,int((215 if not TALL else 400)*S),win(t,19.5,20.2)*fo)
        for i,(ic,ti,su) in enumerate(TILES):
            k=e((t-20.2-i*0.3)/0.6)
            if TALL: x=cx; y=int((640+i*270)*S); tw,th=int(880*S),int(220*S)
            else: r_,c_=divmod(i,2); x=cx+(1 if c_==0 else -1)*int(245*S); y=cy+int((40+r_*230)*S); tw,th=int(470*S),int(200*S)
            tile=Image.new('RGBA',(tw,th),(14,53,92,255)); dt=ImageDraw.Draw(tile)
            tile.alpha_composite(icon(ic,CORAL+(255,),int(90*S)),(tw-int(120*S),int((th-90*S)/2)))
            t1=txt(ti,F(600,40*S)); t2=txt(su,F(400,24*S),MUT)
            tile.alpha_composite(t1,(tw-int(140*S)-t1.width,int(th/2-t1.height-6*S))); tile.alpha_composite(t2,(tw-int(140*S)-t2.width,int(th/2+10*S)))
            put(fr,rnd(tile,int(16*S)),x,y+int((1-k)*60*S),k*fo)
    # و) المتجر
    if 24.6<t<34.2:
        fo=win(t,24.6,25.2,33.6,34.2); lt=t-25.0
        hy=int((120 if not TALL else 250)*S)
        put(fr,txt('المتجر',F(600,34*S),CORAL),cx,hy,fo); put(fr,txt('١٨ خدمة ودورة تطلبها منظمتك مباشرة',F(600,46*S)),cx,hy+int(60*S),fo)
        top=(PST.height-BH)*eio(lt/8.0)*0.85
        by=cy+int((40 if not TALL else -40)*S); k=e((t-24.8)/0.8)
        put(fr,browser(PST,top,BW,BH),cx+int((1-k)*150*S),by,k*fo)
        for i,c in enumerate(CATS):
            kk=win(t,26.0+i*1.6,26.4+i*1.6)
            act=26.0+i*1.6<=t<27.6+i*1.6
            pill=txt(c,F(600,30*S),CREAM if act else INK,pad=int(16*S),bg=CORAL if act else (240,236,228),r=20)
            if TALL: px_=cx; py_=by+BH/2+int((130+i*80)*S)
            else: px_=cx+BW/2-int(40*S)-pill.width/2 - i*0; py_=by-BH/2+int((60+i*70)*S)
            if not TALL: px_=cx-BW/2+int(20*S)+pill.width/2
            put(fr,shadow(pill,int(20*S)) if act else pill,px_,py_,kk*fo)
    # ز) الإصدارات
    if 33.6<t<42.2:
        fo=win(t,33.6,34.2,41.6,42.2)
        hy=int((110 if not TALL else 230)*S)
        put(fr,txt('الإصدارات',F(600,34*S),CORAL),cx,hy,fo); put(fr,txt('١٥ إصدارًا، معرفة متاحة للجميع',F(600,46*S),NAVY),cx,hy+int(60*S),fo)
        cols=5 if not TALL else 3; gw=int((190 if not TALL else 290)*S); gh=int((230 if not TALL else 330)*S)
        drift=int((t-34)*12*S)
        for i,cv in enumerate(COV):
            r_,c_=divmod(i,cols); k=e((t-34.3-i*0.12)/0.7)
            x=cx+((cols-1)/2-c_)*gw; y=hy+int(200*S)+r_*gh+cv.height/2-drift
            put(fr,shadow(cv,int(10*S)),x,y+int((1-k)*120*S),k*fo)
        nb=txt('نشرة «الاستدامة المالية» على لينكدإن، أكثر من ٦٤٠٠ مشترك',F(600,30*S),CREAM,pad=int(18*S),bg=NAVY,r=12)
        put(fr,nb,cx,H-int((90 if not TALL else 200)*S),win(t,38.5,39.2,41.6,42.2))
    # ح) التقويم
    if 41.6<t<49.2:
        fo=win(t,41.6,42.2,48.6,49.2)
        hy=int((120 if not TALL else 250)*S)
        put(fr,txt('تقويم القطاع',F(600,34*S),CORAL),cx,hy,fo); put(fr,txt('الأيام العالمية والمواسم والفعاليات في مكان واحد',F(600,40*S)),cx,hy+int(60*S),fo)
        by=cy+int((60 if not TALL else -120)*S); k=e((t-41.8)/0.8)
        put(fr,browser(PCL,(PCL.height-BH)*0.15*eio((t-42)/6),BW,BH),cx,by+int((1-k)*80*S),k*fo*(1 if TALL else 0.55))
        for i,(dt_,nm) in enumerate(DAYS):
            kk=e((t-43.0-i*0.9)/0.6)
            card=Image.new('RGBA',(int(560*S),int(96*S)),(255,255,255,255)); dc=ImageDraw.Draw(card)
            dc.rectangle([card.width-int(8*S),0,card.width,card.height],fill=CORAL)
            a1=txt(nm,F(600,32*S),NAVY); a2=txt(dt_,F(400,26*S),CORAL)
            card.alpha_composite(a1,(card.width-int(30*S)-a1.width,int(14*S))); card.alpha_composite(a2,(card.width-int(30*S)-a2.width,int(56*S)))
            if TALL: x=cx; y=by+BH/2+int((150+i*115)*S)
            else: x=cx; y=cy+int((-110+i*115)*S)
            put(fr,shadow(rnd(card,int(12*S)),int(12*S)),x+int((1-kk)*100*S),y,kk*fo)
    # ط) الشركاء
    if 48.6<t<54.2:
        fo=win(t,48.6,49.2,53.6,54.2)
        hy=int((170 if not TALL else 420)*S)
        put(fr,txt('جهات وثقت بخبرته',F(600,54*S),NAVY),cx,hy,fo)
        put(fr,txt('من القطاع غير الربحي والجهات الحكومية والقطاع الخاص',F(400,30*S),(94,102,115)),cx,hy+int(60*S),fo)
        rows=3 if not TALL else 5; per=(len(CL)+rows-1)//rows; cw_=int(250*S)
        for rI in range(rows):
            sp=(t-48.6)*int(70*S)*(1 if rI%2 else -1)
            y=hy+int(200*S)+rI*int(140*S)
            for j in range(per*2):
                im=CL[(rI*per+j)%len(CL)]; x=(j*cw_+sp+rI*90*S)%(per*cw_)-cw_
                put(fr,im,x,y,fo,anchor='tl')
    # ي) الختام
    if t>53.8:
        k=win(t,54.0,54.8); tri(d,e((t-53.9)/1.0))
        put(fr,sc(LW,460*S/LW.width),cx,cy-int(160*S),k)
        orn(d,cx,cy-int(50*S),CORAL,int(255*win(t,54.5,55.2)))
        put(fr,txt('استدامة العطاء وأثرٌ يمتد',F(400,46*S),MUT),cx,cy+int(20*S),win(t,54.8,55.6))
        put(fr,txt('hamedalthiabi.com',FL(44*S),CREAM,rtl=False,pad=int(24*S),bg=CORAL),cx,cy+int(130*S),win(t,55.4,56.2))
        put(fr,txt('@hamedalthiabi',FL(30*S),MUT,rtl=False),cx,cy+int(225*S),win(t,56.0,56.8))
    p.stdin.write(fr.convert('RGB').tobytes())
p.stdin.close(); p.wait(); print(OUT)
