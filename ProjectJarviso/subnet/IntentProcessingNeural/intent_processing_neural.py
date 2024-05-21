import tensorflow as tf
import numpy as np
import socket
import threading
import json
from memory.memory import Memory


class IntentProcessingNeural:
    def __init__(self, input_size, output_size, model_renderer, host='localhost', port=5009):
        self.model_renderer = model_renderer
        self.memory = Memory()

        # Using the Functional API for layers with multiple inputs
        inputs = tf.keras.layers.Input(shape=(input_size,))
        x = tf.keras.layers.Dense(128, activation='relu')(inputs)
        x = tf.keras.layers.Dense(128, activation='relu')(x)

        # MultiHeadAttention requires query, key, and value inputs
        attention_output = tf.keras.layers.MultiHeadAttention(num_heads=4, key_dim=64)(x, x)
        outputs = tf.keras.layers.Dense(output_size)(attention_output)

        # Define the functional model
        self.model = tf.keras.Model(inputs=inputs, outputs=outputs)

        self.host = host
        self.port = port
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.start()

    def forward(self, inputs):
        return self.model(inputs)

    def process_intent(self, user_input):
        # Placeholder for real intent processing logic
        intents = {}
        user_input = user_input.lower()
        if "hello" in user_input or "hi" in user_input:
            intents['greeting'] = True
        if "test" in user_input:
            intents['test'] = True
        if "activity" in user_input:
            intents['activity'] = True
        if "communication" in user_input:
            intents['communication'] = True
        if "status" in user_input:
            intents['status'] = True
        if "exit" in user_input:
            intents['exit'] = True
        return intents

    def get_activity_data(self):
        # Placeholder for real activity data
        activity_level = np.random.random()
        return activity_level

    def get_communication_data(self):
        # Placeholder for real communication data
        communication_level = np.random.random()
        return communication_level

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(1024)
            data = json.loads(request.decode('utf-8'))
            if data['type'] == 'intent':
                response = {'intent': self.process_intent(data['user_input'])}
            elif data['type'] == 'activity':
                response = {'activity': self.get_activity_data()}
            elif data['type'] == 'communication':
                response = {'communication': self.get_communication_data()}
            client_socket.send(json.dumps(response).encode('utf-8'))
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[*] IntentProcessingNeural listening on {self.host}:{self.port}")
        while True:
            client, addr = server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()
