# APE 7 — Estimación de resultados mediante el método de Monte Carlo

| | |
| --- | --- |
| **Asignatura** | Simulación — Universidad Nacional de Loja |
| **Docente** | Ing. José Guamán |
| **Unidad** | U2: Generación de números pseudoaleatorios y generación de variables aleatorias |
| **Práctica** | 07 — Estimación de resultados mediante el método de Monte Carlo |
| **Modalidad** | Individual |
| **Autor** | Alejandro Padilla |
| **Guía** | [guia/guia-ape-7.pdf](guia/guia-ape-7.pdf) |
| **Informe** | [documento/](documento/) |
| **Bibliografía** | [referencias.bib](referencias.bib) |

## 1. Enunciado y objetivo

Aplicar el método de Monte Carlo en Python y en Java, con tamaños de muestra de 1 000 a 1 000 000, y comparar la
estimación, el error absoluto y el tiempo de ambos programas. Se resuelven dos modelos:

- **π con el círculo inscrito** (el de la guía): `π ≈ 4 · Nc / N`.
- **Suma de dos dados** (el modelo elegido para la práctica): `P(D1 + D2 = 7) = 6/36 = 1/6`, con cada dado generado
  por transformada inversa, `D = ⌊6u⌋ + 1`.

Los dos programas usan el mismo generador congruencial lineal (a = 1664525, c = 1013904223, m = 2³², semilla 12345),
así que recorren la misma secuencia y cuentan los mismos aciertos; solo cambia el tiempo.

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| el Gentleman (entorno Pi), con un modelo Claude de Anthropic | Leer la guía, proponer el modelo, escribir el código y las pruebas, generar las gráficas y redactar el informe |

## 3. Proceso con IA

1. Lectura de la guía y explicación de la práctica.
2. Indicación de trabajar todo en MVC y de añadir un modelo matemático propio.
3. Elección del modelo de los dados y explicación de su planteamiento.
4. Pruebas primero, luego el modelo en Python, el mismo modelo en Java y la comparación automática.
5. Informe con verificación independiente y revisión del autor.

## 4. Errores de la IA y correcciones

- La primera propuesta eran scripts sueltos; se corrigió a MVC en los dos lenguajes.
- Se propuso una vista con ventana; se dejó la vista de consola y las gráficas, igual que en las APE 5 y 6.
- En la gráfica de las sumas, la leyenda tapaba la barra del 7; se amplió el eje vertical.

## 5. Arquitectura del código

```
codigo/
├── simulacion_ape/                 # Python
│   ├── __main__.py                 # entrada: solo llama al controlador
│   ├── model/
│   │   ├── lcg.py                  # generador congruencial lineal
│   │   ├── monte_carlo.py          # los dos modelos: círculo y dados
│   │   ├── config.py               # parámetros, tamaños y experimentos
│   │   ├── measurement.py          # resultado de una ejecución
│   │   ├── experiment.py           # ejecuta Python y Java y junta los resultados
│   │   └── java_runner.py          # compila y ejecuta la versión Java
│   ├── view/
│   │   ├── console_view.py         # tablas de consola
│   │   └── figures.py              # gráficas
│   └── controller/
│       └── simulation_controller.py
├── java/ape7/                      # Java
│   ├── Main.java                   # entrada: solo llama al controlador
│   ├── model/{Lcg,MonteCarlo,Experiment}.java
│   ├── view/ConsoleView.java
│   └── controller/SimulationController.java
├── tests/test_monte_carlo.py       # 18 pruebas
└── figuras/                        # gráficas del informe
```

## 6. Ejecución

```bash
cd codigo
pip install -r requirements.txt
python -m simulacion_ape            # ejecuta Python y Java, imprime las tablas y guarda CSV y figuras
python -m simulacion_ape --no-figures
python -m pytest                    # pruebas
```

Solo Java (parámetros: a c m semilla n experimento, con experimento `pi` o `dados`):

```bash
javac -d build $(find java -name '*.java')
java -cp build ape7.Main 1664525 1013904223 4294967296 12345 1000000 pi
```

## 7. Resultados

| N | π estimado | Error | P(suma = 7) estimada | Error | Python (s) | Java (s) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 000 | 3.188000 | 0.046407 | 0.165000 | 0.001667 | 0.000478 | 0.000077 |
| 10 000 | 3.151600 | 0.010007 | 0.163300 | 0.003367 | 0.004860 | 0.000673 |
| 100 000 | 3.133240 | 0.008353 | 0.166870 | 0.000203 | 0.048731 | 0.001317 |
| 1 000 000 | 3.141948 | 0.000355 | 0.167162 | 0.000495 | 0.519410 | 0.011249 |

Los tiempos son los del experimento de π. Python y Java contaron los mismos aciertos en los ocho casos.
El error baja en proporción a 1/√N, pero no en cada ejecución: en los dados, 100 000 lanzamientos dieron mejor
resultado que 1 000 000.
