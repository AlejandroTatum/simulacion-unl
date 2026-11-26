package ape8;

import ape8.controller.SimulationController;

/**
 * Punto de entrada delgado: solo llama al controlador.
 *
 * Uso: java ape8.Main [semilla] [n] [carpeta_resultados]
 * (por defecto: 42, 10000 y resultados).
 */
public final class Main {
    private Main() {
    }

    public static void main(String[] args) {
        SimulationController.run(args);
    }
}
