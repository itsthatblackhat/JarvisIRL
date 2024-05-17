from model_renderer import ModelRenderer
import moderngl
import numpy as np

class ActivityVisualization:
    def __init__(self, brain_regions, model_renderer):
        self.brain_regions = brain_regions
        self.ctx = moderngl.create_standalone_context()
        self.model_renderer = model_renderer

    def plot_activity(self, activity_data):
        # Set up matrices (replace with actual camera and model positioning)
        model_matrix = np.eye(4)
        view_matrix = np.eye(4)
        projection_matrix = np.eye(4)

        # Render the model
        self.model_renderer.render(model_matrix, view_matrix, projection_matrix)

def start_activity_visualization(activity_data, brain_regions, model_renderer):
    vis = ActivityVisualization(brain_regions, model_renderer)
    vis.plot_activity(activity_data)
