import numpy as np, wave
from scipy.signal import butter, lfilter
SR=44100; D=26.8; N=int(SR*D); out=np.zeros(N)
rng=np.random.default_rng(3)
def add(sig,t,g=1.0):
    i=int(t*SR); j=min(N,i+len(sig)); out[i:j]+=g*sig[:j-i]
def env(n,a,dec): x=np.arange(n)/SR; return np.minimum(1,x/max(a,1e-4))*np.exp(-x/dec)
def lp(x,f): b,a=butter(2,f/(SR/2)); return lfilter(b,a,x)
def bp(x,f1,f2): b,a=butter(2,[f1/(SR/2),f2/(SR/2)],btype='band'); return lfilter(b,a,x)
def drop():
    n=int(0.35*SR); x=np.arange(n)/SR; f=1400*np.exp(-x*9)+500
    return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,0.002,0.07)
def boom(dur=2.2,f=52):
    n=int(dur*SR); x=np.arange(n)/SR; return np.sin(2*np.pi*f*x+2*np.sin(2*np.pi*f*0.5*x))*env(n,0.01,0.7)
def whoosh(dur=0.9,f1=300,f2=3000):
    n=int(dur*SR); w=rng.standard_normal(n); w=bp(w,f1,f2); x=np.linspace(0,1,n); return w*np.sin(np.pi*x)**2*0.6
def click():
    n=int(0.06*SR); return bp(rng.standard_normal(n),2000,6000)*env(n,0.001,0.012)*0.8
def bell(f=660,dur=3.0):
    n=int(dur*SR); x=np.arange(n)/SR; s=sum(a*np.sin(2*np.pi*f*m*x)*np.exp(-x/(1.2/m)) for m,a in [(1,1),(2,0.45),(3,0.25),(4.2,0.12)])
    return s*env(n,0.004,10)
def rise(dur=1.4):
    n=int(dur*SR); x=np.arange(n)/SR; f=220+260*(x/dur); s=np.sin(2*np.pi*np.cumsum(f)/SR)*0.5+0.3*np.sin(2*np.pi*np.cumsum(f*1.5)/SR)
    return s*np.sin(np.pi*x/dur)**2*0.35
def sparkle(dur=1.6):
    s=np.zeros(int(dur*SR))
    for k in range(18):
        t=rng.uniform(0,dur-0.2); f=rng.uniform(1800,3600); n=int(0.15*SR); x=np.arange(n)/SR
        i=int(t*SR); s[i:i+n]+=np.sin(2*np.pi*f*x)*env(n,0.002,0.04)*rng.uniform(0.1,0.25)
    return s
# أجواء هادئة خفيفة جدًا (ريح ناعمة)
bed=lp(rng.standard_normal(N),500); fade=np.minimum(1,np.arange(N)/(SR*2))*np.minimum(1,(N-np.arange(N))/(SR*2)); out+=bed*fade*0.05
add(drop(),0.55,0.9); add(boom(),0.6,0.55); add(whoosh(1.4,150,1200),0.7,0.35)
add(sparkle(1.4),4.3,0.8); add(whoosh(0.8),4.1,0.35)
add(boom(1.5,70),6.9,0.35); add(rise(),8.6,0.8)
add(whoosh(0.7),10.4,0.4)
for k in range(9): add(click(),10.7+k*0.08,0.35)
add(bell(880,2.0),12.0,0.18)
add(whoosh(0.8,200,2500),13.0,0.35)
add(whoosh(0.9),15.3,0.4)
for t in [17.9,19.7,21.6]: add(whoosh(0.4,800,5000),t-0.15,0.25); add(click(),t,0.5)
add(whoosh(1.0,150,1800),23.2,0.4); add(boom(2.5,48),23.5,0.5); add(bell(660,3.2),23.6,0.3); add(bell(990,3.0),24.5,0.15)
out=out/np.max(np.abs(out))*0.8
end=np.minimum(1,(N-np.arange(N))/(SR*1.2)); out*=end
st=np.stack([out,out*0.97],1)
with wave.open('sfx.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
print('ok')
