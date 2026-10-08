"""Obtiene P0, r y sigma a partir del arreglo de datos."""

import numpy as np


def estimate_parameters(data):
    """P0 es el primer dato; r ajusta ln(P/P0) = r·t por mínimos cuadrados; sigma es la
    desviación estándar de lo que el modelo discreto no explica en cada período."""
    data = np.asarray(data, dtype=float)
    t = np.arange(len(data))
    p0 = data[0]
    r = np.sum(t * np.log(data / p0)) / np.sum(t * t)
    residuals = data[1:] - (data[:-1] + r * data[:-1])
    return {"P0": p0, "r": float(r), "sigma": float(np.std(residuals, ddof=1)), "periods": len(data) - 1}
