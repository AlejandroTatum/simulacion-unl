"""Compila y ejecuta la versión Java para comparar sus resultados con los de Python."""

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import LcgConfig

CODE_DIR = Path(__file__).resolve().parents[2]
JAVA_DIR = CODE_DIR / "java"
JAVA_CLASS = "ape6.Main"


@dataclass(frozen=True)
class JavaRun:
    observed: list[int]
    chi2: float
    df: int
    p_chi2: float
    d_plus: float
    d_minus: float
    d: float
    p_ks: float
    seconds: float


def compile_java(build_dir: Path) -> None:
    """Se ejecuta desde `codigo/` para que `mise.toml` elija el JDK aunque el programa se lance desde otra carpeta."""
    build_dir.mkdir(parents=True, exist_ok=True)
    sources = sorted(str(path) for path in JAVA_DIR.rglob("*.java"))
    subprocess.run(["javac", "-d", str(build_dir), *sources], check=True, cwd=CODE_DIR)


def _java(config: LcgConfig, n: int, build_dir: Path, *extra: str) -> str:
    result = subprocess.run(
        ["java", "-cp", str(build_dir), JAVA_CLASS,
         str(config.a), str(config.c), str(config.m), str(config.seed), str(n), *extra],
        check=True, capture_output=True, text=True, cwd=CODE_DIR,
    )
    return result.stdout


def run_java_states(config: LcgConfig, n: int, build_dir: Path) -> list[int]:
    """Estados X1..Xn que imprime la versión Java."""
    return [int(line) for line in _java(config, n, build_dir, "secuencia").splitlines()]


def run_java_tests(config: LcgConfig, n: int, build_dir: Path) -> JavaRun:
    """Estadísticos, valores p y tiempo que calcula la versión Java."""
    fields = dict(line.split("=", 1) for line in _java(config, n, build_dir).splitlines())
    return JavaRun(
        observed=[int(v) for v in fields["observadas"].split(",")],
        chi2=float(fields["chi2"]),
        df=int(fields["gl"]),
        p_chi2=float(fields["p_chi2"]),
        d_plus=float(fields["d_mas"]),
        d_minus=float(fields["d_menos"]),
        d=float(fields["d"]),
        p_ks=float(fields["p_ks"]),
        seconds=float(fields["tiempo_s"]),
    )
