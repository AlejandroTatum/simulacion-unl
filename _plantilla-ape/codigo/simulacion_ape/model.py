"""Entities and rules of the simulated system.

Example model: a fair die roll. Replace with the practice's system.
"""

import random


def roll_die(rng: random.Random) -> int:
    return rng.randint(1, 6)
