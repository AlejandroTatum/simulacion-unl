package ape6.controller;

import ape6.model.Lcg;
import ape6.model.UniformityTests;
import ape6.model.UniformityTests.ChiSquareResult;
import ape6.model.UniformityTests.KsResult;
import ape6.view.ConsoleView;

/** Controlador: lee los parámetros, coordina el modelo y pasa los resultados a la vista. */
public final class SimulationController {

    private static final int TIMING_REPEATS = 3;

    private SimulationController() {
    }

    public static void run(String[] args) {
        long a = Long.parseLong(args[0]);
        long c = Long.parseLong(args[1]);
        long m = Long.parseLong(args[2]);
        long seed = Long.parseLong(args[3]);
        int n = Integer.parseInt(args[4]);

        if (args.length > 5 && args[5].equals("secuencia")) {
            ConsoleView.showStates(Lcg.states(a, c, m, seed, n));
            return;
        }

        // Se mide generación + ambas pruebas, igual que en Python, y se informa la menor de las repeticiones.
        ChiSquareResult chi = null;
        KsResult ks = null;
        long best = Long.MAX_VALUE;
        for (int r = 0; r < TIMING_REPEATS; r++) {
            long start = System.nanoTime();
            double[] values = Lcg.generate(a, c, m, seed, n);
            chi = UniformityTests.chiSquare(values);
            ks = UniformityTests.kolmogorovSmirnov(values);
            best = Math.min(best, System.nanoTime() - start);
        }
        ConsoleView.showResults(chi, ks, best / 1e9);
    }
}
