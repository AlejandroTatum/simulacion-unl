# Instrucciones para agentes de IA

Repositorio de la asignatura Simulación (UNL, Ing. José Guamán). Reglas obligatorias para toda práctica:

- Cada práctica vive en `unidad-<n>/ape-<m>-<tema>/` y se crea copiando `_plantilla-ape/`.
- Cada APE entrega: `README.md` (proceso con IA), `documento/` (PDF + editable), `referencias.bib` y `codigo/`.
- Arquitectura MVC: `model/`, `view/`, `controller/` en carpetas, `__main__.py` delgado; nunca todo en un solo
  script (`main.py` con todo). Agregar pruebas en `tests/`.
- `codigo/requirements.txt` lista todas las librerías de terceros que importa el código, con versión fijada.
  El docente instala solo con `pip install -r requirements.txt`.
- Usar semilla configurable en toda simulación aleatoria.
- Al crear el código de una APE, crear siempre `codigo/.venv` e instalar `requirements.txt` en él (`python -m venv .venv && .venv/bin/pip install -r requirements.txt`),
  y comprobar que la APE corre con ese entorno. El `.venv` no se sube (está en `.gitignore`).
- `__main__.py` debe funcionar con `python -m simulacion_ape` y también ejecutado por su ruta (botón "Run" del editor):
  si `__package__` está vacío, agrega la carpeta `codigo/` a `sys.path` y usa imports absolutos. Copiarlo de `_plantilla-ape/`.
- Al terminar una APE: completar su `README.md` (en "Proceso con IA" solo la lista de títulos de las iteraciones, sin detalle; correcciones y resultados) y
  agregar una fila en la tabla "Prácticas" del `README.md` raíz y en el `README.md` de su unidad.
- El `README.md` raíz está dirigido al docente: describe el contenido, no las reglas internas.
- Los comentarios y docstrings del código van en español; los identificadores (nombres de funciones y variables) en inglés.
- El informe y los README van en español.
- Bibliografía: solo las diapositivas de la semana, sin citas en el texto (indicación del docente).
