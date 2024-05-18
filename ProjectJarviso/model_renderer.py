import numpy as np
import pywavefront
import moderngl
import moderngl_window as mglw
from magnet import Magnet

# Vertex shader with Phong shading
vertex_shader = """
#version 330
in vec3 in_vert;
in vec3 in_norm;
uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;
out vec3 frag_pos;
out vec3 frag_normal;
void main() {
    frag_pos = vec3(model * vec4(in_vert, 1.0));
    frag_normal = mat3(transpose(inverse(model))) * in_norm;
    gl_Position = proj * view * vec4(frag_pos, 1.0);
}
"""

# Fragment shader with Phong shading
fragment_shader = """
#version 330
in vec3 frag_pos;
in vec3 frag_normal;
out vec4 fragColor;
uniform vec3 light_pos;
uniform vec3 view_pos;
void main() {
    float ambient_strength = 0.1;
    vec3 ambient = ambient_strength * vec3(0.93, 0.73, 0.73);  // Light pinkish-gray color

    vec3 norm = normalize(frag_normal);
    vec3 light_dir = normalize(light_pos - frag_pos);
    float diff = max(dot(norm, light_dir), 0.0);
    vec3 diffuse = diff * vec3(0.93, 0.73, 0.73);  // Light pinkish-gray color

    float specular_strength = 0.5;
    vec3 view_dir = normalize(view_pos - frag_pos);
    vec3 reflect_dir = reflect(-light_dir, norm);
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32);
    vec3 specular = specular_strength * spec * vec3(1.0, 1.0, 1.0);

    vec3 color = ambient + diffuse + specular;
    fragColor = vec4(color, 1.0);
}
"""

def calculate_normals(vertices, indices):
    normals = np.zeros(vertices.shape, dtype=vertices.dtype)
    tris = vertices[indices].reshape(-1, 3, 3)
    tri_normals = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    tri_normals /= np.linalg.norm(tri_normals, axis=1)[:, None]
    for i, face in enumerate(indices.reshape(-1, 3)):
        normals[face] += tri_normals[i]
    normals /= np.linalg.norm(normals, axis=1)[:, None]
    return normals

def rotation_matrix(angle, axis):
    c, s = np.cos(angle), np.sin(angle)
    ax = np.array(axis, dtype='f4')
    ax = ax / np.linalg.norm(ax)
    x, y, z = ax
    return np.array([
        [c + (1 - c) * x * x, (1 - c) * x * y - s * z, (1 - c) * x * z + s * y, 0],
        [(1 - c) * y * x + s * z, c + (1 - c) * y * y, (1 - c) * y * z - s * x, 0],
        [(1 - c) * z * x - s * y, (1 - c) * z * y + s * x, c + (1 - c) * z * z, 0],
        [0, 0, 0, 1]
    ], dtype='f4')

class ModelRenderer:
    def __init__(self, context, obj_path):
        self.context = context
        scene = pywavefront.Wavefront(obj_path, collect_faces=True)
        self.vertices = np.array(scene.vertices, dtype='f4')
        self.indices = np.hstack([np.array(mesh.faces, dtype='i4') for mesh in scene.mesh_list])

        # Calculate normals if not provided
        if hasattr(scene, 'normals') and scene.normals:
            self.normals = np.array(scene.normals, dtype='f4')
        else:
            self.normals = calculate_normals(self.vertices, self.indices)

        self.vbo = self.context.buffer(np.hstack((self.vertices, self.normals)).astype('f4').tobytes())
        self.ibo = self.context.buffer(self.indices.tobytes())
        self.vao = self.context.vertex_array(
            self.context.program(
                vertex_shader=vertex_shader,
                fragment_shader=fragment_shader
            ),
            [(self.vbo, '3f 3f', 'in_vert', 'in_norm')],
            self.ibo
        )

    def render(self, model_matrix, view_matrix, projection_matrix, light_pos, view_pos):
        self.context.clear(0.1, 0.1, 0.1)
        self.context.enable(moderngl.DEPTH_TEST)
        self.context.enable(moderngl.CULL_FACE)

        self.vao.program['model'].write(model_matrix.astype('f4').tobytes())
        self.vao.program['view'].write(view_matrix.astype('f4').tobytes())
        self.vao.program['proj'].write(projection_matrix.astype('f4').tobytes())
        self.vao.program['light_pos'].write(light_pos.astype('f4').tobytes())
        self.vao.program['view_pos'].write(view_pos.astype('f4').tobytes())

        self.vao.render(moderngl.TRIANGLES)

class RendererWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Model Renderer"
    resource_dir = '.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.renderer = ModelRenderer(self.ctx, 'C:/JarvisIRL/ProjectJarviso/BrainModel/Brain.obj')
        self.rotation = np.array([0.0, 0.0, 0.0])
        self.zoom = -2.0
        self.light_pos = np.array([2.0, 2.0, 2.0], dtype='f4')
        self.view_pos = np.array([0.0, 0.0, 2.0], dtype='f4')
        self.auto_rotate = False

    def render(self, time, frame_time):
        model = np.eye(4, dtype='f4')
        model = np.dot(model, np.diag([0.1, 0.1, 0.1, 1.0]))  # Adjust scale if needed

        # Apply auto rotation
        if self.auto_rotate:
            self.rotation[1] += frame_time

        # Apply manual rotation
        model = np.dot(rotation_matrix(self.rotation[0], [1.0, 0.0, 0.0]), model)
        model = np.dot(rotation_matrix(self.rotation[1], [0.0, 1.0, 0.0]), model)
        model = np.dot(rotation_matrix(self.rotation[2], [0.0, 0.0, 1.0]), model)

        view = np.eye(4, dtype='f4')
        view[3][2] = self.zoom

        aspect_ratio = self.wnd.size[0] / self.wnd.size[1]
        proj = np.eye(4, dtype='f4')
        proj[0][0] = 1.0 / (aspect_ratio * np.tan(np.radians(45.0) / 2))
        proj[1][1] = 1.0 / np.tan(np.radians(45.0) / 2)
        proj[2][2] = - (1000.0 + 0.1) / (1000.0 - 0.1)
        proj[2][3] = -1.0
        proj[3][2] = - (2 * 1000.0 * 0.1) / (1000.0 - 0.1)
        proj[3][3] = 0.0

        self.renderer.render(model, view, proj, self.light_pos, self.view_pos)

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys
        if action == keys.ACTION_PRESS:
            if key == keys.UP:
                self.rotation[0] -= 0.1
            elif key == keys.DOWN:
                self.rotation[0] += 0.1
            elif key == keys.LEFT:
                self.rotation[1] -= 0.1
            elif key == keys.RIGHT:
                self.rotation[1] += 0.1
            elif key == keys.W:
                self.zoom += 0.1
            elif key == keys.S:
                self.zoom -= 0.1
            elif key == keys.R:
                self.auto_rotate = not self.auto_rotate  # Toggle auto-rotate

if __name__ == '__main__':
    mglw.run_window_config(RendererWindow)
