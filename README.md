# Simulación — UNL

Repositorio de la asignatura **Simulación**, docente **Ing. José Guamán**.
Estudiante: Alejandro Padilla.

## Estructura

```text
simulacion/
├── unidad-1/
│   └── ape-1-<tema>/
│       ├── README.md          # Cómo se llegó al código con IA
│       ├── documento/         # Informe (PDF entregado + fuente DOCX/LaTeX)
│       ├── referencias.bib    # Bibliografía en BibTeX
│       └── codigo/            # Proyecto Python con arquitectura
├── unidad-2/
├── unidad-3/
└── _plantilla-ape/            # Plantilla base para cada APE nueva
```

## Reglas para todas las prácticas

1. **Una carpeta por APE** dentro de su unidad: `unidad-<n>/ape-<m>-<tema-en-kebab-case>/`.
2. Cada carpeta de APE contiene **obligatoriamente**:
   - `README.md`: proceso seguido con IA para llegar al código esperado.
   - `documento/`: el informe entregado (PDF) y su fuente editable.
   - `referencias.bib`: bibliografía usada en el informe, en formato BibTeX.
   - `codigo/`: implementación en Python.
3. **El código aplica una arquitectura.** Está prohibido resolver la práctica en un único script
   (`main.py` con todo adentro). Mínimo se separan:
   - `config.py`: parámetros de la simulación.
   - `model.py`: entidades y reglas del sistema simulado.
   - `simulation.py`: motor que ejecuta las corridas.
   - `analysis.py`: estadísticas y resultados.
   - `reporting.py`: tablas y gráficas.
   - `__main__.py`: punto de entrada delgado que solo conecta las capas.
   - `tests/`: pruebas de las piezas principales.
4. El `README.md` de cada APE documenta, en orden:
   1. Enunciado y objetivo de la práctica.
   2. Herramientas de IA usadas (modelo, agente).
   3. Prompts principales y decisiones tomadas en cada iteración.
   4. Errores o respuestas incorrectas de la IA y cómo se corrigieron.
   5. Arquitectura final del código y por qué se eligió.
   6. Cómo ejecutar el código y las pruebas.
   7. Resultados obtenidos.
5. Toda simulación con aleatoriedad usa una **semilla configurable** para que los resultados sean reproducibles.
6. Para crear una APE nueva se copia `_plantilla-ape/` y se renombra.

## Ejecutar una APE

```bash
cd unidad-<n>/ape-<m>-<tema>/codigo
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m simulacion_ape
pytest
```
