import numpy as np
import logging
import moderngl
import threading
from pathlib import Path
from subnet import CerebrumNeural, CerebellumNeural, BrainstemNeural, ThalamusNeural, HypothalamusNeural, BasalGangliaNeural, LimbicNeural, ReticularNeural
from memory.memory import Memory
from memory.memory_imprinting import MemoryImprinting
from model_renderer import ModelRenderer  # Import the ModelRenderer here to avoid circular import

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class MasterNeural:
    def __init__(self, input_size, output_size, ctx, model_file):
        logging.info("Initializing MasterNeural")

        # Initialize ModelRenderer
        self.model_renderer = ModelRenderer(ctx, str(model_file))

        # Initialize sub-neural networks
        self.subnets = {
            "cerebrum": CerebrumNeural(input_size, output_size),
            "cerebellum": CerebellumNeural(input_size, output_size, self.model_renderer),
            "brainstem": BrainstemNeural(input_size, output_size, self.model_renderer),
            "thalamus": ThalamusNeural(input_size, output_size, self.model_renderer),
            "hypothalamus": HypothalamusNeural(input_size, output_size, self.model_renderer),
            "basal_ganglia": BasalGangliaNeural(input_size, output_size, self.model_renderer),
            "limbic": LimbicNeural(input_size, output_size, self.model_renderer),
            "reticular": ReticularNeural(input_size, output_size, self.model_renderer)
        }

        # Initialize memory module
        self.memory = Memory()
        self.memory_imprinting = MemoryImprinting()

    def communicate(self):
        logging.debug("Communicating...")

    def coordinate(self):
        logging.debug("Coordinating...")

    def receive_user_input(self):
        user_input = input("You: ")
        logging.debug(f"Received user input: {user_input}")
        return user_input

    def interpret_intents(self, user_input):
        logging.debug("Interpreting intents...")
        past_interactions = self.retrieve_memories()
        intents = {}  # Placeholder for interpreted intents
        return intents

    def retrieve_memories(self):
        logging.debug("Retrieving memories...")
        return self.memory.retrieve_memories()

    def update_memory_imprints(self, memories):
        logging.debug("Updating memory imprints...")
        self.memory_imprinting.update_memory_imprints(memories)

    def make_decisions(self, intents, memories):
        logging.debug("Making decisions...")
        decisions = {subnet: True for subnet in self.subnets}
        return decisions

    def execute_actions(self, decisions):
        logging.debug("Executing actions...")
        for subnet, decision in decisions.items():
            if decision:
                model_matrix = np.eye(4)
                view_matrix = np.eye(4)
                projection_matrix = np.eye(4)
                logging.debug(f"Model Matrix:\n{model_matrix}")
                logging.debug(f"View Matrix:\n{view_matrix}")
                logging.debug(f"Projection Matrix:\n{projection_matrix}")
                self.model_renderer.render(model_matrix, view_matrix, projection_matrix)
            else:
                logging.debug(f"No action executed for {subnet}")

    def handle_errors(self):
        logging.debug("Handling errors...")

    def ensure_safety(self):
        logging.debug("Ensuring safety...")

    def run(self):
        while True:
            user_input = self.receive_user_input()
            intents = self.interpret_intents(user_input)
            memories = self.retrieve_memories()
            self.update_memory_imprints(memories)
            decisions = self.make_decisions(intents, memories)
            self.execute_actions(decisions)
            self.handle_errors()
            self.ensure_safety()

def main():
    input_size = 100  # Example input size
    output_size = 10  # Example output size

    # Initialize model rendering context and file
    ctx = moderngl.create_standalone_context()
    model_file = Path("C:/JarvisIRL/ProjectJarviso/BrainModel/brain3D.3mf")

    # Initialize and run the master neural network
    master_neural = MasterNeural(input_size, output_size, ctx, model_file)

    from visualization import activity_visualization
    from visualization import communication_visualization

    # Define activity data and communication data
    activity_data = {}  # Placeholder for activity data
    communication_data = {}  # Placeholder for communication data

    # Start the visualization threads
    activity_visualization_thread = threading.Thread(target=activity_visualization.start_activity_visualization,
                                                     args=(activity_data, master_neural.subnets.keys(), master_neural.model_renderer))
    communication_visualization_thread = threading.Thread(
        target=communication_visualization.start_communication_visualization,
        args=(communication_data, master_neural.subnets.keys(), master_neural.model_renderer))

    # Start the threads
    activity_visualization_thread.start()
    communication_visualization_thread.start()

    # Run MasterNeural
    master_neural.run()

    # Join the visualization threads to ensure they terminate when the main thread terminates
    activity_visualization_thread.join()
    communication_visualization_thread.join()

if __name__ == "__main__":
    main()
