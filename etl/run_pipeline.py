#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ORQUESTADOR DEL PIPELINE ETL · Bajas de Activos TI (UAO)
========================================================
Encadena las fases Extract -> Transform -> Validate -> Load, con logging
completo y manejo de errores. Es el punto de entrada del pipeline.

USO:
    python3 run_pipeline.py              # ejecución normal
    python3 run_pipeline.py --dry-run    # valida sin escribir al destino

Códigos de salida:
    0  éxito
    1  fallo de validación (datos no aptos)
    2  error inesperado
"""
import sys
import time
import traceback

from logger import get_logger
from extract import extraer
from transform import transformar, calcular_kpis
from validate import validar
from load import cargar


def main(dry_run=False):
    logger = get_logger()
    t0 = time.time()
    logger.info("=" * 60)
    logger.info("INICIO DEL PIPELINE ETL · Bajas de Activos TI (UAO)")
    logger.info(f"Modo: {'DRY-RUN (sin escritura)' if dry_run else 'NORMAL'}")
    logger.info("=" * 60)

    try:
        # 1. EXTRACT
        crudo, meta_ext = extraer(logger)

        # 2. TRANSFORM (+ KPIs)
        limpio, meta_trf = transformar(crudo, logger)
        kpis = calcular_kpis(limpio, logger)

        # 3. VALIDATE
        resultado = validar(limpio, meta_trf, logger)
        if not resultado.ok():
            logger.error("Pipeline ABORTADO: la validación encontró errores.")
            for e in resultado.errores:
                logger.error(f"  - {e}")
            return 1

        # 4. LOAD
        if dry_run:
            logger.info("DRY-RUN: se omite la escritura al destino.")
            destino = {"dry_run": True}
        else:
            destino = cargar(limpio, kpis, logger)

        dur = time.time() - t0
        logger.info("=" * 60)
        logger.info(f"PIPELINE COMPLETADO EN {dur:.2f}s")
        logger.info(f"  Extraídas:     {meta_ext['total']}")
        logger.info(f"  Transformadas: {meta_trf['total']}")
        logger.info(f"  Unidades:      {kpis['KPI-01_total_unidades']}")
        logger.info(f"  Informes:      {kpis['KPI-02_total_informes']}")
        logger.info(f"  Advertencias:  {len(resultado.advertencias)}")
        logger.info(f"  Bitácora:      {getattr(logger, 'log_path', 'n/d')}")
        logger.info("=" * 60)
        return 0

    except Exception as exc:  # noqa: BLE001
        logger.error(f"ERROR INESPERADO: {exc}")
        logger.error(traceback.format_exc())
        return 2


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    sys.exit(main(dry_run=dry))
