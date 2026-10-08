from simulacion_ape.model.analysis import summarize
from simulacion_ape.model.config import SimulationConfig
from simulacion_ape.model.simulation import run


def test_same_seed_reproduces_results():
    config = SimulationConfig(runs=100, seed=7)
    assert run(config) == run(config)


def test_mean_converges_to_expected_value():
    summary = summarize(run(SimulationConfig(runs=20_000, seed=1)))
    assert abs(summary.mean - 3.5) < 0.05


def test_entry_point_runs_when_executed_by_file_path(tmp_path):
    # El botón "Run" del editor ejecuta el archivo por ruta, no con python -m.
    import subprocess
    import sys
    from pathlib import Path

    main_file = Path(__file__).resolve().parents[1] / "simulacion_ape" / "__main__.py"
    result = subprocess.run([sys.executable, str(main_file)], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
