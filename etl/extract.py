#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXTRACT (Sección 1 · Extract).
Carga los datos crudos desde las fuentes CSV y verifica el contrato de esquema.
Diseñado para ser extensible: hoy lee CSV; mañana podría leer Excel o una BD
agregando una función análoga que devuelva la misma estructura (lista de dicts).
"""
import csv
import os

from config import RAW_DIR, SOURCE_FILES, EXPECTED_SOURCE_COLUMNS


def extraer(logger, archivos=None):
    """Lee los CSV de origen y devuelve (filas, metadatos).

    filas: lista de dicts con las columnas del origen + '_source_file'.
    metadatos: dict con conteos por archivo.
    """
    archivos = archivos or SOURCE_FILES
    filas = []
    meta = {"por_archivo": {}, "total": 0}

    logger.info("== FASE EXTRACT ==")
    for nombre in archivos:
        ruta = os.path.join(RAW_DIR, nombre)
        if not os.path.exists(ruta):
            logger.warning(f"Fuente no encontrada, se omite: {ruta}")
            continue
        with open(ruta, newline="", encoding="utf-8-sig") as fh:
            lector = csv.DictReader(fh)
            _verificar_esquema(lector.fieldnames, nombre, logger)
            n_archivo = 0
            for r in lector:
                r["_source_file"] = nombre
                filas.append(r)
                n_archivo += 1
        meta["por_archivo"][nombre] = n_archivo
        logger.info(f"Extraídas {n_archivo} filas de '{nombre}'")

    meta["total"] = len(filas)
    logger.info(f"Total extraído: {meta['total']} filas de {len(meta['por_archivo'])} fuente(s)")
    return filas, meta


def _verificar_esquema(fieldnames, nombre, logger):
    """Verifica que el CSV traiga las columnas esperadas (contrato de datos)."""
    cols = set((fieldnames or []))
    faltan = [c for c in EXPECTED_SOURCE_COLUMNS if c not in cols]
    if faltan:
        logger.error(f"'{nombre}' no cumple el esquema. Faltan columnas: {faltan}")
        raise ValueError(f"Esquema inválido en {nombre}: faltan {faltan}")
