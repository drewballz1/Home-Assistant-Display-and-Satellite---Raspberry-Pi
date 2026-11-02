"""Write plain 3MF core files for Bambu Studio (geometry + per-triangle fuzzy-skin paint).
Objects are placed on a 256 x 256 mm plate in print orientation."""
import trimesh, numpy as np, zipfile, sys
from shapely.geometry import Point
from shapely.ops import unary_union
P='/home/claude/printpack/'

def load(f):
    m=trimesh.load(P+f, process=True); m.merge_vertices(); m.remove_unreferenced_vertices()
    m.apply_translation([-(m.bounds[0][0]+m.bounds[1][0])/2, -(m.bounds[0][1]+m.bounds[1][1])/2, -m.bounds[0][2]])
    return m

def frame_paint(m):
    # paint: mostly vertical faces (|nz| < 0.5) that lie on the OUTER contour of the band
    sec=m.section(plane_origin=[0,0,m.extents[2]/2],plane_normal=[0,0,1]); polys,T=sec.to_2D(to_2D=np.eye(4))
    outer=unary_union([p.exterior.convex_hull for p in polys.polygons_full]).exterior
    c=m.triangles_center; n=m.face_normals
    vert=np.abs(n[:,2])<0.5
    d=np.array([outer.distance(Point(x,y)) for x,y in c[:,:2]])
    radial=np.einsum('ij,ij->i', n[:,:2], c[:,:2])>0          # facing away from the centre
    return vert & radial & (d<0.6)

def write(path, items):
    objs=[]; build=[]
    for i,(name,m,paint,(tx,ty)) in enumerate(items, start=1):
        V='\n'.join(f'<vertex x="{x:.4f}" y="{y:.4f}" z="{z:.4f}"/>' for x,y,z in m.vertices)
        T='\n'.join((f'<triangle v1="{a}" v2="{b}" v3="{c}" paint_fuzzy_skin="4"/>' if (paint is not None and paint[k]) else f'<triangle v1="{a}" v2="{b}" v3="{c}"/>')
                    for k,(a,b,c) in enumerate(m.faces))
        objs.append(f'<object id="{i}" name="{name}" type="model"><mesh><vertices>\n{V}\n</vertices><triangles>\n{T}\n</triangles></mesh></object>')
        build.append(f'<item objectid="{i}" transform="1 0 0 0 1 0 0 0 1 {tx:.3f} {ty:.3f} 0" printable="1"/>')
    model=('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n'
           '<metadata name="Title">TD2 satellite stand</metadata>\n<resources>\n'+'\n'.join(objs)+'\n</resources>\n<build>\n'+'\n'.join(build)+'\n</build>\n</model>\n')
    ct='<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>\n'
    rels='<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>\n'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',ct); z.writestr('_rels/.rels',rels); z.writestr('3D/3dmodel.model',model)

stand=load('stand.stl'); box=load('speaker-box.stl'); cover=load('pi-ports-cover.stl'); frame=load('frame.stl')
# Plate A (256 x 256): stand along the back, box and cover in front; >= 12 mm between parts (room for a 5 mm brim)
sy=256-10-stand.extents[1]/2
items_A=[('stand',stand,None,(128, sy)),
         ('speaker-box',box,None,(10+box.extents[0]/2+20, 10+box.extents[1]/2+5)),
         ('pi-ports-cover',cover,None,(10+box.extents[0]+20+15+cover.extents[0]/2+20, 10+cover.extents[1]/2+25))]
pf=frame_paint(frame)
items_B=[('frame',frame,pf,(128,128))]
write('TD2-plate-A-black-ASA-stand-box-cover.3mf', items_A)
write('TD2-plate-B-olive-frame.3mf', items_B)
# layout report
for nm,items in [('A',items_A),('B',items_B)]:
    for name,m,paint,(tx,ty) in items:
        lo=np.array([tx-m.extents[0]/2, ty-m.extents[1]/2]); hi=np.array([tx+m.extents[0]/2, ty+m.extents[1]/2])
        print(nm, f'{name:15s} x {lo[0]:6.1f}-{hi[0]:6.1f}  y {lo[1]:6.1f}-{hi[1]:6.1f}  h {m.extents[2]:5.1f}', 'painted faces', int(paint.sum()) if paint is not None else 0)
