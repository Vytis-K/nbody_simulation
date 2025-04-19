import matplotlib.pyplot as plt
import matplotlib.animation as animation
from simulation import NBodySimulation

def plot_simulation(bodies, time):
    plt.figure(figsize=(8, 8))
    
    # Plot each body with a different color and size
    for body in bodies:
        plt.scatter(body.position[0], body.position[1], s=100 if body.mass > 1e26 else 50, color='orange' if body.mass > 1e26 else 'blue')
    
    # Adjust plot limits to ensure the full orbit is visible
    plt.xlim(-2.5e11, 2.5e11)  # Increased limits for better visibility
    plt.ylim(-2.5e11, 2.5e11)
    
    plt.title(f'Time = {time:.2f} seconds')
    plt.xlabel('x position (m)')
    plt.ylabel('y position (m)')
    plt.grid(True)
    plt.show()

def animate_orbits(bodies, num_steps, dt):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-2.5e11, 2.5e11)
    ax.set_ylim(-2.5e11, 2.5e11)
    ax.set_xlabel('x position (m)')
    ax.set_ylabel('y position (m)')
    ax.grid(True)

    # Scatter objects for the bodies
    scatters = []
    for body in bodies:
        scatter = ax.scatter(body.position[0], body.position[1], s=100 if body.mass > 1e26 else 50, 
                             color='orange' if body.mass > 1e26 else 'blue')
        scatters.append(scatter)

    def update(frame):
        sim.step(dt)
        for scatter, body in zip(scatters, bodies):
            scatter.set_offsets(body.position)
        ax.set_title(f'Time = {frame * dt:.2f} seconds')
        return scatters

    # Initialize the simulation
    sim = NBodySimulation(bodies)
    
    ani = animation.FuncAnimation(fig, update, frames=num_steps, interval=50, blit=True)
    plt.show()