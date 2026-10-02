"""Statistics computed from simulation outcomes."""

from dataclasses import dataclass
from statistics import mean, stdev


@dataclass(frozen=True)
class Summary:
    mean: float
    std_dev: float
    samples: int


def summarize(outcomes: list[int]) -> Summary:
    return Summary(mean=mean(outcomes), std_dev=stdev(outcomes), samples=len(outcomes))
