"""AA tema 18: deterministic vs stochastic M/M/1 under different loads (rho = 0.5, 0.8, 0.9)."""
import numpy as np

MU, N_CUST, REPS, T = 1.0, 2000, 10, 2.262


def mean_wait(inter, serv):
    w, total = 0.0, 0.0
    for i in range(1, len(inter)):
        w = max(0.0, w + serv[i - 1] - inter[i])
        total += w
    return total / (len(inter) - 1)


for lam in (0.5, 0.8, 0.9):
    rng = np.random.default_rng(18)
    det = mean_wait(np.full(N_CUST, 1 / lam), np.full(N_CUST, 1 / MU))
    reps = np.array([mean_wait(rng.exponential(1 / lam, N_CUST), rng.exponential(1 / MU, N_CUST)) for _ in range(REPS)])
    m, s = reps.mean(), reps.std(ddof=1)
    h = T * s / np.sqrt(REPS)
    theory = lam / (MU * (MU - lam))
    print(f"rho={lam:.1f} det={det:.2f} theory={theory:.2f} mean={m:.2f} CI=[{m - h:.2f}, {m + h:.2f}] "
          f"halfwidth/mean={h / m * 100:.0f}% min={reps.min():.2f} max={reps.max():.2f}")
