"""Two-by-two scenario figure for a single IEEE column, legend outside the plots.

Usage: fig_escenarios.py EXPERIMENTS_DIR FONTS_DIR OUT.png
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
import pandas as pd

exp, fonts, out = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
for f in fonts.glob("*.ttf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams.update({"font.family": "Inter", "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.titleweight": "semibold"})

SCEN = [("base", "E1"), ("e2", "E2"), ("e3", "E3")]
COLORS = {"E1": "#2E6DA4", "E2": "#4E7D58", "E3": "#E07B39"}
STATIONS = ["Ensamblaje", "Acabado"]
res = {lbl: pd.read_csv(exp / f"resumen-{key}.csv").set_index("estacion") for key, lbl in SCEN}
lin = {lbl: pd.read_csv(exp / f"linea-{key}.csv").iloc[0] for key, lbl in SCEN}

fig, axes = plt.subplots(2, 2, figsize=(3.5 * 1.45, 3.9 * 1.45))
w = 0.26
panels = [("Utilización", "utilizacion_media", "utilizacion_teorica", 100, "ρ (%)"),
          ("Longitud de la cola", "lq_media", "lq_teorico", 1, "Lq (muebles)"),
          ("Tiempo de espera", "wq_min_media", "wq_min_teorico", 1, "Wq (min)")]
for ax, (title, sim, teo, k, ylabel) in zip(axes.flat, panels):
    for i, (_, lbl) in enumerate(SCEN):
        for j, st in enumerate(STATIONS):
            x = j + (i - 1) * w
            ax.bar(x, res[lbl].loc[st, sim] * k, w * 0.92, color=COLORS[lbl])
            ax.plot(x, res[lbl].loc[st, teo] * k, marker="D", ms=4, color="#222", zorder=3)
    ax.set_xticks([0, 1], STATIONS)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.margins(y=0.12)
    ax.grid(axis="y", color="#e5e5e5", lw=0.6)
    ax.set_axisbelow(True)

ax = axes[1, 1]
for i, (_, lbl) in enumerate(SCEN):
    cap, prod = lin[lbl]["capacidad_linea_h"], lin[lbl]["throughput_h"]
    ax.bar(i - 0.2, cap, 0.38, color="#6B6158")
    ax.bar(i + 0.2, prod, 0.38, color="#9CB8D4")
    ax.text(i - 0.2, cap + 0.08, f"{cap:.2f}".replace(".", ","), ha="center", fontsize=7.5)
    ax.text(i + 0.2, prod + 0.08, f"{prod:.2f}".replace(".", ","), ha="center", fontsize=7.5)
ax.set_xticks(range(3), [lbl for _, lbl in SCEN])
ax.set_ylim(0, 6)
ax.set_title("Capacidad y producción")
ax.set_ylabel("muebles/h")
ax.grid(axis="y", color="#e5e5e5", lw=0.6)
ax.set_axisbelow(True)

handles = [Patch(color=COLORS[l], label=l) for _, l in SCEN]
handles += [Line2D([], [], marker="D", ms=4, color="#222", ls="", label="Teoría M/M/1"),
            Patch(color="#6B6158", label="Capacidad"), Patch(color="#9CB8D4", label="Producción")]
comma = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
for a in axes.flat:
    a.yaxis.set_major_formatter(comma)
fig.legend(handles=handles, loc="upper center", ncol=6, frameon=False, fontsize=7.5,
           handlelength=1.2, columnspacing=1.0, bbox_to_anchor=(0.5, 1.0))
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(out, dpi=300)
print("saved", out)
