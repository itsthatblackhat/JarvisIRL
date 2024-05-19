# for the 3MF file prep
import lib3mf
import numpy as np

def load_3mf(model_file):
    wrapper = lib3mf.get_wrapper()
    model = wrapper.CreateModel()
    reader = model.QueryReader("3mf")
    reader.ReadFromFile(model_file)

    vertices = []
    faces = []
    objects_iterator = model.GetObjects()
    while objects_iterator.MoveNext():
        obj = objects_iterator.GetCurrent()
        if obj.IsMeshObject():
            mesh_object = obj
            for vertex in mesh_object.GetVertices():
                vertices.append([vertex.Coordinates[0], vertex.Coordinates[1], vertex.Coordinates[2]])
            for triangle in mesh_object.GetTriangleIndices():
                faces.append([triangle.Indices[0], triangle.Indices[1], triangle.Indices[2]])

    return np.array(vertices, dtype='f4'), np.array(faces, dtype='i4')

def save_magnet_points(vertices, output_file):
    # Save all vertices as magnet points
    magnet_points = vertices

    # Save magnet points to a file
    with open(output_file, 'w') as f:
        for point in magnet_points:
            f.write(f'{point[0]}, {point[1]}, {point[2]}\n')

def main():
    model_file = 'C:\\JarvisIRL\\ProjectJarviso\\BrainModel\\brain3D.3mf'
    vertices, faces = load_3mf(model_file)
    output_file = 'C:\\JarvisIRL\\ProjectJarviso\\BrainModel\\magnet_points.txt'
    save_magnet_points(vertices, output_file)
    print(f'Magnet points saved to {output_file}')

if __name__ == "__main__":
    main()
