#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Análisis Exploratorio de Datos (EDA) — Entregable 2.
Calcula TODAS las métricas del EDA con datos reales usando solo la librería
estándar de Python, y expone funciones para generar gráficos en SVG.

Devuelve un diccionario 'R' con todos los resultados, consumido por:
  - generar_notebook_eda.py  (Jupyter .ipynb con salidas pre-calculadas)
  - generar_pdf_eda.py       (informe HTML/PDF)
"""
import csv
import os
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(BASE, "data", "processed", "bajas_consolidado.csv")


def cargar():
    with open(CSV, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def to_int(v, default=0):
    try:
        return int(float(v))
    except (ValueError, TypeError):
        return default


def analizar():
    filas = cargar()
    n = len(filas)
    cols = list(filas[0].keys()) if filas else []

    # --- 2. Dimensiones y tipos ---
    tipos = {
        "Archivo de Origen": "Texto (categórica)",
        "Fecha": "Fecha",
        "Anio": "Entero",
        "Mes": "Entero",
        "NombreMes": "Texto (categórica)",
        "AnioMes": "Texto (categórica)",
        "Trimestre": "Texto (categórica)",
        "Consecutivo": "Texto (categórica)",
        "Cantidad": "Entero (numérica)",
        "Descripcion del elemento": "Texto (libre)",
        "Categoria": "Texto (categórica)",
        "Marca": "Texto (categórica)",
        "Serie No.": "Texto (identificador)",
        "No. inventario": "Texto (identificador)",
        "IMEI": "Texto (identificador)",
        "TieneSerial": "Texto (booleana Si/No)",
        "TieneInventario": "Texto (booleana Si/No)",
        "EsLote": "Texto (booleana Si/No)",
    }

    # --- 3. Estadísticas de 'Cantidad' (única variable numérica continua de interés) ---
    cantidades = [to_int(f["Cantidad"], 1) for f in filas]
    total_unidades = sum(cantidades)
    stats_cant = {
        "n": len(cantidades),
        "suma": total_unidades,
        "media": round(statistics.mean(cantidades), 2),
        "mediana": statistics.median(cantidades),
        "moda": statistics.mode(cantidades),
        "desv_std": round(statistics.pstdev(cantidades), 2),
        "min": min(cantidades),
        "max": max(cantidades),
        "q1": _percentil(cantidades, 25),
        "q3": _percentil(cantidades, 75),
    }
    stats_cant["iqr"] = stats_cant["q3"] - stats_cant["q1"]

    # Distribuciones categóricas
    por_cat = Counter()
    por_cat_u = defaultdict(int)
    por_marca_u = defaultdict(int)
    por_anio_u = defaultdict(int)
    por_mes_u = defaultdict(int)
    por_origen = Counter()
    for f in filas:
        q = to_int(f["Cantidad"], 1)
        por_cat[f["Categoria"]] += 1
        por_cat_u[f["Categoria"]] += q
        por_marca_u[f["Marca"]] += q
        if f["Anio"]:
            por_anio_u[f["Anio"]] += q
        if f["AnioMes"]:
            por_mes_u[f["AnioMes"]] += q
        por_origen[f["Archivo de Origen"]] += 1

    # --- 4. Valores nulos / faltantes por columna ---
    def es_vacio(v):
        return v is None or str(v).strip() == ""
    nulos = {}
    for c in cols:
        faltan = sum(1 for f in filas if es_vacio(f.get(c)))
        nulos[c] = {"faltantes": faltan, "pct": round(100 * faltan / n, 1)}

    # --- 5. Duplicados ---
    # a) Filas completamente idénticas
    firmas = Counter(tuple(f[c] for c in cols) for f in filas)
    filas_dup = sum(c - 1 for c in firmas.values() if c > 1)
    # b) Seriales repetidos (excluyendo vacíos)
    seriales = [f["Serie No."] for f in filas if f["Serie No."].strip()]
    dup_serial = {s: c for s, c in Counter(seriales).items() if c > 1}
    # c) Inventarios repetidos
    invs = [f["No. inventario"] for f in filas if f["No. inventario"].strip()]
    dup_inv = {s: c for s, c in Counter(invs).items() if c > 1}

    # --- 6. Outliers en 'Cantidad' (regla IQR) ---
    lim_sup = stats_cant["q3"] + 1.5 * stats_cant["iqr"]
    lim_inf = stats_cant["q1"] - 1.5 * stats_cant["iqr"]
    outliers = [f for f in filas if to_int(f["Cantidad"], 1) > lim_sup or to_int(f["Cantidad"], 1) < lim_inf]
    outliers_top = sorted(outliers, key=lambda f: -to_int(f["Cantidad"], 1))[:8]

    # --- 7. Correlaciones (entre variables numéricas/derivadas) ---
    # Correlación Mes vs Cantidad (débil esperada) y relación año/unidades.
    meses = [to_int(f["Mes"]) for f in filas if f["Mes"]]
    cant_mes = [to_int(f["Cantidad"], 1) for f in filas if f["Mes"]]
    corr_mes_cant = _pearson(meses, cant_mes)
    # Correlación TieneSerial(1/0) vs TieneInventario(1/0)
    ser = [1 if f["TieneSerial"] == "Si" else 0 for f in filas]
    inv = [1 if f["TieneInventario"] == "Si" else 0 for f in filas]
    corr_ser_inv = _pearson(ser, inv)
    # Tabla de contingencia Serial x Inventario
    cont = Counter((f["TieneSerial"], f["TieneInventario"]) for f in filas)

    # --- 9. Score de calidad de datos ---
    completitud_serial = 100 * sum(ser) / n
    completitud_inv = 100 * sum(inv) / n
    unicidad = 100 * (1 - filas_dup / n)
    # Validez de fecha
    fechas_ok = sum(1 for f in filas if f["Fecha"])
    validez_fecha = 100 * fechas_ok / n
    # Consistencia: registros con categoría distinta de 'Otros'
    categorizados = 100 * sum(1 for f in filas if f["Categoria"] != "Otros") / n
    score = round((completitud_serial + completitud_inv + unicidad + validez_fecha + categorizados) / 5, 1)

    return {
        "n": n, "cols": cols, "tipos": tipos,
        "total_unidades": total_unidades,
        "stats_cant": stats_cant,
        "por_cat": por_cat, "por_cat_u": dict(por_cat_u),
        "por_marca_u": dict(por_marca_u), "por_anio_u": dict(por_anio_u),
        "por_mes_u": dict(por_mes_u), "por_origen": por_origen,
        "nulos": nulos,
        "filas_dup": filas_dup, "dup_serial": dup_serial, "dup_inv": dup_inv,
        "outliers": outliers, "outliers_top": outliers_top,
        "lim_sup": lim_sup, "lim_inf": lim_inf,
        "corr_mes_cant": round(corr_mes_cant, 3),
        "corr_ser_inv": round(corr_ser_inv, 3),
        "contingencia": dict(cont),
        "calidad": {
            "completitud_serial": round(completitud_serial, 1),
            "completitud_inv": round(completitud_inv, 1),
            "unicidad": round(unicidad, 1),
            "validez_fecha": round(validez_fecha, 1),
            "consistencia_cat": round(categorizados, 1),
            "score": score,
        },
    }


def _percentil(data, p):
    s = sorted(data)
    k = (len(s) - 1) * p / 100
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return s[int(k)]
    return round(s[f] + (s[c] - s[f]) * (k - f), 2)


def _pearson(x, y):
    if len(x) < 2:
        return 0.0
    mx, my = statistics.mean(x), statistics.mean(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    dx = math.sqrt(sum((a - mx) ** 2 for a in x))
    dy = math.sqrt(sum((b - my) ** 2 for b in y))
    return num / (dx * dy) if dx and dy else 0.0


if __name__ == "__main__":
    R = analizar()
    print("Registros:", R["n"], "| Columnas:", len(R["cols"]))
    print("Unidades totales:", R["total_unidades"])
    print("Stats Cantidad:", R["stats_cant"])
    print("Nulos Serie No.:", R["nulos"]["Serie No."])
    print("Nulos No. inventario:", R["nulos"]["No. inventario"])
    print("Filas duplicadas:", R["filas_dup"])
    print("Seriales duplicados:", len(R["dup_serial"]))
    print("Outliers (IQR):", len(R["outliers"]), "| límite sup:", R["lim_sup"])
    print("Corr Mes~Cantidad:", R["corr_mes_cant"])
    print("Corr Serial~Inventario:", R["corr_ser_inv"])
    print("SCORE calidad:", R["calidad"]["score"])
