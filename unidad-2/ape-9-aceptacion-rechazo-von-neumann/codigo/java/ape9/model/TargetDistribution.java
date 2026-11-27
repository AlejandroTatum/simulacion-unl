package ape9.model;

import java.util.function.DoubleUnaryOperator;

/** Distribución objetivo f(x) en [0, 1] con su constante M = max(f(x)/g(x)) y propuesta g(x) = 1. */
public final class TargetDistribution {
    /** Distribución de la guía: f(x) = 2x con M = 2 (criterio U ≤ X, ET = 50 %). */
    public static final TargetDistribution LINEAR = new TargetDistribution("f(x)=2x", x -> 2 * x, 2.0);
    /** Actividad complementaria: f(x) = 3x² con M = 3 (criterio U ≤ X², ET = 33.33 %). */
    public static final TargetDistribution QUADRATIC = new TargetDistribution("f(x)=3x²", x -> 3 * x * x, 3.0);

    public final String label;
    public final double m;
    private final DoubleUnaryOperator density;

    private TargetDistribution(String label, DoubleUnaryOperator density, double m) {
        this.label = label;
        this.density = density;
        this.m = m;
    }

    /** Distribución propuesta g(x) = 1 (uniforme). */
    public static double proposalDensity(double x) {
        return 1.0;
    }

    public double density(double x) {
        return density.applyAsDouble(x);
    }

    /** Paso 5.5: R = f(X) / (M·g(X)). */
    public double ratio(double x) {
        return density(x) / (m * proposalDensity(x));
    }

    /** Eficiencia teórica ET = (1/M)·100. */
    public double theoreticalEfficiency() {
        return 100.0 / m;
    }
}
