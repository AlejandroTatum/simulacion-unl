# APE 8 — Generación de variables aleatorias mediante el método de Transformada Inversa

| | |
| --- | --- |
| **Asignatura** | Simulación — Universidad Nacional de Loja |
| **Docente** | Ing. José Guamán |
| **Unidad** | U2: Generación de números pseudoaleatorios y generación de variables aleatorias |
| **Práctica** | 08 — Generación de variables aleatorias mediante el método de Transformada Inversa |
| **Modalidad** | Individual |
| **Autor** | Alejandro Padilla |
| **Guía** | [guia/guia-ape-8.pdf](guia/guia-ape-8.pdf) |
| **Informe** | [documento/](documento/) |
| **Bibliografía** | [referencias.bib](referencias.bib) |

## 1. Enunciado y objetivo

Implementar el método de la Transformada Inversa para generar variables aleatorias con una distribución dada:
generar uniformes U(0,1) y exponenciales, aplicar la inversa de la función acumulada y comparar las muestras con las
distribuciones teóricas. Se implementan en Python y en Java los cinco algoritmos de la guía:

1. **Generar_Uniformes**: N = 10 000 uniformes, su media y varianza (teóricas 1/2 y 1/12) y su histograma.
2. **Transformada_Inversa**: `X = −ln(1 − U) / λ` con λ = 0.5 (se rechaza λ ≤ 0); muestra los 10 primeros valores
   y la cantidad generada.
3. **Comparar_Distribuciones**: histograma de X con la densidad teórica `f(x) = λ·e^(−λx)`.
4. **Comparar_Estadisticas**: media y varianza experimentales frente a `1/λ` y `1/λ²`, con error porcentual.
5. **Comparar_Valores_Lambda**: λ = 0.5, 1.0 y 2.0 en una gráfica comparativa.

La semilla es configurable (por defecto 42). Como indica la guía, los mismos U se transforman con cada λ.

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| el Gentleman (entorno Pi), con un modelo Claude de Anthropic | Leer la guía, escribir el código y las pruebas, generar las gráficas y la tabla, y redactar el informe |

## 3. Proceso con IA

1. Lectura de la guía y plan de la práctica.
2. Implementación MVC en Python y Java.
3. Gráficas y tabla comparativa.
4. Informe.

## 4. Errores de la IA y correcciones

- Los títulos de las gráficas perdían la coma de "U(0,1)" al dar formato al separador de miles; se corrigió el
  formato.
- El CSV de Java escribía la etiqueta "U(0,1)" sin comillas y la coma partía la columna; ahora va entre comillas.

## 5. Arquitectura del código

```
codigo/
├── simulacion_ape/                 # Python
│   ├── __main__.py                 # entrada: solo llama al controlador
│   ├── model/
│   │   ├── config.py               # N, semilla, λ y tasas
│   │   ├── inverse_transform.py    # uniformes, X = −ln(1 − U)/λ y densidad teórica
│   │   ├── analysis.py             # media, varianza y errores porcentuales
│   │   └── simulation.py           # ejecuta los algoritmos 1, 2, 4 y 5
│   ├── view/
│   │   ├── console_view.py         # salida de consola
│   │   └── figures.py              # histogramas y gráfica comparativa
│   └── controller/
│       └── simulation_controller.py
├── java/ape8/                      # Java
│   ├── Main.java                   # entrada: solo llama al controlador
│   ├── model/{InverseTransform,Comparison}.java
│   ├── view/ConsoleView.java
│   └── controller/SimulationController.java
├── tests/test_inverse_transform.py # 21 pruebas (incluye la ejecución de Java)
├── figuras/                        # gráficas del informe
└── resultados/                     # tablas en CSV de Python y de Java
```

El modelo no imprime ni grafica, las vistas no calculan y el controlador solo coordina; en los dos lenguajes se
mantiene la misma separación.

## 6. Ejecución

```bash
cd codigo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m simulacion_ape                 # consola, CSV en resultados/ y figuras en figuras/
python -m simulacion_ape --seed 7 --n 10000 --no-figures
python -m pytest                         # pruebas
```

Java (parámetros opcionales: semilla, N y carpeta de resultados):

```bash
javac -d build $(find java -name '*.java')
java -cp build ape8.Main 42 10000 resultados
```

## 7. Resultados

Con N = 10 000 y semilla 42 (Python: `numpy.random.default_rng`; Java: `java.util.Random`, por eso los números
difieren un poco). La varianza experimental es la muestral (divide entre N − 1).

| λ | Media teórica | Media exp. Python | Media exp. Java | Varianza teórica | Varianza exp. Python | Varianza exp. Java |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.5 | 2.00 | 1.9877 | 2.0114 | 4.00 | 4.0651 | 3.9629 |
| 1.0 | 1.00 | 0.9939 | 1.0057 | 1.00 | 1.0163 | 0.9907 |
| 2.0 | 0.50 | 0.4969 | 0.5028 | 0.25 | 0.2541 | 0.2477 |

Errores porcentuales: Python 0.61 % en la media y 1.63 % en la varianza; Java 0.57 % y 0.93 %. Son iguales para las
tres tasas porque se transforman los mismos U y X escala exactamente con 1/λ.

Uniformes U(0,1): media 0.497122 (Python) y 0.503481 (Java) frente a 0.5; varianza 0.083071 y 0.082317 frente a
1/12 ≈ 0.083333.

Figuras: [histograma-uniforme.png](codigo/figuras/histograma-uniforme.png),
[histograma-exponencial.png](codigo/figuras/histograma-exponencial.png) y
[comparativa-lambda.png](codigo/figuras/comparativa-lambda.png). Al aumentar λ la media y la varianza bajan y los
valores se concentran más cerca de cero.
