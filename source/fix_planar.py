"""Repair fold-overs on flat faces of the stretched stand.

The stretch moves the corners of some long, thin triangles on flat faces by different amounts, and a few
of them flip over (overlapping, inside-out triangles). For every flat face that contains such a fold,
this re-triangulates the whole face from its exact boundary loop(s). Boundary vertices are kept, so the
face still stitches to its neighbours; the surface itself does not move.

usage: python3 fix_planar.py in.stl out.stl
"""
import sys, collections
import numpy as np, trimesh, networkx as nx, mapbox_earcut as earcut
from shapely.geometry import Polygon
sys.path.insert(0, '/home/claude/td2')
from folds import true_folds


def loops_from_edges(edges):
    nxt = collections.defaultdict(list)
    for a, b in edges: nxt[a].append(b)
    used, loops = set(), []
    for a, b in edges:
        if (a, b) in used: continue
        loop, cur, start = [a], b, a
        used.add((a, b))
        while cur != start:
            loop.append(cur)
            cand = [n for n in nxt[cur] if (cur, n) not in used]
            if len(cand) != 1: return None          # ambiguous (pinched) boundary
            used.add((cur, cand[0])); cur = cand[0]
        loops.append(loop)
    return loops


def fix_face(m, seed, tol=0.05):
    n = m.face_normals[seed]; p = m.triangles_center[seed]
    N, C = m.face_normals, m.triangles_center
    cand = np.where((np.abs(N @ n) > 0.999) & (np.abs((C - p) @ n) < tol))[0]
    cs = set(cand.tolist())
    g = nx.Graph(); g.add_nodes_from(cand)
    g.add_edges_from([(a, b) for a, b in m.face_adjacency if a in cs and b in cs])
    R = np.array(sorted(nx.node_connected_component(g, seed)))
    # directed boundary edges, as they appear in R's faces (an edge used once within R)
    und = collections.Counter()
    for f in m.faces[R]:
        for i in range(3): und[tuple(sorted((f[i], f[(i + 1) % 3])))] += 1
    bdir = [(f[i], f[(i + 1) % 3]) for f in m.faces[R] for i in range(3)
            if und[tuple(sorted((f[i], f[(i + 1) % 3])))] == 1]
    loops = loops_from_edges(bdir)
    if loops is None: return None, 'pinched boundary'
    # 2D basis in the face plane
    nn = n / np.linalg.norm(n); a = np.cross(nn, [1, 0, 0] if abs(nn[0]) < 0.9 else [0, 1, 0]); a /= np.linalg.norm(a); b = np.cross(nn, a)
    P2 = lambda L: np.c_[m.vertices[L] @ a, m.vertices[L] @ b]
    polys = [Polygon(P2(L)) for L in loops]
    if not all(pg.is_valid for pg in polys): return None, 'self-intersecting boundary'
    order = np.argsort([-pg.area for pg in polys]); outer = loops[order[0]]
    holes = [loops[i] for i in order[1:]]
    if not all(polys[order[0]].contains(polys[i]) for i in order[1:]): return None, 'loops not nested'
    # earcut wants outer CCW, holes CW (in its own 2D frame); orientation of output fixed below
    def orient(L, ccw):
        pg = Polygon(P2(L)); return L if pg.exterior.is_ccw == ccw else L[::-1]
    rings = [orient(outer, True)] + [orient(h, False) for h in holes]
    allv = np.concatenate(rings); pts = P2(allv)
    ends = np.cumsum([len(r) for r in rings]).astype(np.uint32)
    tri = earcut.triangulate_float64(pts, ends).reshape(-1, 3)
    newf = allv[tri]
    # orientation: boundary edges must keep the direction they had in R
    e0 = set(bdir)
    hits = sum(((f[i], f[(i + 1) % 3]) in e0) for f in newf for i in range(3))
    if hits < len(bdir) / 2: newf = newf[:, ::-1]
    keep = np.ones(len(m.faces), bool); keep[R] = False
    out = trimesh.Trimesh(m.vertices, np.vstack([m.faces[keep], newf]), process=False)
    out.remove_unreferenced_vertices()
    return out, 'face of %d tris re-triangulated as %d (%d loop%s)' % (len(R), len(newf), len(loops), 's' if len(loops) > 1 else '')


def repair(m):
    done = set()
    for it in range(50):
        F = [f for f in true_folds(m) if f not in done]
        if not F: break
        new, msg = fix_face(m, F[0])
        print('  fold at', m.triangles_center[F[0]].round(2), '->', msg)
        if new is None: done.add(F[0]); continue
        if not (new.is_watertight and new.is_winding_consistent):
            print('    rejected: would break watertightness'); done.add(F[0]); continue
        m = new
    return m


if __name__ == '__main__':
    m = trimesh.load(sys.argv[1])
    print(sys.argv[1], 'folds before', len(true_folds(m)))
    r = repair(m)
    print('folds after', len(true_folds(r)), 'watertight', r.is_watertight, 'winding', r.is_winding_consistent,
          'vol %.3f -> %.3f cm3' % (m.volume / 1000, r.volume / 1000))
    r.export(sys.argv[2])
