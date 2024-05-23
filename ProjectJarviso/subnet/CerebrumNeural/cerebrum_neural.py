import tensorflow as tf
import numpy as np
import socket
import threading
import json
from memory.memory import Memory

class CerebrumNeural:
    def __init__(self, input_size, output_size, model_renderer, host='localhost', port=5004):
        self.model_renderer = model_renderer
        self.memory = Memory()
        self.host = host
        self.port = port
        self.model = self.build_model(input_size, output_size)
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.start()

    def build_model(self, input_size, output_size):
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(input_size,)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(output_size)
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def forward(self, inputs):
        return self.model(inputs)

    def get_activity_data(self):
        neuron_activations = self.model.layers[0].output
        activation_values = tf.keras.backend.eval(neuron_activations)
        avg_activation = np.mean(activation_values)
        activity_data = {
            'average_activation': float(avg_activation),
            'activation_values': activation_values.tolist()
        }
        return activity_data

    def get_communication_data(self):
        inputs = tf.keras.backend.placeholder(shape=(1, self.input_size))
        gradients = tf.keras.backend.gradients(self.model.output, self.model.input)
        grad_values = tf.keras.backend.function([self.model.input], gradients)([inputs])
        avg_gradient = np.mean(grad_values)
        communication_data = {
            'average_gradient': float(avg_gradient),
            'gradient_values': grad_values.tolist()
        }
        return communication_data

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
        print(f"[*] CerebrumNeural listening on {self.host}:{self.port}")
        while True:
            client, addr = server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def start_listening(self):
        # This method is a placeholder to match the MasterNeural interface
        pass
