"""Punto de entrada delgado: conecta configuración, simulación, análisis y reportes."""

from .analysis import summarize
from .config import SimulationConfig
from .reporting import format_summary
from .simulation import run


def main() -> None:
    outcomes = run(SimulationConfig())
    print(format_summary(summarize(outcomes)))


if __name__ == "__main__":
    main()
