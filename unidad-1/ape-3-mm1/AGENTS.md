# Instrucciones para agentes de IA

Repositorio grupal de la APE 3 de Simulación (UNL, Ing. José Guamán): sistema de colas M/M/1 con SimPy.
Reglas obligatorias:

- La APE entrega: `README.md` (integrantes y proceso con IA), `documento/` (PDF + editable), `referencias.bib` y `codigo/`.
- Arquitectura MVC: `model/`, `view/`, `controller/` en carpetas, `__main__.py` delgado; nunca todo en un solo
  script (`main.py` con todo). Agregar pruebas en `tests/`.
- `codigo/requirements.txt` lista todas las librerías de terceros que importa el código, con versión fijada.
  El docente instala solo con `pip install -r requirements.txt`.
- Usar semilla configurable en toda simulación aleatoria.
- Crear siempre `codigo/.venv` e instalar `requirements.txt` en él (`python -m venv .venv && .venv/bin/pip install -r requirements.txt`),
  y comprobar que la APE corre con ese entorno. El `.venv` no se sube (está en `.gitignore`).
- `__main__.py` debe funcionar con `python -m simulacion_ape` y también ejecutado por su ruta (botón "Run" del editor):
  si `__package__` está vacío, agrega la carpeta `codigo/` a `sys.path` y usa imports absolutos.
- Al terminar: completar el `README.md` (en "Proceso con IA" solo la lista de títulos de las iteraciones, sin detalle; correcciones y resultados).
- Los comentarios y docstrings del código van en español; los identificadores (nombres de funciones y variables) en inglés.
- El informe y los README van en español.
- Bibliografía: solo las diapositivas de la semana, sin citas en el texto (indicación del docente).

## Trabajo en grupo

- Cada integrante trabaja en su propia rama (`<nombre>/<tema>`) y abre un pull request hacia `main`; no se hace push directo a `main`.
- Antes de empezar a trabajar: `git pull` para traer los cambios de los demás.
- Mantener actualizada la tabla "Integrantes" del `README.md` con la parte a cargo de cada uno.
- La utilización del servidor es ρ = λ/μ (la guía la escribe invertida; el pseudocódigo de la guía es el correcto).
