# Mejoras del Dashboard — versión 2

Documento de la revisión y mejora del `dashboard-bajas-uao.html` existente.
El original **se conserva intacto**; la versión mejorada es **`dashboard-bajas-uao-v2.html`**.

## Cómo abrirlo
- **Doble clic** en `dashboard-bajas-uao-v2.html` → funciona de inmediato (datos embebidos como respaldo).
- **Con servidor** (recomendado para datos siempre al día): `python3 -m http.server` y abrir
  `http://localhost:8000/dashboard-bajas-uao-v2.html` (carga `data/bajas.json`).

---

## 1. Correcciones de calidad de datos
Aplicadas por `scripts/extraer_y_corregir.py` y materializadas en `data/bajas.json`:

- **Reclasificación**: "Teléfono Avaya pantalla" estaba marcado como **Monitor** → corregido a **Teléfono**.
- **Recuperación de marca**: 6 registros que decían "HP", "Dell", etc. en la descripción pero tenían
  marca `Genérico` fueron reasignados a su marca real.

## 2. Nuevas funcionalidades

| Mejora | Detalle |
|---|---|
| **Filtro por Año** | Nuevo selector 2025 / 2026 / ambos. |
| **KPIs año a año** | Tarjetas "Unidades 2025", "Unidades 2026" y **variación %** con indicador ▲/▼. |
| **KPIs de trazabilidad** | "% con número de serie" y "% sin N° de inventario". |
| **Gráfico comparativo 2025 vs 2026** | Barras por categoría enfrentando ambos años. |
| **Sección Calidad de datos** | Barras de progreso: % sin serial, % sin inventario, % lotes. |
| **Exportar CSV** | Botón que descarga la vista **filtrada** en CSV (UTF-8). |
| **Tema persistente** | El modo claro/oscuro se recuerda entre sesiones (`localStorage`). |
| **Accesibilidad** | `aria-label` en botones y chips navegables por teclado (Enter/Espacio). |

## 3. Correcciones técnicas (bugs)

- **Fecha en la tabla**: el original usaba `new Date(iso)`, que puede restar un día por zona horaria,
  y una condición `monthLabel(...)==null` que nunca se cumplía. v2 formatea la fecha ISO directamente
  (`dd/mm/aaaa`) sin desfase.
- **Datos desacoplados del HTML**: ahora viven en `data/bajas.json` (editable y reutilizable), con
  respaldo embebido para uso sin servidor.

## 4. Archivos añadidos

```
data/bajas.json                  ← datos corregidos (consumidos por v2)
dashboard-bajas-uao-v2.html      ← dashboard mejorado
scripts/extraer_y_corregir.py    ← extrae RAW del v1 y corrige datos
scripts/validar_logica.mjs       ← pruebas de agregación (Node)
```

## 5. Validación realizada

- ✅ Sintaxis JS verificada con `node --check` (ambos bloques de script).
- ✅ Lógica de KPIs/trazabilidad/comparativo validada con datos reales (`validar_logica.mjs`):
  935 registros · 1.338 unidades · 2025=651 / 2026=687 (+6 %) · 22 % sin serial · 40 % sin inventario.
- ✅ Servido vía HTTP local: `data/bajas.json` y el HTML responden 200.
