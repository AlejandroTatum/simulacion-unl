package ape6.model;

/**
 * Colas de las distribuciones Chi-cuadrado y de Kolmogorov, programadas sin librerías.
 *
 * Mismas fórmulas que distributions.py (Numerical Recipes, cap. 6 y 14), para obtener los mismos valores p.
 */
public final class Distributions {

    private static final double LANCZOS_G = 7;
    private static final double[] LANCZOS_COEF = {
        0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
        -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6,
        1.5056327351493116e-7,
    };
    private static final double TINY = 1e-300;
    private static final double EPS = 1e-15;
    private static final int MAX_ITERATIONS = 1000;

    private Distributions() {
    }

    /** ln Γ(z) para z ≥ 0.5 con la aproximación de Lanczos. */
    static double logGamma(double z) {
        z -= 1;
        double x = LANCZOS_COEF[0];
        for (int i = 1; i < LANCZOS_COEF.length; i++) {
            x += LANCZOS_COEF[i] / (z + i);
        }
        double t = z + LANCZOS_G + 0.5;
        return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
    }

    /** Q(s, x) = Γ(s, x) / Γ(s): serie si x < s + 1, fracción continua (Lentz) en otro caso. */
    static double regularizedGammaQ(double s, double x) {
        if (x <= 0) {
            return 1.0;
        }
        double logPrefactor = -x + s * Math.log(x) - logGamma(s);
        if (x < s + 1) {
            double term = 1.0 / s;
            double total = term;
            double k = s;
            for (int i = 0; i < MAX_ITERATIONS; i++) {
                k += 1;
                term *= x / k;
                total += term;
                if (Math.abs(term) < Math.abs(total) * EPS) {
                    break;
                }
            }
            return 1.0 - total * Math.exp(logPrefactor);
        }
        double b = x + 1 - s;
        double c = 1 / TINY;
        double d = 1 / b;
        double h = d;
        for (int i = 1; i < MAX_ITERATIONS; i++) {
            double an = -i * (i - s);
            b += 2;
            d = an * d + b;
            if (Math.abs(d) < TINY) {
                d = TINY;
            }
            c = b + an / c;
            if (Math.abs(c) < TINY) {
                c = TINY;
            }
            d = 1 / d;
            double delta = d * c;
            h *= delta;
            if (Math.abs(delta - 1) < EPS) {
                break;
            }
        }
        return Math.exp(logPrefactor) * h;
    }

    /** Valor p de la prueba: P(χ²(gl) ≥ estadístico) = Q(gl/2, χ²/2). */
    public static double chiSquareSf(double statistic, int df) {
        return regularizedGammaQ(df / 2.0, statistic / 2);
    }

    /** Q_KS(λ) = 2 · Σ (-1)^(j-1) · exp(-2 j² λ²); vale 1 cuando la serie no converge (λ pequeño). */
    static double kolmogorovQ(double lam) {
        double a2 = -2 * lam * lam;
        double sign = 2.0;
        double total = 0.0;
        double previous = 0.0;
        for (int j = 1; j <= 100; j++) {
            double term = sign * Math.exp(a2 * j * j);
            total += term;
            if (Math.abs(term) <= 0.001 * previous || Math.abs(term) <= 1e-8 * total) {
                return Math.min(Math.max(total, 0.0), 1.0);
            }
            sign = -sign;
            previous = Math.abs(term);
        }
        return 1.0;
    }

    /** Valor p de K-S con la corrección de Stephens: λ = (√N + 0.12 + 0.11/√N) · D. */
    public static double kolmogorovSf(int n, double d) {
        double sqrtN = Math.sqrt(n);
        return kolmogorovQ((sqrtN + 0.12 + 0.11 / sqrtN) * d);
    }
}
