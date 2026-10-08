# Exposición — Tipos de simulación (Semana 2)

Diapositivas sobre los paradigmas de simulación: estática vs. dinámica, determinística vs. estocástica y discreta vs. continua.
Cada gráfico es una simulación que corre en vivo con semilla configurable.

| Archivo | Uso |
| --- | --- |
| `tipos-de-simulacion.html` | Presentación interactiva (abrir en el navegador) |
| `tipos-de-simulacion.pdf` | Versión estática para entregar o imprimir |
| `guia-expositores.pdf` | Guía de 30 minutos para Víctor, Jimmy, Cael, Francis y Alejandro (fuente: `guia-expositores.html`) |
| `assets/fonts/` | Tipografías locales (funciona sin internet) |

## Controles

- `→` / `Espacio`: siguiente · `←`: anterior · `Inicio` / `Fin`: primera / última
- `F`: pantalla completa · `N`: notas del expositor
- Botón **otra semilla**: nueva corrida en los modelos estocásticos; **repetir**: misma corrida en los determinísticos.

## Regenerar el PDF

```bash
google-chrome-stable --headless=new --no-pdf-header-footer --virtual-time-budget=10000 \
  --print-to-pdf=tipos-de-simulacion.pdf "file://$PWD/tipos-de-simulacion.html?print"
```
