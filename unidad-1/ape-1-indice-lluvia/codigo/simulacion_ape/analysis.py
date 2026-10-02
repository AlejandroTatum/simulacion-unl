"""Comparación entre el modelo base y el modelo ajustado."""

import numpy as np

from .config import HOURS


def rainy_hours(result):
    """Horas cuyo estado es al menos 'Lluvia probable'."""
    return [hour for hour, i in zip(HOURS, result["index"]) if i >= 0.60]


def compare(base, adjusted):
    diff = np.round(adjusted["index"] - base["index"], 4)
    changed = [h for h, b, a in zip(HOURS, base["state"], adjusted["state"]) if b != a]
    return {"max_abs_diff": float(np.abs(diff).max()), "changed_states": changed}
