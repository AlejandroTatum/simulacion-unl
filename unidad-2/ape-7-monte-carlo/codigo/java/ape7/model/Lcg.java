package ape7.model;

/** Generador congruencial lineal: X(n+1) = (a * X(n) + c) mod m, U = X / m. */
public final class Lcg {
    private final long a;
    private final long c;
    private final long m;
    private long state;

    public Lcg(long a, long c, long m, long seed) {
        this.a = a;
        this.c = c;
        this.m = m;
        this.state = seed;
    }

    /** Siguiente estado entero. El producto cabe en un long porque a < 2^31 y X < 2^32. */
    public long nextState() {
        state = Math.floorMod(a * state + c, m);
        return state;
    }

    /** Siguiente uniforme U = X / m, siempre en [0, 1). */
    public double nextUniform() {
        return (double) nextState() / m;
    }
}
