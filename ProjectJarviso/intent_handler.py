import logging
import threading
from memory.memory import Memory
from memory.memory_imprinting import MemoryImprinting
from visualization.activity_visualization import start_activity_visualization
from visualization.communication_visualization import start_communication_visualization
from model_renderer import ModelRenderer

class IntentHandler:
    def __init__(self, context):
        self.memory = Memory()
        self.memory_imprinting = MemoryImprinting()
        self.model_renderer = ModelRenderer(context, 'C:/JarvisIRL/ProjectJarviso/BrainModel/Brain.obj')
        self.brain_regions = [
            'cerebrum', 'cerebellum', 'brainstem', 'thalamus', 'hypothalamus',
            'basal_ganglia', 'limbic', 'reticular'
        ]

        # Initialize activity and communication data structures
        self.activity_data = {region: 0.0 for region in self.brain_regions}
        self.communication_data = {region: 0.0 for region in self.brain_regions}

    def interpret_intents(self, user_input):
        intents = {}

        # Simple keyword-based intent extraction
        if "hello" in user_input.lower():
            intents['greeting'] = True
        if "test" in user_input.lower():
            intents['test'] = True
        if "activity" in user_input.lower():
            intents['activity'] = True
        if "communication" in user_input.lower():
            intents['communication'] = True

        return intents

    def handle_intents(self, intents):
        if 'greeting' in intents:
            self.memory.store_memory({'memory': 'User greeted', 'strength': 1})
            logging.error("User greeted the system")

        if 'test' in intents:
            self.memory.store_memory({'memory': 'User initiated test', 'strength': 1})
            logging.error("User initiated a test")

        if 'activity' in intents:
            self.memory.store_memory({'memory': 'User asked for activity visualization', 'strength': 1})
            logging.error("Starting activity visualization thread")
            threading.Thread(target=start_activity_visualization,
                             args=(self.activity_data, self.brain_regions, self.model_renderer)).start()

        if 'communication' in intents:
            self.memory.store_memory({'memory': 'User asked for communication visualization', 'strength': 1})
            logging.error("Starting communication visualization thread")
            threading.Thread(target=start_communication_visualization,
                             args=(self.communication_data, self.brain_regions, self.model_renderer)).start()

    def update_activity(self, region, intensity):
        if region in self.activity_data:
            self.activity_data[region] = intensity

    def update_communication(self, region, intensity):
        if region in self.communication_data:
            self.communication_data[region] = intensity

    def process_user_input(self, user_input):
        logging.error(f"Processed user input: {user_input}")
        intents = self.interpret_intents(user_input)
        self.handle_intents(intents)
