# Pipeline ETL · Bajas de Activos de TI (UAO)

**Entregable 4 — Complejidad: Alta.** Proceso automatizado que alimenta el dashboard:
extrae de los CSV de origen, limpia y enriquece, valida la integridad, calcula los KPIs y
publica la tabla de hechos lista para Power BI, con logging completo.

## Arquitectura (modular)

```
etl/
├── config.py          # rutas, esquema, parámetros de negocio y umbrales
├── logger.py          # (5) Logs: consola + archivo con marca de tiempo
├── extract.py         # (1) Extract: carga CSV + verifica contrato de esquema
├── transform.py       # (2) Transform: limpieza, derivación y cálculo de KPIs
├── validate.py        # (3) Validación: 7 checks de integridad
├── load.py            # (4) Load: escritura atómica de CSV (Power BI) y KPIs (JSON)
├── run_pipeline.py    # Orquestador: encadena las 4 fases + manejo de errores
├── logs/              # bitácoras de cada ejecución
└── scheduler/         # (7) Automatización: cron, Windows, GitHub Actions
```

Flujo: **Extract → Transform (+KPIs) → Validate → Load**, orquestado por `run_pipeline.py`.

## Cómo ejecutar (Sección 6 · Documentación)

Requisitos: **Python 3.8+** (solo librería estándar; no requiere dependencias externas).

```bash
cd etl
python3 run_pipeline.py              # ejecución normal (escribe al destino)
python3 run_pipeline.py --dry-run    # valida y calcula, sin escribir
```

### Entradas
- `data/raw/bajas_2025.csv`
- `data/raw/bajas_2026.csv`

### Salidas
- `data/processed/bajas_consolidado.csv` — tabla de hechos para Power BI (UTF-8 + BOM).
- `data/kpis/kpis.json` — los 14 KPIs del Entregable 3 calculados.
- `etl/logs/etl_<timestamp>.log` — bitácora de la ejecución.

### Códigos de salida
| Código | Significado |
|---|---|
| 0 | Éxito |
| 1 | Falló la validación (datos no aptos; no se escribe nada) |
| 2 | Error inesperado (ver traza en el log) |

## Fases en detalle

1. **Extract** — lee cada CSV, verifica que traiga las 7 columnas del contrato; omite con
   advertencia las fuentes ausentes.
2. **Transform** — normaliza vacíos (`NG`, `N/N`, `Sin código`…), parsea fechas y cantidades,
   deriva `Categoria`, `Marca`, dimensiones de tiempo e indicadores de calidad; además
   **calcula los 14 KPIs**.
3. **Validate** — 7 checks: volumen mínimo, esquema de salida, % de fechas inválidas,
   cantidades positivas, años en rango, consecutivo presente y trazabilidad. Los **errores
   abortan** el pipeline; las **advertencias** se registran.
4. **Load** — escritura **atómica** (archivo temporal + `os.replace`) para no dejar destinos
   corruptos ante un fallo.

## Validación de resultados (última ejecución verificada)

```
Extraídas 924 filas (473 + 451)  ·  Transformadas 924  ·  7/7 checks PASS
Unidades: 1322  ·  Informes: 104  ·  Sin serie: 22.3%  ·  Sin inventario: 40.4%
PIPELINE COMPLETADO · exit 0
```

## Automatización
Ver `scheduler/README-scheduler.md` (cron, Programador de Windows y GitHub Actions).

## Reproducibilidad y extensión
- **Idempotente:** cada corrida reconstruye las salidas desde cero; re-ejecutar es seguro.
- **Extensible:** para añadir una fuente nueva (p. ej. Excel o base de datos), basta con crear
  una función análoga en `extract.py` que devuelva la misma estructura de filas.
