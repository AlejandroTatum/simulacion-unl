"""Aceptación-rechazo de Von Neumann para Beta(2,2), f(x) = 6x(1 - x).

Es el código del borrador de la exposición. Al ejecutarlo como script corre
n = 10 000 muestras con semilla 42 para M = 1.5, 2, 3 y 6, y guarda en
resultados.json los valores que muestra la versión estática (PDF) de las
diapositivas 13 a 15. La demo del HTML repite el mismo algoritmo con el
mismo generador (PCG64, semilla 42), así que llega a los mismos números.

Uso: python3 beta22.py [--n 10000] [--semilla 42]
"""

import argparse
import json
from pathlib import Path

import numpy as np


def beta_22(x):
    """Densidad objetivo f(x) = 6x(1 - x) en [0, 1]."""
    return 6 * x * (1 - x) if 0 <= x <= 1 else 0.0


def generar(n, m=1.5, semilla=42):
    """Devuelve n muestras aceptadas y el número total de intentos."""
    if n <= 0 or m < 1.5:
        raise ValueError("Parámetros no válidos")
    rng = np.random.default_rng(semilla)
    muestras = []
    intentos = 0
    while len(muestras) < n:
        y = rng.uniform(0, 1)
        u = rng.uniform(0, 1)
        intentos += 1
        if u <= beta_22(y) / m:
            muestras.append(y)
    return np.array(muestras), intentos


def resumen(n, m, semilla, bins=20):
    """Contadores, media, varianza e histograma de densidad para un M."""
    x, k = generar(n, m, semilla)
    densidad, _ = np.histogram(x, bins=bins, range=(0, 1), density=True)
    return {
        "m": m,
        "aceptadas": int(len(x)),
        "rechazadas": int(k - len(x)),
        "intentos": int(k),
        "eficiencia": len(x) / k,
        "teorica": 1 / m,
        "media": float(np.mean(x)),
        "varianza": float(np.var(x)),
        "histograma": [round(float(v), 4) for v in densidad],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--semilla", type=int, default=42)
    args = parser.parse_args()
    corridas = [resumen(args.n, m, args.semilla) for m in (1.5, 2, 3, 6)]
    for r in corridas:
        print(f"M={r['m']:<4} aceptadas={r['aceptadas']} rechazadas={r['rechazadas']} "
              f"intentos={r['intentos']} eficiencia={r['eficiencia']:.4f} (1/M={r['teorica']:.4f}) "
              f"media={r['media']:.4f} varianza={r['varianza']:.4f}")
    # Primeros valores del generador: la demo HTML los usa para comprobar que su PCG64 coincide.
    rng = np.random.default_rng(args.semilla)
    control = [float(rng.uniform(0, 1)) for _ in range(6)]
    salida = {"n": args.n, "semilla": args.semilla, "control_uniformes": control, "corridas": corridas}
    destino = Path(__file__).with_name("resultados.json")
    texto = json.dumps(salida, indent=2, ensure_ascii=False)
    destino.write_text(texto + "\n", encoding="utf-8")
    # Copia para el HTML: un archivo .js se carga sin servidor (file://), un .json no.
    demo = Path(__file__).resolve().parent.parent / "assets" / "demo" / "resultados.js"
    demo.write_text("/* Generado por codigo/beta22.py: no editar a mano. */\n"
                    f"window.PY_RESULTS = {texto};\n", encoding="utf-8")
    print(f"guardado: {destino.name} y assets/demo/{demo.name}")


if __name__ == "__main__":
    main()
