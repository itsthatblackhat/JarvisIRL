# for prepping text file created from 3MF
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
    # Define magnet points (example: using the first 10 vertices as magnet points)
    magnet_points = vertices[:10]

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



###############
## old test code
###############
## def identify_problematic_bytes(file_path):
##    problematic_bytes = []
##     with open(file_path, 'rb') as file:
##         byte = file.read(1)
##         while byte:
##             try:
##                 byte.decode('utf-8')
##             except UnicodeDecodeError:
##                 problematic_bytes.append(byte)
##             byte = file.read(1)
##     return problematic_bytes
## 
## file_path = "BrainModel/Cleaned_Brainconv.obj"
## problematic_bytes = identify_problematic_bytes(file_path)
## print("Problematic bytes:", problematic_bytes)
