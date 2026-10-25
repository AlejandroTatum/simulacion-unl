"""Figura de la diapositiva 6: pico e instante del pico en 30 corridas de Python y de NetLogo."""

import csv
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "codigo"))
from simulacion_ape.model.config import SirConfig
from simulacion_ape.model.replications import run_replications

HERE = Path(__file__).resolve().parent
rows = list(csv.reader(open(HERE / "replicas_netlogo.csv")))
head = rows.index(next(r for r in rows if r and r[0] == "[run number]"))
data = sorted(rows[head + 1:], key=lambda r: int(r[6]))
nl_peak = np.array([float(r[11]) for r in data]); nl_time = np.array([float(r[12]) for r in data])
py = run_replications(SirConfig(), 30)
py_peak, py_time = py.peak_values.astype(float), py.peak_times.astype(float)
print("NL", nl_peak.mean().round(2), nl_peak.std(ddof=1).round(2), nl_time.mean().round(2), len(nl_peak))
print("PY", py_peak.mean().round(2), py_peak.std(ddof=1).round(2), py_time.mean().round(2))

colors = {"Python": "#2563eb", "NetLogo": "#e0606a"}
rng = np.random.default_rng(1)
fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
panels = [("Pico de infectados", "Infectados", py_peak, nl_peak, 33.0),
          ("Instante del pico", "Tiempo", py_time, nl_time, 19.0)]
for ax, (title, ylabel, a, b, ode) in zip(axes, panels):
    for x, (name, vals) in enumerate((("Python", a), ("NetLogo", b))):
        ax.scatter(x + rng.uniform(-0.12, 0.12, len(vals)), vals, s=34, alpha=0.55,
                   color=colors[name], edgecolor="white", linewidth=0.6, zorder=2)
        m = vals.mean()
        ax.hlines(m, x - 0.28, x + 0.28, color=colors[name], linewidth=3, zorder=3)
        ax.text(x + 0.31, m, f"media {m:.1f}", va="center", fontsize=11, color=colors[name], fontweight="bold", bbox=dict(facecolor="white", edgecolor="none", pad=1.5), zorder=4)
    ax.axhline(ode, color="#6b7280", linestyle="--", linewidth=1.2, zorder=1, label=f"ecuaciones (EDO): {ode:g}")
    ax.legend(loc="lower right", fontsize=9, frameon=False)
    ax.set_xticks([0, 1], ["Python", "NetLogo"], fontsize=11)
    ax.set_xlim(-0.5, 1.75)
    ax.set_title(title, fontsize=13)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
fig.suptitle("30 corridas por herramienta (semillas 0 a 29): cada punto es una corrida", fontsize=12)
fig.tight_layout()
fig.savefig(HERE.parent / "figuras" / "comparacion_replicas.png", dpi=160)
