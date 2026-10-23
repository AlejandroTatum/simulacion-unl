# APE 4 — Análisis comparativo de herramientas de simulación mediante un modelo común (SIR)

| | |
| --- | --- |
| **Asignatura** | Simulación — Universidad Nacional de Loja |
| **Docente** | Ing. José Guamán |
| **Unidad** | U1: Introducción a la Simulación |
| **Práctica** | 04 — Análisis comparativo de herramientas de simulación mediante un modelo común |
| **Modalidad** | Individual |
| **Autor** | Alejandro Padilla |
| **Repositorio del grupo** | [AlejandroTatum/simulacion-ape-4-sir](https://github.com/AlejandroTatum/simulacion-ape-4-sir) |
| **Informe** | [documento/](documento/) |
| **Bibliografía** | [referencias.bib](referencias.bib) |

## 1. Enunciado y objetivo

Comparar Python con SimPy y NetLogo como herramientas de simulación mediante un mismo modelo epidemiológico SIR: población 100, 5 infectados iniciales, β = 0.30, γ = 0.10 y 100 pasos de tiempo (R₀ = β/γ = 3). Python genera los datos, NetLogo ejecuta su propia simulación por agentes e importa el CSV de Python para graficarlo y compararlo.

- Implementar el modelo SIR por individuos en Python/SimPy y en NetLogo con los mismos parámetros y la misma regla de contagio.
- Integrar ambas herramientas con un CSV (`tiempo,susceptibles,infectados,recuperados`, 101 filas).
- Comparar resultados (una corrida, 30 réplicas y las ecuaciones diferenciales), analizar el efecto de los números aleatorios y completar la tabla comparativa de la guía.

Alcance: la guía también menciona Java; por decisión del grupo y del alcance acordado con el docente **no se implementó**. La comparación es entre dos herramientas.

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| Agente de programación el Gentleman (Pi) con modelo Claude | Lectura de la guía, modelo SimPy con MVC y pruebas, modelo NetLogo, réplicas y tiempos, figuras e informe. |

La IA ejecutó; las decisiones de alcance (sin Java), regla de contacto, semilla y contenido las tomé yo.

## 3. Proceso con IA

1. Entender la guía y fijar el alcance
2. Regla de contacto común y parámetros
3. Modelo SimPy con arquitectura MVC
4. Modelo NetLogo con importación del CSV
5. Comparación Python y NetLogo, réplicas y tiempos
6. Descarte de Java
7. Informe individual
8. Mejora visual de NetLogo: personas, escenario y animación

## 4. Errores de la IA y correcciones

- **Java descartado:** la IA llegó a implementar una versión en Java (semilla 42: pico 29 en t = 31) que no entraba en el alcance; se eliminó la carpeta `java/` y `resultados_java.csv`, y el informe compara solo Python y NetLogo.
- **Semilla de NetLogo 12345 → 42:** el campo `seed` del modelo traía 12345, distinta de la de Python; se igualó a 42 y se verificó que la corrida da pico 31 en t = 17.
- **NetLogo abierto como modelo vacío:** NetLogo se había iniciado sin cargar ningún archivo y mostraba un modelo nuevo; se abre con **Archivo → Abrir** sobre `netlogo/modelo_sir_netlogo.nlogox` (o `.nlogo`) y lo comprobé con SETUP, GO y CARGAR PYTHON.
- **Movimiento de NetLogo y números aleatorios:** al animar a las personas había que evitar que el dibujo cambiara la epidemia. El movimiento anterior (`rt random 360`) y los `ask` consumían el generador principal, así que se movió todo lo visual a `with-local-randomness` y se conservó un único sorteo heredado; la comprobación fue `cmp` del CSV de la semilla 42 contra el anterior (idéntico con y sin animación, en `.nlogox` y `.nlogo`).

## 5. Arquitectura del código

```text
codigo/simulacion_ape/
├── __main__.py                  # Delgado: solo llama al controlador
├── model/
│   ├── config.py                # Parámetros comunes, semilla y rutas
│   ├── sir_model.py             # Modelo SIR por individuos con proceso de SimPy
│   ├── simulation.py            # Corrida cronometrada y escritura del CSV
│   ├── replications.py          # Réplicas (semillas 0..n-1) y banda del 95 %
│   ├── ode.py                   # Referencia de las ecuaciones (Euler y RK4)
│   ├── analysis.py              # Pico de infectados y recuperados finales
│   └── csv_io.py                # Lectura y escritura del CSV de la guía
├── view/
│   ├── figures.py               # Figuras de Matplotlib
│   └── console_view.py          # Resumen en consola
└── controller/
    └── simulation_controller.py # Argumentos y orquestación de modelo y vistas
netlogo/                         # Modelo NetLogo (.nlogox / .nlogo) y CSV de intercambio
```

MVC separa el modelo de la presentación: las pruebas (9) comprueban la simulación sin dibujar nada, y NetLogo solo conoce el contrato del CSV, no el código de Python.

## 6. Ejecución

```bash
cd codigo
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m simulacion_ape         # CSV en netlogo/, figuras en figuras/ y resumen
pytest                           # 9 pruebas
```

El modelo de NetLogo se abre desde `netlogo/modelo_sir_netlogo.nlogox` (ver [netlogo/README.md](netlogo/README.md)).

## 7. Resultados

Semilla 42 y 30 réplicas (semillas 0 a 29); media ± desviación estándar entre réplicas.

| Métrica | Python (semilla 42) | NetLogo (semilla 42) | Python (30 réplicas) | NetLogo (30 réplicas) | Ecuaciones (Euler) |
| --- | --- | --- | --- | --- | --- |
| Pico de infectados | 36 | 31 | 36.13 ± 6.99 | 35.33 ± 6.93 | 33.0 |
| Instante del pico | 21 | 17 | 19.33 ± 5.06 | 18.83 ± 5.43 | 19 |
| Susceptibles finales | 6 | 7 | 6.67 ± 5.44 | 8.23 ± 6.46 | 5.0 |
| Recuperados finales | 93 | 93 | 93.27 ± 5.46 | 91.77 ± 6.46 | 95.0 |

- Con la misma semilla las herramientas dan corridas distintas (generadores PCG64 y Mersenne Twister, y distinto orden de consumo); con 30 réplicas los promedios coinciden (t de Welch menor que 1.1 en las cuatro métricas).
- Tiempo por corrida: Python 4.5 ms (mediana de 30 corridas; 18 a 30 ms la primera) y NetLogo 34 ms con `animacion?` apagado (250 a 270 ms la primera); proceso completo 0.3 s frente a 2 a 3 s por el arranque de la JVM.
- La parte visual de NetLogo (personas que caminan en una plaza, contagios como líneas rojas) corre dentro de `with-local-randomness`: el CSV de la semilla 42 es idéntico byte a byte con o sin animación y al de la versión anterior.
- Las 30 réplicas de NetLogo y los tiempos se obtuvieron con un experimento de BehaviorSpace adicional ejecutado sin interfaz; el modelo entregado incluye solo el experimento `ejecucion-completa` (semilla 42).
- `figuras/netlogo_vista.png` se compuso con la vista del mundo (personas en una plaza, con líneas rojas de contagio) exportada por NetLogo (`export-view` en los ticks 0, 17 y 100); `export-interface` no funciona sin interfaz, por lo que falta una captura de la ventana completa con los gráficos.

El análisis completo, la tabla comparativa y las preguntas de control están en el informe de `documento/`.
