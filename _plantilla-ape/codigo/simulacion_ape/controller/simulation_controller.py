"""Controlador: ejecuta la simulación y pide a la vista mostrar el resumen."""

from ..model.analysis import summarize
from ..model.config import SimulationConfig
from ..model.simulation import run
from ..view.console_view import show_summary


def main() -> None:
    outcomes = run(SimulationConfig())
    show_summary(summarize(outcomes))
