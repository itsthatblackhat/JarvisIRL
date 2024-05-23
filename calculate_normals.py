import re
import numpy as np
import argparse
from pathlib import Path

def calculate_normals(filepath):
    filepath = Path(filepath)

    with open(filepath, 'r', encoding='utf-8') as obj:
        r = obj.read()

    position_data = read_position(r)
    faces_data = read_faces(r)
    obj_n = obj_normals(position_data, faces_data)

    filename = filepath.stem
    parent_dir = filepath.parent
    output_file_path = parent_dir / f"{filename}_out.obj"

    write_obj(output_file_path, position_data, faces_data, obj_n)

def read_position(r):
    position = []
    v_re = re.compile(r'^v\s+([-\d.e]+)\s+([-\d.e]+)\s+([-\d.e]+)', re.MULTILINE)
    for match in v_re.finditer(r):
        x, y, z = map(float, match.groups())
        position.append([x, y, z])
    return position

def read_faces(r):
    faces = []
    f_re = re.compile(r'^f\s+(\d+)(?:/\d*)?(?:/\d*)?\s+(\d+)(?:/\d*)?(?:/\d*)?\s+(\d+)(?:/\d*)?(?:/\d*)?', re.MULTILINE)
    for match in f_re.finditer(r):
        v1, v2, v3 = map(int, match.groups())
        faces.append([v1 - 1, v2 - 1, v3 - 1])
    return faces

def obj_normals(position, faces):
    normals = []
    normals_dict = {i: [] for i in range(len(position))}

    for f in faces:
        p1, p2, p3 = [np.asarray(position[idx]) for idx in f]
        n = np.cross(p2 - p1, p3 - p1)
        if np.linalg.norm(n) != 0:
            n = n / np.linalg.norm(n)
        for idx in f:
            normals_dict[idx].append(n)

    for i in range(len(position)):
        if normals_dict[i]:
            n = np.mean(normals_dict[i], axis=0)
            n = n / np.linalg.norm(n)
            normals.append(n)
        else:
            normals.append([0, 0, 0])

    return normals

def write_obj(filepath, positions, faces, normals):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'# {filepath.stem}_out.obj\n')

        for p in positions:
            f.write(f'v {p[0]} {p[1]} {p[2]}\n')

        for n in normals:
            f.write(f'vn {n[0]} {n[1]} {n[2]}\n')

        for face in faces:
            f.write(f'f {" ".join([f"{idx+1}//{idx+1}" for idx in face])}\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str, help='Path to the OBJ file')

    args = parser.parse_args()

    calculate_normals(args.filepath)
