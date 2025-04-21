import pandas as pd
import numpy as np
from pathlib import Path

def simulate_and_export(sim, dt, steps, filename_prefix):
    """
    Runs sim.step(dt) for `steps` frames, records every body's (x,y,z)
    at each time, and writes a single CSV to the top‑level data/ folder:
      data/{filename_prefix}_positions.csv
    with columns:
      time, body0_x, body0_y, body0_z, body1_x, ... 
    """
    # Number of bodies
    n = len(sim.bodies)

    # Prepare arrays
    times = np.zeros(steps)
    data  = np.zeros((steps, n * 3))

    # Time-evolve and record
    for k in range(steps):
        sim.step(dt)
        times[k] = k * dt
        row = []
        for b in sim.bodies:
            row.extend(b.position.tolist())
        data[k, :] = row

    # Build DataFrame
    cols = ["time"]
    for i in range(n):
        cols += [f"body{i}_x", f"body{i}_y", f"body{i}_z"]
    df = pd.DataFrame(np.column_stack([times, data]), columns=cols)

    # Ensure top‑level data/ directory exists
    project_root = Path(__file__).resolve().parent.parent
    data_dir     = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    # Write CSV into data/
    filepath = data_dir / f"{filename_prefix}_positions.csv"
    df.to_csv(filepath, index=False)
    print(f"Exported positions to {filepath}")

    return df