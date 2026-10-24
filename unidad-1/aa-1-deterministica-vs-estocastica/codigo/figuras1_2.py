"""Figures for AA tema 18 (same seed and data as mm1_det_vs_stoch.py)."""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
LAM, MU, N_CUST, REPS = 0.8, 1.0, 2000, 10


def mean_wait(inter, serv):
    w, total = 0.0, 0.0
    for i in range(1, len(inter)):
        w = max(0.0, w + serv[i - 1] - inter[i])
        total += w
    return total / (len(inter) - 1)


rng = np.random.default_rng(18)
reps = np.array([mean_wait(rng.exponential(1 / LAM, N_CUST), rng.exponential(1 / MU, N_CUST)) for _ in range(REPS)])
m, s = reps.mean(), reps.std(ddof=1)
half = 2.262 * s / np.sqrt(REPS)
obs = rng.exponential(1 / LAM, 50)
boots = []
for _ in range(1000):
    lb = 1 / rng.choice(obs, 50).mean()
    boots.append(lb / (MU * (MU - lb)) if lb < MU else np.inf)
fin = np.array([b for b in boots if np.isfinite(b)])

plt.rcParams.update({"font.family": "serif", "font.size": 9})

fig, ax = plt.subplots(figsize=(3.4, 2.7), dpi=300)
ax.plot(range(1, REPS + 1), reps, "o", color="#1f4e79", label="Réplica estocástica")
ax.axhline(4.0, color="#444444", ls="--", lw=1, label="Teórico M/M/1 (4.0)")
ax.axhline(0.0, color="#b03a2e", lw=1.2, label="Determinístico (0)")
ax.axhspan(m - half, m + half, color="#1f4e79", alpha=0.12, label=f"IC 95 % [{m - half:.2f}, {m + half:.2f}]")
ax.set_xlabel("Réplica")
ax.set_ylabel("Wq (min)")
ax.set_xticks(range(1, REPS + 1))
ax.legend(fontsize=6.5, loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=False)
fig.tight_layout()
fig.savefig(out / "fig1-replicas-wq.png")

fig, ax = plt.subplots(figsize=(3.4, 2.7), dpi=300)
ax.hist(np.clip(fin, 0, 25), bins=40, color="#1f4e79", alpha=0.75)
p_lo, p_hi = np.percentile(fin, [2.5, 97.5])
ax.axvline(p_lo, color="#444444", ls=":", lw=1)
ax.axvline(p_hi, color="#444444", ls=":", lw=1, label=f"Percentiles 2.5–97.5: {p_lo:.2f}–{p_hi:.2f}")
ax.axvspan(m - half, m + half, color="#b03a2e", alpha=0.2, label="IC 95 % de las réplicas")
ax.set_xlabel("Wq (min), valores > 25 agrupados en 25")
ax.set_ylabel("Frecuencia")
ax.legend(fontsize=6.5, loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=1, frameon=False)
fig.tight_layout()
fig.savefig(out / "fig2-bootstrap-wq.png")
print(f"reps mean {m:.3f} CI [{m - half:.3f}, {m + half:.3f}] boot {p_lo:.2f}-{p_hi:.2f} unstable {np.mean(~np.isfinite(boots)):.3f}")
