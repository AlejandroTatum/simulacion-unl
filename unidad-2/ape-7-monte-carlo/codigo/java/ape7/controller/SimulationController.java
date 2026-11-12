package ape7.controller;

import ape7.model.Experiment;
import ape7.model.Lcg;
import ape7.view.ConsoleView;

/** Controlador: lee los parámetros, ejecuta el experimento y entrega el resultado a la vista. */
public final class SimulationController {
    /** Cada medición de tiempo se repite y se toma el mínimo, igual que en Python. */
    private static final int TIMING_REPEATS = 3;

    private SimulationController() {
    }

    public static void run(String[] args) {
        if (args.length != 6) {
            ConsoleView.showUsage();
            System.exit(2);
        }
        long a = Long.parseLong(args[0]);
        long c = Long.parseLong(args[1]);
        long m = Long.parseLong(args[2]);
        long seed = Long.parseLong(args[3]);
        long n = Long.parseLong(args[4]);
        Experiment experiment = Experiment.fromCode(args[5]);

        long hits = 0;
        long best = Long.MAX_VALUE;
        for (int i = 0; i < TIMING_REPEATS; i++) {
            long start = System.nanoTime();
            hits = experiment.countHits(new Lcg(a, c, m, seed), n);
            best = Math.min(best, System.nanoTime() - start);
        }

        double estimate = experiment.estimate(hits, n);
        ConsoleView.showResult(hits, estimate, experiment.error(estimate), best / 1e9);
    }
}
