# APE 2 — Comparación de modelos determinísticos, estocásticos, discretos y continuos

| | |
| --- | --- |
| **Unidad** | U1: Introducción a la Simulación |
| **Práctica** | 02 — Comparación de modelos determinísticos, estocásticos, discretos y continuos |
| **Informe** | [documento/comparacion-de-modelos-deterministicos-estocasticos-discretos-y-continuos-v001.pdf](documento/comparacion-de-modelos-deterministicos-estocasticos-discretos-y-continuos-v001.pdf) |
| **Bibliografía** | [referencias.bib](referencias.bib) |

## 1. Enunciado y objetivo

Simular el crecimiento de una población con cuatro modelos y compararlos, a partir del arreglo de la guía:

`datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]`

| Modelo | Ecuación |
| --- | --- |
| Determinístico | $P(t) = P_0 e^{rt}$ |
| Discreto | $P_{n+1} = P_n + rP_n$ |
| Estocástico | $P_{n+1} = P_n + rP_n + \varepsilon_n$, con $\varepsilon_n \sim N(0, \sigma)$ |
| Continuo (Euler) | $P(t + \Delta t) = P(t) + \Delta t \cdot rP(t)$ |

Objetivo: diferenciar los principales paradigmas de simulación mediante la construcción de modelos computacionales.

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| Agente de programación el Gentleman (Pi) con modelo Claude | Lectura de la guía, código, pruebas, gráficas y borrador del informe. |
| Subagentes del mismo agente | Evaluación del informe con dos jueces independientes. |

La IA ejecutó; las decisiones de modelo, formato y contenido las tomó el estudiante en cada iteración.

## 3. Proceso con IA

1. Entender la guía
2. Parámetros a partir de los datos
3. Cuatro modelos y pruebas
4. Escenarios de r, sigma y dt
5. Gráficas y redacción
6. Reescritura del informe en voz de estudiante

## 4. Errores de la IA y correcciones

- **Redacción de profesor:** el primer borrador explicaba en lugar de reportar y mezclaba los números dentro de los párrafos. Se reescribió: cada resultado lleva figura, tabla y observaciones cortas.
- **Paso 1 de la guía sin reportar:** la preparación del entorno de Python no figuraba en los pasos. Se agregó al contrastar el informe con la guía.
- **Figuras demasiado altas:** dejaban huecos y títulos huérfanos en el PDF. Se redujo su altura en el código.
- **requirements.txt incompleto:** la plantilla solo traía pytest. Se agregaron numpy y matplotlib con su versión.

## 5. Arquitectura del código

```text
codigo/simulacion_ape/
├── __main__.py                  # Punto de entrada: solo llama al controlador
├── model/                       # Datos y lógica, sin imprimir ni graficar
│   ├── config.py                # Arreglo de la guía, semilla y valores de r, sigma y dt
│   ├── growth_models.py         # Los cuatro modelos de crecimiento
│   ├── estimation.py            # P0, r y sigma a partir del arreglo
│   ├── simulation.py            # Ejecuta los modelos y las corridas de Monte Carlo
│   └── analysis.py              # RMSE frente a los datos y error de Euler
├── view/                        # Presentación, sin cálculos del modelo
│   ├── console_view.py          # Tablas en consola
│   └── chart_view.py            # Gráficas de Matplotlib
└── controller/
    └── simulation_controller.py # Ejecuta los escenarios y pide a las vistas mostrar resultados
```

MVC separa los cálculos de la presentación: se puede cambiar el arreglo de datos en `model/config.py` sin tocar las gráficas, y probar los modelos sin generar ninguna figura.

## 6. Ejecución

```bash
cd codigo
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m simulacion_ape         # imprime las tablas y guarda las figuras en figuras/
pytest                           # 12 pruebas
```

## 7. Resultados

| Parámetro | Valor |
| --- | --- |
| $P_0$ | 1000 |
| $r$ | 0.1204 |
| $\sigma$ | 26.93 |

| Modelo | $P(6)$ | RMSE frente a los datos |
| --- | --- | --- |
| Determinístico | 2059.7 | 26.9 |
| Discreto | 1978.3 | 57.3 |
| Estocástico (semilla 42) | 1914.9 | 82.2 |
| Continuo (Euler, $\Delta t = 0.1$) | 2050.8 | 28.6 |

El determinístico y el continuo son los que mejor siguen los datos. Con la misma tasa, el discreto crece menos que el continuo, y es el caso de Euler con $\Delta t = 1$. Un $\sigma$ mayor separa más las corridas del estocástico sin cambiar su media. El análisis completo está en el [informe](documento/comparacion-de-modelos-deterministicos-estocasticos-discretos-y-continuos-v001.pdf).
