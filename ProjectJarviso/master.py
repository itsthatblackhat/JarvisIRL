import threading
import json
import socket
import logging
import moderngl
import numpy as np
import tensorflow as tf
from subnet import BasalGangliaNeural, BrainstemNeural, CerebellumNeural, CerebrumNeural, HypothalamusNeural, LimbicNeural, ReticularNeural, ThalamusNeural
from visualization import activity_visualization, communication_visualization
from model_renderer import ModelRenderer
from intent_handler import IntentHandler
from memory.memory import Memory
from memory.memory_imprinting import MemoryImprinting

class MasterNeural:
    def __init__(self, input_size, output_size, context, model_file):
        logging.error("Initializing MasterNeural")
        self.model_renderer = ModelRenderer(context, model_file)
        self.memory = Memory()
        self.memory_imprinting = MemoryImprinting(self.memory)
        self.intent_handler = IntentHandler(context, self.model_renderer, self.memory)
        self.subnets = {
            'cerebrum': CerebrumNeural(input_size, output_size, self.model_renderer),
            'cerebellum': CerebellumNeural(input_size, output_size, self.model_renderer),
            'brainstem': BrainstemNeural(input_size, output_size, self.model_renderer),
            'thalamus': ThalamusNeural(input_size, output_size, self.model_renderer),
            'hypothalamus': HypothalamusNeural(input_size, output_size, self.model_renderer),
            'basal_ganglia': BasalGangliaNeural(input_size, output_size, self.model_renderer),
            'limbic': LimbicNeural(input_size, output_size, self.model_renderer),
            'reticular': ReticularNeural(input_size, output_size, self.model_renderer),
        }
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.start()

    def start_server(self):
        host, port = 'localhost', 5000
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)
        print(f"[*] MasterNeural listening on {host}:{port}")
        while True:
            client, addr = server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(1024)
            data = json.loads(request.decode('utf-8'))
            if data['type'] == 'intent':
                response = self.intent_handler.handle_intents(data['content'])
                client_socket.send(json.dumps(response).encode('utf-8'))
            elif data['type'] == 'activity':
                response = {'activity': self.collect_activity_data()}
                client_socket.send(json.dumps(response).encode('utf-8'))
            elif data['type'] == 'communication':
                response = {'communication': self.collect_communication_data()}
                client_socket.send(json.dumps(response).encode('utf-8'))
        except Exception as e:
            logging.error(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def collect_activity_data(self):
        activity_data = {}
        for name, subnet in self.subnets.items():
            activity_data[name] = {'intensity': subnet.get_activity_data()}
        return activity_data

    def collect_communication_data(self):
        communication_data = {}
        for name, subnet in self.subnets.items():
            communication_data[name] = {'intensity': subnet.get_communication_data()}
        return communication_data

    def start_activity_visualization(self, stop_event):
        activity_data = self.collect_activity_data()
        logging.error(f"Starting activity visualization with data: {activity_data}")
        activity_visualization.start_activity_visualization(activity_data, self.subnets.keys(), self.model_renderer, stop_event)

    def start_communication_visualization(self, stop_event):
        communication_data = self.collect_communication_data()
        logging.error(f"Starting communication visualization with data: {communication_data}")
        communication_visualization.start_communication_visualization(communication_data, self.subnets.keys(), self.model_renderer, stop_event)

def main():
    input_size, output_size = 100, 10
    ctx = moderngl.create_standalone_context()
    model_file = 'C:/JarvisIRL/ProjectJarviso/BrainModel/Brain.obj'
    master_neural = MasterNeural(input_size, output_size, ctx, model_file)

    stop_event = threading.Event()
    activity_thread = threading.Thread(target=master_neural.start_activity_visualization, args=(stop_event,))
    communication_thread = threading.Thread(target=master_neural.start_communication_visualization, args=(stop_event,))
    activity_thread.start()
    communication_thread.start()

    try:
        while True:
            user_input = input("You: ")
            logging.error(f"Received user input: {user_input}")
            if user_input.lower() == 'exit':
                stop_event.set()
                break
            response = master_neural.intent_handler.process_user_input(user_input)
            logging.error(response)
    except KeyboardInterrupt:
        stop_event.set()

if __name__ == "__main__":
    main()
