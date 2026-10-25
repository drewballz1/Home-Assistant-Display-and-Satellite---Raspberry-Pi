import trimesh, numpy as np
L = lambda n: trimesh.load(n)
M = np.load('M_use.npy')
s = L('rear_use.stl')
# trimming volume: inside the stand's hull and behind the rim plane
trim = trimesh.creation.box(extents=[400, 400, 200]); trim.apply_translation([0, 0, -5.47 + 0.5 + 100]); trim.apply_transform(M)
trim = trim.intersection(s.convex_hull, engine='manifold')
rails = L('piece_rails.stl').intersection(trim, engine='manifold').difference(L('frame_use.stl'), engine='manifold')
adds_late = ['piece_grip.stl']
for add in ['piece_tabs.stl','piece_ring.stl','piece_bosses.stl','piece_wbox.stl','piece_spkpads.stl','piece_rspad.stl']: s = s.union(L(add), engine='manifold')
s = s.union(rails, engine='manifold')
for cut in ['wcut','vents','grille','mics','spkholes','poke','labels','window','backlabel']: s = s.difference(L(f'piece_{cut}.stl'), engine='manifold')
for add in adds_late: s = s.union(L(add), engine='manifold')
print('stand', s.extents.round(2), 'watertight', s.is_watertight, 'bodies', len(s.split(only_watertight=False)), 'vol cm3', round(s.volume/1000,1))
s.export('stand_use.stl')
