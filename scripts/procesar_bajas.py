#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proyecto: Dashboard Profesional - Bajas de Activos de Tecnologia (TI)
=====================================================================
Rol del analista: Experto en extraccion y analisis de datos.
Usuario final:    Empleado encargado de la administracion de Activos del area de TI.

Este script:
  1. Consolida las bajas 2025 + 2026 en una sola base.
  2. Limpia y normaliza (fechas, cantidades, seriales, inventario).
  3. Deriva columnas de analisis: Anio, Mes, NombreMes, AnioMes, Trimestre,
     Categoria del activo, Marca, TieneSerial, TieneInventario, EsLote.
  4. Exporta la base lista para Power BI (UTF-8 BOM, separador coma).
  5. Genera un reporte EDA en texto (hallazgos y KPIs) y tablas resumen.

Solo usa la libreria estandar de Python (csv, datetime, re, collections).
"""

import csv
import re
import os
from datetime import datetime
from collections import defaultdict, Counter

# -------------------------------------------------------------------------
# Rutas
# -------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORT_DIR = os.path.join(BASE_DIR, "reportes")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

ARCHIVOS = [
    os.path.join(RAW_DIR, "bajas_2025.csv"),
    os.path.join(RAW_DIR, "bajas_2026.csv"),
]

MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}

# -------------------------------------------------------------------------
# Clasificadores de negocio (reglas sobre "Descripción del elemento")
# -------------------------------------------------------------------------
def categorizar(desc):
    """Asigna una Categoria de activo TI a partir de la descripcion."""
    d = desc.lower()
    # El orden importa: reglas mas especificas primero.
    if re.search(r"tel[eé]fono|telefono|avaya|yealink|sip|vantage|celular|smartphone|alcatel|motorola|samsung galaxy|nokia|panasonic|gsm", d):
        if re.search(r"celular|smartphone|galaxy|alcatel|motorola|nokia|gsm|moto e", d):
            return "Telefonia movil"
        return "Telefonia IP/Fija"
    if re.search(r"diadema|headset|audifono|audífono", d):
        return "Diademas/Audio"
    if re.search(r"teclado|keyboard", d):
        return "Teclados"
    if re.search(r"mouse|rat[oó]n", d):
        return "Mouse"
    if re.search(r"monitor|pantalla|display|thunderbolt|cinema display|minitor", d):
        return "Monitores/Pantallas"
    if re.search(r"portatil|portátil|laptop|macbook|latitude|inspiron|vostro|thinkpad|precision|notebook", d):
        return "Computadores portatiles"
    if re.search(r"cpu|computador|optiplex|desktop|imac|mac pro|macpro|netvista|compaq|todo en uno|aio|xps|all.?in.?one|mini pc|didactico", d):
        return "Computadores de escritorio"
    if re.search(r"ipad|tablet|tableta|nexus", d):
        return "Tabletas"
    if re.search(r"switch|enrutador|router|concentrador|power injector|cisco|aironet", d):
        return "Redes/Networking"
    if re.search(r"servidor|lto|nas|disco|sdd|ssd|hdd|backup|seagate|duro|sata dock", d):
        return "Almacenamiento/Servidores"
    if re.search(r"ups|regulador|multitoma|fuente de poder|cargador|power adapter|adaptador de corriente|injector", d):
        return "Energia/UPS"
    if re.search(r"camara|cámara|dlink|proyector|microfono|micrófono|parlante|wacom|digitaliz|calibrador|leap motion|microscopio|scaner|esc[aá]ner|generator|character", d):
        return "Audiovisual/Perifericos especiales"
    if re.search(r"impresora|fax|codigo de barras|código de barras", d):
        return "Impresion/Fax"
    if re.search(r"tarjeta|receptor|modem|módem|pcie|pci|radeon|red rocket|video", d):
        return "Componentes/Tarjetas"
    if re.search(r"silla|mesa", d):
        return "Mobiliario"
    if re.search(r"lote de cable|cable|terminal vga|hdmi|ponchado|crimper|tester|kit|guaya|soporte|trípode|tripode|tablero|tome su numero|lápiz|lapiz|apple pen|digiturno|modulo|módulo|base|tajalapiz|space navigator|dock", d):
        return "Accesorios/Insumos"
    return "Otros"


def marca(desc):
    """Detecta la marca principal mencionada en la descripcion."""
    d = desc.lower()
    marcas = [
        ("Dell", r"\bdell\b|optiplex|latitude|vostro|inspiron|precision|xps"),
        ("Apple", r"apple|imac|macbook|mac pro|macpro|ipad|magsafe|thunderbolt|magic"),
        ("Avaya", r"avaya|vantage"),
        ("Yealink", r"yealink"),
        ("Cisco", r"cisco|aironet|catalyst"),
        ("HP", r"\bhp\b|hewlett"),
        ("Logitech", r"logitech"),
        ("Sennheiser", r"sennheiser|epos|sh230|sh30"),
        ("Plantronics", r"plantronics|hw251"),
        ("Samsung", r"samsung|galaxy"),
        ("Lenovo", r"lenovo|thinkpad"),
        ("IBM", r"\bibm\b|netvista"),
        ("Xkim", r"xkim|kxim"),
        ("Genius", r"genius"),
        ("Wacom", r"wacom"),
        ("LG", r"\blg\b"),
        ("Transcend", r"transcend"),
        ("Startech", r"startech|satdock"),
        ("Huawei", r"huawei"),
        ("Alcatel", r"alcatel"),
        ("Motorola", r"motorola|moto e"),
        ("Nokia", r"nokia"),
        ("Panasonic", r"panasonic"),
        ("Epson", r"epson"),
        ("Google", r"google|nexus"),
        ("Compaq", r"compaq"),
        ("Koss", r"koss"),
        ("PreSonus", r"presonus"),
    ]
    for nombre, patron in marcas:
        if re.search(patron, d):
            return nombre
    return "Sin marca/Generico"


def limpiar_valor(v):
    """Normaliza texto: quita espacios y marca vacios/NG como None."""
    if v is None:
        return ""
    v = v.strip()
    if v.lower() in ("", "ng", "n/n", "n/a", "sin código", "sin codigo", "na"):
        return ""
    return v


def parse_fecha(f):
    """Convierte dd/mm/aaaa a objeto date. Devuelve None si falla."""
    f = f.strip()
    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(f, fmt).date()
        except ValueError:
            continue
    return None


def parse_cantidad(c):
    c = (c or "").strip()
    try:
        return int(float(c))
    except (ValueError, TypeError):
        return 1


# -------------------------------------------------------------------------
# 1 + 2 + 3) Leer, consolidar, limpiar y derivar
# -------------------------------------------------------------------------
filas = []
errores_fecha = 0

for ruta in ARCHIVOS:
    with open(ruta, newline="", encoding="utf-8") as fh:
        lector = csv.DictReader(fh)
        for r in lector:
            desc = limpiar_valor(r.get("Descripción del elemento", ""))
            fecha_raw = r.get("Fecha", "")
            fecha = parse_fecha(fecha_raw)
            if fecha is None:
                errores_fecha += 1
            cantidad = parse_cantidad(r.get("Cantidad", "1"))
            serial = limpiar_valor(r.get("Serie No.", ""))
            inventario = limpiar_valor(r.get("No. inventario", ""))
            # El No. inventario a veces trae "IMEI ..." -> lo marcamos
            es_imei = inventario.lower().startswith("imei")

            cat = categorizar(desc)
            mk = marca(desc)

            fila = {
                "Archivo de Origen": limpiar_valor(r.get("Archivo de Origen", "")),
                "Fecha": fecha.isoformat() if fecha else "",
                "Anio": fecha.year if fecha else "",
                "Mes": fecha.month if fecha else "",
                "NombreMes": MESES_ES.get(fecha.month, "") if fecha else "",
                "AnioMes": f"{fecha.year}-{fecha.month:02d}" if fecha else "",
                "Trimestre": f"{fecha.year}-T{((fecha.month - 1) // 3) + 1}" if fecha else "",
                "Consecutivo": limpiar_valor(r.get("Consecutivo", "")),
                "Cantidad": cantidad,
                "Descripcion del elemento": desc,
                "Categoria": cat,
                "Marca": mk,
                "Serie No.": serial,
                "No. inventario": "" if es_imei else inventario,
                "IMEI": inventario if es_imei else "",
                "TieneSerial": "Si" if serial else "No",
                "TieneInventario": "Si" if (inventario and not es_imei) else "No",
                "EsLote": "Si" if cantidad > 1 else "No",
            }
            filas.append(fila)

# -------------------------------------------------------------------------
# 4) Exportar base consolidada para Power BI (UTF-8 con BOM)
# -------------------------------------------------------------------------
COLUMNAS = [
    "Archivo de Origen", "Fecha", "Anio", "Mes", "NombreMes", "AnioMes", "Trimestre",
    "Consecutivo", "Cantidad", "Descripcion del elemento", "Categoria", "Marca",
    "Serie No.", "No. inventario", "IMEI", "TieneSerial", "TieneInventario", "EsLote",
]

salida_csv = os.path.join(OUT_DIR, "bajas_consolidado.csv")
with open(salida_csv, "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=COLUMNAS)
    w.writeheader()
    for f in filas:
        w.writerow(f)

# -------------------------------------------------------------------------
# Metricas / KPIs
# -------------------------------------------------------------------------
total_registros = len(filas)
total_unidades = sum(f["Cantidad"] for f in filas)
consecutivos = set(f["Consecutivo"] for f in filas if f["Consecutivo"])
total_informes = len(consecutivos)

por_anio_reg = Counter(f["Anio"] for f in filas if f["Anio"])
por_anio_uni = defaultdict(int)
for f in filas:
    if f["Anio"]:
        por_anio_uni[f["Anio"]] += f["Cantidad"]

por_cat_uni = defaultdict(int)
por_cat_reg = Counter()
for f in filas:
    por_cat_uni[f["Categoria"]] += f["Cantidad"]
    por_cat_reg[f["Categoria"]] += 1

por_marca_uni = defaultdict(int)
for f in filas:
    por_marca_uni[f["Marca"]] += f["Cantidad"]

por_aniomes_uni = defaultdict(int)
for f in filas:
    if f["AnioMes"]:
        por_aniomes_uni[f["AnioMes"]] += f["Cantidad"]

sin_serial = sum(1 for f in filas if f["TieneSerial"] == "No")
sin_inv = sum(1 for f in filas if f["TieneInventario"] == "No")
lotes = sum(1 for f in filas if f["EsLote"] == "Si")

# Calidad de datos: seriales duplicados (excluyendo vacios)
seriales = [f["Serie No."] for f in filas if f["Serie No."]]
dup_serial = {s: c for s, c in Counter(seriales).items() if c > 1}

# -------------------------------------------------------------------------
# Exportar tablas resumen (para quien quiera usarlas directo)
# -------------------------------------------------------------------------
def exportar_resumen(nombre, cabecera, filas_tabla):
    ruta = os.path.join(OUT_DIR, nombre)
    with open(ruta, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(cabecera)
        for row in filas_tabla:
            w.writerow(row)

exportar_resumen(
    "resumen_por_categoria.csv",
    ["Categoria", "Registros", "Unidades"],
    sorted([[c, por_cat_reg[c], por_cat_uni[c]] for c in por_cat_uni],
           key=lambda x: -x[2]),
)
exportar_resumen(
    "resumen_por_anio.csv",
    ["Anio", "Registros", "Unidades"],
    sorted([[a, por_anio_reg[a], por_anio_uni[a]] for a in por_anio_uni]),
)
exportar_resumen(
    "resumen_por_mes.csv",
    ["AnioMes", "Unidades"],
    sorted([[k, v] for k, v in por_aniomes_uni.items()]),
)
exportar_resumen(
    "resumen_por_marca.csv",
    ["Marca", "Unidades"],
    sorted([[m, v] for m, v in por_marca_uni.items()], key=lambda x: -x[1]),
)

# -------------------------------------------------------------------------
# 5) Reporte EDA en texto
# -------------------------------------------------------------------------
def pct(parte, total):
    return f"{(100.0 * parte / total):.1f}%" if total else "0%"

lineas = []
A = lineas.append
A("=" * 78)
A("  ANALISIS EXPLORATORIO DE DATOS (EDA) - BAJAS DE ACTIVOS DE TI")
A("  Consolidado 2025 + 2026  |  Fuente: Informes Tecnicos DSU-3.1.3-FO15")
A("=" * 78)
A("")
A(">> KPIs PRINCIPALES")
A(f"   - Registros (lineas de detalle) : {total_registros:,}")
A(f"   - Unidades dadas de baja (suma Cantidad) : {total_unidades:,}")
A(f"   - Informes tecnicos (consecutivos unicos) : {total_informes:,}")
A(f"   - Promedio de unidades por informe : {total_unidades/total_informes:.1f}")
A("")
A(">> DISTRIBUCION POR ANIO (unidades)")
for a in sorted(por_anio_uni):
    A(f"   - {a}: {por_anio_uni[a]:,} unidades  ({por_anio_reg[a]:,} registros)")
A("")
A(">> TOP 10 CATEGORIAS DE ACTIVO (por unidades)")
for c, u in sorted(por_cat_uni.items(), key=lambda x: -x[1])[:10]:
    A(f"   - {c:<42} {u:>6,} u.  ({pct(u, total_unidades)})")
A("")
A(">> TOP 10 MARCAS (por unidades)")
for m, u in sorted(por_marca_uni.items(), key=lambda x: -x[1])[:10]:
    A(f"   - {m:<25} {u:>6,} u.  ({pct(u, total_unidades)})")
A("")
A(">> MESES CON MAYOR VOLUMEN DE BAJAS (Top 8)")
for k, v in sorted(por_aniomes_uni.items(), key=lambda x: -x[1])[:8]:
    A(f"   - {k}: {v:,} unidades")
A("")
A(">> CALIDAD DE LOS DATOS")
A(f"   - Registros sin numero de serie     : {sin_serial:,}  ({pct(sin_serial, total_registros)})")
A(f"   - Registros sin numero de inventario: {sin_inv:,}  ({pct(sin_inv, total_registros)})")
A(f"   - Registros tipo LOTE (cantidad > 1): {lotes:,}  ({pct(lotes, total_registros)})")
A(f"   - Fechas no reconocidas             : {errores_fecha:,}")
A(f"   - Seriales duplicados (posible doble baja / re-registro): {len(dup_serial)}")
if dup_serial:
    muestras = list(dup_serial.items())[:8]
    for s, c in muestras:
        A(f"       * {s}  -> aparece {c} veces")
A("")
A(">> ARCHIVOS GENERADOS PARA POWER BI (carpeta data/processed)")
A("   - bajas_consolidado.csv      (TABLA DE HECHOS principal)")
A("   - resumen_por_categoria.csv")
A("   - resumen_por_anio.csv")
A("   - resumen_por_mes.csv")
A("   - resumen_por_marca.csv")
A("")
A("=" * 78)

reporte_txt = "\n".join(lineas)
with open(os.path.join(REPORT_DIR, "analisis_eda.txt"), "w", encoding="utf-8") as fh:
    fh.write(reporte_txt)

print(reporte_txt)
print(f"\n[OK] Base consolidada: {salida_csv}  ({total_registros} filas)")
