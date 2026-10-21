# Entregable 5 · Diseño de Visualizaciones

**Complejidad:** Media. Diseño visual del dashboard de Bajas de Activos de TI (UAO) con las 8 secciones.

## Formato
El entregable pide *Figma + PDF*. Como alternativa equivalente y editable, se entregan
**mockups vectoriales SVG de alta fidelidad** (nítidos a cualquier escala, se ven en GitHub) más un
**documento de diseño en Word** que consolida las 8 secciones.

## Archivos

| Archivo | Sección(es) | Contenido |
|---|---|---|
| `01-paleta-tipografia.svg` | 2, 3, 8 | Paleta primaria, categórica, semáforo de estados y escala tipográfica |
| `02-wireframe-layout.svg` | 1 | Wireframe de baja fidelidad (grid 12 col, 4 bandas) |
| `03-mockup-alta-fidelidad.svg` | 7 | Mockup final renderizado de la página "Resumen Ejecutivo" |
| `../entregables/Entregable5-Diseno-de-Visualizaciones.docx` | 1–8 | Documento de diseño completo |

Los mockups de las 3 páginas del dashboard Power BI están en `../powerbi/mockups/`.

## Resumen de decisiones de diseño

- **Paleta:** rojo UAO (#E2001A) como marca; azul (#2563EB) de acento; semáforo verde/ámbar/rojo para KPIs con meta.
- **Tipografía:** Segoe UI, máximo 3 niveles de jerarquía por pantalla.
- **Mapeo KPI→gráfico:** cifra→tarjeta, comparación→barras, parte-todo→dona/treemap, evolución→línea, meta→barra de progreso/gauge.
- **Interactividad:** filtros de Año, Categoría, Marca, Mes/Documento y búsqueda, con resaltado cruzado.
- **Ratios:** lienzo 1280×720 (16:9); tarjetas 230×90; línea temporal de ancho completo.

## Cómo exportar a PDF
Abre cualquier SVG o el `.docx` en tu editor y expórtalo a PDF (o *Imprimir → Guardar como PDF*).
Los SVG también pueden importarse a Figma/Illustrator si se desea seguir editando.
