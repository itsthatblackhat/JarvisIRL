import tensorflow as tf
import socket
import threading
import json
import numpy as np

class BasalGangliaNeural:
    def __init__(self, input_size, output_size, model_renderer, host='localhost', port=5001):
        self.model_renderer = model_renderer
        self.input_size = input_size
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(input_size,)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(output_size)
        ])
        self.host = host
        self.port = port
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.start()

    def forward(self, inputs):
        # Convert string input to list of ASCII values and pad/truncate to input_size
        if isinstance(inputs, tf.Tensor):
            inputs = inputs.numpy().tolist()
        if isinstance(inputs[0], str):
            ascii_values = [ord(char) for char in inputs[0]]
            if len(ascii_values) < self.input_size:
                ascii_values += [0] * (self.input_size - len(ascii_values))  # Padding with zeros
            else:
                ascii_values = ascii_values[:self.input_size]  # Truncating to input_size
            inputs = tf.convert_to_tensor([ascii_values], dtype=tf.float32)
        return self.model(inputs)

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
            if data['type'] == 'activity':
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
        print(f"[*] BasalGangliaNeural listening on {self.host}:{self.port}")
        while True:
            client, addr = server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()
