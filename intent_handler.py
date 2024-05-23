import logging
import threading
from memory.memory import Memory
from memory.memory_imprinting import MemoryImprinting
from visualization.activity_visualization import start_activity_visualization
from visualization.communication_visualization import start_communication_visualization

class IntentHandler:
    def __init__(self, context, model_renderer, memory):
        self.context = context
        self.model_renderer = model_renderer
        self.memory = memory
        self.memory_imprinting = MemoryImprinting(self.memory)
        self.brain_regions = [
            'cerebrum', 'cerebellum', 'brainstem', 'thalamus', 'hypothalamus',
            'basal_ganglia', 'limbic', 'reticular'
        ]

        self.activity_data = {region: 0.0 for region in self.brain_regions}
        self.communication_data = {region: 0.0 for region in self.brain_regions}

    def interpret_intents(self, user_input):
        intents = {}

        if "hello" in user_input.lower():
            intents['greeting'] = True
        if "test" in user_input.lower():
            intents['test'] = True
        if "activity" in user_input.lower():
            intents['activity'] = True
        if "communication" in user_input.lower():
            intents['communication'] = True

        return intents

    def handle_intents(self, user_input):
        intents = self.interpret_intents(user_input)

        if 'greeting' in intents:
            self.memory.add_memory('User greeted the system')
            return "Hello! How can I assist you today?"

        if 'test' in intents:
            self.memory.add_memory('User initiated test')
            return "Test initiated."

        if 'activity' in intents:
            self.memory.add_memory('User asked for activity visualization')
            threading.Thread(target=start_activity_visualization,
                             args=(self.activity_data, self.brain_regions, self.model_renderer)).start()
            return "Activity visualization started."

        if 'communication' in intents:
            self.memory.add_memory('User asked for communication visualization')
            threading.Thread(target=start_communication_visualization,
                             args=(self.communication_data, self.brain_regions, self.model_renderer)).start()
            return "Communication visualization started."

        return "Sorry, I didn't understand that."

    def update_activity(self, region, intensity):
        if region in self.activity_data:
            self.activity_data[region] = intensity

    def update_communication(self, region, intensity):
        if region in self.communication_data:
            self.communication_data[region] = intensity

    def process_user_input(self, user_input):
        return self.handle_intents(user_input)
