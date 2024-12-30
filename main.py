from src.body import Body
import pandas as pd
from src.simulation import NBodySimulation
from src.visualization import plot_simulation
from src.visualization import animate_orbits
import numpy as np

def main():
    """
    earth_mass = 5.972e24
    sun_mass = 1.989e30
    earth = Body(earth_mass, [1.5e11, 0], [0, 29.78e3])
    sun = Body(sun_mass, [0, 0], [0, 0])

    bodies = [earth, sun]

    sim = NBodySimulation(bodies)

    dt = 60 * 60 * 24  # one day in seconds
    num_steps = 365  # one year

    for step in range(num_steps):
        sim.step(dt)
        # Debug: Print positions and velocities of bodies
        print(f"Step {step}: Earth position = {earth.position}, Earth velocity = {earth.velocity}")
        print(f"Sun position = {sun.position}, Sun velocity = {sun.velocity}")
        if step % 30 == 0:  # Plot every month
            plot_simulation(bodies, step*dt)
    """  


    earth_mass = 5.972e24
    sun_mass = 1.989e30
    mars_mass = 5.972e24
    earth = Body(earth_mass, [1.5e11, 0], [0, 29.78e3])
    sun = Body(sun_mass, [0, 0], [0, 0])
    mars = Body(mars_mass, [3e11, 0], [0, 29.78e3])

    bodies = [earth, sun, mars]

    dt = 60 * 60 * 24  # one day in seconds
    num_steps = 365  # one year

    animate_orbits(bodies, num_steps, dt)
 
    """
    earth_mass = 5.972e24
    sun_mass = 1.989e30
    earth = Body(earth_mass, [1.5e11, 0], [0, 29.78e3])
    sun = Body(sun_mass, [0, 0], [0, 0])

    bodies = [earth, sun]

    sim = NBodySimulation(bodies)

    positions = []
    velocities = []
    energies = []

    dt = 60 * 60 * 24
    num_steps = 365

    for step in range(num_steps):
        sim.step(dt, method='verlet')

        positions.append([body.position[0] for body in sim.bodies] + [body.position[1] for body in sim.bodies])
        velocities.append([body.velocity[0] for body in sim.bodies] + [body.velocity[1] for body in sim.bodies])
        total_energy = sum(0.5 * body.mass * np.linalg.norm(body.velocity)**2 for body in sim.bodies)
        energies.append(total_energy)

        if step % 30 == 0:
            plot_simulation(bodies, step * dt)

    # save data to csv file
    positions_df = pd.DataFrame(positions, columns=['Earth_x', 'Earth_y', 'Sun_x', 'Sun_y'])
    velocities_df = pd.DataFrame(velocities, columns=['Earth_vx', 'Earth_vy', 'Sun_vx', 'Sun_vy'])
    energies_df = pd.DataFrame(energies, columns=['Total Energy'])

    positions_df.to_csv('data/positions.csv', index=False)
    velocities_df.to_csv('data/velocities.csv', index=False)
    energies_df.to_csv('data/energies.csv', index=False)
    """

if __name__ == "__main__":
    main()