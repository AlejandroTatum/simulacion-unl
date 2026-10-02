# Simulación — Universidad Nacional de Loja

| | |
| --- | --- |
| **Asignatura** | Simulación |
| **Docente** | Ing. José Guamán |
| **Estudiante** | Alejandro Padilla |

Repositorio con las prácticas (APE) de la asignatura, organizadas por unidad.

## Prácticas

| Unidad | APE | Tema | Carpeta |
| --- | --- | --- | --- |
| 1 | — | *Pendiente* | — |

## Contenido de cada APE

Cada práctica está en `unidad-<n>/ape-<m>-<tema>/` y contiene:

| Elemento | Descripción |
| --- | --- |
| `README.md` | Proceso seguido con IA para llegar al código: prompts, iteraciones, correcciones y resultados. |
| `documento/` | Informe entregado (PDF) y su archivo editable. |
| `referencias.bib` | Bibliografía del informe en formato BibTeX. |
| `codigo/` | Implementación en Python organizada en MVC, con su `requirements.txt` y pruebas. |

El código de cada APE sigue la arquitectura MVC, con una carpeta por capa:

| Carpeta / módulo | Responsabilidad |
| --- | --- |
| `model/` | Parámetros, reglas del sistema, simulación y análisis (sin imprimir ni graficar). |
| `view/` | Presentación: tablas en consola y figuras. |
| `controller/` | Coordina el modelo y las vistas. |
| `__main__.py` | Punto de entrada delgado que llama al controlador. |

## Cómo ejecutar una APE

Requisitos: Python 3.10 o superior.

```bash
cd unidad-<n>/ape-<m>-<tema>/codigo
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m simulacion_ape         # ejecuta la simulación
pytest                           # ejecuta las pruebas
```
