package ape6;

import ape6.controller.SimulationController;

/**
 * Punto de entrada delgado: solo llama al controlador.
 *
 * Uso:
 *   java -cp build ape6.Main <a> <c> <m> <semilla> <n>              estadísticos, valores p y tiempo
 *   java -cp build ape6.Main <a> <c> <m> <semilla> <n> secuencia    imprime X1..Xn, uno por línea
 */
public final class Main {

    private Main() {
    }

    public static void main(String[] args) {
        SimulationController.run(args);
    }
}
