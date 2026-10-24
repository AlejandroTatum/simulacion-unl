"""AA tema 18: replications needed for a 10 % relative half-width, then confirm by simulating them.

Also writes figure 3 (Wq vs load: deterministic, theory, stochastic mean with CI 95 %).
Usage: mm1_precision.py <figures_dir>
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def t975(df):
    # Cornish-Fisher expansion of the Student t quantile around z = 1.959964 (t(0.975, 9) = 2.262)
    z = 1.959964
    return (z + (z**3 + z) / (4 * df) + (5 * z**5 + 16 * z**3 + 3 * z) / (96 * df**2)
            + (3 * z**7 + 19 * z**5 + 17 * z**3 - 15 * z) / (384 * df**3))

MU, N_CUST, N0, TARGET = 1.0, 2000, 10, 0.10


def mean_wait(inter, serv):
    w, total = 0.0, 0.0
    for i in range(1, len(inter)):
        w = max(0.0, w + serv[i - 1] - inter[i])
        total += w
    return total / (len(inter) - 1)


def replicate(lam, n, rng):
    return np.array([mean_wait(rng.exponential(1 / lam, N_CUST), rng.exponential(1 / MU, N_CUST)) for _ in range(n)])


def ci(x):
    h = t975(len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))
    return x.mean(), h


rows = []
for lam in (0.5, 0.8, 0.9):
    rng = np.random.default_rng(18)
    pilot = replicate(lam, N0, rng)
    m0, h0 = ci(pilot)
    rel0 = h0 / m0
    # Law: n* = n0 * (h0 / h_target)^2, rounded up
    need = int(np.ceil(N0 * (rel0 / TARGET) ** 2))
    extra = replicate(lam, max(need - N0, 0), rng)
    full = np.concatenate([pilot, extra])
    m1, h1 = ci(full)
    rows.append((lam, m0, h0, rel0, need, m1, h1))
    print(f"rho={lam:.1f} pilot mean={m0:.2f} rel={rel0 * 100:.0f}% need={need} "
          f"final mean={m1:.2f} CI=[{m1 - h1:.2f}, {m1 + h1:.2f}] rel={h1 / m1 * 100:.1f}% theory={lam / (MU * (MU - lam)):.2f}")

out = Path(sys.argv[1])
rhos = np.array([r[0] for r in rows])
plt.rcParams.update({"font.family": "serif", "font.size": 9})
fig, ax = plt.subplots(figsize=(3.4, 2.8), dpi=300)
grid = np.linspace(0.45, 0.92, 100)
ax.plot(grid, grid / (MU * (MU - grid)), color="#444444", ls="--", lw=1, label="Teórico M/M/1")
ax.plot(rhos, np.zeros_like(rhos), "s-", color="#b03a2e", ms=4, lw=1.2, label="Determinístico")
ax.errorbar(rhos, [r[1] for r in rows], yerr=[r[2] for r in rows], fmt="o", color="#1f4e79", ms=4,
            capsize=3, label="10 réplicas (IC 95 %)")
ax.errorbar(rhos + 0.012, [r[5] for r in rows], yerr=[r[6] for r in rows], fmt="o", mfc="white", color="#2e7d32",
            ms=4, capsize=3, label="Réplicas para ±10 % (IC 95 %)")
ax.set_xlabel("Utilización ρ")
ax.set_ylabel("Wq (min)")
ax.set_xticks(rhos)
ax.legend(fontsize=6.5, loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=False)
fig.tight_layout()
fig.savefig(out / "fig3-carga-wq.png")
print("fig3 ok")
