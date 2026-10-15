import numpy as np, wave, sys
sys.path.insert(0,'/home/claude/x/motion')
exec(open('/home/claude/x/motion/sfx2.py').read().split('# --- الجدول ---')[0].replace('D=26.7','D=60.0'))
# الهوية السابقة: طنين خافت ونقرات العدّ
add(pad(7.8,(73.4,110),0.6),0.0,0.12)
for k in range(40): add(tick(),1.2+k*0.085,0.18,0.3 if k%2 else -0.3)
add(bell(587,1.5),5.6,0.08)
# التحول
add(riser(1.0,300,7000),7.0,0.6); add(whoosh(0.8,200,4000),7.85,0.6,-0.4)
add(hit(3.5),8.6+0.6,0.95); add(pad(4.5,(55,82.4,110)),9.0,0.2)
add(shimmer(1.8),10.8,0.7); add(riser(0.9,300,5000),12.3,0.45)
add(whoosh(0.7),13.0,0.5,0.3); add(shimmer(1.6),13.4,0.8); add(hit(2.2,0.6),15.4,0.7); add(riser(1.0,200,3000),16.8,0.45)
add(whoosh(0.7,250,3000),19.1,0.5,-0.3)
for k in range(4): add(hit(1.0,0.25),20.2+k*0.3,0.35); add(tick(),20.2+k*0.3,0.4)
add(riser(0.8,300,6000),23.8,0.4); add(hit(2.4,0.7),24.6,0.75)
bt=0.5
for k in range(int((48.4-25.0)/bt)):
    tt=25.0+k*bt; add(kick(),tt,0.42); add(tick(),tt+bt/2,0.2,0.4 if k%2 else -0.4)
for tt in [26.0,27.6,29.2,30.8]: add(whoosh(0.35,900,7000),tt-0.15,0.3,0.4)
add(pad(9,(55,82.4,110,138.6)),25.0,0.14)
add(whoosh(0.8),33.5,0.5,-0.3)
for k in range(15): add(tick(),34.3+k*0.12,0.3,(k%3-1)*0.4)
add(bell(1318.5,2),38.5,0.1); add(pad(8,(61.7,92.5,123.5)),34.0,0.12)
add(whoosh(0.8),41.5,0.5,0.3)
for k in range(4): add(whoosh(0.3,1200,8000),43.0+k*0.9-0.1,0.3,0.5); add(tick(),43.0+k*0.9,0.4)
add(whoosh(0.8,200,3000),48.5,0.5,-0.3); add(pad(5,(55,82.4,110)),48.6,0.14)
add(riser(1.6,150,8000),52.3,0.75)
add(braam(5.0),53.9,1.0); add(hit(4,1.2),53.9,0.9); add(bell(880,3.5),54.0,0.22); add(bell(1318.5,3.2),55.4,0.12); add(shimmer(2.2),54.2,0.6)
st=np.stack([L,R],1); st=np.tanh(st/np.max(np.abs(st))*1.6)/np.tanh(1.6)*0.89
fade=np.minimum(1,(N-np.arange(N))/(SR*2))[:,None]; st*=fade
with wave.open('/home/claude/x/motion/sfx3.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
print('ok')
