import threading
import logging
import numpy as np
import moderngl
from subnet import AudioProcessingNeural as AudioProcessingNeuralClass
from subnet import BasalGangliaNeural as BasalGangliaNeuralClass
from subnet import BrainstemNeural as BrainstemNeuralClass
from subnet import CerebellumNeural as CerebellumNeuralClass
from subnet import CerebrumNeural as CerebrumNeuralClass
from subnet import HypothalamusNeural as HypothalamusNeuralClass
from subnet import LimbicNeural as LimbicNeuralClass
from subnet import ReticularNeural as ReticularNeuralClass
from subnet import ThalamusNeural as ThalamusNeuralClass
from subnet import IntentProcessingNeural as IntentProcessingNeuralClass
from model_renderer import ModelRenderer
from intent_handler import IntentHandler
from memory import Memory


class MasterNeural:
    def __init__(self, context):
        self.context = context
        self.memory = Memory()
        self.renderer = ModelRenderer(self.context, 'C:/JarvisIRL/ProjectJarviso/BrainModel/Brain.obj')
        self.intent_handler = IntentHandler(context=self.context, model_renderer=self.renderer, memory=self.memory)
        self.neural_networks = self.initialize_neural_networks()

    def initialize_neural_networks(self):
        input_size = 256
        output_size = 10

        basal_ganglia_neural = BasalGangliaNeuralClass(input_size=input_size, output_size=output_size, model_renderer=self.renderer)
        brainstem_neural = BrainstemNeuralClass(input_size=input_size, output_size=output_size, model_renderer=self.renderer)
        cerebellum_neural = CerebellumNeuralClass(input_size=input_size, output_size=output_size, model_renderer=self.renderer)
        cerebrum_neural = CerebrumNeuralClass(input_size=input_size, output_size=output_size, model_renderer=self.renderer)
        hypothalamus_neural = HypothalamusNeuralClass(input_size=input_size, output_size=output_size, model_renderer=self.renderer)
        limbic_neural = LimbicNeuralClass(input_size=input_size, output_size=output_size, model_renderer=self.renderer)
        reticular_neural = ReticularNeuralClass(input_size=input_size, output_size=output_size, model_renderer=self.renderer)
        thalamus_neural = ThalamusNeuralClass(input_size=input_size, output_size=output_size, model_renderer=self.renderer)
        intent_processing_neural = IntentProcessingNeuralClass(input_size=input_size, output_size=output_size, memory=self.memory, model_renderer=self.renderer)
        audio_processing_neural = AudioProcessingNeuralClass(input_size=input_size, output_size=output_size, memory=self.memory, model_renderer=self.renderer)

        return {
            "basal_ganglia": basal_ganglia_neural,
            "brainstem": brainstem_neural,
            "cerebellum": cerebellum_neural,
            "cerebrum": cerebrum_neural,
            "hypothalamus": hypothalamus_neural,
            "limbic": limbic_neural,
            "reticular": reticular_neural,
            "thalamus": thalamus_neural,
            "intent_processing": intent_processing_neural,
            "audio_processing": audio_processing_neural
        }

    def start_neural_networks(self):
        for name, network in self.neural_networks.items():
            logging.info(f"Starting {name} neural network...")
            threading.Thread(target=network.start_listening).start()

    def handle_intent(self, user_input):
        intents = self.intent_handler.process_user_input(user_input)
        for intent, active in intents.items():
            if active and intent in self.neural_networks:
                return self.neural_networks[intent].forward(np.random.rand(1, 256, 1).astype(np.float32))  # Adjusted input shape
        logging.error(f"Unhandled intent: {intents}")
        return "Sorry, I didn't understand that."


def main():
    logging.info("Starting Jarvis Neural Network System...")

    # Creating OpenGL context
    context = moderngl.create_standalone_context()

    master_neural = MasterNeural(context)

    # Log neural network services
    for i, (name, network) in enumerate(master_neural.neural_networks.items(), start=1):
        logging.info(f"[*] {name.capitalize()}Neural listening on localhost:{5000 + i}")

    # Start Neural Network Threads
    master_neural.start_neural_networks()


if __name__ == "__main__":
    main()
