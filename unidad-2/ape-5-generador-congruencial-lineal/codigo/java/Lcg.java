/**
 * Generador Congruencial Lineal en Java: X(n+1) = (a * X(n) + c) mod m.
 *
 * Uso: java Lcg <a> <c> <m> <semilla> <n>
 * Imprime una línea por valor generado: n;X(n);U(n)
 */
public class Lcg {

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

    /** Avanza un paso. a * X cabe en un long porque a < 2^21 y X < 2^32. */
    public long next() {
        state = Math.floorMod(a * state + c, m);
        return state;
    }

    public double normalize(long x) {
        return (double) x / m;
    }

    public static void main(String[] args) {
        long a = Long.parseLong(args[0]);
        long c = Long.parseLong(args[1]);
        long m = Long.parseLong(args[2]);
        long seed = Long.parseLong(args[3]);
        int n = Integer.parseInt(args[4]);

        Lcg generator = new Lcg(a, c, m, seed);
        StringBuilder out = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            long x = generator.next();
            out.append(i).append(';').append(x).append(';').append(generator.normalize(x)).append('\n');
        }
        System.out.print(out);
    }
}
