package ape7.view;

/** Vista: imprime los resultados como líneas clave=valor, que el programa Python lee. */
public final class ConsoleView {
    private ConsoleView() {
    }

    public static void showResult(long hits, double estimate, double error, double seconds) {
        System.out.println("aciertos=" + hits);
        System.out.println("estimacion=" + estimate);
        System.out.println("error=" + error);
        System.out.println("tiempo_s=" + seconds);
    }

    public static void showUsage() {
        System.err.println("Uso: java ape7.Main a c m semilla n experimento   (experimento: pi | dados)");
    }
}
