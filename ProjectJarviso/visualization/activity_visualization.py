import logging
import threading
import time
import numpy as np

def start_activity_visualization(activity_data, brain_regions, model_renderer, stop_event):
    try:
        while not stop_event.is_set():
            for region in brain_regions:
                intensity = activity_data[region].get('intensity', 0.0)
                model_renderer.render_activity({region: intensity})
            logging.info("Rendered activity points")
            time.sleep(1)
    except Exception as e:
        logging.error(f"Error in activity visualization: {e}")

class ActivityVisualization:
    def __init__(self, brain_regions, model_renderer):
        self.brain_regions = brain_regions
        self.model_renderer = model_renderer

    def plot_activity(self, activity_data):
        # Set up matrices
        model_matrix = np.eye(4, dtype='f4')
        view_matrix = np.eye(4, dtype='f4')
        projection_matrix = np.eye(4, dtype='f4')

        # Camera positioning to match model_renderer
        view_matrix[3][2] = -2.0  # Use the same zoom level as in RendererWindow

        aspect_ratio = 1.0  # Assuming square window for simplicity
        projection_matrix[0][0] = 1.0 / (aspect_ratio * np.tan(np.radians(45.0) / 2))
        projection_matrix[1][1] = 1.0 / np.tan(np.radians(45.0) / 2)
        projection_matrix[2][2] = - (1000.0 + 0.1) / (1000.0 - 0.1)
        projection_matrix[2][3] = -1.0
        projection_matrix[3][2] = - (2 * 1000.0 * 0.1) / (1000.0 - 0.1)
        projection_matrix[3][3] = 0.0

        # Render the model
        self.model_renderer.render(model_matrix, view_matrix, projection_matrix, np.array([2.0, 2.0, 2.0]), np.array([0.0, 0.0, 2.0]))

        # Render activity overlay
        self.model_renderer.render_activity(activity_data)
