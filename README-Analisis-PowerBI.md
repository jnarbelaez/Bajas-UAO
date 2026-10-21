# Proyecto: Desarrollo de Dashboard Profesional
## Bajas de Activos del Área de Tecnología (TI)

**Rol:** Experto en extracción y análisis de datos
**Usuario objetivo:** Empleado encargado de la administración de los Activos del área de Tecnología
**Herramienta de visualización:** Power BI (interactivo)
**Datos:** Consolidado **2025 + 2026**
**Fuente:** Informes Técnicos para Baja o Devolución de Activos — formato `DSU-3.1.3-FO15`

---

## 1. Objetivo del proyecto

Transformar los registros de **bajas de activos tecnológicos** (contenidos en los PDF/CSV
`Bajas 2025` y `bajas 2026`) en un **dashboard profesional e interactivo** que permita al
administrador de activos de TI responder preguntas como:

- ¿Cuántos activos se dieron de baja y de qué tipo?
- ¿Cómo evoluciona el volumen de bajas mes a mes y año contra año?
- ¿Qué categorías y marcas concentran las bajas?
- ¿Qué tan completa es la trazabilidad (serial / número de inventario)?

## 2. Mapeo del formato de origen (DSU-3.1.3-FO15 → datos)

Cada CSV reproduce las columnas del Informe Técnico:

| Campo del Informe Técnico | Columna del dato |
|---|---|
| Fecha | `Fecha` |
| Consecutivo | `Consecutivo` |
| Cantidad | `Cantidad` |
| Descripción del Elemento | `Descripción del elemento` |
| Serie No. | `Serie No.` |
| No. Inventario | `No. inventario` |

> Nota: el formato original incluye un campo **"Estado"** (Dañado / Obsoleto / Bueno) que
> **no viene en los CSV**. Se dejó documentado como mejora futura (ver sección 6).

## 3. Estructura del repositorio

```
.
├── README.md                     ← este documento
├── GUIA_POWER_BI.md              ← paso a paso para construir el dashboard
├── data/
│   ├── raw/
│   │   ├── bajas_2025.csv         ← datos originales 2025
│   │   └── bajas_2026.csv         ← datos originales 2026
│   └── processed/
│       ├── bajas_consolidado.csv  ← TABLA DE HECHOS (cargar en Power BI)
│       ├── resumen_por_categoria.csv
│       ├── resumen_por_anio.csv
│       ├── resumen_por_mes.csv
│       └── resumen_por_marca.csv
├── scripts/
│   └── procesar_bajas.py          ← ETL reproducible (solo stdlib de Python)
└── reportes/
    └── analisis_eda.txt           ← hallazgos del análisis exploratorio
```

## 4. Qué hace el proceso de datos (ETL)

`scripts/procesar_bajas.py`:

1. **Consolida** 2025 + 2026 en una sola base.
2. **Limpia**: normaliza fechas (`dd/mm/aaaa` → ISO), cantidades, y marca como vacíos los
   valores no informativos (`NG`, `N/N`, `Sin código`, etc.).
3. **Enriquece** con columnas de análisis:
   - Temporales: `Anio`, `Mes`, `NombreMes`, `AnioMes`, `Trimestre`.
   - De negocio: **`Categoria`** (Mouse, Teclados, Telefonía IP/Fija, Computadores…)
     y **`Marca`** (Dell, Apple, Avaya, Cisco…), derivadas por reglas sobre la descripción.
   - De calidad: `TieneSerial`, `TieneInventario`, `EsLote`, `IMEI`.
4. **Exporta** la base en UTF-8 (BOM) lista para Power BI + tablas resumen + reporte EDA.

## 5. Hallazgos principales (EDA)

> Cifras exactas en `reportes/analisis_eda.txt`.

- **1.322 unidades** dadas de baja en **924 registros**, distribuidas en **104 informes técnicos**.
- Volumen equilibrado entre años: **2025 = 651 u.** y **2026 = 671 u.** (+3 % aprox.).
- **Periféricos** dominan las bajas: **Mouse (20,7 %)**, **Teclados (16,9 %)** y
  **Telefonía IP/Fija (18,8 %)** suman más de la mitad del total.
- Marcas líderes: **Dell (33,7 %)** y **Avaya (11,9 %)**; un tercio son genéricos/sin marca
  (típico de mouse, diademas y accesorios).
- **Picos de baja**: julio 2025 (161 u.) y abril 2026 (135 u.).
- **Oportunidad de mejora en trazabilidad**: 22 % de registros sin serial y 40 % sin número
  de inventario; útil para reforzar el control documental.

## 6. Mejoras futuras sugeridas

- Incorporar el campo **Estado** (Dañado/Obsoleto/Bueno) del formato original para analizar
  motivos de baja y decisiones de disposición.
- Añadir **valor contable / fecha de compra** del activo para estimar vida útil y depreciación.
- Programar actualización periódica del CSV y publicar el `.pbix` en Power BI Service.

## 7. Cómo reproducir

```bash
python3 scripts/procesar_bajas.py
```

Luego sigue **`GUIA_POWER_BI.md`** para construir el dashboard interactivo.
