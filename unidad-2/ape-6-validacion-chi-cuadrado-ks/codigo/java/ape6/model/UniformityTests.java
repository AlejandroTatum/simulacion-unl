package ape6.model;

import java.util.Arrays;

/** Pruebas de bondad de ajuste a U(0, 1): Chi-cuadrado (algoritmo 2) y Kolmogorov-Smirnov. */
public final class UniformityTests {

    public static final int BINS = 10;

    public record ChiSquareResult(int[] observed, double expected, double statistic, int df, double pValue) {
    }

    public record KsResult(double dPlus, double dMinus, double statistic, double pValue) {
    }

    private UniformityTests() {
    }

    /** Cuenta cuántos valores caen en cada subintervalo y suma (O - E)² / E. */
    public static ChiSquareResult chiSquare(double[] values) {
        int[] observed = new int[BINS];
        for (double u : values) {
            observed[Math.min((int) (u * BINS), BINS - 1)]++;
        }
        double expected = (double) values.length / BINS;
        double statistic = 0.0;
        for (int o : observed) {
            double diff = o - expected;
            statistic += diff * diff / expected;
        }
        int df = BINS - 1;
        return new ChiSquareResult(observed, expected, statistic, df, Distributions.chiSquareSf(statistic, df));
    }

    /** D = máx(D+, D-) entre la FDE de los datos ordenados y F(x) = x. */
    public static KsResult kolmogorovSmirnov(double[] values) {
        double[] ordered = values.clone();
        Arrays.sort(ordered);
        int n = ordered.length;
        double dPlus = 0.0;
        double dMinus = 0.0;
        for (int i = 1; i <= n; i++) {
            double u = ordered[i - 1];
            dPlus = Math.max(dPlus, (double) i / n - u);
            dMinus = Math.max(dMinus, u - (double) (i - 1) / n);
        }
        double statistic = Math.max(dPlus, dMinus);
        return new KsResult(dPlus, dMinus, statistic, Distributions.kolmogorovSf(n, statistic));
    }
}
