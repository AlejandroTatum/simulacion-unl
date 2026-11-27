package ape9.controller;

import ape9.model.AcceptanceRejection;
import ape9.model.TargetDistribution;
import ape9.view.ConsoleView;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Controlador: lee los parámetros, ejecuta las simulaciones y guarda la tabla en CSV. */
public final class SimulationController {
    private static final long DEFAULT_SEED = 42L;
    private static final int[] SIZES = {1_000, 5_000, 10_000};
    private static final TargetDistribution[] TARGETS = {TargetDistribution.LINEAR, TargetDistribution.QUADRATIC};
    private static final String HEADER =
            "distribución,N,aceptados,rechazados,eficiencia_experimental,eficiencia_teorica,error_absoluto";

    private SimulationController() {
    }

    public static void run(String[] args) {
        long seed = args.length > 0 ? Long.parseLong(args[0]) : DEFAULT_SEED;
        Path resultsDir = Path.of(args.length > 1 ? args[1] : "resultados");

        // Cada simulación usa la misma semilla, igual que en Python.
        List<AcceptanceRejection> rows = new ArrayList<>();
        for (TargetDistribution target : TARGETS) {
            for (int n : SIZES) {
                rows.add(AcceptanceRejection.run(target, n, seed));
            }
        }

        ConsoleView.showHeader(seed);
        ConsoleView.showTable(rows);
        writeCsv(resultsDir.resolve("eficiencia-java.csv"), rows);
        ConsoleView.showOutput(resultsDir.toString());
    }

    private static void writeCsv(Path path, List<AcceptanceRejection> rows) {
        List<String> lines = new ArrayList<>();
        lines.add(HEADER);
        for (AcceptanceRejection row : rows) {
            lines.add(String.join(",", row.target.label, Integer.toString(row.n), Integer.toString(row.accepted),
                    Integer.toString(row.rejected), Double.toString(row.efficiency()),
                    Double.toString(row.target.theoreticalEfficiency()), Double.toString(row.absoluteError())));
        }
        try {
            Files.createDirectories(path.getParent());
            Files.write(path, lines, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}
