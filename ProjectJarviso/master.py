import json
import logging
import socket
import threading
import numpy as np
import tensorflow as tf
from memory.memory import Memory
from memory.memory_imprinting import MemoryImprinting
from memory.memory_utils import MemoryUtils
from subnet.BasalGangliaNeural.basal_ganglia_neural import BasalGangliaNeural
from subnet.BrainstemNeural.brainstem_neural import BrainstemNeural
from subnet.CerebellumNeural.cerebellum_neural import CerebellumNeural
from subnet.CerebrumNeural.cerebrum_neural import CerebrumNeural
from subnet.HypothalamusNeural.hypothalamus_neural import HypothalamusNeural
from subnet.LimbicNeural.limbic_neural import LimbicNeural
from subnet.ReticularNeural.reticular_neural import ReticularNeural
from subnet.ThalamusNeural.thalamus_neural import ThalamusNeural
from subnet.IntentProcessingNeural.intent_processing_neural import IntentProcessingNeural
from model_renderer import ModelRenderer


class MasterNeural:
    def __init__(self, input_size, output_size, ctx, model_file):
        self.memory = Memory()
        self.memory_imprinting = MemoryImprinting(self.memory)
        self.model_renderer = ModelRenderer(ctx, model_file)
        self.input_size = input_size
        self.output_size = output_size

        self.networks = {
            'basal_ganglia': BasalGangliaNeural(input_size, output_size, self.model_renderer),
            'brainstem': BrainstemNeural(input_size, output_size, self.model_renderer),
            'cerebellum': CerebellumNeural(input_size, output_size, self.model_renderer),
            'cerebrum': CerebrumNeural(input_size, output_size, self.model_renderer),
            'hypothalamus': HypothalamusNeural(input_size, output_size, self.model_renderer),
            'limbic': LimbicNeural(input_size, output_size, self.model_renderer),
            'reticular': ReticularNeural(input_size, output_size, self.model_renderer),
            'thalamus': ThalamusNeural(input_size, output_size, self.model_renderer),
            'intent_processing': IntentProcessingNeural(input_size, output_size, self.model_renderer)
        }

    def handle_intent(self, user_input):
        intents = self.networks['intent_processing'].process_intent(user_input)
        for intent, active in intents.items():
            if active and intent in self.networks:
                return self.networks[intent].forward(np.random.rand(1, self.input_size).astype(np.float32))
        logging.error(f"Unhandled intent: {intents}")
        return "Sorry, I didn't understand that."


def main():
    input_size = 256  # example size
    output_size = 10  # example size
    ctx = None  # appropriate context for ModelRenderer
    model_file = 'BrainModel/Brain.obj'  # path to the model file

    master_neural = MasterNeural(input_size, output_size, ctx, model_file)

    host = 'localhost'
    port = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    logging.info(f"[*] MasterNeural listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, master_neural))
        client_handler.start()


def handle_client(client_socket, master_neural):
    with client_socket as sock:
        while True:
            request = sock.recv(1024).decode('utf-8')
            if not request:
                break
            user_input = request.strip()
            response = master_neural.handle_intent(user_input)
            sock.send(response.encode('utf-8'))


if __name__ == "__main__":
    main()
