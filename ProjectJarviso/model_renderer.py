import numpy as np
import lib3mf
import moderngl
import moderngl_window as mglw

class ModelRenderer:
    def __init__(self, context, model_file):
        self.context = context
        self.model_file = model_file
        self.vertices, self.faces = self.load_3mf(model_file)
        self.normals = self.calculate_normals(self.vertices, self.faces)
        self.program = self.create_program()
        self.create_vertex_buffer()

    def load_3mf(self, model_file):
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

    def calculate_normals(self, vertices, faces):
        normals = np.zeros(vertices.shape, dtype=np.float32)
        for face in faces:
            p1, p2, p3 = vertices[face]
            n = np.cross(p2 - p1, p3 - p1)
            if np.linalg.norm(n) != 0:  # Avoid division by zero
                n = n / np.linalg.norm(n)
            normals[face] += n
        normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)
        return np.nan_to_num(normals)

    def create_program(self):
        vertex_shader = '''
        #version 330
        in vec3 in_vert;
        in vec3 in_norm;
        out vec3 v_vert;
        out vec3 v_norm;
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 proj;
        void main() {
            v_vert = in_vert;
            v_norm = in_norm;
            gl_Position = proj * view * model * vec4(in_vert, 1.0);
        }
        '''
        fragment_shader = '''
        #version 330
        in vec3 v_vert;
        in vec3 v_norm;
        out vec4 fragColor;
        uniform vec3 light;
        void main() {
            float lum = dot(normalize(light - v_vert), normalize(v_norm)) * 0.5 + 0.5;
            fragColor = vec4(lum, lum, lum, 1.0);
        }
        '''
        return self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    def create_vertex_buffer(self):
        vertices = self.vertices
        normals = self.normals

        print(f"Number of vertices: {len(vertices)}")
        print(f"Number of normals: {len(normals)}")

        buffer_data = np.hstack([vertices, normals]).astype('f4').tobytes()
        self.vbo = self.context.buffer(buffer_data)
        self.vao = self.context.simple_vertex_array(self.program, self.vbo, 'in_vert', 'in_norm')

    def render(self, model_matrix, view_matrix, projection_matrix):
        self.context.clear(0.1, 0.1, 0.1)
        self.context.enable(moderngl.DEPTH_TEST)

        model_matrix = np.array(model_matrix, dtype='f4').reshape(4, 4)
        view_matrix = np.array(view_matrix, dtype='f4').reshape(4, 4)
        projection_matrix = np.array(projection_matrix, dtype='f4').reshape(4, 4)

        self.program['model'].write(model_matrix.tobytes())
        self.program['view'].write(view_matrix.tobytes())
        self.program['proj'].write(projection_matrix.tobytes())
        self.program['light'].value = (5.0, 5.0, 5.0)
        self.vao.render(moderngl.TRIANGLES)


class RendererWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Model Renderer"
    resource_dir = '.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.renderer = ModelRenderer(self.ctx, 'C:\\JarvisIRL\\ProjectJarviso\\BrainModel\\brain3D.3mf')
        self.rotation = 0
        self.translation = np.array([0.0, 0.0, -5.0])

    def render(self, time, frame_time):
        model = np.eye(4, dtype='f4')
        model = np.dot(model, np.diag([0.1, 0.1, 0.1, 1.0]))
        view = np.eye(4, dtype='f4')
        view = np.dot(view, np.array([[1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, 1, self.translation[2]],
                                      [0, 0, 0, 1]], dtype='f4'))
        proj = np.eye(4, dtype='f4')
        model = np.dot(model, np.array([[np.cos(self.rotation), 0, np.sin(self.rotation), 0],
                                        [0, 1, 0, 0],
                                        [-np.sin(self.rotation), 0, np.cos(self.rotation), 0],
                                        [0, 0, 0, 1]], dtype='f4'))

        self.renderer.render(model, view, proj)

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.LEFT:
                self.rotation -= 0.1
            elif key == self.wnd.keys.RIGHT:
                self.rotation += 0.1
            elif key == self.wnd.keys.UP:
                self.translation[2] += 0.1
            elif key == self.wnd.keys.DOWN:
                self.translation[2] -= 0.1


if __name__ == "__main__":
    mglw.run_window_config(RendererWindow)
