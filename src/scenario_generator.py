import numpy as np
from src.body import Body

# Astronomical constants
G = 6.67430e-11             # Gravitational constant, m^3 kg^-1 s^-2
AU = 1.495978707e11         # Astronomical unit in meters
DAY = 60 * 60 * 24          # One day in seconds

# Standard masses
SUN_MASS = 1.989e30         # kg
EARTH_MASS = 5.972e24       # kg
MARS_MASS = 6.4171e23       # kg (for variety)


def generate_stable_two_body():
    """
    Stable two-body system: Sun + Earth in circular orbit
    Returns:
        bodies (list of Body): [sun, earth]
        metadata (dict)
    """
    # Sun at origin, stationary
    sun = Body(SUN_MASS, position=[0.0, 0.0], velocity=[0.0, 0.0])
    
    # Earth at 1 AU, circular velocity
    r = AU
n    v = np.sqrt(G * SUN_MASS / r)
    earth = Body(
        EARTH_MASS,
        position=[r, 0.0],
        velocity=[0.0, v]
    )

    bodies = [sun, earth]
    metadata = {
        "scenario": "stable_two_body",
        "num_planets": 1,
        "stability": "stable",
        "resonance_ratio": None
    }
    return bodies, metadata


def generate_unstable_three_body():
    """
    Unstable three-body system: Sun + two Earth-mass planets + one rogue body
    """
    sun = Body(SUN_MASS, position=[0.0, 0.0], velocity=[0.0, 0.0])
    
    # Two planets in opposite circular orbits
    r = AU
    v = np.sqrt(G * SUN_MASS / r)
    planet1 = Body(EARTH_MASS, position=[ r, 0.0], velocity=[0.0,  v])
    planet2 = Body(EARTH_MASS, position=[-r, 0.0], velocity=[0.0, -v])
    
    # Rogue body at 1.5 AU with slight deviation
    r3 = 1.5 * AU
    v3 = np.sqrt(G * SUN_MASS / r3) * 0.8
    rogue = Body(EARTH_MASS, position=[0.0,  r3], velocity=[-v3, 0.0])

    bodies = [sun, planet1, planet2, rogue]
    metadata = {
        "scenario": "unstable_three_body",
        "num_planets": 3,
        "stability": "unstable",
        "resonance_ratio": None
    }
    return bodies, metadata


def generate_resonant_two_planet():
    """
    Resonant two-planet system: Earth-like inner planet + outer planet in 2:1 period resonance
    """
    sun = Body(SUN_MASS, position=[0.0, 0.0], velocity=[0.0, 0.0])
    
    # Inner planet at 1 AU
    a1 = AU
    v1 = np.sqrt(G * SUN_MASS / a1)
    planet1 = Body(EARTH_MASS, position=[a1, 0.0], velocity=[0.0, v1])
    
    # Outer planet: a2 such that P2/P1 = 2 --> a2 = a1 * 2^(2/3)
    a2 = a1 * 2**(2/3)
    v2 = np.sqrt(G * SUN_MASS / a2)
    planet2 = Body(MARS_MASS, position=[a2, 0.0], velocity=[0.0, v2])
    
    bodies = [sun, planet1, planet2]
    metadata = {
        "scenario": "resonant_two_planet",
        "num_planets": 2,
        "stability": "marginal",
        "resonance_ratio": "2:1"
    }
    return bodies, metadata


def generate_all_scenarios():
    """
    Return a list of (bodies, metadata) tuples for all predefined scenarios
    """
    return [
        generate_stable_two_body(),
        generate_unstable_three_body(),
        generate_resonant_two_planet(),
    ]


if __name__ == "__main__":
    # Example usage
    for bodies, metadata in generate_all_scenarios():
        print(f"Loaded scenario: {metadata['scenario']} with {metadata['num_planets']} planets, stability={metadata['stability']}")
