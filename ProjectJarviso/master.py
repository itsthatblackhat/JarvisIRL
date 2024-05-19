import numpy as np
import logging
import moderngl
import threading
import socket
import json
from pathlib import Path
from subnet import BasalGangliaNeural, BrainstemNeural, CerebellumNeural, CerebrumNeural, HypothalamusNeural, LimbicNeural, ReticularNeural, ThalamusNeural
from memory.memory import Memory
from memory.memory_imprinting import MemoryImprinting
from model_renderer import ModelRenderer
from visualization import communication_visualization, activity_visualization
from intent_handler import IntentHandler

# Configure logging
logging.basicConfig(level=logging.ERROR)

class MasterNeural:
    def __init__(self, input_size, output_size, ctx, model_file):
        logging.error("Initializing MasterNeural")

        # Initialize ModelRenderer
        self.model_renderer = ModelRenderer(ctx, str(model_file))

        # Initialize sub-neural networks
        self.subnets = {
            "cerebrum": CerebrumNeural(input_size, output_size, self.model_renderer),
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
        self.intent_handler = IntentHandler(ctx)

    def communicate(self):
        pass

    def coordinate(self):
        pass

    def receive_user_input(self):
        user_input = input("You: ")
        logging.error(f"Received user input: {user_input}")
        return user_input

    def interpret_intents(self, user_input):
        past_interactions = self.retrieve_memories()
        intents = self.intent_handler.interpret_intents(user_input)
        logging.error(f"Interpreted intents: {intents}")
        return intents

    def retrieve_memories(self):
        memories = self.memory.retrieve_memories()
        logging.error(f"Retrieved memories: {memories}")
        return memories

    def update_memory_imprints(self, memories):
        self.memory_imprinting.update_memory_imprints(memories)
        logging.error(f"Updated memory imprints with memories: {memories}")

    def make_decisions(self, intents, memories):
        decisions = {subnet: True for subnet in self.subnets}
        logging.error(f"Made decisions: {decisions}")
        return decisions

    def execute_actions(self, decisions):
        for subnet, decision in decisions.items():
            if decision:
                model_matrix = np.eye(4)
                view_matrix = np.eye(4)
                projection_matrix = np.eye(4)
                self.model_renderer.render(model_matrix, view_matrix, projection_matrix, np.array([2.0, 2.0, 2.0]), np.array([0.0, 0.0, 2.0]))
        logging.error("Executed actions based on decisions")

    def handle_errors(self):
        pass

    def ensure_safety(self):
        pass

    def collect_activity_data(self):
        activity_data = {}
        for name, subnet in self.subnets.items():
            activity_data[name] = subnet.get_activity_data()
        logging.error(f"Collected activity data: {activity_data}")
        return activity_data

    def collect_communication_data(self):
        communication_data = {}
        for name, subnet in self.subnets.items():
            communication_data[name] = subnet.get_communication_data()
        logging.error(f"Collected communication data: {communication_data}")
        return communication_data

    def run(self):
        while True:
            user_input = self.receive_user_input()
            self.intent_handler.process_user_input(user_input)
            intents = self.interpret_intents(user_input)
            memories = self.retrieve_memories()
            self.update_memory_imprints(memories)
            decisions = self.make_decisions(intents, memories)
            self.execute_actions(decisions)
            self.handle_errors()
            self.ensure_safety()

            # Collect data for visualization
            activity_data = self.collect_activity_data()
            communication_data = self.collect_communication_data()

            # Start the visualization threads
            activity_visualization_thread = threading.Thread(target=activity_visualization.start_activity_visualization,
                                                             args=(activity_data, self.subnets.keys(), self.model_renderer))
            communication_visualization_thread = threading.Thread(
                target=communication_visualization.start_communication_visualization,
                args=(communication_data, self.subnets.keys(), self.model_renderer))

            activity_visualization_thread.start()
            communication_visualization_thread.start()

            activity_visualization_thread.join()
            communication_visualization_thread.join()

def main():
    input_size = 100  # Example input size
    output_size = 10  # Example output size

    ctx = moderngl.create_standalone_context()
    model_file = Path("C:/JarvisIRL/ProjectJarviso/BrainModel/Brain.obj")
    master_neural = MasterNeural(input_size, output_size, ctx, model_file)

    master_neural.run()

if __name__ == "__main__":
    main()
