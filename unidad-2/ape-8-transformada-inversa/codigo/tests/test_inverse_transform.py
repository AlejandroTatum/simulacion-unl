"""Pruebas de la transformada inversa, de las estadísticas y de los dos puntos de entrada (Python y Java)."""

import csv
import math
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from simulacion_ape.model.analysis import compare_exponential, compare_uniform, percent_error
from simulacion_ape.model.config import SimulationConfig
from simulacion_ape.model.inverse_transform import exponential_density, generate_uniforms, inverse_exponential
from simulacion_ape.model.simulation import run

CODE_DIR = Path(__file__).resolve().parents[1]
RATES = (0.5, 1.0, 2.0)


# --- Fórmula de la transformada inversa ---------------------------------------------

@pytest.mark.parametrize("rate", RATES)
def test_inverse_of_zero_is_zero(rate):
    assert inverse_exponential(0.0, rate) == 0.0


@pytest.mark.parametrize("rate", RATES)
def test_inverse_of_one_minus_e_inverse_is_the_mean(rate):
    # F(1/λ) = 1 - e^(-1), por eso X(1 - e^(-1)) = 1/λ.
    assert inverse_exponential(1 - math.exp(-1), rate) == pytest.approx(1 / rate)


@pytest.mark.parametrize("u", [0.1, 0.5, 0.9])
def test_inverse_undoes_the_cumulative_distribution(u):
    rate = 0.5
    x = inverse_exponential(u, rate)
    assert 1 - math.exp(-rate * x) == pytest.approx(u)


@pytest.mark.parametrize("rate", [0.0, -1.0])
def test_non_positive_rate_is_rejected(rate):
    with pytest.raises(ValueError):
        inverse_exponential(0.5, rate)
    with pytest.raises(ValueError):
        exponential_density(1.0, rate)
    with pytest.raises(ValueError):
        compare_exponential(np.array([1.0, 2.0]), rate)


def test_density_is_lambda_at_zero_and_zero_for_negative_x():
    assert exponential_density(0.0, 2.0) == pytest.approx(2.0)
    assert exponential_density(-1.0, 2.0) == 0.0


def test_percent_error():
    assert percent_error(2.1, 2.0) == pytest.approx(5.0)


# --- Muestras de N = 10 000 con semilla fija ---------------------------------------

def test_uniforms_are_in_unit_interval_with_expected_mean_and_variance():
    u = generate_uniforms(10_000, 42)
    assert len(u) == 10_000
    assert np.all((u >= 0) & (u < 1))
    stats = compare_uniform(u)
    assert stats.experimental_mean == pytest.approx(0.5, abs=0.01)
    assert stats.experimental_variance == pytest.approx(1 / 12, abs=0.003)


@pytest.mark.parametrize("rate", RATES)
def test_exponential_sample_mean_and_variance_match_theory(rate):
    stats = run(SimulationConfig(seed=42)).stats[rate]
    assert stats.theoretical_mean == pytest.approx(1 / rate)
    assert stats.theoretical_variance == pytest.approx(1 / rate**2)
    assert stats.mean_error_pct < 3.0
    assert stats.variance_error_pct < 6.0


def test_same_seed_reproduces_the_sample():
    first, second = run(SimulationConfig(seed=7)), run(SimulationConfig(seed=7))
    for rate in RATES:
        assert np.array_equal(first.samples[rate], second.samples[rate])


def test_different_seed_changes_the_sample():
    assert not np.array_equal(generate_uniforms(100, 1), generate_uniforms(100, 2))


# --- Puntos de entrada ---------------------------------------------------------------

def test_entry_point_runs_when_executed_by_file_path(tmp_path):
    # El botón "Run" del editor ejecuta el archivo por ruta, no con python -m.
    main_file = CODE_DIR / "simulacion_ape" / "__main__.py"
    result = subprocess.run([sys.executable, str(main_file), "--no-figures"], cwd=tmp_path,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "cantidad de datos generados: 10000" in result.stdout


def test_java_writes_the_comparison_table(tmp_path):
    if shutil.which("javac") is None:
        pytest.skip("javac no está instalado")
    sources = sorted(str(path) for path in (CODE_DIR / "java").rglob("*.java"))
    build_dir = tmp_path / "build"
    # Se ejecuta desde codigo/ para que mise.toml elija el JDK.
    subprocess.run(["javac", "-d", str(build_dir), *sources], check=True, cwd=CODE_DIR)
    result = subprocess.run(["java", "-cp", str(build_dir), "ape8.Main", "42", "10000", str(tmp_path)],
                            capture_output=True, text=True, cwd=CODE_DIR)
    assert result.returncode == 0, result.stderr
    assert "cantidad de datos generados: 10000" in result.stdout
    with (tmp_path / "tabla-lambda-java.csv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [float(row["lambda"]) for row in rows] == list(RATES)
    for row in rows:
        assert float(row["error_media_pct"]) < 3.0
        assert float(row["error_varianza_pct"]) < 6.0
