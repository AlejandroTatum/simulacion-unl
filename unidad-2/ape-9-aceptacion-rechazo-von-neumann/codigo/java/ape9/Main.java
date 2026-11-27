package ape9;

import ape9.controller.SimulationController;

/**
 * Punto de entrada delgado: solo llama al controlador.
 *
 * Uso: java ape9.Main [semilla] [carpeta_resultados]
 * (por defecto: 42 y resultados).
 */
public final class Main {
    private Main() {
    }

    public static void main(String[] args) {
        SimulationController.run(args);
    }
}
