# Entregable 6 · Dashboard Interactivo (FUNCIONANDO)

**Complejidad:** Alta. Dashboard de Bajas de Activos de TI (UAO) operativo y navegable.

## Formato: `.pbix` o equivalente

El entregable admite **".pbix o equivalente"**. Se entregan **dos rutas complementarias**, ambas
funcionando:

1. **Dashboard web interactivo (entregable principal):** `dashboard-bajas-uao.html` — abre con doble
   clic, sin instalar nada. Es un dashboard **real y funcional** construido con Chart.js, con 3
   páginas, filtros globales, drilldowns y date range.
2. **Ruta Power BI (`.pbix`):** la carpeta `powerbi/` contiene el tema, las medidas DAX y la guía
   paso a paso (`ARMAR-PBIX-PASO-A-PASO.md`) para construir el `.pbix` nativo en Power BI Desktop
   (un `.pbix` es binario propietario y solo se genera de forma fiable dentro de esa herramienta).

## Las 9 secciones — cómo se cumplen

| # | Sección | Implementación en el dashboard web | Equivalente Power BI |
|---|---|---|---|
| 1 | **Conexión a datos** | `fetch('data/bajas.json')` con respaldo embebido | Obtener datos → CSV (`bajas_consolidado.csv`) |
| 2 | **Transformaciones BI** | Medidas calculadas en JS (KPIs, agregaciones) + dimensiones derivadas | Medidas DAX (`powerbi/medidas-dax.txt`) + tabla Calendario |
| 3 | **Página 1 · Visión general** | Pestaña "Visión general": 5 KPIs + categoría + año + tendencia | Página "Resumen Ejecutivo" |
| 4 | **Página 2 · Detalle operacional** | Pestaña "Detalle": marcas, documentos y tabla de detalle | Página "Detalle por Activo" |
| 5 | **Página 3 · Análisis comparativo** | Pestaña "Comparativo": 2025 vs 2026, calidad y estacionalidad | Página "Calidad de Datos" |
| 6 | **Filtros globales** | **Date range** (Desde/Hasta), Año, Categoría, Marca y búsqueda; aplican a las 3 páginas | Segmentadores + slicer de fechas |
| 7 | **Drilldowns** | Clic en una barra de categoría → salta a la pág. 2 filtrada; clic en marca → filtra la tabla; breadcrumb para volver | Drill down nativo de Power BI |
| 8 | **Formato profesional** | Paleta UAO, tipografía Segoe UI, tema claro/oscuro, tarjetas consistentes | Tema `tema-uao.json` |
| 9 | **Performance** | Datos en memoria, gráficos destruidos/recreados por página (solo se dibuja la activa) → carga instantánea | Modelo optimizado, medidas eficientes |

## Cómo usarlo

- **Doble clic** en `dashboard-bajas-uao.html` → funciona de inmediato (datos embebidos).
- Con servidor (datos siempre al día): `python3 -m http.server` → abrir
  `http://localhost:8000/dashboard-bajas-uao.html`.

### Interacciones destacadas
- **Date range:** selectores "Desde (mes)" y "Hasta (mes)" acotan el período en todo el tablero.
- **Drilldown:** en la Página 1, clic en una categoría lleva a la Página 2 ya filtrada; el
  breadcrumb superior muestra el filtro activo y permite quitarlo.
- **Exportar CSV** de la vista filtrada y **tema oscuro** persistente.

## Validación realizada

- ✅ Sintaxis JS verificada (`node --check`).
- ✅ Lógica funcional probada con datos reales (`scripts/validar_dashboard_bi.mjs`):
  date range (jul-2025 = 161 u.), drilldowns por categoría/marca, filtros combinados y KPIs
  (1.338 u., +6% anual) → **todas las comprobaciones OK**.
