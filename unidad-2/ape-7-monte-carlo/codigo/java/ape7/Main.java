package ape7;

import ape7.controller.SimulationController;

/**
 * Punto de entrada delgado: solo llama al controlador.
 *
 * Uso: java ape7.Main a c m semilla n experimento
 * donde experimento es "pi" o "dados".
 */
public final class Main {
    private Main() {
    }

    public static void main(String[] args) {
        SimulationController.run(args);
    }
}
