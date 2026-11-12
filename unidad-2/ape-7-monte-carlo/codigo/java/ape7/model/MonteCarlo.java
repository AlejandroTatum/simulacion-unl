package ape7.model;

/**
 * Los dos modelos Monte Carlo: el círculo inscrito (π) y la suma de dos dados.
 * Las operaciones siguen el mismo orden que en Python para contar los mismos aciertos.
 */
public final class MonteCarlo {
    public static final int DICE_TARGET = 7;

    private MonteCarlo() {
    }

    /** Lleva (u, v) al cuadrado [-1,1)² y revisa si cae en el círculo de radio 1. */
    public static boolean insideCircle(double u, double v) {
        double x = 2.0 * u - 1.0;
        double y = 2.0 * v - 1.0;
        return x * x + y * y <= 1.0;
    }

    /** Puntos que caen dentro del círculo inscrito (Nc). Cada punto gasta dos uniformes. */
    public static long countPiHits(Lcg generator, long n) {
        long hits = 0;
        for (long i = 0; i < n; i++) {
            double u = generator.nextUniform();
            double v = generator.nextUniform();
            if (insideCircle(u, v)) {
                hits++;
            }
        }
        return hits;
    }

    /** Transformada inversa de la uniforme discreta: D = ⌊6u⌋ + 1. */
    public static int dieFace(double u) {
        return (int) (6.0 * u) + 1;
    }

    /** Lanzamientos de dos dados cuya suma es 7. Cada lanzamiento gasta dos uniformes. */
    public static long countDiceHits(Lcg generator, long n) {
        long hits = 0;
        for (long i = 0; i < n; i++) {
            int first = dieFace(generator.nextUniform());
            int second = dieFace(generator.nextUniform());
            if (first + second == DICE_TARGET) {
                hits++;
            }
        }
        return hits;
    }
}
