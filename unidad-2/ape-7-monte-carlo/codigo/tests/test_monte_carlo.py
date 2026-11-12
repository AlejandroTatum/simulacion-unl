"""Pruebas del generador, de los dos experimentos Monte Carlo y de la igualdad entre Python y Java."""

import math
import shutil
from itertools import product

import pytest

from simulacion_ape.model.config import DEFAULT_LCG, DICE, PI, SIZES, LcgConfig
from simulacion_ape.model.experiment import run_python
from simulacion_ape.model.java_runner import compile_java, run_java
from simulacion_ape.model.lcg import Lcg
from simulacion_ape.model.monte_carlo import (
    count_dice_hits,
    count_pi_hits,
    die_face,
    dice_sum_counts,
    dice_sum_probability,
    inside_circle,
)


class FixedUniforms:
    """Generador falso: entrega los uniformes que se le indican, en orden."""

    def __init__(self, values):
        self._values = iter(values)

    def next_uniform(self):
        return next(self._values)


# --- Generador congruencial lineal -------------------------------------------------

def test_lcg_first_states_follow_the_recurrence():
    lcg = Lcg(DEFAULT_LCG)
    # X1 = (1664525 * 12345 + 1013904223) mod 2^32, calculado a mano.
    assert lcg.next_state() == 87628868
    assert lcg.next_state() == (1664525 * 87628868 + 1013904223) % 2**32


def test_lcg_uniform_is_state_divided_by_modulus():
    assert Lcg(DEFAULT_LCG).next_uniform() == 87628868 / 2**32


def test_lcg_uniforms_stay_in_unit_interval():
    lcg = Lcg(LcgConfig("pequeño", a=5, c=3, m=16, seed=7))
    values = [lcg.next_uniform() for _ in range(32)]
    assert all(0.0 <= u < 1.0 for u in values)


def test_same_seed_gives_same_sequence():
    first, second = Lcg(DEFAULT_LCG), Lcg(DEFAULT_LCG)
    assert [first.next_state() for _ in range(100)] == [second.next_state() for _ in range(100)]


# --- Modelo de π ---------------------------------------------------------------------

def test_inside_circle_maps_unit_square_to_centered_square():
    assert inside_circle(0.5, 0.5)       # centro (0, 0)
    assert inside_circle(1.0, 0.5)       # borde (1, 0): la frontera cuenta como dentro
    assert not inside_circle(0.0, 0.0)   # esquina (-1, -1)
    assert not inside_circle(0.99, 0.99)


def test_count_pi_hits_uses_two_uniforms_per_point():
    generator = FixedUniforms([0.5, 0.5, 0.0, 0.0, 0.5, 0.75, 0.99, 0.99])
    assert count_pi_hits(generator, 4) == 2


def test_pi_estimate_is_four_times_the_hit_ratio():
    assert PI.estimate(785, 1000) == pytest.approx(3.14)
    assert PI.exact == math.pi


# --- Modelo de los dados -------------------------------------------------------------

def test_die_face_covers_each_sixth_of_the_interval():
    assert [die_face(k / 6) for k in range(6)] == [1, 2, 3, 4, 5, 6]
    assert die_face(0.0) == 1
    assert die_face(0.999999) == 6
    assert die_face(1 / 6 - 1e-12) == 1


def test_count_dice_hits_counts_only_sums_of_seven():
    # (1,6) suma 7, (1,1) suma 2, (4,3) suma 7, (6,6) suma 12
    generator = FixedUniforms([0.0, 0.9, 0.0, 0.0, 0.6, 0.4, 0.9, 0.9])
    assert count_dice_hits(generator, 4) == 2


def test_dice_exact_probability_matches_the_enumeration_of_the_36_cases():
    favourable = sum(1 for a, b in product(range(1, 7), repeat=2) if a + b == 7)
    assert DICE.exact == favourable / 36 == 1 / 6
    assert DICE.estimate(1667, 10000) == pytest.approx(0.1667)


def test_dice_sum_probability_is_the_triangular_distribution():
    assert [dice_sum_probability(s) * 36 for s in range(2, 13)] == pytest.approx(
        [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])
    assert sum(dice_sum_probability(s) for s in range(2, 13)) == pytest.approx(1.0)


def test_dice_sum_counts_agree_with_the_hit_count():
    counts = dice_sum_counts(Lcg(DEFAULT_LCG), 10_000)
    assert sum(counts.values()) == 10_000
    assert counts[7] == count_dice_hits(Lcg(DEFAULT_LCG), 10_000)


# --- Comportamiento estadístico -----------------------------------------------------

@pytest.mark.parametrize("experiment", [PI, DICE], ids=["pi", "dados"])
def test_error_stays_within_four_standard_errors(experiment):
    for n in (1_000, 10_000, 100_000):
        result = run_python(experiment, DEFAULT_LCG, n, repeats=1)
        assert result.error == abs(experiment.exact - result.estimate)
        assert result.error < 4 * experiment.standard_error(n)


def test_standard_error_shrinks_with_the_square_root_of_n():
    assert PI.standard_error(100) / PI.standard_error(10_000) == pytest.approx(10.0)
    assert DICE.standard_error(36) == pytest.approx(math.sqrt((1 / 6) * (5 / 6) / 36))


def test_sizes_are_the_ones_the_guide_asks_for():
    assert SIZES == (1_000, 10_000, 100_000, 1_000_000)


# --- Python frente a Java ------------------------------------------------------------

@pytest.fixture(scope="module")
def java_build(tmp_path_factory):
    if shutil.which("javac") is None:
        pytest.skip("javac no está instalado")
    build_dir = tmp_path_factory.mktemp("java-build")
    compile_java(build_dir)
    return build_dir


@pytest.mark.parametrize("experiment", [PI, DICE], ids=["pi", "dados"])
def test_java_counts_the_same_hits_as_python(experiment, java_build):
    for n in (1_000, 10_000):
        python = run_python(experiment, DEFAULT_LCG, n, repeats=1)
        java = run_java(experiment, DEFAULT_LCG, n, java_build)
        assert java.hits == python.hits
        assert java.estimate == python.estimate
        assert java.error == python.error
