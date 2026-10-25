import trimesh, numpy as np, sys
A='/mnt/user-data/attachments/1c39fdb4-e1b6-5436-b349-4d75d562f47d/'
GLASS_W, GLASS_H, FIT = 189.32, 120.24, 0.3
f = trimesh.load(A+'41436600-esp-screen-frame-v2-no-side-cable-hole.stl')
r = trimesh.load(A+'a04fec79-esp-screen-rear-v2-no-side-cable-hole.stl')
pocket = 87.2
dx = GLASS_W + 2*FIT - pocket          # width growth
dy = GLASS_H + 2*FIT - pocket          # height growth
print('dx,dy', round(dx,2), round(dy,2))

def straddle(m, zone, label):
    # small triangles whose vertices fall in different zones = features that would be distorted
    z = zone[m.faces]
    mixed = (z.min(1) != z.max(1))
    el = m.edges_unique_length.max()
    tri_size = np.linalg.norm(np.ptp(np.asarray(m.vertices)[m.faces],axis=1), axis=1)
    bad = mixed & (tri_size < 15)
    print(label, 'mixed tris', mixed.sum(), 'small mixed', bad.sum())
    if bad.sum():
        c = m.triangles_center[bad]; print('  at', c.min(0).round(1), c.max(0).round(1))
    return bad

# ---- frame: split at centre lines (x=120, y=25.44)
fc = np.array([120.0, 25.44])
v = f.vertices.copy()
zx = (v[:,0] > fc[0]).astype(int); zy = (v[:,1] > fc[1]).astype(int)
straddle(f, zx, 'frame x'); straddle(f, zy, 'frame y')
v[:,0] += np.where(zx, dx/2, -dx/2); v[:,1] += np.where(zy, dy/2, -dy/2)
f2 = trimesh.Trimesh(v, f.faces.copy(), process=False)

# ---- rear: x split at 0; profile corner zones (similarity growth about apex A)
Ap = np.array([14.1, -5.47]); Cp = np.array([107.75, -5.47]); Bp = np.array([90.44, 51.47])
L = np.linalg.norm(Cp - Ap); k = 1 + dy / L                  # bottom corner moves exactly dy along the screen
print('k', round(k,4))
u = (k-1)*(Cp-Ap); w = (k-1)*(Bp-Ap)
v = r.vertices.copy()
XS = 21.0   # split clear of the cable hole (|x|<16.6) and the snap tabs (|x| 27-29)
zx = np.where(v[:,0] > XS, 1, np.where(v[:,0] < -XS, -1, 0))
straddle(r, zx, 'rear x')
# barycentric zones
T = np.array([[Ap[0],Bp[0],Cp[0]],[Ap[1],Bp[1],Cp[1]],[1,1,1]])
bc = np.linalg.solve(T, np.vstack([v[:,1], v[:,2], np.ones(len(v))]))
zp = bc.argmax(0)   # 0=A,1=B,2=C
straddle(r, zp, 'rear profile')
shift = np.zeros((len(v),2)); shift[zp==1] = w; shift[zp==2] = u
v[:,0] += zx*dx/2; v[:,1:] += shift
r2 = trimesh.Trimesh(v, r.faces.copy(), process=False)
for m,n in [(f2,'frame'),(r2,'rear')]:
    print(n, m.extents.round(2), 'watertight', m.is_watertight, 'winding', m.is_winding_consistent, 'vol', round(m.volume/1000,1))
f2.export('/home/claude/td2/frame_stretched.stl'); r2.export('/home/claude/td2/rear_stretched.stl')
np.save('/home/claude/td2/params.npy', dict(dx=dx,dy=dy,k=k,A=Ap,B=Bp,C=Cp,u=u,w=w))

# --- diagnose: mixed triangles whose shift difference is NOT in their plane (real distortion)
def harm(m, shifts):
    s = shifts[m.faces]                     # (n,3,3)
    d = s - s[:,[0]]                        # shift differences
    n = m.face_normals
    dev = np.abs(np.einsum('nij,nj->ni', d, n)).max(1)
    return dev
S = np.zeros((len(r.vertices),3)); S[:,0] = zx*dx/2; S[:,1:] = shift
dev = harm(r, S); bad = dev > 0.05
print('rear harmful tris', bad.sum(), 'area', round(r.area_faces[bad].sum(),1))
if bad.sum():
    c = r.triangles_center[bad]; 
    import collections
    print(np.round(c[np.argsort(-r.area_faces[bad])][:15],1))
