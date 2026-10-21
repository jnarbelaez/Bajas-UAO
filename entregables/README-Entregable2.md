# Entregable 2 · Análisis Exploratorio de Datos (EDA)

**Complejidad:** Media · **Fuente:** Informes Técnicos DSU-3.1.3-FO15 · **Período:** 2025–2026

Explora en profundidad los datos crudos de bajas de activos de TI de la UAO. Cubre las 9 secciones
exigidas y 12 visualizaciones.

## Archivos del entregable

| Archivo | Descripción |
|---|---|
| **`Entregable2-EDA.ipynb`** | Jupyter Notebook con las 9 secciones. Código ejecutable (pandas / matplotlib / seaborn) y salidas pre-calculadas con los datos reales. |
| **`Entregable2-EDA-Informe.html`** | Informe imprimible a PDF (8–10 páginas) con las 12 figuras embebidas. |
| **`eda_figuras/`** | Las 12 visualizaciones en SVG (fig01–fig12). |

## Resultados clave (datos reales)

- **924 registros × 18 variables · 1.322 unidades.**
- **Cantidad:** media 1,43 · mediana 1 · máx 50 (lotes).
- **Nulos:** 40,4% sin N° inventario · 22,3% sin serie → principal hallazgo de calidad.
- **Duplicados:** 0 filas idénticas · 5 seriales repetidos (revisar).
- **Outliers:** 77 registros, todos lotes legítimos (regla IQR).
- **Correlaciones:** Mes↔Cantidad ≈ 0 · Serie↔Inventario = 0,24 (positiva débil).
- **Score de calidad general: 87,2 / 100 (bueno).**

## Cómo obtener el PDF (8–10 páginas)

El entorno no tiene un conversor HTML→PDF, por lo que el informe se entrega como HTML listo para exportar:

1. Abre `Entregable2-EDA-Informe.html` en tu navegador (doble clic).
2. **Imprimir** (Ctrl/Cmd + P) → **Destino: Guardar como PDF** → tamaño **A4**.
3. Guarda como `Entregable2-EDA-Informe.pdf`.

Los saltos de página ya están definidos para que el PDF quede paginado correctamente.

## Cómo ejecutar el notebook

En un entorno con Jupyter: `jupyter notebook Entregable2-EDA.ipynb` → *Celda → Ejecutar todo*.
Requiere `pandas`, `matplotlib` y `seaborn`. Las figuras del notebook se regeneran desde
`../data/processed/bajas_consolidado.csv`.

## Reproducibilidad

```bash
cd scripts
python3 eda_motor.py            # calcula todas las métricas del EDA
python3 eda_graficos.py         # regenera las 12 figuras SVG
python3 generar_notebook_eda.py # regenera el .ipynb
python3 generar_pdf_eda.py      # regenera el informe HTML/PDF
```
