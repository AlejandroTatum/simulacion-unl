"""Entidades y reglas del sistema simulado.

Modelo de ejemplo: lanzamiento de un dado justo. Reemplazar por el sistema de la práctica.
"""

import random


def roll_die(rng: random.Random) -> int:
    return rng.randint(1, 6)
