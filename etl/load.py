#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOAD (Sección 4 · Load).
Escribe la tabla de hechos limpia (CSV UTF-8 con BOM, apto para Power BI) y
los KPIs calculados (JSON). Escribe primero a un archivo temporal y luego lo
renombra (escritura atómica) para no dejar un destino corrupto si algo falla.
"""
import csv
import json
import os

from config import OUTPUT_FACT, OUTPUT_KPIS, PROCESSED_DIR, KPI_DIR, FACT_COLUMNS


def cargar(filas, kpis, logger):
    logger.info("== FASE LOAD ==")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(KPI_DIR, exist_ok=True)

    # 1) Tabla de hechos -> CSV (escritura atómica)
    tmp = OUTPUT_FACT + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=FACT_COLUMNS)
        w.writeheader()
        for f in filas:
            w.writerow({c: f.get(c, "") for c in FACT_COLUMNS})
    os.replace(tmp, OUTPUT_FACT)
    logger.info(f"Tabla de hechos escrita: {OUTPUT_FACT} ({len(filas)} filas)")

    # 2) KPIs -> JSON
    tmp_k = OUTPUT_KPIS + ".tmp"
    with open(tmp_k, "w", encoding="utf-8") as fh:
        json.dump(kpis, fh, ensure_ascii=False, indent=2)
    os.replace(tmp_k, OUTPUT_KPIS)
    logger.info(f"KPIs escritos: {OUTPUT_KPIS} ({len(kpis)} métricas)")

    return {"fact": OUTPUT_FACT, "kpis": OUTPUT_KPIS, "filas": len(filas)}
