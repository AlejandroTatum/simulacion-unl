"""Aplica el modelo a las lecturas del día con la regla de Tf y los pesos indicados."""

from .config import CLOUDINESS, HUMIDITY, TEMPERATURE, WEIGHTS
from .model import classify, rain_index


def run(tf_rule, weights=WEIGHTS):
    h, n = HUMIDITY / 100, CLOUDINESS / 100
    tf = tf_rule(TEMPERATURE)
    index = rain_index(h, n, tf, weights)
    return {"H": h, "N": n, "Tf": tf, "index": index, "state": classify(index)}
