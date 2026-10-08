"""Los cuatro modelos de crecimiento poblacional de la guía."""

import numpy as np


def deterministic(p0, r, t):
    """Modelo determinístico: P(t) = P0 · e^(r·t), sin aleatoriedad."""
    return p0 * np.exp(r * np.asarray(t, dtype=float))


def discrete(p0, r, periods):
    """Modelo discreto: P(n+1) = P(n) + r · P(n), la población cambia período a período."""
    population = [float(p0)]
    for _ in range(periods):
        population.append(population[-1] + r * population[-1])
    return np.array(population)


def stochastic(p0, r, sigma, periods, rng):
    """Modelo estocástico: el discreto más un ruido ε ~ N(0, σ); la población no baja de 0."""
    population = [float(p0)]
    for _ in range(periods):
        current = population[-1]
        noise = rng.normal(0, sigma)
        population.append(max(current + r * current + noise, 0.0))
    return np.array(population)


def continuous_euler(p0, r, horizon, dt):
    """Modelo continuo dP/dt = r · P aproximado con Euler: P ← P + dt · r · P."""
    steps = int(round(horizon / dt))
    t = np.linspace(0, steps * dt, steps + 1)
    population = [float(p0)]
    for _ in range(steps):
        population.append(population[-1] + dt * r * population[-1])
    return t, np.array(population)
