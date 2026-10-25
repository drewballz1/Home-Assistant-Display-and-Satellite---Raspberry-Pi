import json, numpy as np, sys
uw=np.array([0,-0.3407,0.9402]); nw=np.array([0,-0.9402,-0.3407])
def wp(x,s,d=0): return (np.array([x,76,7.1])+s*uw+d*nw).round(2).tolist()
def v(a): return np.round(a,2).tolist()
C=dict(stand='#c9ced4',frame='#7b8794',glass='#141a24',pcb='#1d6b3a',rs='#2b2f36',metal='#c9ced3',dark='#3a3f45',spk='#9aa3ad',box='#d6913f',foam='#f2d16b',bar='#6d7680',door='#c9ced4',screw='#e8e8e8')
def P(f,c,**k): d=dict(f='p_%s.stl'%f,c=c); d.update(k); return d
def O(vec,k): return v(np.array(vec)*k)
glass=P('glass',C['glass'],metal=0.3,rough=0.25,e=False)
stand=P('stand',C['stand']); frame=P('frame',C['frame']); door=P('door',C['door'])
pi=[P('pi_pcb',C['pcb']),P('pi_metal',C['metal'],metal=0.5,rough=0.4),P('pi_dark',C['dark'])]
rs=[P('rs_pcb',C['rs']),P('rs_comp',C['metal'],metal=0.4,rough=0.5,ea=40,eo=0.25)]
spk=[P('speaker',C['spk'],metal=0.3,ea=40,eo=0.3)]
inside=pi+rs+spk+[P('box',C['box']),P('bar',C['bar'],metal=0.5),P('mic_foam',C['foam']),P('foam_ring',C['foam'])]
S=[]
# ---------- overview
S.append(dict(out='raw_ov_front.png',w=1000,h=760,fov=20,cam=[-330,-560,330],target=[0,28,56],parts=[stand,frame,glass,door],shadow=True,ground=0))
S.append(dict(out='raw_ov_back.png',w=1000,h=760,fov=20,cam=[330,600,300],target=[0,40,52],parts=[stand,frame,glass,door],shadow=True,ground=0))
# ---------- back features
W1=1700
L=[dict(p=wp(-45,96,-1.8),t='Exhaust holes',at=[1380,170]),
   dict(p=wp(-1.47,81.5,-2.3),t='MUTE button',at=[1380,290]),
   dict(p=wp(6.22,80.74,-1.8),t='USR poke hole',at=[1380,380]),
   dict(p=wp(-52.15,30,-2),t='Speaker grille',at=[1380,640]),
   dict(p=[wp(-52.15+i*30,42+j*30,-1.8) for i in [-1,1] for j in [-1,1]],t='Speaker box screws\n4x M3, countersunk',at=[1380,850]),
   dict(p=wp(0,8,-1.8),t='Rear cable hole\n(Pi USB-C power)',at=[1380,1030]),
   dict(p=[wp(0.49,92,-1.8),wp(71.49,92,-1.8)],t='Mic pinholes (2)',at=[330,150]),
   dict(p=wp(80,44,-1.8),t='"PI PORTS" label',at=[330,560]),
   dict(p=[96,50,46],t='Pi ports cover',at=[330,800])]
S.append(dict(out='back-features.png',w=W1,h=1150,fov=22,cam=[300,500,300],target=[2,48,50],parts=[stand,frame,glass,door],labels=L,shadow=True,ground=0))
# ---------- mute close-ups (whole piece, camera zoomed in)
tgt=np.array(wp(22,86,-2)); out_n=-nw
L=[dict(p=wp(-1.47,82.5,-2.3),t='MUTE button\n(flexure tab, grip ridges)',at=[1150,190]),
   dict(p=wp(-1.47-5.5,80,-2),t='1 mm slot frees the tab',at=[1150,560]),
   dict(p=wp(-1.47,73.4,-1.8),t='"MUTE" engraved',at=[1150,780]),
   dict(p=wp(6.22,80.74,-1.8),t='USR poke hole',at=[330,700]),
   dict(p=[wp(0.49,92,-1.8),wp(71.49,92,-1.8)],t='Mic pinholes',at=[330,130])]
S.append(dict(out='raw_mute_out.png',w=1500,h=950,fov=18,cam=v(tgt+300*out_n+np.array([-60,0,70])),target=v(tgt),parts=[stand,frame,glass,door],labels=L,key=[400,500,300],hemi=1.6,keyI=1.6))
tin=np.array(wp(25,88,2)); in_n=nw
Lb=[dict(p=wp(-1.47,80.74,0.1),t='Nub on back of MUTE tab',at=[1150,840]),
    dict(p=[wp(-5+5.49,92,0.9),wp(-5+76.49,92,0.9)],t='Mic pads (foam squares\nseal mic to pinhole)',at=[1150,150]),
    dict(p=[wp(-5+2.46,75+31.56,3),wp(-5+60.16,75+2.66,3)],t='ReSpeaker standoffs\n(M2 pilot holes)',at=[340,150]),
    dict(p=[wp(-11.2+61.5,15+52.5,5)],t='Pi standoff',at=[340,860])]
camin=v(tin+330*in_n+np.array([-40,0,170]))
S.append(dict(out='raw_mute_in.png',w=1500,h=950,fov=19,cam=camin,target=v(tin),parts=[stand],labels=Lb,key=[-200,-500,700]))
Lc=[dict(p=wp(-5+40,75+30,4.6),t='ReSpeaker Lite\n(mics + buttons\nface the wall)',at=[340,330]),
    dict(p=wp(-5+5.49,92,1.6),t='Foam square',at=[340,140]),
    dict(p=wp(-5+2.46,75+31.56,4.6),t='M2 screw',at=[1150,150]),
    dict(p=wp(20,40,22),t='Pi 5',at=[1150,850])]
S.append(dict(out='raw_mute_in2.png',w=1500,h=950,fov=19,cam=camin,target=v(tin),parts=[stand,P('mic_foam',C['foam'])]+[dict(x,o=0.6) for x in rs]+pi,labels=Lc,key=[-200,-500,700]))
# ---------- inside mounts: bare + populated, looking into the open face
cin=[-170,-420,300]; tI=[-2,48,48]
Lm=[dict(p=[wp(-5+2.46,75+31.56,3),wp(-5+60.16,75+2.66,3)],t='ReSpeaker standoffs (2, M2)',at=[1380,110]),
    dict(p=[wp(-5+5.49,92,0.9),wp(-5+76.49,92,0.9)],t='Mic pads',at=[1380,220]),
    dict(p=wp(-1.47,80.74,0.1),t='MUTE tab',at=[1380,320]),
    dict(p=[40,40,14],t='Weight pocket\n(opens at the back)',at=[1380,720]),
    dict(p=[wp(-11.2+a,15+b,5) for a in [3.5,61.5] for b in [3.5,52.5]],t='Pi 5 standoffs (4, M2.5)',at=[1380,950]),
    dict(p=[wp(-52.15+i*30,42+j*30,3) for i in [-1,1] for j in [-1,1]],t='Speaker pads (4)',at=[330,170]),
    dict(p=wp(-52.15,42,0),t='Speaker grille',at=[330,400]),
    dict(p=[20,-0.2,9.2],t='Spacer ring\n(display rests here)',at=[330,960])]
S.append(dict(out='raw_in_bare.png',w=W1,h=1100,fov=24,cam=cin,target=tI,parts=[stand],labels=Lm))
Lp=[dict(p=wp(30,102,4.6),t='ReSpeaker Lite',at=[1380,150]),
    dict(p=[94,48,42],t='Pi ports cover',at=[1380,520]),
    dict(p=wp(20,42,20),t='Raspberry Pi 5\n+ Active Cooler',at=[1380,860]),
    dict(p=[60,30,20],t='Steel weight bar',at=[1380,1010]),
    dict(p=wp(-52.15,42,32),t='Speaker box\n(3" speaker inside)',at=[330,250])]
S.append(dict(out='raw_in_full.png',w=W1,h=1100,fov=24,cam=cin,target=tI,parts=[stand,door]+inside,labels=Lp))
# ---------- speaker assembly, exploded out through the open face
e=np.array([0,-0.956,0.292])
ex=[stand,P('foam_ring',C['foam'],off=O(e,35)),P('speaker',C['spk'],metal=0.3,ea=40,eo=0.3,off=O(e,95)),P('box',C['box'],off=O(e,175))]
Ls=[dict(p=wp(-52.15,30,0),t='Grille in the back wall',at=[330,900]),
    dict(p=[wp(-52.15+30,42+j*30,3) for j in [-1,1]],t='Screw pads (4; screws\ncome in from the back)',at=[330,700]),
    dict(p=v(np.array(wp(-52.15,42-36,1.5))+35*e),t='3 mm foam ring',at=[330,470]),
    dict(p=v(np.array(wp(-52.15-30,42,12))+95*e),t='3" speaker,\ncone toward the wall',at=[330,250]),
    dict(p=v(np.array(wp(-52.15,42,60))+175*e),t='Speaker box (~160 cm³),\nthin gasket on the rim',at=[1380,120])]
S.append(dict(out='raw_spk_ex.png',w=W1,h=1100,fov=19,cam=[-600,-680,470],target=[-55,-45,55],parts=ex,labels=Ls))
sc=[stand,frame,glass,door,P('screws',C['screw'],metal=0.6,rough=0.3,off=O(-nw,22))]
Lsc=[dict(p=[v(np.array(wp(-52.15+i*30,42+j*30,-1.8))+22*(-nw)) for i in [-1,1] for j in [-1,1]],t='4x M3 x 16 countersunk\nself-tapping, from the back',at=[1300,140])]
S.append(dict(out='raw_spk_back.png',w=W1,h=1000,fov=18,cam=[-170,540,330],target=[-48,62,54],parts=sc,labels=Lsc))
# ---------- pi ports cover: closed + removed (viewed from that side)
pc_cam=[560,110,150]; pc_t=[80,42,42]
S.append(dict(out='raw_pc_closed.png',w=1300,h=950,fov=22,cam=pc_cam,target=pc_t,parts=[stand,frame,glass,door]+pi,
  labels=[dict(p=[95.8,48,44],t='Clip-on cover\n(plain, no text)',at=[1000,150])]))
S.append(dict(out='raw_pc_open.png',w=1300,h=950,fov=22,cam=pc_cam,target=pc_t,parts=[stand,frame,glass,P('door',C['door'],off=[30,-100,-5])]+pi,
  labels=[dict(p=[77,40,45],t='USB + Ethernet\n(right-angle USB-A plug)',at=[300,170]),dict(p=[126,-52,57],t='Cover: snap rim +\nfingernail notch',at=[1000,820])]))
# ---------- speaker box: rim side + section through the mounted box
bc=np.array([-52,40,45])
S.append(dict(out='raw_box.png',w=1000,h=900,fov=24,cam=v(bc+300*(-nw)+np.array([-120,0,90])),target=v(bc),parts=[P('box',C['box'])],
  labels=[dict(p=v(np.array(wp(-52.15-30,42+30,6))),t='Pilot holes (4)\nfor the M3 screws',at=[260,160]),dict(p=wp(-52.15,42,28),t='Cavity: round to fit\nthe speaker basket',at=[740,820])]))
S.append(dict(out='raw_box_cut.png',w=1000,h=900,fov=29,cam=v(bc+np.array([-380,-90,110])),target=v(bc+np.array([0,8,2])),
  clip=[dict(n=[1,0,0],d=52.15)],parts=[P('stand',C['stand'],cap='#8f969e'),P('box',C['box'],cap='#a5682a'),P('speaker',C['spk'],metal=0.3,ea=40,eo=0.3,cap='#6c747d'),P('screws',C['screw'],metal=0.6,cap='#999'),P('foam_ring',C['foam'],cap='#d9b23f')],
  labels=[dict(p=wp(-52.15,42,40),t='Sealed box',at=[220,140]),dict(p=wp(-52.15,42+20,10),t='Speaker',at=[220,300]),dict(p=wp(-52.15,42,-1),t='Back wall + grille',at=[780,820])]))
for x in S:
    if x['out'] in ('raw_mute_in.png','raw_mute_in2.png'): x['fs']=38
    if x['out'] in ('raw_pc_closed.png','raw_pc_open.png','raw_box.png','raw_box_cut.png'): x['fs']=30
json.dump(S,open(sys.argv[1],'w'))
print(len(S))
