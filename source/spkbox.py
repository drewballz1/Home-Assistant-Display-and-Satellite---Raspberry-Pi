import trimesh, numpy as np
M = np.load('M_use.npy')
uw = np.array([0, -0.3407, 0.9402]); nw = np.array([0, -0.9402, -0.3407])
WALL_Y0, FLOOR = 76.0, 7.1
SPK_X, SPK_S = -52.15, 52.0
PAD = 3.0; FRAME_T = 1.0                 # pads, speaker frame thickness
RIM = PAD + FRAME_T                      # box rim sits on the back of the speaker frame
def W(x, s):
    T = np.eye(4); T[:3,0] = [1,0,0]; T[:3,1] = uw; T[:3,2] = nw
    T[:3,3] = [x, WALL_Y0 + s*uw[1], FLOOR + s*uw[2]]; return T
Wspk = W(SPK_X, SPK_S)
def local_box(x0,x1,y0,y1,z0,z1):
    b = trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); b.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); b.apply_transform(Wspk); return b
def local_cyl(cx,cy,r,z0,z1, n=96):
    c = trimesh.creation.cylinder(radius=r, height=z1-z0, sections=n); c.apply_translation([cx,cy,(z0+z1)/2]); c.apply_transform(Wspk); return c
def stl_halfspace(zmin):   # region behind (inside of) the display, in original STL coords: z >= zmin
    b = trimesh.creation.box(extents=[600,600,400]); b.apply_translation([0,0,zmin+200]); b.apply_transform(M); return b
def use_box(x0,x1,y0,y1,z0,z1):
    b = trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); b.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return b
def allowed(e):
    a = stl_halfspace(-5.47 + 1.0 + e)                  # behind the stand's rim plane (display's 2 mm driver-board area sits in front of it)
    deep = trimesh.creation.box(extents=[80+4+2*e, 70+4+2*e, 40]); deep.apply_translation([0, 78.33, -2.55 + 2 + e - 20]); deep.apply_transform(M)
    a = a.difference(deep, engine='manifold')            # keep 2 mm off the display's central posts/connectors zone
    a = a.intersection(use_box(-300,300,-300,300, 8 + e, 300), engine='manifold')    # above the floor
    a = a.difference(use_box(-300,300,-300, 45.8 + e, -10, 23.2 + e), engine='manifold') # clear of the weight box
    return a
H = 40.0; WALLT = 2.0
outer = local_box(-H,H,-H,H, RIM, RIM+60).intersection(allowed(0), engine='manifold')
cav   = local_cyl(0,0, 35.5, RIM-1, RIM+60).intersection(allowed(WALLT), engine='manifold')
# always leave room for the magnet (Ø45 x 25.5 incl. frame), bulging the box locally if needed
outer = outer.union(local_cyl(0,0, 22.5+2.0, RIM, PAD+25.5+0.5+1.6), engine='manifold')
cav   = cav.union(local_cyl(0,0, 22.5+0.5, RIM-1, PAD+25.5+0.5), engine='manifold')
box = outer.difference(cav, engine='manifold')
for i in (-1,1):
    for j in (-1,1):
        box = box.difference(local_cyl(i*30, j*30, 1.7, RIM-1, RIM+70, 32), engine='manifold')      # M3 clearance
        box = box.difference(local_cyl(i*30, j*30, 3.3, RIM+4, RIM+70, 32), engine='manifold')    # counterbore, 4 mm clamp
# wire exit (seal with hot glue), on the side facing the Pi
w = trimesh.creation.cylinder(radius=1.6, height=20, sections=24); w.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
w.apply_translation([34, -20, RIM+5]); w.apply_transform(Wspk); box = box.difference(w, engine='manifold')
print('box watertight', box.is_watertight, 'bodies', len(box.split(only_watertight=False)), 'extents', box.extents.round(1))
print('sealed air volume (cm3, approx, before speaker)', round(cav.volume/1000,1))
box.export('spkbox_use.stl')
# print orientation: rim face down
Tinv = np.linalg.inv(Wspk); bp = box.copy(); bp.apply_transform(Tinv); bp.apply_translation([0,0,-bp.bounds[0][2]])
n = bp.face_normals[:,2]; c = bp.triangles_center[:,2]
print('box print overhang (>45deg) mm2', round(bp.area_faces[(n < -0.7072) & (c > 0.3)].sum(),1))
bp.export('out/td2-speaker-box.stl')
