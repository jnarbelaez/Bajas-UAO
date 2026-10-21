#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de logging del pipeline ETL (Sección 5 · Logs).
Registra cada ejecución en consola y en un archivo con marca de tiempo,
de modo que quede trazabilidad de qué pasó en cada corrida.
"""
import logging
import os
from datetime import datetime

from config import LOG_DIR


def get_logger(nombre="etl_bajas"):
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(nombre)
    if logger.handlers:          # evita duplicar handlers en re-ejecuciones
        return logger
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

    # Handler a consola
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # Handler a archivo (una bitácora por ejecución)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"etl_{ts}.log")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    logger.log_path = log_path
    return logger
