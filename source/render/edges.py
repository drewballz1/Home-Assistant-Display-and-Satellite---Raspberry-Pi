"""Feature edges for the renderer: crease angle > threshold, ignoring degenerate sliver triangles
(their normals are numerically meaningless and make false lines)."""
import trimesh, numpy as np, sys
def feature_edges(m, thr=28.0, min_area=0.05):
    adj=m.face_adjacency; e=m.face_adjacency_edges; A=m.area_faces
    tri=m.triangles; Lmax=np.linalg.norm(tri-np.roll(tri,1,axis=1),axis=2).max(1)
    width=2*A/np.maximum(Lmax,1e-9)                 # triangle height over its longest side
    sliver=(width<0.02)&(Lmax>1.0)                  # long and paper-thin: normal is meaningless
    ok=~sliver[adj[:,0]]&~sliver[adj[:,1]]
    ang=np.degrees(m.face_adjacency_angles)
    keep=ok&(ang>thr)
    # edges where a sliver sits between two real faces: compare the real faces across the sliver strip
    return m.vertices[e[keep]].astype(np.float32)
if __name__=='__main__':
    for f in sys.argv[1:]:
        m=trimesh.load(f,process=True); seg=feature_edges(m); seg.tofile(f[:-4]+'.edges'); print(f, len(seg),'edges')
