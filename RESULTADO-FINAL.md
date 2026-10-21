# Resultado Final · Dashboard Profesional de Bajas de Activos de TI

> Universidad Autónoma de Occidente · Datos 2025–2026 · Fuente: Informes Técnicos DSU-3.1.3-FO15
> Repositorio: [`jnarbelaez/Bajas-UAO`](https://github.com/jnarbelaez/Bajas-UAO)

Este documento demuestra, con evidencia verificable, que el dashboard cumple los seis criterios de
un dashboard profesional. Cada afirmación se puede comprobar ejecutando el comando indicado.

---

## ✅ 1. Responde preguntas de negocio reales

El dashboard responde las **7 preguntas de negocio** definidas en el Entregable 1, traducidas en
**14 KPIs** (Entregable 3) y materializadas en 3 páginas interactivas (Entregable 6).

| Pregunta | Dónde se responde |
|---|---|
| ¿Cuánto y qué se da de baja? | KPIs + gráfico por categoría (Página 1) |
| ¿Qué marcas y cómo evoluciona? | Treemap + tendencia mensual (Páginas 1 y 2) |
| ¿Dónde están los picos? | Serie temporal y estacionalidad (Páginas 1 y 3) |
| ¿Qué tan trazable es el inventario? | Indicadores de calidad (Página 3) |

**Evidencia:** `entregables/Entregable1-*.docx` (preguntas) → `entregables/Entregable3-*.docx` (KPIs).

---

## ✅ 2. Basado en datos limpios y validados

No se confía en números sin verificar: el pipeline ETL valida la integridad **antes** de publicar.

- **7 checks de validación** (volumen, esquema, fechas, cantidades, años, consecutivos, trazabilidad).
- Los errores **abortan** el pipeline; nada corrupto llega al dashboard.
- Score de calidad de datos documentado: **87,2/100** (Entregable 2).

**Evidencia (ejecútalo tú mismo):**
```bash
cd etl && python3 run_pipeline.py
# → 7/7 checks PASS · 924 filas · 1.322 unidades · exit 0
```

---

## ✅ 3. Se actualiza automáticamente (no es estático)

- Pipeline **reproducible e idempotente**: reconstruye datos y KPIs desde las fuentes.
- **Scheduler** incluido para cron, Programador de Windows y GitHub Actions.

**Evidencia:** `etl/scheduler/etl-schedule.yml` (ejecución mensual automatizada).
```bash
# Añadir nuevos CSV a data/raw/ y:
cd etl && python3 run_pipeline.py   # regenera todo; el dashboard se refresca al recargar
```

---

## ✅ 4. Intuitivo y usable (no bonito pero incomprendido)

- 3 páginas con flujo claro: visión general → detalle → comparativo.
- **Filtros globales** (rango de fechas, año, categoría, marca, búsqueda) y **drilldowns** con
  breadcrumb para navegar de resumen a detalle con un clic.
- Diseño guiado por una **guía de estilo** (Entregable 5): paleta, tipografía y jerarquía.

**Evidencia (lógica verificada con datos reales):**
```bash
node scripts/validar_dashboard_bi.mjs
# → date range, drilldowns y KPIs: todas las comprobaciones OK
```

---

## ✅ 5. Documentado y mantenible (no es un misterio)

- **README maestro** con setup y estructura completa.
- Documentación por capa: `etl/README.md`, `diseno/README.md`, `powerbi/ARMAR-PBIX-PASO-A-PASO.md`.
- Documentación técnica, guía de usuario, diccionario de datos, limitaciones y roadmap (Entregable 7).
- Todo el código es **reproducible** mediante los scripts de `scripts/`.

**Evidencia:** 12+ documentos de apoyo; cada entregable tiene su README.

---

## ✅ 6. Presentable en una entrevista (portfoliable)

- Proyecto **end-to-end**: datos crudos → ETL → KPIs → diseño → dashboard → documentación.
- Historia de commits limpia con **10 Pull Requests** revisables.
- **Presentación ejecutiva** (13 slides) y **guion de video** de 5 min listos.
- Decisiones de ingeniería explicadas (validación, idempotencia, escritura atómica).

**Evidencia:** `entregables/Entregable7-Presentacion-Ejecutiva.pptx` + historial del repositorio.

---

## Resumen de los 7 entregables

| # | Entregable | Complejidad | Formato | Estado |
|---|-----------|-------------|---------|--------|
| 1 | Especificación de Requisitos | Básica | Word | ✅ |
| 2 | Análisis Exploratorio de Datos | Media | Notebook + Informe | ✅ |
| 3 | KPIs e Indicadores | Media | Word | ✅ |
| 4 | Pipeline ETL | Alta | Python + Notebook | ✅ |
| 5 | Diseño de Visualizaciones | Media | SVG + Word | ✅ |
| 6 | Dashboard Interactivo | Alta | Web + Power BI | ✅ |
| 7 | Documentación y Presentación | Media | Word + PPTX + guion | ✅ |

---

## Cifras clave del proyecto

- **1.322** unidades dadas de baja · **924** registros · **104** informes técnicos.
- **2025:** 651 u. · **2026:** 671 u. · variación **+3,1%**.
- Categoría líder: **Mouse (20,7%)** · Marca líder: **Dell (33,7%)**.
- Calidad de datos: **87,2/100** · oportunidad: trazabilidad de inventario (40,4% sin registrar).
