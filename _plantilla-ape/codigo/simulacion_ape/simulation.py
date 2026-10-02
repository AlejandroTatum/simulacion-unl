"""Simulation engine: runs the model a configured number of times."""

import random

from .config import SimulationConfig
from .model import roll_die


def run(config: SimulationConfig) -> list[int]:
    rng = random.Random(config.seed)
    return [roll_die(rng) for _ in range(config.runs)]
