#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VALIDACIÓN (Sección 3 · Validación).
Ejecuta checks de integridad sobre los datos transformados. Distingue entre:
  - ERRORES (rompen el pipeline): el dato no es apto para cargar.
  - ADVERTENCIAS (no rompen): se registran para seguimiento de calidad.
"""
from config import (FACT_COLUMNS, ANIOS_VALIDOS,
                    MAX_PCT_FECHAS_INVALIDAS, MIN_REGISTROS_ESPERADOS)


class ResultadoValidacion:
    def __init__(self):
        self.errores = []
        self.advertencias = []
        self.checks = []

    def ok(self):
        return len(self.errores) == 0

    def registrar(self, nombre, paso, detalle=""):
        self.checks.append((nombre, "PASS" if paso else "FAIL", detalle))


def validar(filas, metricas_transform, logger):
    logger.info("== FASE VALIDACIÓN ==")
    R = ResultadoValidacion()
    n = len(filas)

    # Check 1: volumen mínimo
    paso = n >= MIN_REGISTROS_ESPERADOS
    R.registrar("Volumen mínimo", paso, f"{n} filas (mín {MIN_REGISTROS_ESPERADOS})")
    if not paso:
        R.errores.append(f"Muy pocos registros: {n} < {MIN_REGISTROS_ESPERADOS}")

    # Check 2: esquema de salida completo
    cols_ok = all(all(c in f for c in FACT_COLUMNS) for f in filas[:1]) if filas else False
    R.registrar("Esquema de salida", cols_ok, f"{len(FACT_COLUMNS)} columnas requeridas")
    if not cols_ok:
        R.errores.append("La estructura de salida no contiene todas las columnas esperadas")

    # Check 3: % de fechas inválidas bajo umbral
    pct_fechas = 100 * metricas_transform["fechas_invalidas"] / n if n else 0
    paso = pct_fechas <= MAX_PCT_FECHAS_INVALIDAS
    R.registrar("Fechas válidas", paso, f"{pct_fechas:.1f}% inválidas (máx {MAX_PCT_FECHAS_INVALIDAS}%)")
    if not paso:
        R.errores.append(f"Demasiadas fechas inválidas: {pct_fechas:.1f}%")

    # Check 4: cantidades positivas
    neg = sum(1 for f in filas if f["Cantidad"] <= 0)
    R.registrar("Cantidades positivas", neg == 0, f"{neg} con cantidad <= 0")
    if neg:
        R.errores.append(f"{neg} registros con Cantidad <= 0")

    # Check 5: años dentro del rango esperado (advertencia)
    fuera = sum(1 for f in filas if f["Anio"] and f["Anio"] not in ANIOS_VALIDOS)
    R.registrar("Años en rango", fuera == 0, f"{fuera} fuera de {sorted(ANIOS_VALIDOS)}")
    if fuera:
        R.advertencias.append(f"{fuera} registros con año fuera del rango esperado")

    # Check 6: consecutivo presente (advertencia)
    sin_cons = sum(1 for f in filas if not f["Consecutivo"])
    R.registrar("Consecutivo presente", sin_cons == 0, f"{sin_cons} sin consecutivo")
    if sin_cons:
        R.advertencias.append(f"{sin_cons} registros sin número de documento (DITI)")

    # Check 7: trazabilidad (advertencia informativa)
    sin_inv = sum(1 for f in filas if f["TieneInventario"] == "No")
    pct_inv = 100 * sin_inv / n if n else 0
    R.registrar("Trazabilidad inventario", True, f"{pct_inv:.1f}% sin inventario (informativo)")
    if pct_inv > 25:
        R.advertencias.append(f"Trazabilidad baja: {pct_inv:.1f}% sin número de inventario")

    # Log resumen
    for nombre, estado, detalle in R.checks:
        nivel = logger.info if estado == "PASS" else logger.error
        nivel(f"  [{estado}] {nombre}: {detalle}")
    for w in R.advertencias:
        logger.warning(f"  ADVERTENCIA: {w}")

    if R.ok():
        logger.info(f"Validación superada ({len(R.checks)} checks, {len(R.advertencias)} advertencias)")
    else:
        logger.error(f"Validación FALLÓ con {len(R.errores)} error(es)")
    return R
