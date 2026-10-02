"""Mathematical model: temperature factor, rain index and state rules."""

import numpy as np

from .config import DEFAULT_STATE, STATES, WEIGHTS


def tf_continuous(temp):
    """Adjusted model: the guide's table is the line Tf = 1 - 0.05(T - 10), bounded to [0.1, 1]."""
    return np.round(np.clip(1 - 0.05 * (np.asarray(temp) - 10), 0.1, 1.0), 4)


def tf_table(temp):
    """Base model: uses the table row at or below T (rows every 2 °C from 10 °C)."""
    return tf_continuous(10 + 2 * np.floor((np.asarray(temp) - 10) / 2))


def rain_index(h, n, tf):
    """I = 0.5H + 0.3N + 0.2Tf, rounded so values like 0.60 are not read as 0.5999."""
    w_h, w_n, w_tf = WEIGHTS
    return np.round(w_h * h + w_n * n + w_tf * tf, 4)


def classify(index):
    """Maps each index value to its state using the guide's rule table."""
    index = np.asarray(index)
    conditions = [index >= bound for bound, _ in STATES]
    return np.select(conditions, [state for _, state in STATES], default=DEFAULT_STATE)
