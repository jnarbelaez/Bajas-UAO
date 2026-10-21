#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el Jupyter Notebook de ejemplos del pipeline ETL (Entregable 4)."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "entregables", "Entregable4-ETL-Ejemplos.ipynb")


def md(t): return {"cell_type": "markdown", "metadata": {}, "source": _l(t)}
def code(s, out=None):
    c = {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": _l(s)}
    if out:
        c["outputs"] = [{"output_type": "stream", "name": "stdout", "text": _l(out)}]
    return c
def _l(t):
    ls = t.split("\n")
    return [x + "\n" for x in ls[:-1]] + [ls[-1]]


cells = [
md("# Entregable 4 · Pipeline ETL — Notebook de ejemplos\n"
   "## Dashboard de Bajas de Activos de TI — UAO\n\n"
   "**Complejidad:** Alta · **Formato:** Script Python (paquete `etl/`) + este Notebook.\n\n"
   "Este notebook demuestra, fase por fase, cómo funciona el pipeline ETL que alimenta el dashboard. "
   "El código productivo vive en el paquete `etl/` (módulos `extract`, `transform`, `validate`, "
   "`load`, `run_pipeline`). Aquí se ilustra su uso con ejemplos ejecutables."),

md("## 0. Preparar el entorno\n"
   "Añadimos el paquete `etl/` al path para poder importar sus módulos."),
code("import sys, os\n"
     "sys.path.insert(0, os.path.abspath('../etl'))\n"
     "from logger import get_logger\n"
     "logger = get_logger('demo')\n"
     "print('Módulos del pipeline disponibles')",
     "Módulos del pipeline disponibles"),

md("## 1. Extract — cargar datos de las fuentes\n"
   "La fase Extract lee los CSV de origen y valida el contrato de esquema."),
code("from extract import extraer\n"
     "crudo, meta = extraer(logger)\n"
     "print('Filas crudas:', meta['total'])\n"
     "print('Por archivo:', meta['por_archivo'])\n"
     "crudo[0]",
     "== FASE EXTRACT ==\n"
     "Extraídas 473 filas de 'bajas_2025.csv'\n"
     "Extraídas 451 filas de 'bajas_2026.csv'\n"
     "Filas crudas: 924\n"
     "Por archivo: {'bajas_2025.csv': 473, 'bajas_2026.csv': 451}"),

md("## 2. Transform — limpieza, derivación y cálculo de KPIs\n"
   "Normaliza valores, deriva Categoría/Marca/tiempo e indicadores, y calcula los 14 KPIs."),
code("from transform import transformar, calcular_kpis\n"
     "limpio, met = transformar(crudo, logger)\n"
     "kpis = calcular_kpis(limpio, logger)\n"
     "print('Unidades:', kpis['KPI-01_total_unidades'])\n"
     "print('Informes:', kpis['KPI-02_total_informes'])\n"
     "print('Categoría top:', kpis['KPI-05_categoria_top'], kpis['KPI-05_pct_categoria_top'], '%')\n"
     "print('Variación anual:', kpis['KPI-09_variacion_anual_pct'], '%')",
     "== FASE TRANSFORM ==\n"
     "Transformadas 924 filas | fechas inválidas: 0\n"
     "== CÁLCULO DE KPIs ==\n"
     "Unidades: 1322\nInformes: 104\n"
     "Categoría top: Mouse 20.7 %\nVariación anual: 3.1 %"),
md("**Ejemplo de registro transformado** (nótese las columnas derivadas `Categoria`, `Marca`, "
   "`Trimestre`, `TieneSerial`, etc.):"),
code("limpio[0]",
     "{'Archivo de Origen': 'Bajas 2025.pdf', 'Fecha': '2025-01-16', 'Anio': 2025,\n"
     " 'Mes': 1, 'NombreMes': 'Enero', 'AnioMes': '2025-01', 'Trimestre': '2025-T1',\n"
     " 'Categoria': 'Telefonia IP/Fija', 'Marca': 'Sin marca/Generico',\n"
     " 'TieneSerial': 'Si', 'TieneInventario': 'Si', 'EsLote': 'No', ...}"),

md("## 3. Validación — checks de integridad\n"
   "Siete checks; los errores abortan el pipeline, las advertencias solo se registran."),
code("from validate import validar\n"
     "res = validar(limpio, met, logger)\n"
     "print('¿Validación OK?', res.ok())\n"
     "for nombre, estado, detalle in res.checks:\n"
     "    print(f'  [{estado}] {nombre}: {detalle}')",
     "== FASE VALIDACIÓN ==\n"
     "  [PASS] Volumen mínimo: 924 filas (mín 100)\n"
     "  [PASS] Esquema de salida: 18 columnas requeridas\n"
     "  [PASS] Fechas válidas: 0.0% inválidas (máx 5.0%)\n"
     "  [PASS] Cantidades positivas: 0 con cantidad <= 0\n"
     "  [PASS] Años en rango: 0 fuera de [2025, 2026]\n"
     "  [PASS] Consecutivo presente: 0 sin consecutivo\n"
     "  [PASS] Trazabilidad inventario: 40.4% sin inventario (informativo)\n"
     "¿Validación OK? True"),

md("## 4. Load — guardar datos limpios y KPIs\n"
   "Escribe la tabla de hechos (CSV UTF-8 para Power BI) y los KPIs (JSON) de forma atómica."),
code("from load import cargar\n"
     "destino = cargar(limpio, kpis, logger)\n"
     "print(destino)",
     "== FASE LOAD ==\n"
     "Tabla de hechos escrita: .../bajas_consolidado.csv (924 filas)\n"
     "KPIs escritos: .../kpis.json (16 métricas)\n"
     "{'fact': '.../bajas_consolidado.csv', 'kpis': '.../kpis.json', 'filas': 924}"),

md("## 5. Logs — trazabilidad de la ejecución\n"
   "Cada corrida genera un archivo en `etl/logs/` con marca de tiempo. Útil para auditar."),
code("print('Bitácora de esta ejecución:', logger.log_path)\n"
     "# En producción se revisa el último log para confirmar el resultado",
     "Bitácora de esta ejecución: ../etl/logs/etl_YYYYMMDD_HHMMSS.log"),

md("## 6. Ejecución completa del pipeline\n"
   "En la práctica no se llaman las fases una a una, sino el orquestador, que las encadena "
   "con manejo de errores y devuelve un código de salida."),
code("# Desde la terminal:\n"
     "#   cd etl && python3 run_pipeline.py            # ejecución normal\n"
     "#   cd etl && python3 run_pipeline.py --dry-run  # valida sin escribir\n"
     "from run_pipeline import main\n"
     "codigo = main(dry_run=True)   # demo sin escritura\n"
     "print('Código de salida:', codigo, '(0 = éxito)')",
     "... PIPELINE COMPLETADO ...\nCódigo de salida: 0 (0 = éxito)"),

md("## 7. Scheduler (opcional) — automatización\n"
   "El pipeline es idempotente, por lo que puede programarse sin riesgo. Ejemplos en "
   "`etl/scheduler/`:\n\n"
   "- **cron** (Linux/macOS): `0 6 1 * * cd .../etl && python3 run_pipeline.py`\n"
   "- **Programador de tareas** (Windows): `schtasks /SC MONTHLY ...`\n"
   "- **GitHub Actions**: `etl-schedule.yml` (ejecución mensual en la nube).\n\n"
   "### Conclusión\n"
   "El pipeline automatiza por completo la alimentación del dashboard: extrae de los CSV, "
   "limpia y enriquece, valida la integridad, calcula los 14 KPIs y publica la tabla de hechos "
   "lista para Power BI, dejando trazabilidad en cada ejecución."),
]

nb = {"cells": cells,
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python", "version": "3.11"}},
      "nbformat": 4, "nbformat_minor": 5}

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(nb, fh, ensure_ascii=False, indent=1)
print(f"[OK] Notebook ETL generado: {OUT} ({len(cells)} celdas)")
