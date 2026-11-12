"""Compila y ejecuta la versión Java para comparar sus resultados con los de Python."""

import subprocess
from pathlib import Path

from .config import Experiment
from .lcg import LcgConfig
from .measurement import Measurement

CODE_DIR = Path(__file__).resolve().parents[2]
JAVA_DIR = CODE_DIR / "java"
JAVA_CLASS = "ape7.Main"


def compile_java(build_dir: Path) -> None:
    """Se ejecuta desde `codigo/` para que `mise.toml` elija el JDK aunque el programa se lance desde otra carpeta."""
    build_dir.mkdir(parents=True, exist_ok=True)
    sources = sorted(str(path) for path in JAVA_DIR.rglob("*.java"))
    subprocess.run(["javac", "-d", str(build_dir), *sources], check=True, cwd=CODE_DIR)


def run_java(experiment: Experiment, config: LcgConfig, n: int, build_dir: Path) -> Measurement:
    """Aciertos, estimación, error y tiempo que calcula la versión Java."""
    result = subprocess.run(
        ["java", "-cp", str(build_dir), JAVA_CLASS,
         str(config.a), str(config.c), str(config.m), str(config.seed), str(n), experiment.key],
        check=True, capture_output=True, text=True, cwd=CODE_DIR,
    )
    fields = dict(line.split("=", 1) for line in result.stdout.splitlines())
    return Measurement(
        hits=int(fields["aciertos"]),
        estimate=float(fields["estimacion"]),
        error=float(fields["error"]),
        seconds=float(fields["tiempo_s"]),
    )
