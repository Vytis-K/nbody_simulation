import numpy as np

# define the gravitational object
class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.force = np.zeros_like(position, dtype=float)
    
    def update_position(self, dt):
        self.position += self.velocity * dt

    def update_velocity(self, dt):
        self.velocity += (self.force / self.mass) * dt