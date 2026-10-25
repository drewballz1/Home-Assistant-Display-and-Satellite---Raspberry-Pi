import gmsh, numpy as np, trimesh
gmsh.initialize(); gmsh.option.setNumber("General.Terminal", 0)
gmsh.model.occ.importShapes('/home/claude/rs/rs.step'); gmsh.model.occ.synchronize()
gmsh.option.setNumber("Mesh.MeshSizeMax", 3.0); gmsh.option.setNumber("Mesh.MeshSizeMin", 0.2)
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 12)
gmsh.model.mesh.generate(2)
pcb, comp = [], []
for d,t in gmsh.model.getEntities(3):
    name = gmsh.model.getEntityName(d,t)
    tris=[]; 
    for sd,st in gmsh.model.getBoundary([(d,t)], oriented=False):
        types, etags, ntags = gmsh.model.mesh.getElements(2, abs(st))
        for ty, nt in zip(types, ntags):
            if ty==2: tris.append(nt.reshape(-1,3))
    if not tris: continue
    (pcb if name.endswith('_PCB') else comp).append(np.vstack(tris))
nodes, coords, _ = gmsh.model.mesh.getNodes()
P = coords.reshape(-1,3); idx = {int(n):i for i,n in enumerate(nodes)}
def mk(lst):
    F = np.vectorize(idx.get)(np.vstack(lst).astype(int)); m = trimesh.Trimesh(P, F, process=True); m.remove_unreferenced_vertices()
    m.apply_translation([-40.24, 107.96, 0]); return m
for n,l in [('rs_pcb',pcb),('rs_comp',comp)]:
    m=mk(l); m.export(n+'_local.stl'); print(n, m.bounds.round(2).tolist(), len(m.faces))
