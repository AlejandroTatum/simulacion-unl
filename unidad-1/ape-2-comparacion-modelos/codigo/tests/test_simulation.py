import numpy as np
import pytest

from simulacion_ape.model.analysis import euler_error, rmse
from simulacion_ape.model.config import DATA
from simulacion_ape.model.estimation import estimate_parameters
from simulacion_ape.model.growth_models import continuous_euler, deterministic, discrete, stochastic
from simulacion_ape.model.simulation import monte_carlo, run_all


def test_parameters_come_from_the_data_array():
    params = estimate_parameters(DATA)
    assert params["P0"] == 1000
    assert params["r"] == pytest.approx(0.1204, abs=1e-4)
    assert params["sigma"] > 0


def test_deterministic_is_exponential():
    t = np.arange(7)
    assert np.allclose(deterministic(1000, 0.1, t), 1000 * np.exp(0.1 * t))


def test_discrete_is_compound_growth():
    assert np.allclose(discrete(1000, 0.1, 6), 1000 * 1.1 ** np.arange(7))


def test_stochastic_without_noise_equals_discrete():
    rng = np.random.default_rng(1)
    assert np.allclose(stochastic(1000, 0.1, 0, 6, rng), discrete(1000, 0.1, 6))


def test_stochastic_is_reproducible_with_the_same_seed():
    a = stochastic(1000, 0.1, 50, 6, np.random.default_rng(42))
    b = stochastic(1000, 0.1, 50, 6, np.random.default_rng(42))
    c = stochastic(1000, 0.1, 50, 6, np.random.default_rng(7))
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)


def test_stochastic_population_never_goes_negative():
    path = stochastic(10, -0.5, 500, 30, np.random.default_rng(3))
    assert path.min() >= 0


def test_euler_with_unit_step_equals_discrete():
    t, p = continuous_euler(1000, 0.1, 6, 1.0)
    assert np.allclose(t, np.arange(7))
    assert np.allclose(p, discrete(1000, 0.1, 6))


def test_euler_error_shrinks_with_smaller_step():
    errors = [euler_error(1000, 0.1204, 6, dt) for dt in (1.0, 0.5, 0.1, 0.01)]
    assert errors == sorted(errors, reverse=True)
    assert errors[-1] < 1


def test_sign_of_r_decides_growth_or_decay():
    t = np.arange(7)
    assert np.all(np.diff(deterministic(1000, 0.1, t)) > 0)
    assert np.all(np.diff(deterministic(1000, -0.1, t)) < 0)
    assert np.allclose(discrete(1000, 0, 6), 1000)


def test_new_decreasing_array_gives_negative_rate():
    params = estimate_parameters(DATA[::-1])
    assert params["P0"] == 2100
    assert params["r"] < 0


def test_run_all_returns_the_four_models_on_the_same_horizon():
    results = run_all(estimate_parameters(DATA), dt=0.1, seed=42)
    assert set(results) == {"Determinístico", "Discreto", "Estocástico", "Continuo (Euler)"}
    for t, p in results.values():
        assert t[0] == 0 and t[-1] == pytest.approx(6)
        assert p[0] == 1000


def test_monte_carlo_band_contains_the_mean():
    band = monte_carlo(1000, 0.1204, 40, 6, runs=200, seed=42)
    assert np.all(band["p5"] <= band["mean"]) and np.all(band["mean"] <= band["p95"])
    assert rmse(band["mean"], discrete(1000, 0.1204, 6)) < 20


def test_entry_point_runs_when_executed_by_file_path(tmp_path):
    # El botón "Run" del editor ejecuta el archivo por ruta, no con python -m.
    import subprocess
    import sys
    from pathlib import Path

    main_file = Path(__file__).resolve().parents[1] / "simulacion_ape" / "__main__.py"
    result = subprocess.run([sys.executable, str(main_file)], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "figuras" / "comparacion_modelos.png").exists()
