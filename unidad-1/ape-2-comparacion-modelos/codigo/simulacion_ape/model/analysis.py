"""Medidas para comparar los modelos con los datos y entre sí."""

import numpy as np

from .growth_models import continuous_euler, deterministic


def rmse(predicted, observed):
    """Raíz del error cuadrático medio entre dos series del mismo tamaño."""
    return float(np.sqrt(np.mean((np.asarray(predicted) - np.asarray(observed)) ** 2)))


def at_periods(t, population, periods):
    """Toma los valores de una serie en los instantes enteros 0, 1, ..., periods."""
    return np.interp(np.arange(periods + 1), t, population)


def fit_table(results, data):
    """Valor de cada modelo en cada período y su error frente a los datos observados."""
    periods = len(data) - 1
    table = {}
    for name, (t, population) in results.items():
        values = at_periods(t, population, periods)
        table[name] = {"values": values, "rmse": rmse(values, data)}
    return table


def euler_error(p0, r, horizon, dt):
    """Error absoluto de Euler al final del horizonte frente a la solución exacta P0 · e^(r·t)."""
    _, population = continuous_euler(p0, r, horizon, dt)
    return float(abs(population[-1] - deterministic(p0, r, horizon)))
