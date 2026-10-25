import trimesh, numpy as np
exec(open('spkbox.py').read().split('def allowed')[0])
SPK_S = 42.0
Wspk = W(SPK_X, SPK_S)
H, WT = 40.0, 2.0
def plane_keep(point, normal, off=0.0):
    # huge box covering the half-space {x : (x-point)·normal >= off}
    n = np.array(normal, float); n /= np.linalg.norm(n)
    b = trimesh.creation.box(extents=[2000,2000,2000]); b.apply_translation([0,0,1000])
    R = trimesh.geometry.align_vectors([0,0,1], n); b.apply_transform(R); b.apply_translation(np.array(point) + off*n); return b
Mr = M[:3,:3]; mt = M[:3,3]
rim_pt = Mr @ [0,0,-5.47] + mt; rim_back = Mr @ [0,0,1]          # rim plane, normal pointing into the stand
LID = 5.0                                                          # keep the box this far behind the rim plane
lid  = lambda off: plane_keep(rim_pt, rim_back, LID + off)
chamfer = lambda off: plane_keep([0, 0, 7.6], [0, 0, 1], off)      # flat bottom, resting just above the floor
outer = local_box(-H,H,-H,H, RIM, RIM+60).intersection(lid(0), engine='manifold').intersection(chamfer(0), engine='manifold')
cav   = local_cyl(0,0, 38.8, RIM-1, RIM+60).intersection(local_box(-38.5,38.5,-38.5,38.5, RIM-1, RIM+60), engine='manifold').intersection(lid(WT), engine='manifold').intersection(chamfer(WT), engine='manifold')
box = outer.difference(cav, engine='manifold')
for i in (-1,1):
    for j in (-1,1):
        box = box.difference(local_cyl(i*30, j*30, 1.3, RIM-1, RIM+10, 32), engine='manifold')   # 2.6 mm pilot, 10 mm deep (M3 self-tapping from the back)
w = trimesh.creation.cylinder(radius=1.6, height=20, sections=24); w.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
w.apply_translation([34, -20, RIM+5]); w.apply_transform(Wspk); box = box.difference(w, engine='manifold')
print('box watertight', box.is_watertight, 'bodies', len(box.split(only_watertight=False)), 'air cm3', round(cav.volume/1000,1))
box.export('spkbox_use.stl')
bp = box.copy(); bp.apply_transform(np.linalg.inv(Wspk)); bp.apply_translation([0,0,-bp.bounds[0][2]]); bp.export('out/td2-speaker-box.stl')
print('print size', bp.extents.round(1))
