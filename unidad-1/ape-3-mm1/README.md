# APE 3 — Simulación de un sistema de líneas de espera M/M/1 mediante SimPy

| | |
| --- | --- |
| **Asignatura** | Simulación — Universidad Nacional de Loja |
| **Docente** | Ing. José Guamán |
| **Unidad** | U1: Introducción a la Simulación |
| **Práctica** | 03 — Simulación de un sistema de líneas de espera M/M/1 |
| **Modalidad** | Grupal |
| **Repositorio del grupo** | [AlejandroTatum/simulacion-ape-3-mm1](https://github.com/AlejandroTatum/simulacion-ape-3-mm1) |
| **Informe** | [documento/](documento/) |
| **Bibliografía** | [referencias.bib](referencias.bib) |

## Integrantes

| Integrante | Responsabilidad |
| --- | --- |
| Andrés Tapia | Trabajo compartido: modelo M/M/1 en SimPy, ventana en vivo, pruebas e informe. |
| Ariel González | Trabajo compartido: modelo M/M/1 en SimPy, ventana en vivo, pruebas e informe. |
| Gyna Yupanqui | Trabajo compartido: modelo M/M/1 en SimPy, ventana en vivo, pruebas e informe. |
| Alejandro Padilla | Trabajo compartido: modelo M/M/1 en SimPy, ventana en vivo, pruebas e informe. |

## 1. Enunciado y objetivo

Simular un sistema de líneas de espera M/M/1 con Python y SimPy, y analizar el comportamiento de los clientes, la cola y el servidor. El sistema real modelado es la **caja rápida de un supermercado**: los clientes llegan según un proceso de Poisson (tasa λ), forman una fila única FIFO y una sola cajera los atiende con tiempos exponenciales (tasa μ). La unidad de tiempo es el minuto.

- Implementar un modelo M/M/1 con la biblioteca SimPy.
- Calcular las métricas teóricas del sistema: $\rho = \lambda/\mu$, $L$, $L_q$, $W$ y $W_q$.
- Comparar los resultados teóricos con los simulados en los tres escenarios de la guía (λ = 2.0, 2.5 y 2.9; μ = 3.0).

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| Agente de programación el Gentleman (Pi) con modelo Claude | Lectura de la guía, modelo SimPy, fórmulas teóricas, pruebas, gráficas, ventana en vivo e informe. |

La IA ejecutó; las decisiones de modelo, formato y contenido las tomó el grupo en cada iteración.

## 3. Proceso con IA

1. Entender la guía
2. Modelo SimPy y métricas teóricas
3. Arquitectura MVC
4. Gráficas y pantalla en vivo
5. Informe grupal
6. Ventana en vivo con Matplotlib en lugar de HTML

## 4. Errores de la IA y correcciones

- **Utilización invertida en la guía:** el fundamento teórico escribe la utilización como μ/λ; se usó ρ = λ/μ, que es lo que indica el pseudocódigo de la guía y lo que da valores menores que 1 en los tres escenarios.
- **Columna equivocada en la primera versión del informe:** la tabla de comparación tomó los valores de la animación de 60 minutos («Simulado ahora») y no los de la corrida de 20 000 minutos; se detectó al compararla con la tabla de la consola y se corrigió con los valores de semilla 42.

## 5. Arquitectura del código

```text
codigo/simulacion_ape/
├── __main__.py                  # Punto de entrada: solo llama al controlador
├── model/                       # Datos y lógica, sin imprimir ni graficar
│   ├── config.py                # Escenarios (λ, μ), tiempo simulado y semilla
│   ├── queue_system.py          # Modelo SimPy: llegadas, fila FIFO y una caja
│   ├── theory.py                # Fórmulas M/M/1 y condición de estabilidad λ < μ
│   ├── analysis.py              # Métricas simuladas (en el tiempo y por cliente)
│   ├── state.py                 # Estado del sistema en un instante
│   ├── live.py                  # Corrida (λ, μ) lista para la pantalla en vivo
│   └── simulation.py            # Corre un escenario y reúne teoría y simulación
├── view/                        # Presentación, sin cálculos del modelo
│   ├── console_view.py          # Tabla comparativa en consola
│   ├── chart_view.py            # Gráficas estáticas para el informe
│   └── live/                    # Pantalla en vivo: una ventana de Matplotlib (animación, tablero, gráficas)
└── controller/
    └── simulation_controller.py # Opciones de línea de comandos y orquestación
```

MVC separa los cálculos de la presentación: se puede cambiar un escenario en `model/config.py` sin tocar las gráficas, y probar el modelo sin generar ninguna figura. La pantalla en vivo es una ventana de Matplotlib con deslizadores de λ y μ; no simula por su cuenta: el controlador le entrega una función que pide al modelo una corrida con las tasas elegidas, y las pruebas comprueban que lo que muestra coincide con el modelo. El detalle de opciones y controles está en [codigo/README.md](codigo/README.md).

## 6. Ejecución

```bash
cd codigo
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m simulacion_ape         # tabla, gráficas en resultados/ y ventana en vivo de Matplotlib
pytest                           # 21 pruebas
```

## 7. Resultados

Corrida de 20 000 minutos por escenario con semilla 42.

| Escenario | ρ teórico / simulado | L teórico / simulado | W teórico / simulado (min) | Error máximo |
| --- | --- | --- | --- | --- |
| 1. Estable (λ = 2.0) | 0.667 / 0.670 | 2.000 / 2.036 | 1.000 / 1.022 | 2.8 % |
| 2. Mayor utilización (λ = 2.5) | 0.833 / 0.835 | 5.000 / 5.029 | 2.000 / 2.016 | 0.9 % |
| 3. Cerca de saturación (λ = 2.9) | 0.967 / 0.968 | 29.000 / 26.592 | 10.000 / 9.183 | 8.6 % |

La simulación reproduce la teoría con errores menores al 3 % en los dos primeros escenarios. Al acercarse ρ a 1, la cola y la espera crecen de forma no lineal (L pasa de 2 a 29 clientes) y la simulación tarda mucho más en llegar al estado estable, por eso el error del escenario 3 es mayor. El análisis completo está en el informe de `documento/`.
