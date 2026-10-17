"""Pruebas de la aplicación completa: punto de entrada, tabla de consola y mensajes."""

import os
import subprocess
import sys
from pathlib import Path

from simulacion_ape.controller.simulation_controller import main

MAIN_FILE = Path(__file__).resolve().parents[1] / "simulacion_ape" / "__main__.py"


def test_entry_point_runs_when_executed_by_file_path(tmp_path):
    # El botón "Run" del editor ejecuta el archivo por ruta, no con python -m.
    result = subprocess.run(
        [sys.executable, str(MAIN_FILE), "--sin-animacion", "--tiempo", "300", "--resultados", str(tmp_path)],
        cwd=tmp_path, capture_output=True, text=True, env={**os.environ, "MPLBACKEND": "Agg"},
    )
    assert result.returncode == 0, result.stderr
    assert "Escenario 3: Cerca de saturación" in result.stdout
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "cola_en_el_tiempo.png", "comparacion_teorico_simulado.png",
        "convergencia_espera.png", "dispersion_espera.png", "histograma_espera.png",
    ]


def test_console_table_keeps_the_reference_numbers(tmp_path, capsys):
    main(["--sin-animacion", "--resultados", str(tmp_path)])
    lines = [line.split() for line in capsys.readouterr().out.splitlines() if line.startswith("  L ")]
    assert [line[-3:-1] for line in lines] == [["2.000", "2.036"], ["5.000", "5.029"], ["29.000", "26.592"]]


def test_unstable_custom_scenario_is_not_simulated(tmp_path, capsys):
    main(["--llegada", "3.5", "--servicio", "3", "--sin-animacion", "--resultados", str(tmp_path)])
    assert "el sistema no es estable (λ = 3.5 ≥ μ = 3.0)" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []


def test_without_a_graphical_backend_it_explains_how_to_get_one(tmp_path, capsys):
    main(["--tiempo", "300", "--resultados", str(tmp_path)])  # las pruebas usan Agg: no hay ventana
    assert "Instale Tk" in capsys.readouterr().out
