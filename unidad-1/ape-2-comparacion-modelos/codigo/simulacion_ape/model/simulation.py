"""Ejecuta los cuatro modelos con los mismos parámetros y las corridas de Monte Carlo."""

import numpy as np

from .growth_models import continuous_euler, deterministic, discrete, stochastic


def run_all(params, dt, seed):
    """Devuelve {nombre: (tiempo, población)} de los cuatro modelos sobre el mismo horizonte."""
    p0, r, sigma, periods = params["P0"], params["r"], params["sigma"], params["periods"]
    t_fine = np.linspace(0, periods, periods * 50 + 1)
    t_periods = np.arange(periods + 1)
    rng = np.random.default_rng(seed)
    return {
        "Determinístico": (t_fine, deterministic(p0, r, t_fine)),
        "Discreto": (t_periods, discrete(p0, r, periods)),
        "Estocástico": (t_periods, stochastic(p0, r, sigma, periods, rng)),
        "Continuo (Euler)": continuous_euler(p0, r, periods, dt),
    }


def monte_carlo(p0, r, sigma, periods, runs, seed):
    """Repite el modelo estocástico y resume las corridas con la media y la banda del 5 % al 95 %."""
    rng = np.random.default_rng(seed)
    paths = np.array([stochastic(p0, r, sigma, periods, rng) for _ in range(runs)])
    return {
        "paths": paths,
        "mean": paths.mean(axis=0),
        "p5": np.percentile(paths, 5, axis=0),
        "p95": np.percentile(paths, 95, axis=0),
    }
