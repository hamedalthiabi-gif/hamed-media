import subprocess
from PIL import Image, ImageDraw, ImageFont
import os; B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','brand')+'/'
W,H=1080,1920
NAVY=(0,37,68); CORAL=(187,104,65); CREAM=(248,245,239)
F=lambda w,s: ImageFont.truetype(B+f'plex-{w}.ttf',s,layout_engine=ImageFont.Layout.RAQM)
def logo_badge(out):
    lg=Image.open(B+'logo_navy.png'); lw=230
    lg=lg.resize((lw,int(lg.height*lw/lg.width)),Image.LANCZOS)
    w,h=lw+44,lg.height+30
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,w-1,h-1],radius=18,fill=(248,245,239,235))
    im.paste(lg,(22,15),lg); im.save(out); return w,h
def banner(title,tag,out):
    ft=F(600,58); fg=F(600,34)
    d0=ImageDraw.Draw(Image.new('RGB',(1,1)))
    # wrap to max 2 lines within 900px
    words=title.split(); lines=[]; cur=''
    for w_ in words:
        c=(cur+' '+w_).strip()
        if d0.textlength(c,font=ft,direction='rtl')<=860: cur=c
        else: lines.append(cur); cur=w_
    lines.append(cur)
    tw=max(d0.textlength(l,font=ft,direction='rtl') for l in lines)
    gw=d0.textlength(tag,font=fg,direction='rtl')
    bw=1080; lh=84; bh=max(len(lines),2)*lh+40+(30 if len(lines)<2 else 0); gh=58
    im=Image.new('RGBA',(max(bw,int(gw+60)),gh+bh),(0,0,0,0)); d=ImageDraw.Draw(im)
    R=im.width
    d.rectangle([0,0,R,gh],fill=NAVY+(255,))
    d.text((R-28,gh/2),tag,font=fg,fill=CREAM,anchor='rm',direction='rtl')
    d.rectangle([R-bw,gh,R,gh+bh],fill=CORAL+(255,))
    for i,l in enumerate(lines):
        d.text((R-45,gh+20+lh/2+i*lh+(bh-40-len(lines)*lh)/2),l,font=ft,fill=CREAM,anchor='rm',direction='rtl')
    im.save(out); return im.size
def render(src,out,title,tag='سلسلة القطاع الجديد',t_in=0.0,t_out=5.0,start=0):
    lw,lh=logo_badge('/tmp/logo.png')
    bw,bh=banner(title,tag,'/tmp/ban.png')
    X=W-bw; Y=int(H*0.455); s=0.4
    # ease-out slide in from right, ease-in slide out to right
    xe=(f"if(lt(t,{t_in}),W,if(lt(t,{t_in+s}),{X}+(W-{X})*pow(1-(t-{t_in})/{s},3),"
        f"if(lt(t,{t_out}),{X},if(lt(t,{t_out+s}),{X}+(W-{X})*pow((t-{t_out})/{s},3),W))))")
    fc=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=0x002544,setsar=1[b];"
        f"[b][1:v]overlay=40:{int(H*0.095)}[l];[l][2:v]overlay=x='{xe}':y={Y}:eval=frame,format=yuv420p[v]")
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',src,'-i','/tmp/logo.png','-loop','1','-i','/tmp/ban.png',
        '-filter_complex',fc,'-map','[v]','-map','0:a','-shortest','-c:v','libx264','-crf','21','-preset','veryfast',
        '-c:a','copy','-movflags','+faststart',out],check=True)
def logo_only_tl(src,out):
    logo_badge('/tmp/logo.png')
    fc=(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=0x002544,setsar=1[b];"
        f"[b][1:v]overlay=40:{int(H*0.095)},format=yuv420p[v]")
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-i','/tmp/logo.png','-filter_complex',fc,'-map','[v]','-map','0:a',
        '-c:v','libx264','-crf','21','-preset','veryfast','-c:a','copy','-movflags','+faststart',out],check=True)
