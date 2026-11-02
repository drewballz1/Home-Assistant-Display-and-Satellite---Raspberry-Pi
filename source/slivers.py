import trimesh, numpy as np, sys
def slivers(m, max_area=0.05, min_len=5.0):
    tri=m.triangles; L=np.linalg.norm(tri-np.roll(tri,1,axis=1),axis=2).max(1)
    return np.where((m.area_faces<max_area)&(L>min_len))[0]
if __name__=='__main__':
    for f in sys.argv[1:]:
        m=trimesh.load(f); s=slivers(m); print(f'{f:28s} slivers (area<0.05 mm2, >5 mm long): {len(s)}')
