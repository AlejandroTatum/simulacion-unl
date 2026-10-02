"""Modelo matemático: factor de temperatura, índice de lluvia y reglas de estado."""

import numpy as np

from .config import DEFAULT_STATE, STATES, WEIGHTS


def tf_continuous(temp):
    """Modelo ajustado: la tabla de la guía es la recta Tf = 1 - 0.05(T - 10), acotada a [0.1, 1]."""
    return np.round(np.clip(1 - 0.05 * (np.asarray(temp) - 10), 0.1, 1.0), 4)


def tf_table(temp):
    """Modelo base: usa la fila de la tabla igual o inferior a T (filas cada 2 °C desde 10 °C)."""
    return tf_continuous(10 + 2 * np.floor((np.asarray(temp) - 10) / 2))


def rain_index(h, n, tf):
    """I = 0.5H + 0.3N + 0.2Tf, redondeado para que valores como 0.60 no se lean como 0.5999."""
    w_h, w_n, w_tf = WEIGHTS
    return np.round(w_h * h + w_n * n + w_tf * tf, 4)


def classify(index):
    """Asigna a cada valor del índice su estado según la tabla de reglas de la guía."""
    index = np.asarray(index)
    conditions = [index >= bound for bound, _ in STATES]
    return np.select(conditions, [state for _, state in STATES], default=DEFAULT_STATE)
