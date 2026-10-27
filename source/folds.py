import trimesh, numpy as np, sys
def folds(m, thr=150):
    ang=np.degrees(m.face_adjacency_angles); adj=m.face_adjacency
    bad=np.unique(adj[ang>thr].ravel())
    return bad
if __name__=='__main__':
    for f in sys.argv[1:]:
        m=trimesh.load(f); b=folds(m)
        print('%-60s faces %6d  folded faces %4d  watertight %s  winding %s' % (f.split('/')[-1], len(m.faces), len(b), m.is_watertight, m.is_winding_consistent))
        if len(b): c=m.triangles_center[b]; print('    centres span', c.min(0).round(1), c.max(0).round(1))

def true_folds(m, thr=170, tol=0.02):
    ang=np.degrees(m.face_adjacency_angles); adj=m.face_adjacency; out=[]
    for (a,b),an in zip(adj[ang>thr], ang[ang>thr]):
        fa,fb=m.faces[a],m.faces[b]; other=[v for v in fb if v not in fa]
        if not other: continue
        d=abs((m.vertices[other[0]]-m.vertices[fa[0]])@m.face_normals[a])
        if d<tol and min(m.area_faces[a],m.area_faces[b])>0.01: out+= [a,b]
    return np.unique(out)
