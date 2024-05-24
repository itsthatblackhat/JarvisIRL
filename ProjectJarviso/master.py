import logging
import moderngl_window as mglw
from moderngl_window import WindowConfig
import numpy as np
from model_renderer import rotation_matrix, ModelRenderer
from subnet import (
    BasalGangliaNeural, BrainstemNeural, CerebellumNeural, CerebrumNeural,
    HypothalamusNeural, LimbicNeural, ReticularNeural, ThalamusNeural,
    IntentProcessingNeural, AudioProcessingNeural
)
from memory.memory import Memory
from visualization.activity_visualization import start_activity_visualization, ActivityVisualization
from visualization.communication_visualization import start_communication_visualization, CommunicationVisualization
import threading

class MasterNeural:
    def __init__(self, model_renderer):
        self.model_renderer = model_renderer
        self.memory = Memory()
        self.neural_networks = self.initialize_neural_networks()

    def initialize_neural_networks(self):
        input_size = 100
        output_size = 10

        basal_ganglia_neural = BasalGangliaNeural(input_size=input_size, output_size=output_size, model_renderer=self.model_renderer)
        brainstem_neural = BrainstemNeural(input_size=input_size, output_size=output_size, model_renderer=self.model_renderer)
        cerebellum_neural = CerebellumNeural(input_size=input_size, output_size=output_size, model_renderer=self.model_renderer)
        cerebrum_neural = CerebrumNeural(input_size=input_size, output_size=output_size, model_renderer=self.model_renderer)
        hypothalamus_neural = HypothalamusNeural(input_size=input_size, output_size=output_size, model_renderer=self.model_renderer)
        limbic_neural = LimbicNeural(input_size=input_size, output_size=output_size, model_renderer=self.model_renderer)
        reticular_neural = ReticularNeural(input_size=input_size, output_size=output_size, model_renderer=self.model_renderer)
        thalamus_neural = ThalamusNeural(input_size=input_size, output_size=output_size, model_renderer=self.model_renderer)
        intent_processing_neural = IntentProcessingNeural(input_size=input_size, output_size=output_size, memory=self.memory, model_renderer=self.model_renderer)
        audio_processing_neural = AudioProcessingNeural(input_size=input_size, output_size=output_size, model_renderer=self.model_renderer)

        return {
            "basal_ganglia_neural": basal_ganglia_neural,
            "brainstem_neural": brainstem_neural,
            "cerebellum_neural": cerebellum_neural,
            "cerebrum_neural": cerebrum_neural,
            "hypothalamus_neural": hypothalamus_neural,
            "limbic_neural": limbic_neural,
            "reticular_neural": reticular_neural,
            "thalamus_neural": thalamus_neural,
            "intent_processing_neural": intent_processing_neural,
            "audio_processing_neural": audio_processing_neural
        }

    def run(self):
        for name, neural_network in self.neural_networks.items():
            neural_network.start_listening()

    def render(self, model_matrix, view_matrix, projection_matrix, light_pos, view_pos):
        self.model_renderer.render(model_matrix, view_matrix, projection_matrix, light_pos, view_pos)

    def handle_user_input(self, input_data):
        intent_response = self.neural_networks["intent_processing_neural"].handle_input(input_data)
        return intent_response

class RendererWindow(WindowConfig):
    gl_version = (3, 3)
    title = "Master Neural Network Renderer"
    resource_dir = '.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_renderer = ModelRenderer(self.ctx, 'C:/JarvisIRL/ProjectJarviso/BrainModel/Brain.obj')
        self.master_neural = MasterNeural(self.model_renderer)
        self.master_neural.run()
        self.rotation = np.array([0.0, 0.0, 0.0])
        self.zoom = -2.0
        self.light_pos = np.array([2.0, 2.0, 2.0], dtype='f4')
        self.view_pos = np.array([0.0, 0.0, 5.0], dtype='f4')
        self.auto_rotate = False

        # Start the input thread
        self.input_thread = threading.Thread(target=self.input_loop)
        self.input_thread.daemon = True
        self.input_thread.start()

    def render(self, time, frame_time):
        model = np.eye(4, dtype='f4')
        model = np.dot(model, np.diag([0.1, 0.1, 0.1, 1.0]))

        if self.auto_rotate:
            self.rotation[1] += frame_time

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

        self.master_neural.render(model, view, proj, self.light_pos, self.view_pos)

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
                self.auto_rotate = not self.auto_rotate

    def input_loop(self):
        while True:
            user_input = input("Enter input for Jarvis: ")
            response = self.master_neural.handle_user_input(user_input)
            logging.info(f"Response from Jarvis: {response}")

def main():
    mglw.run_window_config(RendererWindow)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
