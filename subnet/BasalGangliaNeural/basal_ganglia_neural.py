import tensorflow as tf
import numpy as np
import socket
import threading
import json

class BasalGangliaNeural:
    def __init__(self, input_size, output_size, model_renderer, host='localhost', port=5001):
        self.input_size = input_size
        self.output_size = output_size
        self.model_renderer = model_renderer
        self.model = self.build_model()
        self.host = host
        self.port = port

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(self.input_size,)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(self.output_size)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
        return model

    def start_listening(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[*] BasalGangliaNeural listening on {self.host}:{self.port}")
        while True:
            client, addr = server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(1024)
            data = json.loads(request.decode('utf-8'))
            if data['type'] == 'forward':
                response = self.forward(data['input'])
            else:
                response = {"error": "Unknown request type"}
            client_socket.send(json.dumps(response).encode('utf-8'))
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def forward(self, inputs):
        inputs = np.array(inputs).reshape(-1, self.input_size)
        prediction = self.model.predict(inputs)
        return prediction.tolist()
