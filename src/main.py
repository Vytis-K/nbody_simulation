from body import Body
import pandas as pd
from simulation import NBodySimulation
from visualization import plot_simulation
from visualization import animate_orbits
import numpy as np

from scenario_generator import random_multi_planet_system
from visualization3d import animate_3d

def main():
    bodies, meta = random_multi_planet_system(
        star_mass=1.989e30,
        n_planets=5,
        a_min=0.8e11,
        a_max=3.0e11
    )
    print("Scenario:", meta)

    sim = NBodySimulation(bodies)
    dt = 60*60*24        # one day
    steps = 365          # one year

    animate_3d(bodies, sim, dt, steps)

if __name__ == "__main__":
    main()