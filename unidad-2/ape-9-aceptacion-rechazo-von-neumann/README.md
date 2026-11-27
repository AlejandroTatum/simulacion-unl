# APE 9 — Generación de variables aleatorias mediante el método de aceptación-rechazo de Von Neumann

| | |
| --- | --- |
| **Asignatura** | Simulación — Universidad Nacional de Loja |
| **Docente** | Ing. José Guamán |
| **Unidad** | U2: Generación de números pseudoaleatorios y generación de variables aleatorias |
| **Práctica** | 09 — Método de aceptación-rechazo de Von Neumann |
| **Modalidad** | Individual |
| **Autor** | Alejandro Padilla |
| **Guía** | [guia/guia-ape-9.pdf](guia/guia-ape-9.pdf) |
| **Informe** | [documento/](documento/) |
| **Bibliografía** | [referencias.bib](referencias.bib) |

## 1. Enunciado y objetivo

Implementar y analizar el método de aceptación-rechazo de Von Neumann para generar variables aleatorias con una
distribución objetivo a partir de una distribución propuesta. Se implementa en Python y en Java el algoritmo
ACEPTACION_RECHAZO de la guía:

1. Se generan N candidatos; en cada repetición se genera X ~ U(0,1) y luego U ~ U(0,1).
2. Se calcula `R = f(X) / (M·g(X))` con la propuesta `g(x) = 1`.
3. Si `U ≤ R` se guarda X y se cuenta como aceptado; si no, se cuenta como rechazado.
4. Eficiencia `E = (aceptados / N)·100`, comparada con la teórica `ET = (1/M)·100`.

Distribuciones objetivo en 0 ≤ x ≤ 1:

| Distribución | M | Criterio | ET |
| --- | ---: | --- | ---: |
| `f(x) = 2x` (guía) | 2 | U ≤ X | 50 % |
| `f(x) = 3x²` (actividad complementaria) | 3 | U ≤ X² | 33.33 % |

Se hacen tres simulaciones (N = 1 000, 5 000 y 10 000) por distribución. La semilla es configurable (por defecto
42) y cada simulación parte de la misma semilla.

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| el Gentleman (entorno Pi), con un modelo Claude de Anthropic | Leer la guía, escribir el código y las pruebas, generar las gráficas y la tabla, y redactar el informe |

## 3. Proceso con IA

1. Lectura de la guía y plan de la práctica.
2. Pruebas del criterio de aceptación y de la eficiencia.
3. Implementación MVC en Python y Java.
4. Gráficas y tabla de eficiencias.
5. Informe.

## 4. Errores de la IA y correcciones

- La leyenda de la gráfica de aceptados y rechazados tapaba puntos; se amplió el eje vertical sobre la cota M.

## 5. Arquitectura del código

```
codigo/
├── simulacion_ape/                     # Python
│   ├── __main__.py                     # entrada: solo llama al controlador
│   ├── model/
│   │   ├── config.py                   # semilla y valores de N
│   │   ├── distributions.py            # f(x) = 2x y 3x², g(x) = 1, M y eficiencia teórica
│   │   ├── acceptance_rejection.py     # algoritmo ACEPTACION_RECHAZO y criterio U ≤ R
│   │   └── simulation.py               # tres simulaciones por distribución
│   ├── view/
│   │   ├── console_view.py             # tabla en consola
│   │   └── figures.py                  # histograma con f(x), aceptados/rechazados y eficiencias
│   └── controller/
│       └── simulation_controller.py
├── java/ape9/                          # Java
│   ├── Main.java                       # entrada: solo llama al controlador
│   ├── model/{TargetDistribution,AcceptanceRejection}.java
│   ├── view/ConsoleView.java
│   └── controller/SimulationController.java
├── tests/test_acceptance_rejection.py  # 23 pruebas (incluye la ejecución de Java)
├── figuras/                            # gráficas del informe
└── resultados/                         # tablas en CSV de Python y de Java
```

El modelo no imprime ni grafica, las vistas no calculan y el controlador solo coordina; en los dos lenguajes se
mantiene la misma separación.

## 6. Ejecución

```bash
cd codigo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m simulacion_ape                 # consola, CSV en resultados/ y figuras en figuras/
python -m simulacion_ape --seed 7 --no-figures
python -m pytest                         # pruebas
```

Java (parámetros opcionales: semilla y carpeta de resultados):

```bash
javac -d build $(find java -name '*.java')
java -cp build ape9.Main 42 resultados
```

## 7. Resultados

Semilla 42 (Python: `numpy.random.default_rng`; Java: `java.util.Random`, por eso los números difieren). El error
absoluto es |E − ET| en puntos porcentuales.

| Distribución | N | Aceptados Python | Rechazados Python | E Python % | Aceptados Java | Rechazados Java | E Java % | ET % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| f(x) = 2x | 1 000 | 482 | 518 | 48.20 | 504 | 496 | 50.40 | 50.00 |
| f(x) = 2x | 5 000 | 2 505 | 2 495 | 50.10 | 2 474 | 2 526 | 49.48 | 50.00 |
| f(x) = 2x | 10 000 | 5 022 | 4 978 | 50.22 | 4 945 | 5 055 | 49.45 | 50.00 |
| f(x) = 3x² | 1 000 | 326 | 674 | 32.60 | 335 | 665 | 33.50 | 33.33 |
| f(x) = 3x² | 5 000 | 1 651 | 3 349 | 33.02 | 1 622 | 3 378 | 32.44 | 33.33 |
| f(x) = 3x² | 10 000 | 3 350 | 6 650 | 33.50 | 3 257 | 6 743 | 32.57 | 33.33 |

La eficiencia experimental queda a menos de 2 puntos de la teórica en todos los casos. Con M = 3 se rechazan dos de
cada tres candidatos, frente a uno de cada dos con M = 2: cuanto mayor es M, menos eficiente es el método. La media
de los valores aceptados con N = 10 000 (Python) es 0.6668 para 2x (teórica 2/3) y 0.7457 para 3x² (teórica 3/4).

Figuras (N = 10 000):
[histograma-lineal.png](codigo/figuras/histograma-lineal.png),
[aceptados-rechazados-lineal.png](codigo/figuras/aceptados-rechazados-lineal.png),
[histograma-cuadratica.png](codigo/figuras/histograma-cuadratica.png),
[aceptados-rechazados-cuadratica.png](codigo/figuras/aceptados-rechazados-cuadratica.png) y
[comparativa-eficiencia.png](codigo/figuras/comparativa-eficiencia.png).
