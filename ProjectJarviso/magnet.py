import numpy as np

class Magnet:
    def __init__(self, position, strength):
        self.position = np.array(position, dtype='f4')
        self.strength = strength

    def attract(self, particle_pos):
        direction = self.position - particle_pos
        distance = np.linalg.norm(direction)
        if distance == 0:
            return np.array([0.0, 0.0, 0.0], dtype='f4')
        force = self.strength * direction / (distance ** 2)
        return force
