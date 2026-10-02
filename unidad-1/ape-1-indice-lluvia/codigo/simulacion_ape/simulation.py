"""Runs the model over the day's readings with a given temperature-factor rule."""

from .config import CLOUDINESS, HUMIDITY, TEMPERATURE
from .model import classify, rain_index


def run(tf_rule):
    h, n = HUMIDITY / 100, CLOUDINESS / 100
    tf = tf_rule(TEMPERATURE)
    index = rain_index(h, n, tf)
    return {"H": h, "N": n, "Tf": tf, "index": index, "state": classify(index)}
