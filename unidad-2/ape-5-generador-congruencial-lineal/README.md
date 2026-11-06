# APE 5 — Implementación y análisis del Generador Congruencial Lineal en Python y Java

| | |
| --- | --- |
| **Asignatura** | Simulación — Universidad Nacional de Loja |
| **Docente** | Ing. José Guamán |
| **Unidad** | U2: Generación de números pseudoaleatorios y generación de variables aleatorias |
| **Práctica** | 05 — Implementación y análisis del Generador Congruencial Lineal en Python y Java |
| **Modalidad** | Individual |
| **Autor** | Alejandro Padilla |
| **Guía** | [guia/guia-ape-5.pdf](guia/guia-ape-5.pdf) |
| **Informe** | [documento/](documento/) |
| **Bibliografía** | [referencias.bib](referencias.bib) |

## 1. Enunciado y objetivo

Implementar el Generador Congruencial Lineal X(n+1) = (a · X(n) + c) mod m con a = 1664525, c = 1013904223,
m = 2³² y semilla 12345 en Python y en Java, generar 10 000 valores, comparar las primeras 20 observaciones de
ambos programas, graficar la secuencia, analizar el período y comparar los resultados al cambiar la semilla.

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| Claude (agente de código) | Estructura MVC, implementación Java, pruebas y gráficas |

## 3. Proceso con IA

1. Lectura de la guía y de las diapositivas de la semana 5
2. Pruebas del generador (primer valor calculado a mano, semilla, período)
3. Implementación del LCG en Python y en Java
4. Comparación de las secuencias y análisis del período con Hull-Dobell
5. Gráficas y comparación de semillas

## 4. Errores de la IA y correcciones

- La comparación con Java fallaba porque el JDK (instalado con mise) no tenía versión activa → se agregó
  `codigo/mise.toml` y Java se compila y ejecuta desde `codigo/`, así funciona desde cualquier carpeta.

## 5. Arquitectura del código

```text
codigo/
├── simulacion_ape/
│   ├── __main__.py                  # Delgado: solo llama al controlador
│   ├── model/
│   │   ├── config.py                # Parámetros a, c, m, semilla y n de la guía
│   │   ├── lcg.py                   # Recursión X(n+1) = (a·X(n) + c) mod m y normalización U(n) = X(n)/m
│   │   ├── period.py                # Condiciones de Hull-Dobell y medición del período
│   │   ├── java_runner.py           # Compila y ejecuta la versión Java
│   │   └── analysis.py              # Tabla Python vs Java, media, varianza, correlación
│   ├── view/
│   │   ├── console_view.py          # Tablas de consola
│   │   └── figures.py               # Gráficas en figuras/
│   └── controller/
│       └── simulation_controller.py # Orquesta modelo y vistas
├── java/Lcg.java                    # El mismo algoritmo en Java
└── tests/test_lcg.py                # 9 pruebas
```

El modelo no imprime ni grafica; la vista no calcula. Java se ejecuta como programa aparte y Python lee su salida,
así la comparación usa exactamente lo que produce cada lenguaje.

## 6. Ejecución

Requisitos: Python 3 (probado con 3.14) y un JDK (probado con Temurin 21).

```bash
cd codigo
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m simulacion_ape          # tabla, período, semillas; CSV en resultados/ y figuras en figuras/
pytest                            # 9 pruebas
```

La versión Java también corre sola: `javac -d build java/Lcg.java && java -cp build Lcg 1664525 1013904223 4294967296 12345 20`.

## 7. Resultados

- Python y Java producen la misma secuencia: 0 diferencias en los 10 000 valores (X1 = 87628868).
- Los parámetros cumplen las tres condiciones de Hull-Dobell: período completo 2³²; ningún valor se repite en la muestra.
- Con m = 16, a = 5 y c = 3 el período es 16; con a = 4 y c = 2 la secuencia se estanca (período 1).
- Con las semillas 12345, 54321 y 1 la media queda cerca de 0,5 y la varianza cerca de 1/12; la correlación entre
  valores consecutivos es cercana a 0.

El detalle está en el informe de [documento/](documento/).
