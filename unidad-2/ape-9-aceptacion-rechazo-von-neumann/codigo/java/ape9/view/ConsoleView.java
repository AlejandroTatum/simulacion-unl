package ape9.view;

import ape9.model.AcceptanceRejection;
import java.util.List;
import java.util.Locale;

/** Vista de consola: imprime la tabla de eficiencias. */
public final class ConsoleView {
    private ConsoleView() {
    }

    public static void showHeader(long seed) {
        System.out.println("APE 9 (Java): método de aceptación-rechazo de Von Neumann");
        System.out.println("distribución propuesta g(x) = 1   semilla = " + seed);
    }

    public static void showTable(List<AcceptanceRejection> rows) {
        System.out.println();
        System.out.printf(Locale.ROOT, "%-12s  %6s  %9s  %10s  %8s  %7s  %10s%n", "distribución", "N", "aceptados",
                "rechazados", "E exp. %", "ET %", "error abs.");
        for (AcceptanceRejection row : rows) {
            System.out.printf(Locale.ROOT, "%-12s  %6d  %9d  %10d  %8.2f  %7.2f  %10.2f%n", row.target.label, row.n,
                    row.accepted, row.rejected, row.efficiency(), row.target.theoreticalEfficiency(),
                    row.absoluteError());
        }
    }

    public static void showOutput(String path) {
        System.out.println();
        System.out.println("CSV en " + path);
    }
}
