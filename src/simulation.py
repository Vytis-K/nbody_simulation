import numpy as np
from body import Body

class NBodySimulation:
    def __init__(self, bodies, G=6.67430e-11):
        self.bodies = bodies
        self.G = G

    def compute_forces(self):
        for body in self.bodies:
            body.force = np.zeros_like(body.position)
        for i, body1 in enumerate(self.bodies):
            for j, body2 in enumerate(self.bodies):
                if i != j:
                    r = body2.position - body1.position
                    distance = np.linalg.norm(r)
                    if distance == 0:
                        continue
                    f_magnitude = (self.G * body1.mass * body2.mass) / (distance**2)
                    body1.force += f_magnitude * (r / distance)

    """
    def step(self, dt):
        self.compute_forces()
        for body in self.bodies:
            body.update_velocity(dt)
            body.update_position(dt)
    """

    def euler_step(self, dt):
        for body in self.bodies:
            body.velocity += (body.force / body.mass) * dt
            body.position += body.velocity * dt
    
    def velocity_verlet_step(self, dt):
        for body in self.bodies:
            body.velocity += 0.5 * (body.force / body.mass) * dt

        for body in self.bodies:
            body.position += body.velocity * dt

        self.compute_forces()

        for body in self.bodies:
            body.velocity += 0.5 * (body.force / body.mass) * dt

    def rk4_step(self, dt):
        for body in self.bodies:
            k1_v = (body.force / body.mass) * dt
            k1_x = body.velocity * dt

            temp_position = body.position + 0.5 * k1_x
            temp_velocity = body.velocity + 0.5 * k1_v
            self.compute_forces()

            k2_v = (body.force / body.mass) * dt
            k2_x = temp_velocity * dt

            temp_position = body.position + 0.5 * k2_x
            temp_velocity = body.velocity + 0.5 * k2_v
            self.compute_forces()

            k3_v = (body.force / body.mass) * dt
            k3_x = temp_velocity * dt

            temp_position = body.position + k3_x
            temp_velocity = body.velocity + k3_v
            self.compute_forces()

            k4_v = (body.force / body.mass) * dt
            k4_x = temp_velocity * dt

            body.velocity += (k1_v + 2 * k2_v + 2 * k3_v + k4_v) / 6.0
            body.position += (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6.0


    def step(self, dt, method='euler'):
        self.compute_forces()
        if method == 'euler':
            self.euler_step(dt)
        elif method == 'verlet':
            self.velocity_verlet_step(dt)
        elif method == 'rk4':
            self.rk4_step(dt)
