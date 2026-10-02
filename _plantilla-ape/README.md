# APE <m> — <Tema>

## 1. Enunciado y objetivo

<Resumen del enunciado entregado por el docente y objetivo de la práctica.>

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| <modelo / agente> | <para qué se usó> |

## 3. Proceso con IA

### Iteración 1
- **Prompt:** <prompt usado>
- **Resultado:** <qué devolvió la IA>
- **Decisión:** <qué se aceptó, qué se cambió y por qué>

### Iteración 2
- ...

## 4. Errores de la IA y correcciones

- <respuesta incorrecta> → <cómo se detectó y corrigió>

## 5. Arquitectura del código

```text
codigo/simulacion_ape/
├── config.py       # Parámetros de la simulación
├── model.py        # Entidades y reglas del sistema
├── simulation.py   # Motor de ejecución de corridas
├── analysis.py     # Estadísticas de resultados
├── reporting.py    # Tablas y gráficas
└── __main__.py     # Punto de entrada que conecta las capas
```

<Justificación de la arquitectura elegida.>

## 6. Ejecución

```bash
cd codigo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m simulacion_ape
pytest
```

## 7. Resultados

<Resultados principales y su interpretación. El detalle está en `documento/`.>
