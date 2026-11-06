"""Pruebas del generador, de Chi-cuadrado, de K-S y de la equivalencia Python-Java."""

import shutil

import pytest
from scipy import stats

from simulacion_ape.model.config import CONFIGS, GLIBC, N, RANDU, SMALL_MODULUS
from simulacion_ape.model.distributions import chi_square_sf, kolmogorov_sf
from simulacion_ape.model.experiment import max_statistic_difference, run_python, run_row, sequence_mismatches
from simulacion_ape.model.java_runner import compile_java
from simulacion_ape.model.lcg import generate, lcg_states
from simulacion_ape.model.uniformity import chi_square_test, decision, ks_test, rejects_h0

needs_java = pytest.mark.skipif(shutil.which("javac") is None, reason="se necesita un JDK")


@pytest.fixture(scope="module")
def build_dir(tmp_path_factory):
    path = tmp_path_factory.mktemp("java-build")
    compile_java(path)
    return path


def test_first_state_by_hand():
    # X1 = (1103515245 · 1 + 12345) mod 2^32 = 1103527590
    assert lcg_states(GLIBC, 1) == [1_103_527_590]


def test_values_are_in_unit_interval():
    values = generate(GLIBC, N)
    assert len(values) == N
    assert all(0 <= u < 1 for u in values)


def test_chi_square_by_hand():
    # 10 valores: 3 en [0, 0.1), 1 en cada uno de [0.1, 0.8) y ninguno en [0.8, 1). E = 1.
    values = [0.01, 0.02, 0.03, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75]
    result = chi_square_test(values)
    assert result.observed == [3, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    assert result.expected == 1
    assert result.statistic == pytest.approx(4 + 0 * 7 + 1 + 1)  # (3-1)² + 2 · (0-1)²
    assert result.df == 9


@pytest.mark.parametrize("statistic", [0.5, 2.44, 9.0, 16.92, 30.0, 120.0])
def test_chi_square_p_value_matches_scipy(statistic):
    assert chi_square_sf(statistic, 9) == pytest.approx(stats.chi2.sf(statistic, 9), abs=1e-12)


def test_critical_value_gives_alpha():
    assert chi_square_sf(stats.chi2.ppf(0.95, 9), 9) == pytest.approx(0.05, abs=1e-12)


def test_ks_by_hand():
    # D+ = máx(1/3 - 0.1, 2/3 - 0.4, 1 - 0.7) = 0.3; D- = máx(0.1, 0.4 - 1/3, 0.7 - 2/3) = 0.1
    result = ks_test([0.7, 0.1, 0.4])
    assert result.d_plus == pytest.approx(0.3)
    assert result.d_minus == pytest.approx(0.1)
    assert result.statistic == pytest.approx(0.3)


def test_ks_matches_scipy():
    values = generate(GLIBC, N)
    expected = stats.kstest(values, "uniform", method="exact")
    result = ks_test(values)
    assert result.statistic == pytest.approx(expected.statistic, abs=1e-15)
    assert result.p_value == pytest.approx(expected.pvalue, abs=0.01)


def test_ks_p_value_is_one_for_tiny_d():
    assert kolmogorov_sf(N, 0.0) == 1.0


@pytest.mark.parametrize("p_value, rejected", [(0.05, False), (0.2, False), (0.0499, True), (0.0, True)])
def test_decision_rule(p_value, rejected):
    assert rejects_h0(p_value) is rejected
    assert decision(p_value) == ("Se rechaza H0" if rejected else "No se rechaza H0")


def test_good_generators_pass_and_small_modulus_fails():
    for config in (GLIBC, RANDU):
        run = run_python(config, N, repeats=1)
        assert not rejects_h0(run.chi.p_value) and not rejects_h0(run.ks.p_value)
    small = run_python(SMALL_MODULUS, N, repeats=1)
    assert rejects_h0(small.chi.p_value) and rejects_h0(small.ks.p_value)


@needs_java
@pytest.mark.parametrize("config", CONFIGS, ids=lambda c: c.name)
def test_java_produces_the_same_sequence(config, build_dir):
    assert sequence_mismatches(config, N, build_dir) == 0


@needs_java
@pytest.mark.parametrize("config", CONFIGS, ids=lambda c: c.name)
def test_java_computes_the_same_statistics(config, build_dir):
    row = run_row(config, N, build_dir)
    assert row.java.observed == row.python.chi.observed
    assert row.java.df == row.python.chi.df
    assert max_statistic_difference(row) < 1e-12
