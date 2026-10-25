import trimesh, numpy as np
exec(open('check.py').read().split("def inter")[0])   # reuse envelopes from check.py
def inter(a,b):
    i = a.intersection(b, engine='manifold'); return 0.0 if i.is_empty else round(i.volume,2)
P = {n: trimesh.load(f) for n,f in [('pi','pi_env.stl'),('speaker','piece_spkenv.stl'),('respeaker','piece_rsenv.stl'),('weightbar_box','piece_wbox.stl')]}
# refined display back (official drawing): 2.05 mm driver-board bump over 168.55 x 98.21, deep parts (Pi posts, FFC, J1) only in a central zone
bump = box(-168.55/2,168.55/2, yc-98.21/2, yc+98.21/2, -5.47-spacer, -5.47-spacer+2.05)
deep = box(-40,40, yc-35, yc+35, -5.47-spacer, -5.47-spacer+(14.92-T))
for g in (bump, deep): g.apply_transform(M)
rearp = bump.union(deep, engine='manifold')
P['display back'] = rearp; P['glass'] = glass
names = list(P)
for i in range(len(names)):
    for j in range(i+1, len(names)):
        v = inter(P[names[i]], P[names[j]])
        if v: print('COLLIDE', names[i], names[j], v)
for n in ['pi','speaker','respeaker']:
    print(n, 'vs stand', inter(P[n], stand), '| inside hull', stand.convex_hull.contains(P[n].vertices).all(),
          '| gap to display back', round(trimesh.proximity.closest_point(rearp, P[n].vertices)[1].min(),1))
print('frame vs stand', inter(frame_use, stand))

bx = trimesh.load('spkbox_use.stl')
for n,m in [('stand',stand),('pi',P['pi']),('respeaker',P['respeaker']),('display back',rearp),('weight box',P['weightbar_box']),('speaker (frame+basket+magnet)',P['speaker'])]:
    print('speaker box vs', n, inter(bx, m))
