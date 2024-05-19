import threading
import time
import logging

from model_renderer import ModelRenderer
import moderngl
import numpy as np

class CommunicationVisualization:
    def __init__(self, brain_regions, model_renderer):
        self.brain_regions = brain_regions
        self.ctx = moderngl.create_standalone_context()
        self.model_renderer = model_renderer

    def plot_communication(self, communication_data):
        model_matrix = np.eye(4)
        view_matrix = np.eye(4)
        projection_matrix = np.eye(4)

        self.model_renderer.render(model_matrix, view_matrix, projection_matrix, [2.0, 2.0, 2.0], [0.0, 0.0, 2.0])
        self.model_renderer.render_communication_overlay(communication_data)

def visualize_communication(data, model_renderer):
    while True:
        for key, intensity in data.items():
            if not isinstance(intensity, (int, float)):
                raise ValueError(f"Expected intensity to be int or float, but got {type(intensity).__name__}")
            logging.info(f"Rendering communication for {key} with intensity {intensity}")
            model_renderer.render_communication(key, intensity)
        time.sleep(1)

def start_communication_visualization(data, regions, model_renderer):
    communication_thread = threading.Thread(target=visualize_communication, args=(data, model_renderer))
    communication_thread.start()
    communication_thread.join()
