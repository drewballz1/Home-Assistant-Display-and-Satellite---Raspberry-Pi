import trimesh, numpy as np, sys
def islands(path):
    m=trimesh.load(path); zs=np.arange(0.1, m.bounds[1,2], 0.2)
    secs=m.section_multiplane(plane_origin=[0,0,0], plane_normal=[0,0,1], heights=zs); prev=None; out=[]
    for z,s in zip(zs,secs):
        polys=[] if s is None else list(s.polygons_full)
        if prev is not None:
            for p in polys:
                if p.area>=0.01 and not any(p.intersects(q) for q in prev): out.append((round(z,1),round(p.area,2),round(p.centroid.x,1),round(p.centroid.y,1)))
        prev=polys
    return out
for f in sys.argv[1:]:
    r=islands(f); print(f'{f}: {len(r)} mid-air starts', r[:10])
