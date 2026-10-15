from PIL import Image, ImageDraw, ImageFont
import os; B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','brand')+'/'; O=B+'launch/'
NAVY=(0,37,68); CORAL=(187,104,65); CREAM=(248,245,239); MUT=(170,182,198)
F=lambda w,s: ImageFont.truetype(B+f'plex-{w}.ttf',s,layout_engine=ImageFont.Layout.RAQM)
def T(d,xy,t,f,c=CREAM,a='mm'): d.text(xy,t,font=f,fill=c,anchor=a,direction='rtl')
def base(W,H,tri=260):
    im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
    d.polygon([(0,0),(tri,0),(0,tri)],fill=CORAL); d.polygon([(W,H),(W,H-tri),(W-tri,H)],fill=CORAL)
    return im,d
def logo(im,w,x,y):
    lg=Image.open(B+'logo_white.png').convert('RGBA'); lg=lg.resize((w,int(lg.height*w/lg.width)),Image.LANCZOS)
    im.paste(lg,(x-w//2,y),lg); return lg.height
def pill(d,cx,cy,t,f,fill=CORAL,pad=36,h=84):
    tw=d.textlength(t,font=f,direction='rtl'); d.rectangle([cx-tw/2-pad,cy-h/2,cx+tw/2+pad,cy+h/2],fill=fill); T(d,(cx,cy),t,f)
def dots(d,cx,y,n=4,c=CORAL):
    for i in range(n):
        x=cx-(n-1)*25+i*50
        if i%2: d.polygon([(x,y-9),(x+9,y),(x,y+9),(x-9,y)],fill=c)
        else: d.ellipse([x-8,y-8,x+8,y+8],fill=c)
# 1) main announcement 1080x1350
W,H=1080,1350; im,d=base(W,H); logo(im,380,W//2,170)
dots(d,W//2,400)
T(d,(W//2,560),'قريبًا',F(600,190))
T(d,(W//2,730),'الموقع الرسمي لحامد الذيابي',F(600,56))
pill(d,W//2,860,'الأربعاء ١١ نوفمبر، الساعة ١١ صباحًا',F(600,44))
T(d,(W//2,1010),'استدامة العطاء وأثر يمتد',F(400,44),MUT)
im.save(O+'01_قريبا.png')
# 2) countdown cards
for n,lab in [(10,'أيام'),(7,'أيام'),(3,'أيام'),(1,'يوم واحد')]:
    im,d=base(W,H); logo(im,300,W//2,150)
    T(d,(W//2,420),'باقي على الإطلاق',F(600,60))
    ar=str(n).translate(str.maketrans('0123456789','٠١٢٣٤٥٦٧٨٩'))
    if n==1: T(d,(W//2,640),'يوم واحد',F(600,170),CORAL)
    else:
        T(d,(W//2,640),ar,F(600,300),CORAL); T(d,(W//2,830),lab,F(600,70))
    pill(d,W//2,990,'١١ نوفمبر، الساعة ١١ صباحًا',F(600,44))
    T(d,(W//2,1150),'hamedalthiabi.com',ImageFont.truetype(B+'plex-latin-400.ttf',34),MUT)
    im.save(O+f'02_باقي_{n}.png')
# 3) launch day
im,d=base(W,H); logo(im,380,W//2,170); dots(d,W//2,400)
T(d,(W//2,560),'انطلقنا',F(600,170))
T(d,(W//2,730),'الموقع الرسمي متاح الآن',F(600,58))
pill(d,W//2,860,'hamedalthiabi.com',ImageFont.truetype(B+'plex-latin-400.ttf',46))
T(d,(W//2,1010),'استدامة العطاء وأثر يمتد',F(400,44),MUT)
im.save(O+'03_يوم_الإطلاق.png')
# 4) headers
for name,(W2,H2) in [('04_غلاف_اكس',(1500,500)),('05_غلاف_لينكدان',(1584,396))]:
    im,d=base(W2,H2,tri=int(H2*0.55)); lh=logo(im,int(H2*0.55),int(W2*0.72),int(H2*0.5)-int(H2*0.55*218/700)//2)
    T(d,(int(W2*0.33),int(H2*0.38)),'الموقع الرسمي قريبًا',F(600,int(H2*0.13)))
    pill(d,int(W2*0.33),int(H2*0.62),'١١ نوفمبر، الساعة ١١ صباحًا',F(600,int(H2*0.075)),h=int(H2*0.16),pad=24)
    im.save(O+name+'.png')
print('ok')
