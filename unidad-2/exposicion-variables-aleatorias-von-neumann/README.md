# Exposición — Métodos para generar variables aleatorias (Aceptación-Rechazo de Von Neumann)

Exposición grupal de 30 minutos para tres expositores (9 minutos cada uno y 3 de preguntas) sobre el método de
aceptación-rechazo de Von Neumann. La transformada inversa la explica el docente, así que la presentación solo la nombra
como punto de partida (diapositiva 3) y se concentra en lo esencial: la idea de proponer y filtrar, los ingredientes f, g
y M con sus condiciones, el algoritmo y por qué funciona, el ejemplo Beta(2,2) resuelto a mano, una actividad en la que el
público dicta los valores (diapositiva 13), una demo en vivo que corre el código Python del ejemplo dentro de la
presentación (diapositivas 14 y 15) y cuándo conviene usarlo. Cierra con una ronda de preguntas interactiva (diapositiva 18).

| Archivo | Uso |
| --- | --- |
| `index.html` | Presentación animada de 18 diapositivas con la actividad, la demo en vivo y la ronda final de preguntas (abrir en el navegador; funciona sin internet) |
| `index.pdf` | Versión estática; la diapositiva 13 muestra un ejemplo resuelto, las 14 y 15 la corrida real de Python (semilla 42, n = 10 000) y la 18 todas las respuestas |
| `guia-expositores.pdf` | Guía A4 de 9 páginas para los tres expositores: tiempos, frase de apertura literal, puntos clave, transiciones, cómo llevar la actividad en 2 minutos, respuestas preparadas y plan B (fuente: `guia-expositores.html`) |
| `codigo/beta22.py` | Código del ejemplo Beta(2,2); genera `codigo/resultados.json` y `assets/demo/resultados.js` |
| `outline.txt` | Esquema aprobado: diapositiva, mensaje, expositor y tiempo |
| `assets/` | Tipografías, KaTeX y la demo (`assets/demo/`) locales; las miniaturas `index-thumb-NN.png` y `guia-expositores-thumb-N.png` son vistas previas de cada página |
| `components/` | Componentes nuevos de esta presentación (demo, tabla de intentos, actividad de aceptación y preguntas con botón de respuesta) |

## Reparto

| Expositor | Diapositivas | Tiempo |
| --- | --- | --- |
| Expositor 1 | 1–7: objetivo, puente desde la inversa, la idea de proponer y filtrar, ingredientes y la cota M | 0:00–9:00 |
| Expositor 2 | 8–13: algoritmo, regla, demostración, Beta(2,2) a mano y actividad | 9:00–18:00 |
| Expositor 3 | 14–17: demo en vivo con histograma, costo 1/M y E[T] = M, cuándo conviene y cierre | 18:00–27:00 |
| Todos (modera el expositor 3) | 18: ronda final de preguntas | 27:00–30:00 |

## Controles

- `→` / `Espacio`: siguiente · `←`: anterior · `Inicio` / `Fin`: primera / última
- `F`: pantalla completa · `N`: notas del expositor
- Actividad (diapositiva 13): casillas **Candidato Y** y **Uniforme U** (entre 0 y 1) y botón **Decidir** (o `Enter` dentro
  de la casilla). Muestra el umbral 4Y(1−Y), la comparación U ≤ 4Y(1−Y), el veredicto y el punto sobre la curva; avisa si
  un valor está fuera de rango. Lo que se escribe en las casillas no cambia de diapositiva; `Esc` vuelve a las flechas.
- Demo (diapositivas 14 y 15): botones **Iniciar**, **Pausa**, **Reiniciar** y **M = 1.5 / 2 / 3 / 6**;
  teclas `S` (iniciar o pausar), `R` (reiniciar) y `1`–`4` (elegir M). La corrida es la misma en las dos diapositivas.
- Preguntas (diapositiva 18): cada pregunta tiene un botón **Ver respuesta** (clic del mouse) que muestra u oculta su respuesta
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
