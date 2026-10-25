import trimesh, numpy as np
M = np.load('M_use.npy')
stand = trimesh.load('stand_use.stl'); pi = trimesh.load('pi_env.stl')
frame = trimesh.load('frame_final.stl')
spacer = 12.0 - 6.45; T = 6.45
# frame -> rear STL coords -> use coords
Tf = np.eye(4); Tf[:3,3] = [-120.0, 78.33 - 25.44, -4.0]
frame_use = frame.copy(); frame_use.apply_transform(M @ Tf)
# display envelopes in rear STL coords
def box(x0,x1,y0,y1,z0,z1):
    b = trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); b.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return b
yc = 78.33
glass = box(-189.32/2,189.32/2, yc-120.24/2, yc+120.24/2, -5.47-spacer-T, -5.47-spacer)
rearp = box(-168.55/2,168.55/2, yc-98.21/2, yc+98.21/2, -5.47-spacer, -5.47-spacer+(14.92-T))   # driver-board body + standoffs (official 168.55 x 98.21, 14.92 total), conservatively full depth
for g in (glass, rearp): g.apply_transform(M)
def inter(a,b):
    try:
        i = a.intersection(b); return round(i.volume,2) if not i.is_empty else 0.0
    except Exception as e: return f'err {e}'
print('pi  vs stand      ', inter(pi, stand))
print('pi  vs display back', inter(pi, rearp))
print('glass vs stand    ', inter(glass, stand))
print('glass vs frame    ', inter(glass, frame_use))
print('display back vs stand', inter(rearp, stand))
print('frame vs stand    ', inter(frame_use, stand), '(snap-tab interference expected, small)')
d = trimesh.proximity.closest_point(rearp, pi.vertices)[1].min()
print('min gap pi -> display back envelope', round(d,1), 'mm')
inside = stand.convex_hull.contains(pi.vertices).all(); print('pi inside stand hull', inside)
frame_use.export('frame_use.stl'); glass.export('glass_use.stl'); rearp.export('dispback_use.stl')
