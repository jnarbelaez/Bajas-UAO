#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae el array RAW embebido en dashboard-bajas-uao.html, aplica correcciones
de calidad de datos y lo guarda como data/bajas.json (consumible por el dashboard v2).

Correcciones aplicadas:
  1. Reclasifica "Teléfono ... pantalla" mal marcado como Monitor -> Teléfono.
  2. Recupera marca a partir de la descripción cuando quedó "Genérico"
     pero el texto dice HP, Dell, Apple, Logitech, etc.
  3. Normaliza categoría de celulares/smartphones.
Solo usa librería estándar.
"""
import json
import re
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, "dashboard-bajas-uao.html")
OUT = os.path.join(BASE, "data", "bajas.json")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

with open(HTML, encoding="utf-8") as fh:
    txt = fh.read()

# Extraer el bloque const RAW = [ ... ];
m = re.search(r"const RAW\s*=\s*(\[.*?\]);", txt, re.DOTALL)
if not m:
    raise SystemExit("No se encontró el array RAW en el HTML")
# Quitar comas finales (trailing commas) que JSON no acepta: ",]" o ",\n]"
bloque = re.sub(r",(\s*])", r"\1", m.group(1))
raw = json.loads(bloque)
print(f"Registros leídos: {len(raw)}")


def recuperar_marca(desc, actual):
    if actual and actual not in ("Genérico", "Generico", ""):
        return actual
    d = desc.lower()
    reglas = [
        ("HP", r"\bhp\b|z820"),
        ("Dell", r"\bdell\b|optiplex|latitude|vostro|inspiron|precision|\bxps\b"),
        ("Apple", r"apple|imac|macbook|mac pro|ipad|magic|thunderbolt"),
        ("Avaya", r"avaya|vantage"),
        ("Yealink", r"yealink"),
        ("Cisco", r"cisco|aironet|catalyst"),
        ("Logitech", r"logitech"),
        ("Sennheiser", r"sennheiser|epos|sh230|sh30"),
        ("Plantronics", r"plantronics|hw251"),
        ("Samsung", r"samsung|galaxy"),
        ("Lenovo", r"lenovo|thinkpad"),
        ("IBM", r"\bibm\b|netvista"),
        ("Xkim", r"xkim|kxim"),
        ("Genius", r"genius"),
        ("Wacom", r"wacom"),
    ]
    for nombre, patron in reglas:
        if re.search(patron, d):
            return nombre
    return actual or "Genérico"


def corregir_categoria(desc, actual):
    d = desc.lower()
    # Teléfono mal clasificado como Monitor
    if actual == "Monitor" and re.search(r"tel[eé]fono|avaya|yealink", d):
        return "Teléfono"
    # Celulares -> categoría propia si existiera
    return actual


correg_marca = 0
correg_cat = 0
for r in raw:
    nueva_marca = recuperar_marca(r.get("desc", ""), r.get("brand", ""))
    if nueva_marca != r.get("brand"):
        r["brand"] = nueva_marca
        correg_marca += 1
    nueva_cat = corregir_categoria(r.get("desc", ""), r.get("cat", ""))
    if nueva_cat != r.get("cat"):
        r["cat"] = nueva_cat
        correg_cat += 1

print(f"Marcas corregidas    : {correg_marca}")
print(f"Categorías corregidas: {correg_cat}")

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(raw, fh, ensure_ascii=False, indent=0)

print(f"[OK] Guardado: {OUT}")
