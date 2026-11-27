#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPORT DASHBOARD (parte de la fase Load).
Genera data/bajas.json con el formato que consume el dashboard web y actualiza
los datos de respaldo embebidos en dashboard-bajas-uao.html (para que funcione
con doble clic). Así el dashboard sale siempre de la misma fuente validada que
la tabla de hechos.
"""
import json
import os
import re

from config import ROOT

OUTPUT_JSON = os.path.join(ROOT, "data", "bajas.json")
DASHBOARD_HTML = os.path.join(ROOT, "dashboard-bajas-uao.html")

# Categorías del ETL -> categorías que usa el dashboard
CAT_DASHBOARD = {
    "Telefonia IP/Fija": "Teléfono",
    "Telefonia movil": "Celular",
    "Computadores de escritorio": "CPU/Computador",
    "Computadores portatiles": "Portátil",
    "Monitores/Pantallas": "Monitor",
    "Teclados": "Teclado",
    "Mouse": "Mouse",
    "Diademas/Audio": "Diadema/Audio",
    "Tabletas": "Tablet",
    "Redes/Networking": "Red/Networking",
}
MARCA_DASHBOARD = {"Sin marca/Generico": "Genérico"}


def a_formato_dashboard(filas):
    out = []
    for f in filas:
        out.append({
            "src": f["Archivo de Origen"],
            "doc": f["Consecutivo"],
            "date": f["Fecha"],
            "qty": f["Cantidad"],
            "cat": CAT_DASHBOARD.get(f["Categoria"], "Otros"),
            "desc": f["Descripcion del elemento"],
            "brand": MARCA_DASHBOARD.get(f["Marca"], f["Marca"]),
            "serie": f["Serie No."],
            "inv": f["No. inventario"] or f["IMEI"],
        })
    return out


def exportar(filas, logger):
    registros = a_formato_dashboard(filas)

    tmp = OUTPUT_JSON + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(registros, fh, ensure_ascii=False, indent=0)
    os.replace(tmp, OUTPUT_JSON)
    logger.info(f"JSON del dashboard escrito: {OUTPUT_JSON} ({len(registros)} registros)")

    # Respaldo embebido en el HTML (funciona con doble clic)
    if not os.path.exists(DASHBOARD_HTML):
        logger.warning("No se encontró el HTML del dashboard; se omite el respaldo embebido")
        return len(registros)
    with open(DASHBOARD_HTML, encoding="utf-8") as fh:
        html = fh.read()
    patron = re.compile(r"window\.RAW_FALLBACK = \[.*?\];", re.DOTALL)
    if not patron.search(html):
        logger.warning("El HTML no contiene RAW_FALLBACK; se omite el respaldo embebido")
        return len(registros)
    nuevo = "window.RAW_FALLBACK = " + json.dumps(registros, ensure_ascii=False, separators=(",", ":")) + ";"
    html = patron.sub(lambda _m: nuevo, html, count=1)
    with open(DASHBOARD_HTML, "w", encoding="utf-8") as fh:
        fh.write(html)
    logger.info("Respaldo embebido del dashboard actualizado")
    return len(registros)
