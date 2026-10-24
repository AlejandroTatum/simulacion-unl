"""M/M/1 example for AA tema 18: deterministic vs stochastic vs input uncertainty."""
import numpy as np

LAM, MU, N_CUST, REPS = 0.8, 1.0, 2000, 10


def mean_wait(inter, serv):
    # Lindley recursion: Wq_{n+1} = max(0, Wq_n + S_n - A_{n+1})
    w, total = 0.0, 0.0
    for i in range(1, len(inter)):
        w = max(0.0, w + serv[i - 1] - inter[i])
        total += w
    return total / (len(inter) - 1)


rng = np.random.default_rng(18)
det = mean_wait(np.full(N_CUST, 1 / LAM), np.full(N_CUST, 1 / MU))
reps = np.array([mean_wait(rng.exponential(1 / LAM, N_CUST), rng.exponential(1 / MU, N_CUST)) for _ in range(REPS)])
m, s = reps.mean(), reps.std(ddof=1)
t = 2.262  # t_{0.975, 9}
print(f"deterministic Wq = {det:.3f}")
print(f"theory Wq = {LAM / (MU * (MU - LAM)):.3f}")
print("reps:", " ".join(f"{x:.2f}" for x in reps))
print(f"mean={m:.3f} sd={s:.3f} CI95=[{m - t * s / np.sqrt(REPS):.3f}, {m + t * s / np.sqrt(REPS):.3f}]")

# Input uncertainty: lambda estimated from 50 observed interarrival times, bootstrap
obs = rng.exponential(1 / LAM, 50)
lam_hat = 1 / obs.mean()
boots = []
for _ in range(1000):
    lb = 1 / rng.choice(obs, 50).mean()
    boots.append(lb / (MU * (MU - lb)) if lb < MU else np.inf)
boots = np.array(boots)
fin = boots[np.isfinite(boots)]
print(f"lam_hat={lam_hat:.3f} Wq(lam_hat)={lam_hat / (MU * (MU - lam_hat)):.3f}")
print(f"unstable share (lam>=mu)={np.mean(~np.isfinite(boots)):.3f}")
print(f"bootstrap Wq pct 2.5/50/97.5 = {np.percentile(fin, 2.5):.2f} {np.percentile(fin, 50):.2f} {np.percentile(fin, 97.5):.2f}")
