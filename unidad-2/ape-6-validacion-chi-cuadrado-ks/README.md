# APE 6 — Validación estadística de números pseudoaleatorios mediante Chi-cuadrado y Kolmogorov-Smirnov

| | |
| --- | --- |
| **Asignatura** | Simulación — Universidad Nacional de Loja |
| **Docente** | Ing. José Guamán |
| **Unidad** | U2: Generación de números pseudoaleatorios y generación de variables aleatorias |
| **Práctica** | 06 — Validación estadística de números pseudoaleatorios mediante Chi-cuadrado y Kolmogorov-Smirnov |
| **Modalidad** | Individual |
| **Autor** | Alejandro Padilla |
| **Guía** | [guia/guia-ape-6.pdf](guia/guia-ape-6.pdf) |
| **Informe** | [documento/](documento/) |
| **Bibliografía** | [referencias.bib](referencias.bib) |

## 1. Enunciado y objetivo

Generar números pseudoaleatorios con el método congruencial lineal (LCG) en Python y en Java y evaluar su
uniformidad en [0, 1) con las pruebas Chi-cuadrado (10 subintervalos, gl = 9) y Kolmogorov-Smirnov, con α = 0.05.
Se comparan cuatro configuraciones del generador y tamaños de muestra de 1 000 a 1 000 000, con los tiempos de
ambos programas.

La tabla de resultados esperados de la guía pide "π estimado" y "Error", columnas de una estimación por Monte Carlo
que ningún paso de esta práctica produce. Siguiendo la tabla del ejemplo computacional de las diapositivas de la
semana 6 (diapositiva 18), se reemplazaron por χ², p, D y p, manteniendo N y los tiempos de Python y Java.

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| Claude (agente de código) | Estructura MVC en Python y Java, pruebas estadísticas, pruebas automáticas, gráficas e informe |

## 3. Proceso con IA

1. Lectura de la guía y detección de la tabla de π, que no corresponde a esta práctica
2. Revisión de las diapositivas de la semana 6: no estiman π; la diapositiva 18 da la tabla modelo
3. Implementación del LCG, Chi-cuadrado y Kolmogorov-Smirnov en Python y en Java con las mismas fórmulas
4. Comparación de configuraciones y de tamaños de muestra, con tiempos de ambos programas
5. Redacción del informe, preguntas de control y conclusiones

## 4. Errores de la IA y correcciones

- La primera versión de Java era una sola clase. Se dividió en modelo, vista y controlador, igual que Python;
  los resultados quedaron idénticos.
- La primera conclusión decía que con N = 200 el generador de módulo pequeño no se detectaba. Era cierto solo para
  Kolmogorov-Smirnov (p = 0.356); Chi-cuadrado sí lo rechaza (χ² = 19.0, p = 0.025). Se corrigió en el informe.

## 5. Arquitectura del código

```text
codigo/
├── simulacion_ape/
│   ├── __main__.py                  # Delgado: solo llama al controlador
│   ├── model/
│   │   ├── config.py                # Configuraciones del LCG, tamaños, k = 10 y α = 0.05
│   │   ├── lcg.py                   # X(n+1) = (a·X(n) + c) mod m y U(n) = X(n)/m
│   │   ├── distributions.py         # Valores p sin librerías (gamma incompleta, serie de Kolmogorov)
│   │   ├── uniformity.py            # Pruebas Chi-cuadrado y Kolmogorov-Smirnov, criterio de decisión
│   │   ├── java_runner.py           # Compila y ejecuta la versión Java
│   │   └── experiment.py            # Configuraciones y tamaños en Python y Java, con tiempos
│   ├── view/
│   │   ├── console_view.py          # Tablas de consola
│   │   └── figures.py               # Gráficas en figuras/
│   └── controller/
│       └── simulation_controller.py # Orquesta modelo y vistas, escribe los CSV
├── java/ape6/
│   ├── Main.java                    # Delgado: solo llama al controlador
│   ├── model/                       # Lcg, Distributions, UniformityTests
│   ├── view/ConsoleView.java        # Salida clave=valor que lee Python
│   └── controller/SimulationController.java
└── tests/test_pruebas.py            # 26 pruebas (SciPy solo para contrastar los valores p)
```

El modelo no imprime ni grafica; la vista no calcula. Java se ejecuta como programa aparte y Python lee su salida,
así la comparación usa exactamente lo que produce cada lenguaje.

## 6. Ejecución

Requisitos: Python 3 (probado con 3.14) y un JDK (probado con Temurin 21).

```bash
cd codigo
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m simulacion_ape          # tablas; CSV en resultados/ y figuras en figuras/
pytest                            # 26 pruebas
```

La versión Java también corre sola:
`javac -d build $(find java -name '*.java') && java -cp build ape6.Main 1103515245 12345 4294967296 1 10000`.

## 7. Resultados

- Python y Java producen la misma secuencia (0 diferencias) y los mismos estadísticos en las cuatro configuraciones.
- El LCG de glibc reproduce el ejemplo de las diapositivas: χ² = 2.44, p = 0.983, D = 0.0071.
- glibc, APE 5 y RANDU no se rechazan; el módulo pequeño (m = 16) se rechaza con ambas pruebas (χ² = 937.50).
- RANDU pasa ambas pruebas aunque sus tríos caen en 15 planos: una prueba no demuestra aleatoriedad.
- Con 1 000 000 de números, Java es unas 8 veces más rápido que Python.

El detalle está en el informe de [documento/](documento/).
