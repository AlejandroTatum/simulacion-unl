package ape7.model;

/** Un modelo Monte Carlo: estimador = scale · aciertos / N. */
public enum Experiment {
    PI("pi", Math.PI, 4.0) {
        @Override
        public long countHits(Lcg generator, long n) {
            return MonteCarlo.countPiHits(generator, n);
        }
    },
    DICE("dados", 6.0 / 36, 1.0) {
        @Override
        public long countHits(Lcg generator, long n) {
            return MonteCarlo.countDiceHits(generator, n);
        }
    };

    private final String code;
    private final double exact;
    private final double scale;

    Experiment(String code, double exact, double scale) {
        this.code = code;
        this.exact = exact;
        this.scale = scale;
    }

    public abstract long countHits(Lcg generator, long n);

    public double estimate(long hits, long n) {
        return scale * hits / n;
    }

    /** Error absoluto |valor real − estimación|. */
    public double error(double estimate) {
        return Math.abs(exact - estimate);
    }

    public static Experiment fromCode(String code) {
        for (Experiment experiment : values()) {
            if (experiment.code.equals(code)) {
                return experiment;
            }
        }
        throw new IllegalArgumentException("Experimento desconocido: " + code + " (use pi o dados)");
    }
}
