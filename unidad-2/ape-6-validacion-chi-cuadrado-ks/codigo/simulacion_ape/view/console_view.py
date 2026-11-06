"""Tablas de consola: solo presenta resultados ya calculados."""

from ..model.experiment import Row, max_statistic_difference
from ..model.uniformity import decision


def show_frequencies(row: Row) -> None:
    chi = row.python.chi
    print(f"\nFrecuencias ({row.config.name}, N = {row.n}, E = {chi.expected:g} por intervalo)")
    print(f"{'Intervalo':<14}{'O Python':>10}{'O Java':>10}{'(O-E)²/E':>12}")
    for i, (o_py, o_java) in enumerate(zip(chi.observed, row.java.observed)):
        lower, upper = i / len(chi.observed), (i + 1) / len(chi.observed)
        contribution = (o_py - chi.expected) ** 2 / chi.expected
        print(f"[{lower:.1f}, {upper:.1f}){'':<4}{o_py:>10}{o_java:>10}{contribution:>12.4f}")
    print(f"χ² = {chi.statistic:.4f}, gl = {chi.df}, p = {chi.p_value:.4f} → {decision(chi.p_value)}")


def show_configurations(rows: list[Row], mismatches: dict[str, int]) -> None:
    print("\nTabla 1. Configuraciones del generador (N = 10 000, k = 10, α = 0.05)")
    print(f"{'Generador':<16}{'χ²':>10}{'p χ²':>8}{'D':>9}{'p KS':>8}  {'Decisión χ²':<17}{'Decisión KS':<17}"
          f"{'Dif. secuencia':>15}")
    for row in rows:
        py = row.python
        print(f"{row.config.name:<16}{py.chi.statistic:>10.2f}{py.chi.p_value:>8.3f}{py.ks.statistic:>9.4f}"
              f"{py.ks.p_value:>8.3f}  {decision(py.chi.p_value):<17}{decision(py.ks.p_value):<17}"
              f"{mismatches[row.config.name]:>15}")


def show_sizes(rows: list[Row]) -> None:
    print(f"\nTabla 2. Python vs Java por tamaño de muestra ({rows[0].config.name})")
    print(f"{'N':>10}{'χ²':>10}{'p χ²':>8}{'D':>10}{'p KS':>8}{'t Python (s)':>14}{'t Java (s)':>12}"
          f"{'Dif. máx.':>11}")
    for row in rows:
        py = row.python
        print(f"{row.n:>10}{py.chi.statistic:>10.2f}{py.chi.p_value:>8.3f}{py.ks.statistic:>10.5f}"
              f"{py.ks.p_value:>8.3f}{py.seconds:>14.4f}{row.java.seconds:>12.4f}"
              f"{max_statistic_difference(row):>11.1e}")
