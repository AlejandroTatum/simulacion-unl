"""Simulation parameters, kept apart from the logic that uses them."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationConfig:
    runs: int = 10_000
    seed: int = 42
