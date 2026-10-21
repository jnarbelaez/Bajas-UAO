# Dashboard de Bajas de Activos de TI — Universidad Autónoma de Occidente

Proyecto integral de analítica: desde los datos crudos de **bajas de activos tecnológicos**
(formato institucional DSU-3.1.3-FO15) hasta un **dashboard interactivo funcionando**, con pipeline
ETL, KPIs, diseño visual y documentación completa. Período analizado: **2025–2026**.

> **Rol del proyecto:** analítica de datos para el responsable de la administración de activos
> del área de Tecnología (TI). **Usuario final:** equipo de TI, Compras y Auditoría.

---

## 🚀 Inicio rápido (setup)

**Requisitos:** solo un navegador web. Opcional: Python 3.8+ para regenerar datos/ejecutar el ETL.

### Opción 1 — Ver el dashboard (sin instalar nada)
Abre **`dashboard-bajas-uao.html`** con doble clic en cualquier navegador. Funciona de inmediato
(los datos van embebidos como respaldo).

### Opción 2 — Con servidor local (datos siempre al día)
```bash
git clone https://github.com/jnarbelaez/Bajas-UAO.git
cd Bajas-UAO
python3 -m http.server 8000
# Abrir http://localhost:8000/dashboard-bajas-uao.html
```

### Opción 3 — Regenerar datos y KPIs con el pipeline ETL
```bash
cd etl
python3 run_pipeline.py        # Extract → Transform → Validate → Load
# Genera data/processed/bajas_consolidado.csv y data/kpis/kpis.json
```

### Opción 4 — Construir el dashboard en Power BI
Sigue `powerbi/ARMAR-PBIX-PASO-A-PASO.md` (tema, medidas DAX y guía de 8 fases).

---

## 📂 Estructura del repositorio

```
.
├── dashboard-bajas-uao.html      # ⭐ Dashboard interactivo (3 páginas, drilldowns, date range)
├── README.md                     # este archivo
├── data/
│   ├── raw/                      # CSV de origen (bajas_2025, bajas_2026)
│   ├── processed/                # tabla de hechos consolidada (para Power BI)
│   ├── kpis/                     # KPIs calculados (JSON)
│   └── bajas.json                # datos que consume el dashboard web
├── etl/                          # E4 · Pipeline ETL (paquete modular + scheduler)
├── powerbi/                      # E4/E6 · Tema, medidas DAX, guía .pbix y mockups
├── diseno/                       # E5 · Wireframes, paleta y mockups de alta fidelidad
├── entregables/                  # E1–E7 · Documentos de cada entregable
├── reportes/                     # Análisis EDA en texto
├── scripts/                      # Generadores y validadores reproducibles
└── legacy/                       # Artefactos de iteraciones previas (histórico)
```

> 📌 **¿Buscas una visión de cierre?** Lee **[`RESULTADO-FINAL.md`](RESULTADO-FINAL.md)**: demuestra,
> con evidencia verificable, cómo el dashboard cumple los seis criterios de un dashboard profesional.

---

## 📦 Entregables del proyecto

| # | Entregable | Ubicación | Formato |
|---|-----------|-----------|---------|
| 1 | Especificación de Requisitos | `entregables/Entregable1-*.docx` | Word |
| 2 | Análisis Exploratorio de Datos | `entregables/Entregable2-EDA.*` | Notebook + Informe |
| 3 | KPIs e Indicadores | `entregables/Entregable3-*.docx` | Word |
| 4 | Pipeline ETL | `etl/` + `entregables/Entregable4-*.ipynb` | Python + Notebook |
| 5 | Diseño de Visualizaciones | `diseno/` + `entregables/Entregable5-*.docx` | SVG + Word |
| 6 | Dashboard Interactivo | `dashboard-bajas-uao.html` + `powerbi/` | Web + Power BI |
| 7 | Documentación y Presentación | `entregables/Entregable7-*` | Word + PPTX + guion |

---

## 📊 Resultados clave (datos reales 2025–2026)

- **1.322 unidades** dadas de baja en **924 registros** y **104 informes técnicos**.
- Equilibrio interanual: 2025 = 651 u. · 2026 = 671 u. (**+3,1 %**).
- Categorías líderes: **Mouse (20,7 %)**, Telefonía IP (18,8 %), Teclados (16,9 %).
- Marcas: **Dell (33,7 %)**, Avaya (11,9 %).
- Calidad de datos: **score 87,2/100**; oportunidad de mejora en trazabilidad
  (**40,4 % sin inventario**, 22,3 % sin serie).

---

## 🔄 Mantenimiento

1. Añade o reemplaza los CSV en `data/raw/`.
2. Ejecuta `cd etl && python3 run_pipeline.py` (regenera la tabla de hechos y los KPIs).
3. En el dashboard web pulsa recargar; en Power BI, **Actualizar**.

El pipeline es idempotente y valida la integridad antes de escribir, por lo que re-ejecutar es seguro.

---

## 📄 Documentación

- **Guía de usuario y documentación técnica:** `entregables/Entregable7-Documentacion.docx`
- **Cómo armar el .pbix:** `powerbi/ARMAR-PBIX-PASO-A-PASO.md`
- **Pipeline ETL:** `etl/README.md`
- **Diseño visual:** `diseno/README.md`

---

*Universidad Autónoma de Occidente · Fuente: Informes Técnicos para Baja o Devolución de Activos
(DSU-3.1.3-FO15).*
