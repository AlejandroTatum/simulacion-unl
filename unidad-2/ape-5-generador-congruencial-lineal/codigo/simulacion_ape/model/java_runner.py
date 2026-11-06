"""Compila y ejecuta la implementación Java para comparar su secuencia con la de Python."""

import subprocess
from pathlib import Path

from .config import LcgConfig

CODE_DIR = Path(__file__).resolve().parents[2]
JAVA_SOURCE = CODE_DIR / "java" / "Lcg.java"


def run_java_lcg(config: LcgConfig, build_dir: Path) -> list[int]:
    """Devuelve los estados X1..Xn que imprime `java Lcg` con los mismos parámetros.

    Se ejecuta desde `codigo/` para que `mise.toml` elija el JDK aunque el programa se lance desde otra carpeta.
    """
    build_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(["javac", "-d", str(build_dir), str(JAVA_SOURCE)], check=True, cwd=CODE_DIR)
    result = subprocess.run(
        ["java", "-cp", str(build_dir), "Lcg",
         str(config.a), str(config.c), str(config.m), str(config.seed), str(config.n)],
        check=True, capture_output=True, text=True, cwd=CODE_DIR,
    )
    return [int(line.split(";")[1]) for line in result.stdout.splitlines()]
