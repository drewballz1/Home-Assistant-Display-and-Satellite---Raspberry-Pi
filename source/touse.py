import trimesh, numpy as np
n_desk = np.array([0, 0.96, 0.29]); n_desk /= np.linalg.norm(n_desk)
up = -n_desk; X = np.array([1.,0,0]); Y = np.cross(up, X)
Rm = np.vstack([X, Y, up])
if (Rm @ [0,0,-1])[1] > 0:   # screen outward normal should point to -Y (front)
    Y = -Y; X = -X; Rm = np.vstack([X, Y, up])
R = np.eye(4); R[:3,:3] = Rm
def to_use(m):
    m = m.copy(); m.apply_transform(R)
    T = np.eye(4); T[2,3] = -m.bounds[0][2]; T[1,3] = -m.bounds[0][1]; m.apply_transform(T)
    return m, T @ R
if __name__ == '__main__':
    r = trimesh.load('rear_stretched.stl')
    ru, M = to_use(r); np.save('M_use.npy', M); ru.export('rear_use.stl')
    print('use bounds', ru.bounds.round(2), 'det', round(np.linalg.det(Rm),3))
    print('screen normal', (Rm @ [0,0,-1]).round(3), 'tilt from horizontal', round(np.degrees(np.arccos(abs((Rm@[0,0,-1])[2]))),1))
