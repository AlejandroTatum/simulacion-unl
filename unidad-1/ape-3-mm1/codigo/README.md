# Código — Simulación M/M/1 de una caja rápida de supermercado

El sistema real modelado es la **caja rápida de un supermercado**. Los clientes llegan según un proceso de
Poisson (tasa λ), forman una fila única FIFO y una sola cajera los atiende con tiempos exponenciales (tasa μ).
La unidad de tiempo es el minuto.

El programa:

1. Simula con SimPy los tres escenarios de la guía (λ = 2.0, 2.5 y 2.9; μ = 3.0) durante 20 000 minutos.
2. Calcula las métricas teóricas (ρ, L, Lq, W, Wq) y las simuladas, y las compara en una tabla con el error %.
3. Guarda las gráficas estáticas en `resultados/` (para el informe).
4. Abre la **pantalla en vivo**, una sola ventana de Matplotlib (temporizador del canvas con blitting manual y `matplotlib.widgets`)
   donde todo avanza al mismo tiempo:
   - **Animación del local**: cada cliente entra, camina a su lugar en la fila serpentina, pasa a la caja
     (con barra de progreso del cobro) y sale. Una lámpara indica si la caja está libre o atendiendo, y un
     aviso rojo aparece cuando la cola crece cerca de la saturación.
   - **Tablero de resultados**: reloj, estado de la caja, contadores (en cola, en el sistema, atendidos,
     llegaron) y ρ, L, Lq, W y Wq en tres columnas: teórico, simulado hasta el minuto actual y simulado en la
     corrida larga de 20 000 minutos.
   - **Tres gráficas en vivo**: clientes en el sistema L(t) y en la cola Lq(t) con sus valores teóricos;
     histograma de tiempos entre llegadas con la curva teórica λe^(−λt); histograma de tiempos de servicio
     con la curva teórica μe^(−μt).
   - **Deslizadores de λ y μ**: al soltarlos, el modelo vuelve a simular con la misma semilla y se actualiza
     todo, incluida la columna de 20 000 minutos. Si λ ≥ μ la animación continúa (la cola crece), aparece
     "Sistema inestable: λ ≥ μ, la teoría no aplica" y se ocultan los valores teóricos y la corrida larga.

La ventana no simula nada por su cuenta. El controlador le entrega una función `(λ, μ) → corrida` armada con
funciones del modelo (`model/live.py`) y la ventana solo dibuja lo que esa corrida le dice en cada minuto.
Las pruebas de `tests/test_live_view.py` comprueban, sin abrir ventanas (backend Agg), que lo que muestra
coincide con el modelo.

## Ejecución

```bash
cd codigo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m simulacion_ape            # tabla + gráficas + ventana en vivo
pytest
```

También funciona con el botón "Run" del editor sobre `simulacion_ape/__main__.py`.

La ventana necesita un entorno gráfico y Tk (o cualquier otro backend interactivo de Matplotlib). Si
Matplotlib solo tiene el backend sin pantalla (Agg), el programa lo avisa y explica cómo instalar Tk
(Linux: `sudo apt install python3-tk` o `sudo pacman -S tk`; Windows y macOS ya lo incluyen con Python).
Con `--sin-animacion` no hace falta.

| Opción | Uso |
| --- | --- |
| `--escenario 3` | Escenario con el que se abre la ventana en vivo |
| `--duracion 60` | Minutos del sistema que reproduce la ventana (por defecto 60; no puede superar `--tiempo`) |
| `--velocidad 2` | Minutos simulados por segundo al abrir la ventana (por defecto 1) |
| `--sin-animacion` | Solo tabla y gráficas, sin abrir la ventana |
| `--llegada 3.5 --servicio 3` | λ y μ personalizados: la tabla y las gráficas usan ese escenario y la ventana abre con esos valores; si λ ≥ μ la tabla informa que el sistema no es estable |
| `--tiempo`, `--semilla` | Minutos simulados para las métricas y semilla aleatoria |
| `--resultados` | Carpeta donde se guardan las gráficas |

### Controles de la ventana en vivo

| Control | Acción |
| --- | --- |
| Botones 1, 2, 3 | Cargan un escenario de la guía y mueven los deslizadores a sus valores |
| Deslizadores λ y μ | Eligen las tasas (pasos de 0.1); al soltar el mouse se vuelve a simular |
| Pausar / Reanudar / Repetir | Detiene y reanuda el reloj; al terminar los minutos, vuelve a reproducir |
| Reiniciar | Vuelve al minuto 0 con las mismas tasas |
| Velocidad (0.5, 1, 2, 4) | Minutos simulados por segundo real |
| Teclas | `Espacio` pausa, `R` reinicia, `1` `2` `3` escenarios, `←` `→` velocidad |

El video de demostración se graba con cualquier grabador de pantalla (OBS, la grabadora de Windows o macOS)
mientras corre la ventana.

## Resultados generados (`resultados/`)

| Archivo | Contenido |
| --- | --- |
| `cola_en_el_tiempo.png` | Tamaño de la cola durante una jornada de 8 horas, con Lq teórico |
| `convergencia_espera.png` | Espera promedio acumulada cliente a cliente frente a Wq teórico |
| `histograma_espera.png` | Distribución de los tiempos de espera por escenario |
| `dispersion_espera.png` | Espera de cada cliente según su orden de llegada (un punto por cliente), con Wq teórico |
| `comparacion_teorico_simulado.png` | ρ, L, Lq, W y Wq teóricos frente a simulados |

## Arquitectura (MVC)

```text
simulacion_ape/
├── __main__.py                  # Delgado: solo llama al controlador
├── model/
│   ├── config.py                # Escenarios (λ, μ), tiempo simulado, semilla, duración de la pantalla
│   ├── queue_system.py          # Modelo SimPy: llegadas, fila FIFO y una caja (Resource capacidad 1)
│   ├── theory.py                # Fórmulas teóricas M/M/1 y condición de estabilidad λ < μ
│   ├── analysis.py              # Métricas simuladas (promedios en el tiempo y por cliente)
│   ├── state.py                 # Estado del sistema en un instante (quién espera, quién es atendido)
│   ├── simulation.py            # Corre un escenario y reúne resultados teóricos y simulados
│   └── live.py                  # Corrida (λ, μ) con todo lo que consulta la ventana en vivo
├── view/
│   ├── console_view.py          # Tabla comparativa y mensajes en consola
│   ├── chart_view.py            # Gráficas estáticas para el informe
│   └── live/                    # Ventana de Matplotlib de la pantalla en vivo
│       ├── window.py            # Diseño, botones, deslizadores y ciclo de animación
│       ├── scene.py             # Animación del local: fila, caja, salida
│       ├── board.py             # Tablero: reloj, contadores y tabla teórico vs. simulado
│       ├── charts.py            # L(t), Lq(t) y los dos histogramas
│       └── theme.py             # Paleta de colores y `hide_frame`
└── controller/
    └── simulation_controller.py # Opciones de línea de comandos y orquestación
```

## Notas del modelo

- La utilización es ρ = λ/μ (la guía la escribe invertida en el fundamento teórico; su pseudocódigo es correcto).
- L, Lq y ρ simulados se promedian **en el tiempo**; W y Wq se promedian **por cliente**.
- Llegadas y servicios usan flujos aleatorios independientes derivados de la misma semilla, así los tres
  escenarios se comparan con la misma secuencia base.
- En la pantalla en vivo, la columna "Simulado ahora" usa solo los primeros minutos y por eso se aleja de la
  teoría; la columna de la corrida larga muestra cómo converge. Al cambiar λ o μ se usa la misma semilla.
- En el escenario 3 (ρ ≈ 0.97) la simulación tarda mucho en llegar al estado estable y su varianza es alta,
  por eso el error frente a la teoría es mayor que en los otros escenarios.
