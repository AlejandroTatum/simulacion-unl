package ape8.model;

/** Algoritmo 4: media y varianza experimentales frente a las teóricas, con error porcentual. */
public final class Comparison {
    public final String label;
    public final double theoreticalMean;
    public final double experimentalMean;
    public final double theoreticalVariance;
    public final double experimentalVariance;

    public Comparison(String label, double theoreticalMean, double[] values, double theoreticalVariance) {
        this.label = label;
        this.theoreticalMean = theoreticalMean;
        this.experimentalMean = mean(values);
        this.theoreticalVariance = theoreticalVariance;
        this.experimentalVariance = sampleVariance(values, experimentalMean);
    }

    /** Uniforme U(0,1): media teórica 1/2 y varianza 1/12. */
    public static Comparison uniform(double[] u) {
        return new Comparison("U(0,1)", 0.5, u, 1.0 / 12.0);
    }

    /** Exponencial: media teórica 1/lambda y varianza 1/lambda². */
    public static Comparison exponential(double[] x, double rate) {
        InverseTransform.validateRate(rate);
        return new Comparison(Double.toString(rate), 1.0 / rate, x, 1.0 / (rate * rate));
    }

    public double meanErrorPct() {
        return percentError(experimentalMean, theoreticalMean);
    }

    public double varianceErrorPct() {
        return percentError(experimentalVariance, theoreticalVariance);
    }

    static double percentError(double experimental, double theoretical) {
        return Math.abs(experimental - theoretical) / theoretical * 100.0;
    }

    static double mean(double[] values) {
        double sum = 0.0;
        for (double value : values) {
            sum += value;
        }
        return sum / values.length;
    }

    /** Varianza muestral (divide entre N - 1), igual que en Python. */
    static double sampleVariance(double[] values, double mean) {
        double sum = 0.0;
        for (double value : values) {
            sum += (value - mean) * (value - mean);
        }
        return sum / (values.length - 1);
    }
}
