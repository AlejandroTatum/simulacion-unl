"""Pruebas del método de aceptación-rechazo y de los dos puntos de entrada (Python y Java)."""

import csv
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from simulacion_ape.model.acceptance_rejection import accepts, acceptance_rejection
from simulacion_ape.model.config import SimulationConfig
from simulacion_ape.model.distributions import LINEAR, QUADRATIC, TARGETS
from simulacion_ape.model.simulation import run

CODE_DIR = Path(__file__).resolve().parents[1]
N = 10_000


# --- Criterio de aceptación ----------------------------------------------------------

def test_candidate_is_accepted_when_u_equals_r():
    assert accepts(0.5, 0.5)


def test_candidate_is_accepted_below_and_rejected_above_r():
    assert accepts(0.49, 0.5)
    assert not accepts(0.51, 0.5)


@pytest.mark.parametrize("target, x, ratio", [(LINEAR, 0.3, 0.3), (QUADRATIC, 0.5, 0.25)])
def test_ratio_matches_the_guide_criterion(target, x, ratio):
    # R = f(X) / (M·g(X)): para 2x es X y para 3x² es X².
    assert target.ratio(x) == pytest.approx(ratio)


@pytest.mark.parametrize("target, efficiency", [(LINEAR, 50.0), (QUADRATIC, 100 / 3)])
def test_theoretical_efficiency_is_one_over_m(target, efficiency):
    assert target.theoretical_efficiency == pytest.approx(efficiency)


# --- Muestras con semilla fija ------------------------------------------------------

@pytest.mark.parametrize("target", TARGETS)
@pytest.mark.parametrize("n", [1_000, 5_000, N])
def test_accepted_plus_rejected_is_n(target, n):
    result = acceptance_rejection(target, n, 42)
    assert result.n_accepted + result.n_rejected == n
    assert len(result.candidates) == len(result.uniforms) == n
    assert len(result.accepted_values) == result.n_accepted


@pytest.mark.parametrize("target", TARGETS)
def test_efficiency_is_close_to_theory(target):
    result = acceptance_rejection(target, N, 42)
    assert result.efficiency == pytest.approx(result.n_accepted / N * 100)
    assert abs(result.efficiency - target.theoretical_efficiency) < 2.0


@pytest.mark.parametrize("target", TARGETS)
def test_accepted_values_lie_in_unit_interval(target):
    values = acceptance_rejection(target, N, 42).accepted_values
    assert np.all((values >= 0) & (values <= 1))


@pytest.mark.parametrize("target, mean", [(LINEAR, 2 / 3), (QUADRATIC, 3 / 4)])
def test_accepted_sample_mean_matches_target(target, mean):
    values = acceptance_rejection(target, N, 42).accepted_values
    assert float(np.mean(values)) == pytest.approx(mean, abs=0.015)


def test_same_seed_reproduces_the_result():
    first, second = acceptance_rejection(LINEAR, 1_000, 7), acceptance_rejection(LINEAR, 1_000, 7)
    assert np.array_equal(first.accepted_values, second.accepted_values)
    assert first.n_accepted == second.n_accepted


def test_different_seed_changes_the_result():
    first, second = acceptance_rejection(LINEAR, 1_000, 1), acceptance_rejection(LINEAR, 1_000, 2)
    assert not np.array_equal(first.candidates, second.candidates)


def test_run_produces_one_row_per_target_and_n():
    rows = run(SimulationConfig()).rows
    assert [(row.target.label, row.n) for row in rows] == [
        (target.label, n) for target in TARGETS for n in (1_000, 5_000, N)]
    for row in rows:
        assert row.absolute_error == pytest.approx(abs(row.efficiency - row.target.theoretical_efficiency))


# --- Puntos de entrada ---------------------------------------------------------------

def test_entry_point_runs_when_executed_by_file_path(tmp_path):
    # El botón "Run" del editor ejecuta el archivo por ruta, no con python -m.
    main_file = CODE_DIR / "simulacion_ape" / "__main__.py"
    result = subprocess.run([sys.executable, str(main_file), "--no-figures"], cwd=tmp_path,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "f(x)=3x²" in result.stdout


def test_java_writes_the_efficiency_table(tmp_path):
    if shutil.which("javac") is None:
        pytest.skip("javac no está instalado")
    sources = sorted(str(path) for path in (CODE_DIR / "java").rglob("*.java"))
    build_dir = tmp_path / "build"
    # Se ejecuta desde codigo/ para que mise.toml elija el JDK.
    subprocess.run(["javac", "-d", str(build_dir), *sources], check=True, cwd=CODE_DIR)
    result = subprocess.run(["java", "-cp", str(build_dir), "ape9.Main", "42", str(tmp_path)],
                            capture_output=True, text=True, cwd=CODE_DIR)
    assert result.returncode == 0, result.stderr
    with (tmp_path / "eficiencia-java.csv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [(row["distribución"], int(row["N"])) for row in rows] == [
        (target.label, n) for target in TARGETS for n in (1_000, 5_000, N)]
    for row in rows:
        assert int(row["aceptados"]) + int(row["rechazados"]) == int(row["N"])
        assert float(row["error_absoluto"]) < 3.0
