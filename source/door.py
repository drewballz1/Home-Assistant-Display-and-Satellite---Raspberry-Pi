import trimesh, numpy as np
from shapely.geometry import Polygon, LineString
from shapely import affinity
uw=np.array([-0.3407,0.9402]); nw=np.array([-0.9402,-0.3407]); P0=np.array([76.0,7.1])   # (y,z) back-wall frame
pt=lambda s,Z: P0+s*uw+Z*nw
pi_s0=15
W = Polygon([pt(pi_s0+0.5,5.5), pt(pi_s0+55.5,5.5), pt(pi_s0+55.5,23.0), pt(pi_s0+0.5,23.0)]).buffer(1.0, join_style=2)   # window (y,z)
XO, XI = 94.86, 93.10            # side wall outer / inner face (x)
def ext(poly, x0, x1):           # extrude a (y,z) polygon along x
    m = trimesh.creation.extrude_polygon(poly, x1-x0)   # extrude in z of (X=y,Y=z)
    T = np.array([[0,0,1,x0],[1,0,0,0],[0,1,0,0],[0,0,0,1]],float)  # (X,Y,Z)->(x=Z+x0, y=X, z=Y)
    m.apply_transform(T); return m
cut = ext(W, XI-1, XO+1); cut.export('piece_window.stl')
# ---- cover: 1.2 mm plate overlapping 2.5 mm, snap rim behind it, two click bumps, fingernail notch
plate_poly = W.buffer(2.0, join_style=1)
plate = ext(plate_poly, XO, XO+1.2)
ch = ext(plate_poly.buffer(-0.8), XO+0.4, XO+1.2)   # soften outer edge: chamfer by hull
plate = trimesh.util.concatenate([ext(plate_poly, XO, XO+0.4), ch]).convex_hull if False else plate
rim  = ext(W.buffer(-0.15).difference(W.buffer(-1.35)), XI-0.6, XO+0.01)
door = plate.union(rim, engine='manifold')
# bumps on the two long edges (parallel to the back wall), near the rim tip
c = np.array(W.exterior.coords)
edges = [(c[i],c[i+1]) for i in range(len(c)-1)]
edges = sorted(edges, key=lambda e: -np.linalg.norm(e[1]-e[0]))[:2]
for a,b in edges:
    mid=(a+b)/2; d=(b-a)/np.linalg.norm(b-a); n=np.array([d[1],-d[0]])
    # outward normal: point away from window centroid
    cen=np.array(W.centroid.coords[0]); n = n if np.dot(mid-cen,n)>0 else -n
    tri = Polygon([mid-0.7*n-6*d, mid-0.7*n+6*d, mid+0.3*n+6*d, mid+0.3*n-6*d])
    bump = ext(tri, XI-0.55, XI-0.05)
    door = door.union(bump, engine='manifold')
# fingernail notch: on the UNDERSIDE of the plate overhang at the front-lower corner,
# leaving a 0.6 mm gap between plate and wall to get a nail under; top face stays clean
from shapely.geometry import Point
fc = np.array(plate_poly.exterior.coords); lowfront = fc[np.argmin(fc[:,0]+fc[:,1])]
scoop = Point(lowfront).buffer(7.0).intersection(plate_poly.buffer(1.0).difference(W.buffer(0.5, join_style=2)))
notch = ext(scoop, XO-0.05, XO+0.6)
door = door.difference(notch, engine='manifold')
print('door watertight', door.is_watertight, 'bodies', len(door.split(only_watertight=False)), 'size', door.extents.round(1))
door.export('door_use.stl')
dp = door.copy(); dp.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])); dp.apply_translation(-dp.bounds[0])
# plate face should be on the bed: flip if needed
if dp.area_faces[dp.triangles_center[:,2]<0.05].sum() < 100: dp.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[1,0,0])); dp.apply_translation(-dp.bounds[0])
dp.export('out/td2-side-door.stl'); print('door print size', dp.extents.round(1))
