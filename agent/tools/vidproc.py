import subprocess, sys, json
from PIL import Image, ImageDraw
import cover
import os; B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','brand')+'/'
def probe(f):
    o=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',f]))
    a=[s for s in o['streams'] if s['codec_type']=='audio'][0]
    return int(a['sample_rate'])
def badge(width,out):
    lg=Image.open(B+'logo_white.png'); w=int(width*0.24); lw=int(w*0.8)
    lg=lg.resize((lw,int(lg.height*lw/lg.width)),Image.LANCZOS)
    h=lg.height+int(w*0.16)
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,w-1,h-1],radius=int(h*0.22),fill=(0,37,68,225))
    im.paste(lg,((w-lw)//2,(h-lg.height)//2),lg); im.save(out); return out
def logo_only(src,out,pos):
    w=int(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width','-of','csv=p=0',src]).decode().strip())
    b=badge(w,'/tmp/badge.png'); m=int(w*0.04)
    xy={'tc':f'(W-w)/2:{m}','tr':f'W-w-{m}:{m}','tl':f'{m}:{m}'}[pos]
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-i',b,'-filter_complex',f'[0:v][1:v]overlay={xy}','-c:v','libx264','-crf','20','-preset','medium','-c:a','copy','-movflags','+faststart',out],check=True)
def with_cover(src,out,title,tag):
    cover.make(title,tag,'/tmp/cv.png'); sr=probe(src)
    fc=(f"[1:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x002544,setsar=1,fps=30,format=yuv420p[v1];"
        f"[0:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[v0];"
        f"[2:a]atrim=0:1.5,asetpts=PTS-STARTPTS[a0];[1:a]aresample={sr}[a1];"
        f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]")
    subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-t','1.5','-i','/tmp/cv.png','-i',src,
        '-f','lavfi','-t','1.5','-i',f'anullsrc=r={sr}:cl=stereo','-filter_complex',fc,'-map','[v]','-map','[a]',
        '-c:v','libx264','-crf','20','-preset','medium','-c:a','aac','-b:a','128k','-movflags','+faststart',out],check=True)
