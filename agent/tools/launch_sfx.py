# تصميم صوتي سينمائي لإطلاق الهوية: صعود، ضربات، طنين عميق، نبض، ضربة ختام
import numpy as np, wave
from scipy.signal import butter, lfilter, fftconvolve, sawtooth
SR=44100; D=26.7; N=int(SR*D); L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(5)
def add(s,t,g=1.0,pan=0.0):
    i=int(t*SR); j=min(N,i+len(s)); L[i:j]+=g*(1-pan)*s[:j-i]; R[i:j]+=g*(1+pan)*s[:j-i]
x_=lambda n: np.arange(n)/SR
def env(n,a,d): x=x_(n); return np.minimum(1,x/max(a,1e-4))*np.exp(-x/d)
def lp(s,f): b,a=butter(2,min(f,SR/2.1)/(SR/2)); return lfilter(b,a,s)
def hp(s,f): b,a=butter(2,f/(SR/2),'high'); return lfilter(b,a,s)
def bp(s,a1,a2): b,a=butter(2,[a1/(SR/2),a2/(SR/2)],'band'); return lfilter(b,a,s)
IR=rng.standard_normal(int(2.8*SR))*np.exp(-x_(int(2.8*SR))/0.7); IR/=np.sum(np.abs(IR))**0.5*30
def verb(s,wet=0.35): w=fftconvolve(s,IR)[:len(s)+len(IR)//2]; d=np.zeros(len(w)); d[:len(s)]=s; return d*(1-wet)+w*wet*3
def sub(f0=55,f1=32,dur=2.5):
    n=int(dur*SR); x=x_(n); f=f1+(f0-f1)*np.exp(-x*6); return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,0.003,0.8)
def hit(dur=3.0,big=1.0):
    n=int(0.25*SR); noise=lp(rng.standard_normal(n),2500)*env(n,0.001,0.05)
    s=np.zeros(int(dur*SR)); s[:n]+=noise*0.8; s+=sub(60,30,dur)*1.2*big
    return verb(s,0.4)
def braam(dur=4.5):
    n=int(dur*SR); x=x_(n); s=sum(sawtooth(2*np.pi*f*x*(1+0.002*np.sin(2*np.pi*0.3*x)))*a for f,a in [(55,1),(82.4,0.7),(110,0.6),(164.8,0.3)])
    cut=200+1800*np.exp(-x*1.2); out=np.zeros(n)
    for k in range(0,n,2048): out[k:k+2048]=lp(s[k:k+2048+0],cut[k])[:len(out[k:k+2048])]
    v=verb(out*env(n,0.02,1.4)*0.35,0.45); v[:n]+=sub(50,28,dur)*0.8; return v
def riser(dur=1.6,f1=200,f2=4000):
    n=int(dur*SR); x=x_(n)/dur; w=rng.standard_normal(n); out=np.zeros(n)
    for k in range(0,n,1024):
        fc=f1*(f2/f1)**x[k]; out[k:k+1024]=bp(w[k:k+1024],fc*0.6,min(fc*1.4,20000))
    tone=np.sin(2*np.pi*np.cumsum(80+400*x**2)/SR)*0.3
    return (out*0.8+tone)*x**2.2
def whoosh(dur=0.8,f1=250,f2=3500):
    n=int(dur*SR); x=np.linspace(0,1,n); return bp(rng.standard_normal(n),f1,f2)*np.sin(np.pi*x)**3
def shimmer(dur=1.8):
    s=np.zeros(int(dur*SR))
    for _ in range(26):
        t=rng.uniform(0,dur-0.3); f=rng.choice([1760,2093,2637,3136,3520]); n=int(0.3*SR)
        i=int(t*SR); s[i:i+n]+=np.sin(2*np.pi*f*x_(n))*env(n,0.002,0.09)*rng.uniform(0.08,0.2)
    return verb(s,0.5)
def pad(dur,notes=(55,82.4,110,130.8),g=1.0):
    n=int(dur*SR); x=x_(n); s=sum(np.sin(2*np.pi*f*x)+0.3*np.sin(2*np.pi*2*f*x+0.4) for f in notes)/len(notes)
    e=np.minimum(1,x/1.5)*np.minimum(1,(dur-x)/1.2); return s*e*g
def kick(): n=int(0.35*SR); return sub(110,45,0.35)*env(n,0.001,0.09)*1.4
def tick(): n=int(0.05*SR); return hp(rng.standard_normal(n),6000)*env(n,0.0005,0.01)
def bell(f=880,dur=3.0):
    n=int(dur*SR); x=x_(n); return verb(sum(a*np.sin(2*np.pi*f*m*x)*np.exp(-x/(1.4/m)) for m,a in [(1,1),(2.01,0.4),(3.02,0.2)])*env(n,0.003,9),0.5)
# --- الجدول ---
add(riser(0.6,400,6000),0.0,0.5); add(hit(3.5),0.58,1.0)
add(pad(10.5,(55,82.4,110)),0.6,0.22)
add(riser(1.2,300,5000),3.1,0.55); add(whoosh(0.9),4.0,0.5,0.3); add(shimmer(2.2),4.3,0.9)
add(hit(2.5,0.6),6.85,0.7); add(riser(1.4,200,3000),8.5,0.45); add(bell(1318,2),9.9,0.12)
add(whoosh(0.7),10.35,0.55,-0.3); add(hit(2,0.5),10.65,0.6)
add(pad(6,(61.7,92.5,123.5)),10.6,0.18)
add(whoosh(0.9,200,2500),12.9,0.45,0.3)
add(riser(1.0,300,6000),14.4,0.4); add(hit(2.2,0.7),15.4,0.75)
bt=0.5
for k in range(int((23.2-15.6)/bt)):
    t=15.6+k*bt; add(kick(),t,0.55*(0.6+0.4*k/15))
    add(tick(),t+bt/2,0.25,0.4 if k%2 else -0.4)
for t in [17.9,19.75,21.6]: add(whoosh(0.45,900,7000),t-0.2,0.35,0.5)
add(pad(7.6,(55,82.4,110,138.6)),15.6,0.16)
add(riser(2.0,150,8000),21.4,0.75)
add(braam(4.8),23.45,1.0); add(hit(3.5,1.2),23.45,0.9); add(bell(880,3.2),23.6,0.22); add(bell(1318.5,3.0),24.4,0.12); add(shimmer(2.0),23.7,0.6)
st=np.stack([L,R],1); st=np.tanh(st/np.max(np.abs(st))*1.6)/np.tanh(1.6)*0.89
fade=np.minimum(1,(N-np.arange(N))/(SR*1.5))[:,None]; st*=fade
with wave.open('sfx2.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
print('ok')
