from body import Body
import pandas as pd
from simulation import NBodySimulation
from visualization import plot_simulation
from visualization import animate_orbits
import numpy as np

from scenario_generator import random_multi_planet_system
from visualization3d import animate_3d

from scenario_generator import close_encounter_system
from data_exporter import simulate_and_export

from scenario_generator import (
    random_multi_planet_system,
    close_encounter_system,
    resonant_drift_system
)
from lightcurve_generator import generate_synthetic_dataset

def main():
    """
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
    """
    
    scenarios = [
        random_multi_planet_system(
            star_mass=1.989e30,
            n_planets=3, a_min=0.8e11, a_max=2.0e11
        ),
        close_encounter_system(
            star_mass=1.989e30, a1=1.0e11, a2=1.5e11, delta_v=500.0
        ),
        resonant_drift_system(
            star_mass=1.989e30, resonance_ratio=2.0
        ),
    ]

    # 2) choose parameters:
    dt              = 60*60*24        # one day
    steps           = 365             # simulate one year
    R_star          = 6.96e8          # Sun radius [m]
    # map body-index→radius: 1,2,... planets
    planet_radii    = {1:6.37e6, 2:6.37e6, 3:7.1e7}  
    los             = np.array([1,0,0])  # look along +x axis
    noise_std       = 1e-4            # ~100 ppm noise
    threshold_sigma = 5.0             # 5σ detection

    # 3) generate and export:
    meta = generate_synthetic_dataset(
        scenarios,
        dt, steps,
        R_star,
        planet_radii,
        los,
        noise_std,
        threshold_sigma,
        output_dir="data/lightcurves"
    )

    print("All scenario metadata:", meta)
    
    """
    # 1) build your unstable scenario
    bodies, metadata = close_encounter_system(
        star_mass=1.989e30,
        a1=1.0e11,
        a2=1.5e11,
        delta_v=800.0
    )
    print("Scenario:", metadata)

    # 2) set up sim
    sim = NBodySimulation(bodies)
    dt    = 60*60*24   # day
    steps = 500        # ~1.4 years

    # 3) run & export
    df = simulate_and_export(sim, dt, steps, "unstable_close_encounter")

    # optionally inspect head
    print(df.head())
    """

if __name__ == "__main__":
    main()