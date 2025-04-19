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