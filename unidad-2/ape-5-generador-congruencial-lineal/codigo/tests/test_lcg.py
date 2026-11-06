import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from simulacion_ape.model.config import LcgConfig
from simulacion_ape.model.java_runner import run_java_lcg
from simulacion_ape.model.lcg import lcg_states, normalize
from simulacion_ape.model.period import find_period, hull_dobell


def test_first_state_matches_hand_computation():
    # X1 = (1664525 · 12345 + 1013904223) mod 2^32 = 87628868
    assert lcg_states(LcgConfig(n=1))[0] == 87_628_868


def test_same_seed_reproduces_the_sequence():
    config = LcgConfig(n=500)
    assert lcg_states(config) == lcg_states(config)


def test_different_seed_changes_the_sequence():
    assert lcg_states(LcgConfig(n=20)) != lcg_states(LcgConfig(n=20, seed=54321))


def test_normalized_values_are_in_unit_interval():
    config = LcgConfig(n=10_000)
    values = normalize(lcg_states(config), config.m)
    assert len(values) == 10_000
    assert all(0.0 <= u < 1.0 for u in values)


def test_guide_parameters_satisfy_hull_dobell():
    conditions = hull_dobell(1_664_525, 1_013_904_223, 2**32)
    assert all(conditions.values())


def test_full_period_when_hull_dobell_holds_on_small_modulus():
    assert all(hull_dobell(5, 3, 16).values())
    assert find_period(5, 3, 16, seed=7) == 16


def test_short_period_with_inadequate_parameters():
    assert not all(hull_dobell(4, 2, 16).values())
    assert find_period(4, 2, 16, seed=7) < 16


@pytest.mark.skipif(shutil.which("javac") is None, reason="JDK no disponible")
def test_java_produces_the_same_sequence_as_python(tmp_path):
    config = LcgConfig(n=1_000)
    assert run_java_lcg(config, tmp_path) == lcg_states(config)


def test_entry_point_runs_when_executed_by_file_path(tmp_path):
    # El botón "Run" del editor ejecuta el archivo por ruta, no con python -m.
    main_file = Path(__file__).resolve().parents[1] / "simulacion_ape" / "__main__.py"
    result = subprocess.run([sys.executable, str(main_file), "--no-figures"], cwd=tmp_path,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "Período" in result.stdout
