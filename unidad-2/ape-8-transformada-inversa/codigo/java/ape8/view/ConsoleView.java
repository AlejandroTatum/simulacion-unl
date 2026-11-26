package ape8.view;

import ape8.model.Comparison;
import java.util.List;
import java.util.Locale;

/** Vista de consola: imprime las muestras y la tabla comparativa. */
public final class ConsoleView {
    private ConsoleView() {
    }

    public static void showHeader(int n, long seed) {
        System.out.println("APE 8 (Java): método de la Transformada Inversa");
        System.out.println("N = " + n + "   semilla = " + seed);
    }

    public static void showUniform(Comparison stats) {
        System.out.println();
        System.out.println("Algoritmo 1: uniformes U(0,1)");
        System.out.printf(Locale.ROOT, "  media    experimental = %.6f   teórica = %.6f   error = %.4f %%%n",
                stats.experimentalMean, stats.theoreticalMean, stats.meanErrorPct());
        System.out.printf(Locale.ROOT, "  varianza experimental = %.6f   teórica = %.6f   error = %.4f %%%n",
                stats.experimentalVariance, stats.theoreticalVariance, stats.varianceErrorPct());
    }

    public static void showSample(double[] x, double rate) {
        System.out.println();
        System.out.println("Algoritmo 2: transformada inversa con λ = " + rate);
        System.out.println("  primeros 10 valores de X:");
        for (int i = 0; i < Math.min(10, x.length); i++) {
            System.out.printf(Locale.ROOT, "    X[%2d] = %.6f%n", i + 1, x[i]);
        }
        System.out.println("  cantidad de datos generados: " + x.length);
    }

    public static void showTable(List<Comparison> rows) {
        System.out.println();
        System.out.println("Algoritmos 4 y 5: medidas experimentales y teóricas");
        System.out.printf(Locale.ROOT, "%5s  %11s  %10s  %10s  %9s  %13s  %12s%n", "λ", "media teór.", "media exp.",
                "var. teór.", "var. exp.", "error media %", "error var. %");
        for (Comparison row : rows) {
            System.out.printf(Locale.ROOT, "%5s  %11.4f  %10.4f  %10.4f  %9.4f  %13.4f  %12.4f%n", row.label,
                    row.theoreticalMean, row.experimentalMean, row.theoreticalVariance, row.experimentalVariance,
                    row.meanErrorPct(), row.varianceErrorPct());
        }
    }

    public static void showOutput(String path) {
        System.out.println();
        System.out.println("CSV en " + path);
    }
}
