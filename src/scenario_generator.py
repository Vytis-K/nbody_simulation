import numpy as np
from body import Body
from orbital_utils import orbital_elements_to_state_vectors

# Astronomical constants
G = 6.67430e-11             # Gravitational constant, m^3 kg^-1 s^-2
AU = 1.495978707e11         # Astronomical unit in meters
DAY = 60 * 60 * 24          # One day in seconds

# Standard masses
SUN_MASS = 1.989e30         # kg
EARTH_MASS = 5.972e24       # kg
MARS_MASS = 6.4171e23       # kg (for variety)


def generate_stable_two_body():
    sun = Body(SUN_MASS, position=[0.0, 0.0], velocity=[0.0, 0.0])
    r = AU
    v = np.sqrt(G * SUN_MASS / r)
    earth = Body(EARTH_MASS, position=[r, 0.0], velocity=[0.0, v])

    metadata = {
        "scenario": "stable_two_body",
        "num_planets": 1,
        "stability": "stable",
        "resonance_ratio": None
    }
    return [sun, earth], metadata


def generate_unstable_three_body():
    sun = Body(SUN_MASS, position=[0.0, 0.0], velocity=[0.0, 0.0])
    r = AU
    v = np.sqrt(G * SUN_MASS / r)
    planet1 = Body(EARTH_MASS, position=[r, 0.0], velocity=[0.0, v])
    planet2 = Body(EARTH_MASS, position=[-r, 0.0], velocity=[0.0, -v])
    r3 = 1.5 * AU
    v3 = np.sqrt(G * SUN_MASS / r3) * 0.8
    rogue = Body(EARTH_MASS, position=[0.0, r3], velocity=[-v3, 0.0])

    metadata = {
        "scenario": "unstable_three_body",
        "num_planets": 3,
        "stability": "unstable",
        "resonance_ratio": None
    }
    return [sun, planet1, planet2, rogue], metadata


def generate_resonant_two_planet():
    sun = Body(SUN_MASS, position=[0.0, 0.0], velocity=[0.0, 0.0])
    a1 = AU
    v1 = np.sqrt(G * SUN_MASS / a1)
    planet1 = Body(EARTH_MASS, position=[a1, 0.0], velocity=[0.0, v1])
    a2 = a1 * 2**(2/3)
    v2 = np.sqrt(G * SUN_MASS / a2)
    planet2 = Body(MARS_MASS, position=[a2, 0.0], velocity=[0.0, v2])

    metadata = {
        "scenario": "resonant_two_planet",
        "num_planets": 2,
        "stability": "marginal",
        "resonance_ratio": "2:1"
    }
    return [sun, planet1, planet2], metadata


def generate_equal_three_body(side_length=AU, mass=SUN_MASS):
    """
    Three equal-mass bodies at vertices of an equilateral triangle orbiting their center-of-mass
    Returns:
        bodies (list of Body): three Body instances
        metadata (dict)
    """
    # Side of the triangle and distance from COM
    d = side_length
    r = d / np.sqrt(3)

    # Corrected angular velocity for equilateral Lagrange solution
    omega = np.sqrt(3 * G * mass / (d**3))

    bodies = []
    angles = [0, 2*np.pi/3, 4*np.pi/3]
    for theta in angles:
        # Position in plane
        pos = [r * np.cos(theta), r * np.sin(theta)]
        # Tangential velocity (v = ωr)
        vel = [-omega * r * np.sin(theta), omega * r * np.cos(theta)]
        bodies.append(Body(mass, position=pos, velocity=vel))

    metadata = {
        "scenario": "equal_three_body",
        "num_planets": 3,
        "stability": "stable",
        "resonance_ratio": None
    }
    return bodies, metadata

def random_multi_planet_system(
    star_mass: float,
    n_planets: int = 5,
    a_min: float = 0.5e11,
    a_max: float = 2.5e11
):
    """
    Generates one star + `n_planets`, each with random
    semi-major axis, eccentricity, and inclination.
    Returns (bodies_list, metadata_dict).
    """
    bodies = []
    # 1) Star at origin
    star = Body(star_mass, [0,0,0], [0,0,0])
    bodies.append(star)

    # 2) Prepare metadata
    metadata = {
        "type": "random_multi_planet",
        "n_planets": n_planets,
        "elements": []
    }

    mu = G * (star_mass)  # planet masses ≪ star mass

    for k in range(n_planets):
        # sample orbital elements
        a   = np.random.uniform(a_min, a_max)
        e   = np.random.uniform(0.0, 0.4)           # up to e=0.4
        inc = np.deg2rad(np.random.uniform(0, 10))  # up to 10°
        raan  = np.random.uniform(0, 2*np.pi)
        argp  = np.random.uniform(0, 2*np.pi)
        M0    = np.random.uniform(0, 2*np.pi)
        m_planet = 5.0e24  # e.g. Earth‑mass scale

        # convert to cartesian
        pos, vel = orbital_elements_to_state_vectors(
            a, e, inc, raan, argp, M0, mu
        )

        planet = Body(m_planet, pos, vel)
        bodies.append(planet)

        # record elements
        metadata["elements"].append({
            "a": a,
            "e": e,
            "i": float(np.rad2deg(inc)),
            "raan": float(np.rad2deg(raan)),
            "argp": float(np.rad2deg(argp)),
            "M0": float(np.rad2deg(M0)),
            "mass": m_planet
        })

    return bodies, metadata


def close_encounter_system(
    star_mass: float,
    planet_mass: float = 5e24,
    a1: float = 1.0e11,
    a2: float = 1.5e11,
    delta_v: float = 500.0
):
    """
    Two planets on initially circular coplanar orbits, but give
    the outer one a kick so that it will have a close encounter.
    """
    # star
    bodies = [Body(star_mass, [0,0,0], [0,0,0])]

    mu = G * star_mass
    # inner planet: circular
    r1, v1 = orbital_elements_to_state_vectors(a1, 0.0, 0.0, 0.0, 0.0, 0.0, mu)
    p1 = Body(planet_mass, r1, v1)
    bodies.append(p1)

    # outer planet: circular + small extra radial kick
    r2, v2 = orbital_elements_to_state_vectors(a2, 0.0, 0.0, 0.0, 0.0, 0.0, mu)
    v2 = v2 + np.array([0, delta_v, 0])  # perturb in y-direction
    p2 = Body(planet_mass, r2, v2)
    bodies.append(p2)

    metadata = {
        "type": "close_encounter",
        "a1": a1,
        "a2": a2,
        "delta_v": delta_v
    }
    return bodies, metadata


def resonant_drift_system(
    star_mass: float,
    planet_mass: float = 5e24,
    a_inner: float = 1.0e11,
    resonance_ratio: float = 1.5  # e.g. 3:2 when =1.5
):
    """
    Two planets whose periods differ only slightly from exact resonance,
    so that resonant interactions will build over time.
    """
    bodies = [Body(star_mass, [0,0,0], [0,0,0])]
    mu = G * star_mass

    # exact circular inner
    r1, v1 = orbital_elements_to_state_vectors(
        a_inner, 0.0, 0.0, 0.0, 0.0, 0.0, mu
    )
    p1 = Body(planet_mass, r1, v1)
    bodies.append(p1)

    # outer at near resonance
    a_outer = a_inner * (resonance_ratio)**(2/3) * 1.01
    r2, v2 = orbital_elements_to_state_vectors(
        a_outer, 0.0, 0.0, 0.0, 0.0, 0.0, mu
    )
    p2 = Body(planet_mass, r2, v2)
    bodies.append(p2)

    metadata = {
        "type": "resonant_drift",
        "a_inner": a_inner,
        "a_outer": a_outer,
        "target_ratio": resonance_ratio
    }
    return bodies, metadata


def generate_all_random(n_systems=3, **kwargs):
    """
    Generate N different random multi‑planet systems.
    """
    scenarios = []
    for _ in range(n_systems):
        bodies, meta = random_multi_planet_system(**kwargs)
        scenarios.append((bodies, meta))
    return scenarios


def generate_all_scenarios():
    return [
        generate_stable_two_body(),
        generate_unstable_three_body(),
        generate_resonant_two_planet(),
        generate_equal_three_body(),
    ]


if __name__ == "__main__":
    for bodies, meta in generate_all_scenarios():
        print(f"Loaded scenario: {meta['scenario']} with {len(bodies)} bodies, stability={meta['stability']}")
