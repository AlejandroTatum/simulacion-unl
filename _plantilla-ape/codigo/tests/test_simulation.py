from simulacion_ape.analysis import summarize
from simulacion_ape.config import SimulationConfig
from simulacion_ape.simulation import run


def test_same_seed_reproduces_results():
    config = SimulationConfig(runs=100, seed=7)
    assert run(config) == run(config)


def test_mean_converges_to_expected_value():
    summary = summarize(run(SimulationConfig(runs=20_000, seed=1)))
    assert abs(summary.mean - 3.5) < 0.05
