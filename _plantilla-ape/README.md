# APE <m> — <Tema>

## 1. Enunciado y objetivo

<Resumen del enunciado entregado por el docente y objetivo de la práctica.>

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| <modelo / agente> | <para qué se usó> |

## 3. Proceso con IA

1. <Título de la iteración 1>
2. <Título de la iteración 2>

## 4. Errores de la IA y correcciones

- <respuesta incorrecta> → <cómo se detectó y corrigió>

## 5. Arquitectura del código

```text
codigo/simulacion_ape/
├── __main__.py                  # Delgado: solo llama al controlador
├── model/
│   ├── config.py                # Parámetros de la simulación
│   ├── dice.py                  # Entidades y reglas del sistema
│   ├── simulation.py            # Motor de ejecución de corridas
│   └── analysis.py              # Estadísticas de resultados
├── view/
│   └── console_view.py          # Salida de resultados (tablas, gráficas)
└── controller/
    └── simulation_controller.py # Orquesta modelo y vistas
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
