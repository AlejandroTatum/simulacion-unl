# Instrucciones para agentes de IA

Repositorio de la asignatura Simulación (UNL, Ing. José Guamán). Reglas obligatorias para toda práctica:

- Cada práctica vive en `unidad-<n>/ape-<m>-<tema>/` y se crea copiando `_plantilla-ape/`.
- Cada APE entrega: `README.md` (proceso con IA), `documento/` (PDF + editable), `referencias.bib` y `codigo/`.
- Nunca concentrar la solución en un solo script (`main.py` con todo). Respetar la separación por capas
  (`config`, `model`, `simulation`, `analysis`, `reporting`, `__main__` delgado) y agregar pruebas en `tests/`.
- `codigo/requirements.txt` lista todas las librerías de terceros que importa el código, con versión fijada.
  El docente instala solo con `pip install -r requirements.txt`.
- Usar semilla configurable en toda simulación aleatoria.
- Al terminar una APE: completar su `README.md` (prompts, iteraciones, correcciones, resultados) y
  agregar una fila en la tabla "Prácticas" del `README.md` raíz y en el `README.md` de su unidad.
- El `README.md` raíz está dirigido al docente: describe el contenido, no las reglas internas.
- Los comentarios y docstrings del código van en español; los identificadores (nombres de funciones y variables) en inglés.
- El informe y los README van en español.
- Bibliografía: solo las diapositivas de la semana, sin citas en el texto (indicación del docente).
