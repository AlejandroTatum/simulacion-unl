package ape8.controller;

import ape8.model.Comparison;
import ape8.model.InverseTransform;
import ape8.view.ConsoleView;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Controlador: lee los parámetros, ejecuta los algoritmos y guarda la tabla en CSV. */
public final class SimulationController {
    private static final long DEFAULT_SEED = 42L;
    private static final int DEFAULT_N = 10_000;
    private static final double RATE = 0.5;
    private static final double[] RATES = {0.5, 1.0, 2.0};
    private static final String HEADER =
            "media_teorica,media_experimental,varianza_teorica,varianza_experimental,error_media_pct,error_varianza_pct";

    private SimulationController() {
    }

    public static void run(String[] args) {
        long seed = args.length > 0 ? Long.parseLong(args[0]) : DEFAULT_SEED;
        int n = args.length > 1 ? Integer.parseInt(args[1]) : DEFAULT_N;
        Path resultsDir = Path.of(args.length > 2 ? args[2] : "resultados");

        // Los mismos U se transforman con cada lambda, como indica la guía.
        double[] u = InverseTransform.generateUniforms(n, seed);
        Comparison uniform = Comparison.uniform(u);
        double[] x = InverseTransform.inverseExponential(u, RATE);

        List<Comparison> table = new ArrayList<>();
        for (double rate : RATES) {
            table.add(Comparison.exponential(InverseTransform.inverseExponential(u, rate), rate));
        }

        ConsoleView.showHeader(n, seed);
        ConsoleView.showUniform(uniform);
        ConsoleView.showSample(x, RATE);
        ConsoleView.showTable(table);

        writeCsv(resultsDir.resolve("tabla-lambda-java.csv"), "lambda", table);
        writeCsv(resultsDir.resolve("uniforme-java.csv"), "distribucion", List.of(uniform));
        ConsoleView.showOutput(resultsDir.toString());
    }

    private static void writeCsv(Path path, String key, List<Comparison> rows) {
        List<String> lines = new ArrayList<>();
        lines.add(key + "," + HEADER);
        for (Comparison row : rows) {
            // "U(0,1)" contiene una coma, por eso la etiqueta va entre comillas.
            String label = row.label.contains(",") ? "\"" + row.label + "\"" : row.label;
            lines.add(String.join(",", label, Double.toString(row.theoreticalMean),
                    Double.toString(row.experimentalMean), Double.toString(row.theoreticalVariance),
                    Double.toString(row.experimentalVariance), Double.toString(row.meanErrorPct()),
                    Double.toString(row.varianceErrorPct())));
        }
        try {
            Files.createDirectories(path.getParent());
            Files.write(path, lines, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}
