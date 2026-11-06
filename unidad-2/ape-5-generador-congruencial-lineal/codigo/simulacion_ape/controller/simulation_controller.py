"""Controlador: genera las secuencias, compara Python con Java, analiza el período y las semillas."""

import argparse
import csv
import shutil
from dataclasses import replace
from pathlib import Path

from ..model.analysis import compare, mismatches, sequence_stats
from ..model.config import ALTERNATIVE_SEEDS, COMPARED_VALUES, LcgConfig
from ..model.java_runner import run_java_lcg
from ..model.lcg import lcg_states, normalize
from ..model.period import find_period, first_repetition, hull_dobell
from ..view import console_view

CODE_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = CODE_DIR / "resultados"
FIGURES_DIR = CODE_DIR / "figuras"

# Módulo pequeño para medir el período recorriendo el ciclo completo (con m = 2^32 no es práctico).
SMALL_CASES = (("a=5, c=3, m=16 (adecuados)", 5, 3, 16), ("a=4, c=2, m=16 (inadecuados)", 4, 2, 16))


def write_sequence_csv(path: Path, states: list[int], m: int) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["n", "X", "U"])
        writer.writerows((i, x, x / m) for i, x in enumerate(states, start=1))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="APE 5: Generador Congruencial Lineal en Python y Java")
    parser.add_argument("--no-figures", action="store_true", help="no genera las gráficas")
    args = parser.parse_args(argv)

    config = LcgConfig()
    python_states = lcg_states(config)
    values = normalize(python_states, config.m)
    RESULTS_DIR.mkdir(exist_ok=True)
    write_sequence_csv(RESULTS_DIR / "secuencia_python.csv", python_states, config.m)
    console_view.show(f"Python: {len(python_states)} valores con a={config.a}, c={config.c}, "
                      f"m={config.m}, semilla={config.seed}")

    if shutil.which("javac") is None:
        console_view.show("Java: JDK no disponible, se omite la comparación")
    else:
        java_states = run_java_lcg(config, RESULTS_DIR / "java-build")
        write_sequence_csv(RESULTS_DIR / "secuencia_java.csv", java_states, config.m)
        rows = compare(python_states, java_states, config.m, COMPARED_VALUES)
        console_view.show(console_view.format_comparison(rows))
        console_view.show(f"Diferencias en los {config.n} valores: {mismatches(python_states, java_states)}")

    small = [(label, hull_dobell(a, c, m), find_period(a, c, m, seed=7), m) for label, a, c, m in SMALL_CASES]
    console_view.show(console_view.format_period(hull_dobell(config.a, config.c, config.m), config.m,
                                                 first_repetition(python_states), config.n, small))

    seed_sequences = {config.seed: values}
    for seed in ALTERNATIVE_SEEDS:
        alt = replace(config, seed=seed)
        seed_sequences[seed] = normalize(lcg_states(alt), alt.m)
    stats = [sequence_stats(seed, seq) for seed, seq in seed_sequences.items()]
    console_view.show(console_view.format_seeds(stats))

    if not args.no_figures:
        from ..view import figures

        FIGURES_DIR.mkdir(exist_ok=True)
        figures.plot_sequence(values, FIGURES_DIR / "secuencia.png")
        figures.plot_pairs_and_histogram(values, FIGURES_DIR / "pares-histograma.png")
        figures.plot_seeds(seed_sequences, FIGURES_DIR / "semillas.png")
        console_view.show(f"Figuras guardadas en {FIGURES_DIR}")
