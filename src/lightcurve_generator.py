import copy
import json
import numpy as np
import pandas as pd
from pathlib import Path
from simulation import NBodySimulation

def simulate_lightcurve(
    initial_bodies,
    dt,
    steps,
    R_star,
    planet_radii,
    los=np.array([1.0, 0.0, 0.0]),
    noise_std=1e-4
):
    """
    Runs an N-body sim for `steps` frames of size dt, then returns a DataFrame
    with columns [time, flux, flux_noisy].

    - initial_bodies: list of Body (star must be at index 0).
    - R_star: stellar radius [m].
    - planet_radii: dict mapping body-index -> radius [m], e.g. {1:6.37e6,2:6.37e6}.
    - los: observer line‑of‑sight unit vector (points *toward* observer).
    - noise_std: σ of Gaussian noise to add to flux.
    """
    # copy bodies so we don't mutate originals
    bodies = copy.deepcopy(initial_bodies)
    sim = NBodySimulation(bodies)

    times = np.arange(steps) * dt
    flux  = np.ones(steps)

    los_unit = los / np.linalg.norm(los)

    for t in range(steps):
        total_drop = 0.0
        # for each planet (skip index 0, the star)
        for idx, body in enumerate(bodies[1:], start=1):
            # vector from star→planet
            rel = body.position - bodies[0].position
            # project onto LOS
            z = np.dot(rel, los_unit)
            # perpendicular distance
            r_perp = rel - z * los_unit
            d = np.linalg.norm(r_perp)

            Rp = planet_radii.get(idx, 0.0)
            # simple occultation check
            if d < (R_star + Rp):
                # fraction drop ≈ area ratio
                total_drop += (Rp / R_star)**2

        # clamp flux ≥ 0
        flux[t] = max(1.0 - total_drop, 0.0)

        # advance simulation one step
        sim.step(dt)

    # add Gaussian noise
    noise = np.random.normal(loc=0.0, scale=noise_std, size=steps)
    flux_noisy = flux + noise

    return pd.DataFrame({
        "time": times,
        "flux": flux,
        "flux_noisy": flux_noisy
    })


def detect_transits(df, threshold_sigma=5.0):
    """
    Simple transit finder on `df["flux_noisy"]`.

    - threshold_sigma: how many σ below the median to call 'in transit'.

    Returns a list of events, each a dict:
      {start_time, end_time, duration, depth}
    """
    f = df["flux_noisy"].values
    t = df["time"].values

    median = np.median(f)
    sigma  = np.std(f)
    thresh = median - threshold_sigma * sigma

    in_transit = f < thresh
    events = []
    i = 0
    while i < len(f):
        if in_transit[i]:
            start = i
            while i < len(f) and in_transit[i]:
                i += 1
            end = i - 1
            depth = float(median - np.min(f[start : end + 1]))
            events.append({
                "start_time": float(t[start]),
                "end_time":   float(t[end]),
                "duration":   float(t[end] - t[start]),
                "depth":      depth
            })
        else:
            i += 1

    return events


def generate_synthetic_dataset(
    scenarios,
    dt,
    steps,
    R_star,
    planet_radii,
    los,
    noise_std,
    threshold_sigma,
    output_dir="data/lightcurves"
):
    """
    For each (bodies, metadata) in `scenarios`, simulate a light curve,
    detect transits, save:
      - data/lightcurves/lc_{i}.csv
      - data/lightcurves/events_{i}.json
    and write a master metadata.json.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    all_meta = []
    for i, (bodies, meta) in enumerate(scenarios):
        # simulate
        df = simulate_lightcurve(
            initial_bodies=bodies,
            dt=dt, steps=steps,
            R_star=R_star,
            planet_radii=planet_radii,
            los=los,
            noise_std=noise_std
        )

        # detect
        events = detect_transits(df, threshold_sigma=threshold_sigma)

        # save files
        lc_path     = out / f"lc_{i}.csv"
        events_path = out / f"events_{i}.json"
        df.to_csv(lc_path, index=False)
        with open(events_path, "w") as f:
            json.dump(events, f, indent=2)

        # assemble metadata entry
        entry = {
            "scenario_index": i,
            "lightcurve_file": str(lc_path),
            "events_file":     str(events_path),
            **meta
        }
        all_meta.append(entry)

    # write master metadata
    with open(out / "metadata.json", "w") as f:
        json.dump(all_meta, f, indent=2)

    print(f"Generated {len(scenarios)} light curves in {output_dir}/")
    return all_meta
