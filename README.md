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
| `codigo/` | Implementación en Python organizada por capas, con su `requirements.txt` y pruebas. |

El código de cada APE separa responsabilidades en módulos:

| Módulo | Responsabilidad |
| --- | --- |
| `config.py` | Parámetros de la simulación (incluida la semilla). |
| `model.py` | Entidades y reglas del sistema simulado. |
| `simulation.py` | Ejecución de las corridas. |
| `analysis.py` | Cálculo de estadísticas. |
| `reporting.py` | Presentación de tablas y gráficas. |
| `__main__.py` | Punto de entrada que conecta los módulos. |

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

Las simulaciones usan una semilla fija, por lo que los resultados son reproducibles.
