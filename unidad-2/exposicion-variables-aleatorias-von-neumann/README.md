# Exposición — Métodos para generar variables aleatorias (Aceptación-Rechazo de Von Neumann)

Exposición grupal de 60 minutos para tres expositores (18 minutos cada uno y 6 de preguntas): variables aleatorias y
distribuciones, números pseudoaleatorios, la transformada inversa, el método de aceptación-rechazo de Von Neumann
(ingredientes, condiciones, algoritmo y demostración), el ejemplo Beta(2,2) resuelto a mano, una actividad en la que el
público dicta los valores (diapositiva 27) y una demo en vivo que corre el código Python del ejemplo dentro de la
presentación. Cierra con una ronda de preguntas interactiva (diapositiva 37).

| Archivo | Uso |
| --- | --- |
| `index.html` | Presentación animada de 37 diapositivas con la actividad, la demo en vivo y la ronda final de preguntas (abrir en el navegador; funciona sin internet) |
| `index.pdf` | Versión estática; la diapositiva 27 muestra un ejemplo resuelto, las 29 a 32 la corrida real de Python (semilla 42, n = 10 000) y la 37 todas las respuestas |
| `guia-expositores.pdf` | Guía A4 de 16 páginas para los tres expositores: tiempos, frase de apertura literal, puntos clave, transiciones, cómo llevar la actividad, banco de preguntas, respuestas preparadas y plan B (fuente: `guia-expositores.html`) |
| `codigo/beta22.py` | Código del ejemplo Beta(2,2); genera `codigo/resultados.json` y `assets/demo/resultados.js` |
| `outline.txt` | Esquema aprobado: diapositiva, mensaje, expositor y tiempo |
| `assets/` | Tipografías, KaTeX y la demo (`assets/demo/`) locales; `assets/thumbs/` miniaturas y capturas de respaldo de la demo |
| `components/` | Componentes nuevos de esta presentación (demo, tabla de intentos, actividad de aceptación y preguntas con botón de respuesta) |

## Reparto

| Expositor | Diapositivas | Tiempo |
| --- | --- | --- |
| Expositor 1 | 1–15: fundamentos y métodos de generación | 0:00–18:00 |
| Expositor 2 | 16–27: algoritmo, demostración, ejemplo a mano y actividad | 18:00–36:00 |
| Expositor 3 | 28–36: implementación, demo en vivo, eficiencia, usos y cierre | 36:00–54:00 |
| Todos (modera el expositor 3) | 37: ronda final de preguntas | 54:00–60:00 |

## Controles

- `→` / `Espacio`: siguiente · `←`: anterior · `Inicio` / `Fin`: primera / última
- `F`: pantalla completa · `N`: notas del expositor
- Actividad (diapositiva 27): casillas **Candidato Y** y **Uniforme U** (entre 0 y 1) y botón **Decidir** (o `Enter` dentro
  de la casilla). Muestra el umbral 4Y(1−Y), la comparación U ≤ 4Y(1−Y), el veredicto y el punto sobre la curva; avisa si
  un valor está fuera de rango. Lo que se escribe en las casillas no cambia de diapositiva; `Esc` vuelve a las flechas.
- Demo (diapositivas 29 a 32): botones **Iniciar**, **Pausa**, **Reiniciar** y **M = 1.5 / 2 / 3 / 6**;
  teclas `S` (iniciar o pausar), `R` (reiniciar) y `1`–`4` (elegir M). La corrida es la misma en las cuatro diapositivas.
- Preguntas (diapositiva 37): cada pregunta tiene un botón **Ver respuesta** (clic del mouse) que muestra u oculta su respuesta
  sin cambiar de diapositiva.

La demo usa el mismo generador que `numpy.random.default_rng(42)`, así que al terminar muestra los mismos números que Python:

| M | Aceptación teórica 1/M | Observada | Intentos esperados n·M | Intentos observados |
| --- | --- | --- | --- | --- |
| 1.5 | 66.67 % | 66.80 % | 15 000 | 14 969 |
| 2 | 50 % | 50.02 % | 20 000 | 19 991 |
| 3 | 33.33 % | 33.21 % | 30 000 | 30 107 |
| 6 | 16.67 % | 16.67 % | 60 000 | 59 983 |

Con M = 1.5: media 0.5036 (teórica 0.5) y varianza 0.0497 (teórica 0.05).

## Regenerar

Desde la carpeta de la exposición:

```bash
pip install -r codigo/requirements.txt
python3 codigo/beta22.py   # valores de la demo y del PDF
google-chrome-stable --headless=new --no-pdf-header-footer --virtual-time-budget=10000 \
  --print-to-pdf=index.pdf "file://$PWD/index.html?print"
```
