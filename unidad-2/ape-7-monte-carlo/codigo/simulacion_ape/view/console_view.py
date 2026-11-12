"""Vista de consola: imprime las tablas de resultados."""

from ..model.experiment import Row
from ..model.lcg import LcgConfig


def show_header(config: LcgConfig) -> None:
    print("APE 7: método de Monte Carlo")
    print(f"Generador: {config.name}  a={config.a}  c={config.c}  m={config.m}  semilla={config.seed}")


def show_rows(rows: list[Row]) -> None:
    experiment = rows[0].experiment
    print(f"\n{experiment.label}   valor real = {experiment.exact:.10f}")
    print(f"{'N':>9}  {'aciertos':>8}  {'estimación':>12}  {'error abs.':>10}  {'error est.':>10}  "
          f"{'t Python (s)':>12}  {'t Java (s)':>10}  {'Py/Java':>7}  igual")
    for row in rows:
        py, java = row.python, row.java
        print(f"{row.n:>9,}  {py.hits:>8}  {py.estimate:>12.8f}  {py.error:>10.6f}  "
              f"{experiment.standard_error(row.n):>10.6f}  {py.seconds:>12.6f}  {java.seconds:>10.6f}  "
              f"{py.seconds / java.seconds:>7.1f}  {'sí' if row.same_result else 'NO'}")


def show_dice_sums(counts: dict[int, int], probability) -> None:
    n = sum(counts.values())
    print(f"\nDistribución de la suma de dos dados (N = {n:,})")
    print(f"{'suma':>4}  {'veces':>8}  {'frecuencia':>10}  {'exacta':>8}")
    for total, count in counts.items():
        print(f"{total:>4}  {count:>8}  {count / n:>10.5f}  {probability(total):>8.5f}")


def show_outputs(results_dir, figures_dir) -> None:
    if figures_dir is not None:
        print(f"\nFiguras en {figures_dir}")
    print(f"CSV en {results_dir}")
