# APE 1 — Índice de posibilidad de lluvia

| | |
| --- | --- |
| **Unidad** | U1: Introducción a la Simulación |
| **Práctica** | 01 — Construcción y simulación computacional de un modelo matemático |
| **Informe** | [documento/ape-1-indice-lluvia.pdf](documento/ape-1-indice-lluvia.pdf) |
| **Bibliografía** | [referencias.bib](referencias.bib) |

## 1. Enunciado y objetivo

Simular el comportamiento de la atmósfera durante 24 horas y determinar en qué horas existe posibilidad de lluvia con el índice

$$I = 0.5H + 0.3N + 0.2T_f$$

donde $H$ y $N$ son la humedad y la nubosidad normalizadas y $T_f$ es el factor de temperatura de la tabla de la guía. Se pide llenar la tabla de nueve lecturas horarias, ajustar el modelo, llenar de nuevo la tabla y presentar las gráficas.

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| Agente de programación el Gentleman (Pi) con modelo Claude | Lectura de la guía, propuesta del modelo, código, pruebas, gráficas y borrador del informe. |
| Subagentes del mismo agente | Reestructuración del código en MVC, verificación independiente y evaluación del informe con dos jueces. |

La IA ejecutó; las decisiones de modelo, formato y contenido las tomó el estudiante en cada iteración.

## 3. Proceso con IA

### Iteración 1 — Entender la guía
- **Prompt:** "Aquí está la práctica, revísala y sigue el formato; el código quiero algo corto, fácil de entender para explicar y eficiente."
- **Resultado:** la IA detectó tres puntos ambiguos: la guía pide Java y Python, no dice qué ajustar, y las lecturas de 17 °C y 15 °C no están en la tabla de $T_f$. También notó que las preguntas de control hablan del modelo exponencial ($P_0$, $r$), que no es el de esta práctica.
- **Decisión:** solo Python; responder las preguntas de control tal como están, con una nota aclaratoria.

### Iteración 2 — Primer modelo y pruebas
- **Prompt:** implementar el modelo con pruebas a partir del ejemplo de la guía (90 %, 80 %, 18 °C → $I = 0.81$).
- **Resultado:** se escribieron primero las pruebas, se vio que fallaban y luego se implementó el modelo con NumPy, calculando las nueve horas en una sola operación.
- **Decisión:** la IA observó que la tabla de $T_f$ es exactamente la recta $T_f = 1 - 0.05(T - 10)$, lo que resuelve las temperaturas que faltan.

### Iteración 3 — Ajuste pedido por el docente
- **Prompt:** "El docente pide ajustar el modelo de la fórmula para que la suma de los valores dé 1."
- **Resultado:** la IA aclaró que los pesos originales ya suman 1 y propuso redistribuirlos manteniendo esa condición, con una tabla del efecto de cada opción.
- **Decisión:** modelo ajustado $I_{aj} = 0.4H + 0.4N + 0.2T_f$ con $T_f$ por la recta.

### Iteración 4 — Arquitectura MVC
- **Prompt:** "El código debe ser MVC, separado por carpetas."
- **Resultado:** el código pasó de módulos sueltos a las carpetas `model/`, `view/` y `controller/`, con la misma salida que antes y las pruebas en verde.

### Iteración 5 — Gráficas y redacción
- **Prompts:** separar las gráficas del índice original y del ajustado; mejorar la separación entre ambos modelos en el informe; explicaciones más cortas y claras; ecuaciones en formato de ecuación; bibliografía solo con las diapositivas y sin citas.
- **Resultado:** cada modelo tiene su tabla, su gráfica de aportes y su gráfica del índice, más una comparación final. El estudiante parafraseó y recortó el borrador en Word, y esos cambios se pasaron tal cual al informe.

## 4. Errores de la IA y correcciones

- **Índice mal clasificado por punto flotante:** un valor como 0.60 podía quedar como 0.5999… y caer en el estado equivocado. Se corrigió redondeando el índice a cuatro decimales antes de clasificar.
- **Bibliografía con libros:** la IA propuso libros y artículos, y uno tenía un año incorrecto que detectó el verificador de fuentes. Se reemplazó todo por las diapositivas de la semana, como pide el docente.
- **Justificación incorrecta del ajuste:** el borrador decía que el ajuste servía "para que los pesos sumen 1", cuando ya sumaban 1. Lo detectaron los dos jueces independientes y se corrigió antes de la entrega.
- **Descripción de una gráfica que no coincidía con los datos:** se decía que la humedad baja hasta el mediodía, pero sube a las 08:00. Se corrigió.
- **Figuras fuera de su sección en el PDF:** las seis figuras quedaban juntas al final. Se ajustó la generación para que cada una quede en su subsección.

## 5. Arquitectura del código

```text
codigo/simulacion_ape/
├── __main__.py                  # Punto de entrada: solo llama al controlador
├── model/                       # Datos y lógica, sin imprimir ni graficar
│   ├── config.py                # Pesos, umbrales y lecturas de la guía
│   ├── rain_model.py            # T_f (tabla y recta), índice y clasificación
│   ├── simulation.py            # Aplica el modelo a las nueve horas
│   └── analysis.py              # Compara el modelo base con el ajustado
├── view/                        # Presentación, sin cálculos del modelo
│   ├── console_view.py          # Tablas en consola
│   └── chart_view.py            # Gráficas de Matplotlib
└── controller/
    └── simulation_controller.py # Ejecuta los modelos y pide a las vistas mostrar resultados
```

MVC separa los cálculos de la presentación: se puede cambiar un peso en `model/config.py` sin tocar las gráficas, y probar el modelo sin generar ninguna figura.

## 6. Ejecución

```bash
cd codigo
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m simulacion_ape         # imprime las tablas y guarda las figuras en figuras/
pytest                           # 7 pruebas
```

## 7. Resultados

| Hora | I base | Estado base | I ajustado | Estado ajustado |
| --- | --- | --- | --- | --- |
| 06:00 | 0.605 | Lluvia probable | 0.580 | Baja posibilidad |
| 12:00 | 0.470 | Baja posibilidad | 0.440 | Baja posibilidad |
| 18:00 | 0.885 | Lluvia | 0.888 | Lluvia |

Los dos modelos coinciden en que el mediodía es el momento con menos posibilidad de lluvia y que desde las 16:00 lo más probable es que llueva. El modelo ajustado solo cambia el estado de las 06:00. El análisis completo está en el [informe](documento/ape-1-indice-lluvia.pdf).
