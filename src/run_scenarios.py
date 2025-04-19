import argparse
from simulation import NBodySimulation
from visualization import plot_simulation, animate_orbits
from scenario_generator import (
    generate_stable_two_body,
    generate_unstable_three_body,
    generate_resonant_two_planet,
    generate_equal_three_body,
    DAY
)

def main():
    parser = argparse.ArgumentParser(description="Run n-body scenarios")
    parser.add_argument(
        "--scenario",
        choices=[
            "stable_two_body",
            "unstable_three_body",
            "resonant_two_planet",
            "equal_three_body",
        ],
        default="stable_two_body",
        help="Which scenario to run"
    )
    parser.add_argument(
        "--mode",
        choices=["static", "animate"],
        default="static",
        help="Static end‐point plot or full animation"
    )
    parser.add_argument(
        "--dt", type=float, default=DAY,
        help="Time step in seconds (default = 1 day)"
    )
    parser.add_argument(
        "--steps", type=int, default=365,
        help="Number of steps (default = 365)"
    )
    parser.add_argument(
        "--method",
        choices=["euler", "verlet", "rk4"],
        default="verlet",
        help="Integration method"
    )
    args = parser.parse_args()

    # Map names to generator functions
    scenario_map = {
        "stable_two_body": generate_stable_two_body,
        "unstable_three_body": generate_unstable_three_body,
        "resonant_two_planet": generate_resonant_two_planet,
        "equal_three_body": generate_equal_three_body,
    }

    bodies, meta = scenario_map[args.scenario]()
    print(f"Loaded scenario: {meta['scenario']} with {len(bodies)} bodies, stability={meta['stability']}")

    sim = NBodySimulation(bodies)

    if args.mode == "static":
        # run all steps then show one plot
        for _ in range(args.steps):
            sim.step(args.dt, method=args.method)
        plot_simulation(bodies, args.steps * args.dt)
    else:
        # full animation
        animate_orbits(bodies, args.steps, args.dt)

if __name__ == "__main__":
    main()
