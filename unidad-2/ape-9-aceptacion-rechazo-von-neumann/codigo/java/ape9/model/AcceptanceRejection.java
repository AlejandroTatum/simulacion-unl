package ape9.model;

import java.util.Random;

/** Algoritmo ACEPTACION_RECHAZO de la guía; cada objeto es una simulación con N candidatos. */
public final class AcceptanceRejection {
    public final TargetDistribution target;
    public final int n;
    public final int accepted;
    public final int rejected;

    private AcceptanceRejection(TargetDistribution target, int n, int accepted) {
        this.target = target;
        this.n = n;
        this.accepted = accepted;
        this.rejected = n - accepted;
    }

    /** Paso 5.6: el candidato se acepta si U ≤ R (la igualdad también se acepta). */
    public static boolean accepts(double u, double r) {
        return u <= r;
    }

    /** Pasos 1 a 5: genera X y luego U en cada repetición y cuenta los aceptados. */
    public static AcceptanceRejection run(TargetDistribution target, int n, long seed) {
        Random rng = new Random(seed);
        int accepted = 0;
        for (int i = 0; i < n; i++) {
            double x = rng.nextDouble();
            double u = rng.nextDouble();
            if (accepts(u, target.ratio(x))) {
                accepted++;
            }
        }
        return new AcceptanceRejection(target, n, accepted);
    }

    /** Paso 6: E = (aceptados / N)·100. */
    public double efficiency() {
        return accepted * 100.0 / n;
    }

    /** |E experimental − ET| en puntos porcentuales. */
    public double absoluteError() {
        return Math.abs(efficiency() - target.theoreticalEfficiency());
    }
}
