# AA 1 — Simulación determinística vs. estocástica: impacto en la interpretación y la incertidumbre

| | |
| --- | --- |
| **Asignatura** | Simulación — Universidad Nacional de Loja |
| **Docente** | Ing. José Guamán |
| **Unidad** | U1: Introducción a la Simulación |
| **Actividad** | AA 1 — Ensayo investigativo, tema 18 |
| **Modalidad** | Individual |
| **Autor** | Alejandro Padilla |
| **Informe** | [documento/](documento/) (versión vigente: v002) |
| **Bibliografía** | [referencias.bib](referencias.bib) |
| **Guía** | [guia/guia-aa.txt](guia/guia-aa.txt) |

## 1. Enunciado y objetivo

Tema asignado 18: *Simulación determinística vs. estocástica: impacto en la interpretación de resultados e incertidumbre* (keywords: deterministic vs stochastic simulation, uncertainty quantification). La guía pide un ensayo en formato IEEE a dos columnas, de 4 a 6 páginas y con al menos 5 papers de Scopus, IEEE Xplore o ACM Digital Library.

- Revisar la literatura que compara ambos enfoques o propone métodos para cuantificar la incertidumbre (7 artículos revisados por pares, 2000–2024, y el libro de Law como referencia metodológica).
- Contrastar coincidencias y contradicciones entre los trabajos.
- Aplicar los conceptos a un ejemplo propio: una cola M/M/1 resuelta de forma determinística, estocástica y con incertidumbre en el parámetro de llegada.

## 2. Herramientas de IA

| Herramienta | Uso |
| --- | --- |
| Agente de programación el Gentleman (Pi) con modelo Claude | Búsqueda y verificación de fuentes, matriz de evidencia, scripts del ejemplo M/M/1, figuras y maquetado IEEE. |

La IA ejecutó; la elección del ejemplo, la extensión y el contenido final los decidí y aprobé yo.

## 3. Proceso

1. Lectura de la guía y de la rúbrica; checklist de requisitos antes de redactar.
2. Búsqueda de fuentes y verificación de cada referencia (DOI, autores, año); matriz de evidencia por afirmación.
3. Ejemplo M/M/1 (λ = 0.8, μ = 1.0, 2000 clientes por réplica, semilla 18) con la recursión de Lindley.
4. Primer borrador; verificación independiente de cada requisito de la guía contra el texto.
5. Ampliación a 4 páginas de contenido: escenarios de carga (Tabla 3), réplicas necesarias para una precisión dada (Tabla 4, Figura 3) y limitaciones del ejemplo.
6. Maquetado IEEE a dos columnas, auditoría visual del PDF, revisión final y entrega.
7. Autoevaluación contra la rúbrica y correcciones menores (v002): cifras de la fórmula con punto decimal, frase sin cita reemplazada por la aclaración de que ningún artículo proviene de ACM, y referencias con revistas abreviadas en estilo IEEE y mes de publicación.

| Versión | Cambios |
| --- | --- |
| v001 | Primera entrega. |
| v002 | Correcciones del paso 7; mismo contenido y mismas 4 páginas. |

## 4. Código

Los scripts de [codigo/](codigo/) generan todas las cifras del ejemplo. No siguen la arquitectura MVC de las APE: son scripts de apoyo del ensayo, uno por resultado.

| Script | Resultado en el ensayo |
| --- | --- |
| `tabla2_deterministica_vs_estocastica.py` | Tabla 2: Wq determinística, teórica, 10 réplicas con IC 95 % e incertidumbre de entrada (bootstrap de λ). |
| `tabla3_escenarios_carga.py` | Tabla 3: Wq para ρ = 0.5, 0.8 y 0.9. |
| `tabla4_precision_figura3.py` | Tabla 4 y Figura 3: réplicas necesarias para una semiamplitud de 10 % de la media. |
| `figuras1_2.py` | Figura 1 (dispersión de réplicas) y Figura 2 (distribución bootstrap). |

```bash
cd unidad-1/aa-1-deterministica-vs-estocastica/codigo
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python tabla2_deterministica_vs_estocastica.py
python tabla3_escenarios_carga.py
python tabla4_precision_figura3.py figuras
python figuras1_2.py figuras
```

Las figuras de [codigo/figuras/](codigo/figuras/) son las mismas del informe.

## 5. Resultados

| Modelo (ρ = 0.8) | Wq (minutos) |
| --- | --- |
| Determinístico | 0.00 |
| Teórico M/M/1 | 4.00 |
| Estocástico, 10 réplicas | 4.57, IC 95 % [3.48, 5.66] |
| Estocástico, 57 réplicas | 4.16, IC 95 % [3.88, 4.44] |
| Incertidumbre de entrada (λ estimado con 50 datos) | percentiles 2.5–97.5: 1.53 a 20.97 |

El modelo determinístico predice que nadie espera, porque elimina justamente la variabilidad que genera la cola. Una sola réplica estocástica varía entre 2.64 y 7.24 minutos, así que el resultado se reporta como intervalo. Si además λ se estima de pocos datos, la incertidumbre del parámetro supera a la de las réplicas.
