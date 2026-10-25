import numpy as np, trimesh, shutil
T='/home/claude/td2/'
uw=np.array([0,-0.3407,0.9402]); nw=np.array([0,-0.9402,-0.3407])
def W(x,s):
    M=np.eye(4); M[:3,0]=[1,0,0]; M[:3,1]=uw; M[:3,2]=nw; M[:3,3]=np.array([x,76,7.1])+s*uw; return M
def tr(v): M=np.eye(4); M[:3,3]=v; return M
def box(x0,y0,z0,x1,y1,z1):
    b=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); b.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return b
def cyl(x,y,z0,z1,d,n=40):
    c=trimesh.creation.cylinder(radius=d/2,height=z1-z0,sections=n); c.apply_translation([x,y,(z0+z1)/2]); return c
out={}
# --- ReSpeaker (rs_x0=-5, rs_s0=75, gap 3)
for n in ['rs_pcb','rs_comp']:
    m=trimesh.load(n+'_local.stl'); m.apply_transform(W(-5,75)@tr([0,0,3.0])); out[n]=m
# --- Pi 5 (local: x 0..85, y 0..56, PCB z 0..1.6, parts +z) at pi_x0=-11.2, pi_s0=15, standoff 5
pcb=box(0,0,0,85,56,1.6)
holes=[cyl(hx,hy,-1,3,2.7,20) for hx in [3.5,61.5] for hy in [3.5,52.5]]
pcb=pcb.difference(trimesh.util.concatenate(holes),engine='manifold')
silver=[box(85-17.4+2,29.1-6.6,1.6,85+2,29.1+6.6,1.6+15.6), box(85-17.4+2,47-6.6,1.6,85+2,47+6.6,1.6+15.6),
        box(85-21.5+3,10.2-8,1.6,85+3,10.2+8,1.6+13.5),
        box(11.2-4.5,-1.2,1.6,11.2+4.5,6.3,1.6+3.3), box(25.8-3.8,-1.2,1.6,25.8+3.8,6.3,1.6+3.1), box(39.2-3.8,-1.2,1.6,39.2+3.8,6.3,1.6+3.1)]
dark=[box(7,50.5,1.6,58,55.5,1.6+8.5), box(6,5,1.6,57,48,1.6+2.5)]
fins=[box(6,5+i*3.3,4.1,40,5+i*3.3+1.4,1.6+9.6) for i in range(13)]
fan=[cyl(47,27,4.1,1.6+9.8,30,48)]
L=W(-11.2,15)@tr([0,0,5])
for n,parts in [('pi_pcb',[pcb]),('pi_metal',silver),('pi_dark',dark+fins+fan)]:
    m=trimesh.util.concatenate(parts); m.apply_transform(L); out[n]=m
# --- speaker (Adafruit CAD): front up at local z=1.33 -> Z = 3 (on the pads), cone toward the wall
s=trimesh.load('/home/claude/rs/spk1313.stl'); R=np.diag([-1,1,-1,1.0]); s.apply_transform(W(-52.15,42)@tr([0,0,3+1.33])@R); out['speaker']=s
out['foam_ring']=cyl(0,0,0,3,74,64).difference(cyl(0,0,-1,4,67,64),engine='manifold'); out['foam_ring'].apply_transform(W(-52.15,42))
pads=[box(-4,-4,0.92-1.0+1.0-1.0,4,4,0) for _ in []]
mic=[box(mx-4,17-4,0,mx+4,17+4,1.0) for mx in [5.49,76.49]]
# mic pad top is at pad_h=0.92 off the wall
m=trimesh.util.concatenate(mic); m.apply_transform(W(-5,75)@tr([0,0,0.92])); out['mic_foam']=m
# screws M3x16 countersunk, from outside the back
sc=[]
for i in [-1,1]:
    for j in [-1,1]:
        h=trimesh.creation.cone(radius=3.1,height=3.1,sections=24); h.apply_transform(np.diag([1,1,-1,1.0])); h.apply_translation([0,0,1.6]); 
        hc=box(-3.2,-3.2,-0.01,3.2,3.2,0.01)  # placeholder
        shank=cyl(0,0,0,14.4,2.9,16)
        head=trimesh.creation.cylinder(radius=3.1,height=1.6,sections=24); head.apply_translation([0,0,0.8])
        scr=trimesh.util.concatenate([head, shank]); scr.apply_translation([0,0,-1.8]); scr.apply_transform(W(-52.15+i*30,42+j*30)); sc.append(scr)
out['screws']=trimesh.util.concatenate(sc)
# weight bar 95.25 x 25.4 x 12.7 at pocket x=40
out['bar']=box(40-47.6,44.6-25.4,7.15,40+47.6,44.6,7.15+12.7)
for n,m in out.items(): m.export(f'p_{n}.stl'); print(n, m.bounds.round(1).tolist())
for n,f in [('stand','stand_use.stl'),('frame','frame_use.stl'),('glass','glass_use.stl'),('box','spkbox_use.stl'),('door','door_use.stl')]:
    shutil.copy(T+f, f'p_{n}.stl')
