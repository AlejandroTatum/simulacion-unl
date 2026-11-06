package ape6.model;

/** Generador Congruencial Lineal: X(n+1) = (a * X(n) + c) mod m. */
public final class Lcg {

    private Lcg() {
    }

    /** X1..Xn a partir de la semilla (la semilla no se incluye). a * X cabe en un long porque a < 2^31 y X < 2^32. */
    public static long[] states(long a, long c, long m, long seed, int n) {
        long[] states = new long[n];
        long x = seed;
        for (int i = 0; i < n; i++) {
            x = Math.floorMod(a * x + c, m);
            states[i] = x;
        }
        return states;
    }

    /** Secuencia U1..Un = X(n) / m, valores en [0, 1). */
    public static double[] generate(long a, long c, long m, long seed, int n) {
        long[] states = states(a, c, m, seed, n);
        double[] values = new double[n];
        for (int i = 0; i < n; i++) {
            values[i] = (double) states[i] / m;
        }
        return values;
    }
}
