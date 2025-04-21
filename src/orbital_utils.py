import numpy as np

def kepler_E(M, e, tol=1e-10):
    """
    Solve Kepler’s equation M = E - e sin E for the eccentric anomaly E.
    """
    # Initial guess
    E = M if e < 0.8 else np.pi
    for _ in range(100):
        f = E - e * np.sin(E) - M
        fp = 1 - e * np.cos(E)
        dE = f / fp
        E -= dE
        if abs(dE) < tol:
            break
    return E

def orbital_elements_to_state_vectors(a, e, i, raan, argp, M, mu):
    """
    Convert classical orbital elements to ECI position & velocity vectors.

    Parameters
    ----------
    a     : semi-major axis [m]
    e     : eccentricity
    i     : inclination [rad]
    raan  : longitude of ascending node [rad]
    argp  : argument of periapsis [rad]
    M     : mean anomaly at epoch [rad]
    mu    : G*(M_star + m_planet) [m^3 / s^2]

    Returns
    -------
    r_eci : np.array([x, y, z]) position vector in inertial frame
    v_eci : np.array([vx, vy, vz]) velocity vector in inertial frame
    """
    # 1) Solve for eccentric anomaly E
    E = kepler_E(M, e)

    # 2) Compute position in the orbital plane
    x_op = a * (np.cos(E) - e)
    y_op = a * np.sqrt(1 - e**2) * np.sin(E)
    r = np.hypot(x_op, y_op)

    # 3) Compute velocity in the orbital plane
    #    vis‑viva / geometry gives:
    vx_op = - (np.sqrt(mu * a) / r) * np.sin(E)
    vy_op =   (np.sqrt(mu * a * (1 - e**2)) / r) * np.cos(E)

    # 4) Build rotation matrices
    cos_Ω, sin_Ω = np.cos(raan), np.sin(raan)
    cos_i, sin_i = np.cos(i),    np.sin(i)
    cos_ω, sin_ω = np.cos(argp), np.sin(argp)

    # R = R3(Ω) · R1(i) · R3(ω)
    R3_Ω = np.array([[ cos_Ω, -sin_Ω, 0],
                     [ sin_Ω,  cos_Ω, 0],
                     [     0,      0, 1]])
    R1_i = np.array([[1,     0,      0],
                     [0,  cos_i, -sin_i],
                     [0,  sin_i,  cos_i]])
    R3_ω = np.array([[ cos_ω, -sin_ω, 0],
                     [ sin_ω,  cos_ω, 0],
                     [     0,      0, 1]])
    R = R3_Ω @ R1_i @ R3_ω

    # 5) Rotate into inertial frame
    r_eci = R @ np.array([x_op, y_op, 0.0])
    v_eci = R @ np.array([vx_op, vy_op, 0.0])
    return r_eci, v_eci
