import trimesh, numpy as np, sys
def thin(m, n=60000, thr=0.2):
    p, fi = trimesh.sample.sample_surface(m, n); nn = m.face_normals[fi]
    o = p - nn*1e-4
    d = np.full(n, np.inf)
    for s in range(0, n, 4000):
        loc, ri, ti = m.ray.intersects_location(o[s:s+4000], -nn[s:s+4000], multiple_hits=False)
        d[s+ri] = np.linalg.norm(loc - o[s+ri], axis=1)
    bad = d < thr
    return p[bad], d[bad]
if __name__ == '__main__':
    for f in sys.argv[1:]:
        m = trimesh.load(f); P, D = thin(m)
        print('%-28s thin spots (<0.2 mm): %d' % (f, len(P)))
        if len(P):
            import collections
            cl = collections.Counter(map(tuple, np.round(P/4)*4))
            for k, c in cl.most_common(12): print('   near', k, c, 'min %.3f' % D[np.all(np.abs(P-np.array(k))<=2.01,axis=1)].min())
