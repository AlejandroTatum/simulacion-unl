"""Motor de simulación: ejecuta el modelo el número de veces configurado."""

import random

from .config import SimulationConfig
from .dice import roll_die


def run(config: SimulationConfig) -> list[int]:
    rng = random.Random(config.seed)
    return [roll_die(rng) for _ in range(config.runs)]
