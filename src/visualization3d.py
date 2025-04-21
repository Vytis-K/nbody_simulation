import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib.animation import FuncAnimation

def animate_3d(bodies, sim, dt, steps):
    """
    Animate in 3D the list of Body objects under NBodySimulation `sim`.
    """
    fig = plt.figure(figsize=(8,8))
    ax  = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')

    # choose limits based on expected a_max
    lim = max(
        max(abs(body.position).max() for body in bodies),
        1e11
    )
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.grid(True)

    # create scatter for each body
    scatters = [
        ax.scatter([], [], [], s=(100 if body.mass>1e26 else 50))
        for body in bodies
    ]

    def init():
        for sc in scatters:
            sc._offsets3d = ([], [], [])
        return scatters

    def update(frame):
        sim.step(dt)
        for sc, body in zip(scatters, bodies):
            x,y,z = body.position
            sc._offsets3d = ([x], [y], [z])
        return scatters

    ani = FuncAnimation(
        fig, update, frames=steps,
        init_func=init, interval=50, blit=False
    )
    plt.show()
    return ani
