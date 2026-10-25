import trimesh, numpy as np
from shapely.geometry import box as sbox
f = trimesh.load('frame_stretched.stl')
cx, cy = 120.0, 25.44
PW, PH = 189.92, 120.84          # pocket (glass 189.32 x 120.24 + 0.3/side)
R_GLASS = 8.0 + 0.3
def rr(w, h, r):
    return sbox(cx - w/2 + r, cy - h/2 + r, cx + w/2 - r, cy + h/2 - r).buffer(r, resolution=32)
def slab(poly, z0, z1):
    m = trimesh.creation.extrude_polygon(poly, z1 - z0); m.apply_translation([0,0,z0]); return m
# 1) pocket corners in the glass zone -> R8.3
z0, z1 = -13.50, -7.10
fill1 = slab(sbox(cx-PW/2-0.01, cy-PH/2-0.01, cx+PW/2+0.01, cy+PH/2+0.01), z0, z1).difference(slab(rr(PW, PH, R_GLASS), z0-1, z1+1), engine='manifold')
# 2) lip window corners, following the original chamfer (inset 1.30 at the face -> 2.32 at the back of the lip)
zf, zb = -14.41, -13.45
i_f, i_b = 1.30, 2.32
loft = trimesh.util.concatenate([slab(rr(PW-2*i_f, PH-2*i_f, R_GLASS-i_f), zf-0.5, zf), slab(rr(PW-2*i_b, PH-2*i_b, R_GLASS-i_b), zb, zb+0.01)]).convex_hull
fill2 = slab(sbox(cx-PW/2+0.5, cy-PH/2+0.5, cx+PW/2-0.5, cy+PH/2-0.5), zf+0.01, zb).difference(loft, engine='manifold')
out = f.union(fill1, engine='manifold').union(fill2, engine='manifold')
print('frame', out.extents.round(2), 'watertight', out.is_watertight, 'bodies', len(out.split(only_watertight=False)), 'added mm3', round(out.volume - f.volume, 1))
out.export('frame_rounded.stl')
