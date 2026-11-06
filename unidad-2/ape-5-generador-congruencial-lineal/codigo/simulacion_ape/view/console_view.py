"""Vista de consola: tablas y resúmenes en texto."""

from ..model.analysis import ComparisonRow, SequenceStats


def format_comparison(rows: list[ComparisonRow]) -> str:
    lines = [f"{'n':>3} {'X(n) Python':>12} {'X(n) Java':>12} {'U(n) Python':>12} {'U(n) Java':>12} Igual"]
    for row in rows:
        lines.append(f"{row.index:>3} {row.x_python:>12} {row.x_java:>12} "
                     f"{row.u_python:>12.8f} {row.u_java:>12.8f} {'sí' if row.equal else 'NO'}")
    return "\n".join(lines)


def format_period(conditions: dict[str, bool], m: int, first_repeat: int | None, n: int,
                  small_cases: list[tuple[str, dict[str, bool], int, int]]) -> str:
    lines = ["Período (teorema de Hull-Dobell, parámetros de la guía):"]
    lines += [f"  - {name}: {'cumple' if ok else 'no cumple'}" for name, ok in conditions.items()]
    verdict = f"período completo τ = m = {m}" if all(conditions.values()) else "período menor que m"
    lines.append(f"  => {verdict}")
    repeat = "ningún valor se repite" if first_repeat is None else f"primera repetición en n = {first_repeat}"
    lines.append(f"  Muestra de {n} valores: {repeat}")
    lines.append("Período medido en módulos pequeños:")
    for label, small_conditions, period, m_small in small_cases:
        holds = "cumple" if all(small_conditions.values()) else "no cumple"
        lines.append(f"  - {label}: Hull-Dobell {holds}, período = {period} de m = {m_small}")
    return "\n".join(lines)


def format_seeds(stats: list[SequenceStats]) -> str:
    lines = ["Comparación de semillas (media ideal 0.5, varianza ideal 1/12 = 0.0833):"]
    for s in stats:
        first = ", ".join(f"{u:.4f}" for u in s.first_values)
        lines.append(f"  semilla {s.seed}: media = {s.mean:.4f}, varianza = {s.variance:.4f}, "
                     f"correlación U(n)-U(n+1) = {s.lag1_correlation:+.4f}; primeros: {first}")
    return "\n".join(lines)


def show(text: str) -> None:
    print(text)
    print()
