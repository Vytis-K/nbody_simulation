```markdown
# N‑Body Exoplanet Transit Simulation & Detection

A modular Python project to:

1. Simulate realistic multi-body orbital systems (2D & 3D)  
2. Generate synthetic transit light curves (with noise)  
3. Label each transit event (depth, duration, timestamp)  
4. Export time-series and metadata for machine learning  
5. Benchmark classical detection methods (BLS & TLS) against ground truth

---

## Directory Structure

```
.
├── data/
│   ├── lightcurves/             # synthetic light curves & event labels
│   └── *.csv                    # exported positions, velocities, energies
├── src/
│   ├── body.py                  # Body class, positions & velocities
│   ├── simulation.py            # NBodySimulation & integration methods
│   ├── orbital_utils.py         # Kepler solver, orbital elements → state vectors
│   ├── scenario_generator.py    # fixed & random system builders
│   ├── visualization.py         # 2D plotting & animation
│   ├── visualization3d.py       # 3D matplotlib animation
│   ├── data_exporter.py         # simulate & export positions.csv
│   ├── lightcurve_generator.py  # flux simulation, noise, transit detection
│   └── benchmark_detection.py   # BLS & TLS benchmarking harness
├── tests/                       # (optional) pytest test modules
├── main.py                      # example end‑to‑end script
├── requirements.txt             # Python dependencies
└── README.md                    # this file
```

---

## Installation

1. Clone the repository and navigate to its root:
   ```bash
   git clone <repo-url>
   cd nbody_simulation
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate       # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure a GUI backend is available for animations (e.g., `pip install pyqt5`).

---

## Modules & Usage

### 1. Orbital Scenarios

- Generate stable, unstable, resonant, or random multi‑planet systems.  
- Each scenario returns a list of `Body` instances and metadata.

Example:
```python
from src.scenario_generator import random_multi_planet_system

bodies, metadata = random_multi_planet_system(
    star_mass=1.989e30,
    n_planets=5,
    a_min=0.8e11,
    a_max=3.0e11
)
```

### 2. Integrators & Simulation

- Supported integrators: Euler, Velocity Verlet, RK4.  
- Advance the system with:
  ```python
  from src.simulation import NBodySimulation

  sim = NBodySimulation(bodies)
  dt = 60 * 60 * 24  # one day in seconds
  sim.step(dt, method='verlet')
  ```

### 3. Visualization

- **2D** orbit plots and animations via `src/visualization.py`.  
- **3D** scatter animations via `src/visualization3d.py`.

Example:
```python
from src.visualization3d import animate_3d

ani = animate_3d(bodies, sim, dt=86400, steps=365)
```

### 4. Data Export

- Record each body’s 3D position vs. time and export to CSV in `data/`.  
- Use:
  ```python
  from src.data_exporter import simulate_and_export

  df = simulate_and_export(sim, dt=86400, steps=365, filename_prefix="example")
  ```

### 5. Synthetic Light Curves

- Simulate flux time-series with simple transit modeling:  
  - Flux = 1 − ∑(Rp/R⋆)² when planet overlaps the star  
  - Add Gaussian noise  
  - Detect transits via a sigma threshold  
- Outputs saved under `data/lightcurves/`:
  - `lc_{i}.csv` (time, flux, flux_noisy)  
  - `events_{i}.json` (list of transit events)  
  - `metadata.json` (linking scenarios, light curves, and events)

### 6. Benchmarking Classical Detectors

- Run **Box Least Squares (BLS)** using Astropy.  
- Run **Transit Least Squares (TLS)** using `transitleastsquares`.  
- Compare results to ground truth events, flagging:
  - Missed transits  
  - Incorrect periodicity  
- Summary written to `data/benchmark_results.json`.

---

## Running Examples

1. **End‑to‑end simulation and export**  
   ```bash
   python main.py
   ```
2. **Generate synthetic light curves & event labels**  
   (if `main.py` invokes `generate_synthetic_dataset`)
3. **Run benchmark detection**  
   ```bash
   python src/benchmark_detection.py
   ```

---

## requirements.txt

```text
numpy<2.0
pandas>=1.0
matplotlib>=3.0
astropy>=5.0
transitleastsquares>=1.3
pytest>=7.0
```

---

## Contributing

Contributions welcome! Possible improvements:

- Add limb‑darkening profiles and ingress/egress smoothing  
- Implement additional integrators or performance optimizations  
- Provide web‑friendly visualizations (e.g., with Plotly)  
- Expand unit tests in the `tests/` directory

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```




Commands to run:

# Static plot of the stable two-body system (default settings)
python src/run_scenarios.py

# Animate the resonant two-planet system over 200 days with RK4
python src/run_scenarios.py \
  --scenario resonant \
  --mode animate \
  --dt 86400 \
  --steps 200 \
  --method rk4

# Static plot of the unstable three-body system, 500 steps
python src/run_scenarios.py \
  --scenario unstable \
  --mode static \
  --steps 500