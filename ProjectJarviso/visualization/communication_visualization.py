from model_renderer import ModelRenderer
import moderngl
import numpy as np

class CommunicationVisualization:
    def __init__(self, brain_regions):
        self.brain_regions = brain_regions
        self.ctx = moderngl.create_standalone_context()

    def plot_communication(self, communication_data):
        # Initialize Model Renderer
        model_renderer = ModelRenderer(self.ctx, "C:/JarvisIRL/ProjectJarviso/BrainModel/Brain_Model.fbx")
        model_renderer.load_model()

        # Set up matrices (replace with actual camera and model positioning)
        model_matrix = np.eye(4)
        view_matrix = np.eye(4)
        projection_matrix = np.eye(4)

        # Render the model
        model_renderer.render(model_matrix, view_matrix, projection_matrix)

def start_communication_visualization(communication_data, brain_regions):
    visualization = CommunicationVisualization(brain_regions)
    visualization.plot_communication(communication_data)
