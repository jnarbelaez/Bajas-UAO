# Dashboard Ejecutivo · Bajas de Activos TI · UAO

Aplicación web **autocontenida en un único archivo HTML** (CSS y JavaScript embebidos, Chart.js vía CDN) que funciona como Dashboard Ejecutivo de las **solicitudes de baja de activos TI** (documentos DITI) de la Unidad de Servicio al Usuario de la Universidad Autónoma de Occidente.

## 📄 Archivo

- [`dashboard-bajas-uao.html`](dashboard-bajas-uao.html) — ábrelo directamente en cualquier navegador (doble clic). No requiere servidor ni instalación.

## 📊 Qué incluye

**KPIs principales (6 tarjetas):** unidades dadas de baja, solicitudes DITI, categorías de activo, participación de la categoría top, % de equipos de cómputo y marcas/fabricantes.

**Gráficos interactivos (Chart.js):**
1. Distribución por categoría (dona)
2. Participación por marca / fabricante (barras)
3. Tendencia mensual de bajas — unidades vs. nº de solicitudes (línea + barra)
4. Top 8 modelos / descripciones
5. Unidades por documento (DITI)

**Filtros avanzados (tiempo real, sin recargar):** mes, marca, documento DITI, buscador libre (descripción/serie/inventario) y chips por categoría, con botón de *Limpiar filtros*.

**Diseño:** minimalista y responsivo, con **modo claro/oscuro** elegante y tipografía limpia.

## 📈 Datos

Mapeados directamente desde las tablas de las solicitudes de baja:

- **343** líneas de activo
- **617** unidades
- **53** solicitudes (DITI)
- **11** categorías · **33** marcas
- Periodo: septiembre 2024 – diciembre 2025
