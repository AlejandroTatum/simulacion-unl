package ape8.model;

import java.util.Random;

/** Uniformes U(0,1) y exponencial generada por Transformada Inversa. */
public final class InverseTransform {
    private InverseTransform() {
    }

    /** Algoritmo 1: vector de N números aleatorios uniformes en [0, 1). */
    public static double[] generateUniforms(int n, long seed) {
        Random rng = new Random(seed);
        double[] u = new double[n];
        for (int i = 0; i < n; i++) {
            u[i] = rng.nextDouble();
        }
        return u;
    }

    /** La tasa lambda de la exponencial debe ser mayor que cero. */
    public static void validateRate(double rate) {
        if (!(rate > 0)) {
            throw new IllegalArgumentException("lambda debe ser mayor que 0 (se recibió " + rate + ")");
        }
    }

    /** Algoritmo 2: X = -ln(1 - U) / lambda. */
    public static double inverseExponential(double u, double rate) {
        validateRate(rate);
        return -Math.log(1.0 - u) / rate;
    }

    /** Aplica la transformada inversa a todo el vector U. */
    public static double[] inverseExponential(double[] u, double rate) {
        double[] x = new double[u.length];
        for (int i = 0; i < u.length; i++) {
            x[i] = inverseExponential(u[i], rate);
        }
        return x;
    }
}
