import numpy as np
from body import Body

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
