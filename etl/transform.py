#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRANSFORM (Sección 2 · Transform).
Limpia y normaliza los datos crudos, deriva columnas de análisis
(Categoría, Marca, dimensiones de tiempo, indicadores de calidad) y
calcula los KPIs definidos en el Entregable 3.
"""
import re
from datetime import datetime
from collections import Counter, defaultdict

from config import VALORES_NO_INFORMATIVOS, MESES_ES, FACT_COLUMNS


# ---------------------------------------------------------------------------
# Reglas de clasificación de negocio
# ---------------------------------------------------------------------------
def categorizar(desc):
    d = desc.lower()
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
    d = desc.lower()
    reglas = [
        ("Dell", r"\bdell\b|optiplex|latitude|vostro|inspiron|precision|\bxps\b"),
        ("Apple", r"apple|imac|macbook|mac pro|macpro|ipad|magsafe|thunderbolt|magic"),
        ("Avaya", r"avaya|vantage"), ("Yealink", r"yealink"),
        ("Cisco", r"cisco|aironet|catalyst"), ("HP", r"\bhp\b|hewlett|z820"),
        ("Logitech", r"logitech"), ("Sennheiser", r"sennheiser|epos|sh230|sh30"),
        ("Plantronics", r"plantronics|hw251"), ("Samsung", r"samsung|galaxy"),
        ("Lenovo", r"lenovo|thinkpad"), ("IBM", r"\bibm\b|netvista"),
        ("Xkim", r"xkim|kxim"), ("Genius", r"genius"), ("Wacom", r"wacom"),
        ("LG", r"\blg\b"), ("Transcend", r"transcend"), ("Startech", r"startech|satdock"),
        ("Huawei", r"huawei"), ("Alcatel", r"alcatel"), ("Motorola", r"motorola|moto e"),
        ("Nokia", r"nokia"), ("Panasonic", r"panasonic"), ("Epson", r"epson"),
        ("Google", r"google|nexus"), ("Compaq", r"compaq"), ("Koss", r"koss"),
        ("PreSonus", r"presonus"),
    ]
    for nombre, patron in reglas:
        if re.search(patron, d):
            return nombre
    return "Sin marca/Generico"


# ---------------------------------------------------------------------------
# Limpieza de valores
# ---------------------------------------------------------------------------
def limpiar(v):
    if v is None:
        return ""
    v = str(v).strip()
    return "" if v.lower() in VALORES_NO_INFORMATIVOS else v


def parse_fecha(f):
    f = (f or "").strip()
    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(f, fmt).date()
        except ValueError:
            continue
    return None


def parse_cantidad(c):
    try:
        return int(float(str(c).strip()))
    except (ValueError, TypeError):
        return 1


# ---------------------------------------------------------------------------
# Transformación principal
# ---------------------------------------------------------------------------
def transformar(filas, logger):
    """Devuelve (filas_limpias, metricas_transform)."""
    logger.info("== FASE TRANSFORM ==")
    out = []
    fechas_invalidas = 0
    for r in filas:
        desc = limpiar(r.get("Descripción del elemento", ""))
        fecha = parse_fecha(r.get("Fecha", ""))
        if fecha is None:
            fechas_invalidas += 1
        cantidad = parse_cantidad(r.get("Cantidad", "1"))
        serial = limpiar(r.get("Serie No.", ""))
        inv = limpiar(r.get("No. inventario", ""))
        es_imei = inv.lower().startswith("imei")

        out.append({
            "Archivo de Origen": limpiar(r.get("Archivo de Origen", "")),
            "Fecha": fecha.isoformat() if fecha else "",
            "Anio": fecha.year if fecha else "",
            "Mes": fecha.month if fecha else "",
            "NombreMes": MESES_ES.get(fecha.month, "") if fecha else "",
            "AnioMes": f"{fecha.year}-{fecha.month:02d}" if fecha else "",
            "Trimestre": f"{fecha.year}-T{((fecha.month - 1)//3)+1}" if fecha else "",
            "Consecutivo": limpiar(r.get("Consecutivo", "")),
            "Cantidad": cantidad,
            "Descripcion del elemento": desc,
            "Categoria": categorizar(desc),
            "Marca": marca(desc),
            "Serie No.": serial,
            "No. inventario": "" if es_imei else inv,
            "IMEI": inv if es_imei else "",
            "TieneSerial": "Si" if serial else "No",
            "TieneInventario": "Si" if (inv and not es_imei) else "No",
            "EsLote": "Si" if cantidad > 1 else "No",
        })

    logger.info(f"Transformadas {len(out)} filas | fechas inválidas: {fechas_invalidas}")
    metricas = {"fechas_invalidas": fechas_invalidas, "total": len(out)}
    return out, metricas


# ---------------------------------------------------------------------------
# Cálculo de KPIs (Entregable 3) sobre los datos ya transformados
# ---------------------------------------------------------------------------
def calcular_kpis(filas, logger):
    logger.info("== CÁLCULO DE KPIs ==")
    total_u = sum(f["Cantidad"] for f in filas)
    consecutivos = {f["Consecutivo"] for f in filas if f["Consecutivo"]}
    por_cat, por_marca, por_anio, por_mes = (defaultdict(int) for _ in range(4))
    sin_serial = sin_inv = 0
    for f in filas:
        por_cat[f["Categoria"]] += f["Cantidad"]
        por_marca[f["Marca"]] += f["Cantidad"]
        if f["Anio"]:
            por_anio[f["Anio"]] += f["Cantidad"]
        if f["AnioMes"]:
            por_mes[f["AnioMes"]] += f["Cantidad"]
        sin_serial += 1 if f["TieneSerial"] == "No" else 0
        sin_inv += 1 if f["TieneInventario"] == "No" else 0

    n = len(filas)
    cat_top = max(por_cat.items(), key=lambda x: x[1]) if por_cat else ("", 0)
    marca_top = max(por_marca.items(), key=lambda x: x[1]) if por_marca else ("", 0)
    mes_pico = max(por_mes.items(), key=lambda x: x[1]) if por_mes else ("", 0)
    u25 = por_anio.get(2025, 0)
    u26 = por_anio.get(2026, 0)
    seriales = [f["Serie No."] for f in filas if f["Serie No."]]
    dup_serial = sum(1 for _, c in Counter(seriales).items() if c > 1)

    kpis = {
        "KPI-01_total_unidades": total_u,
        "KPI-02_total_informes": len(consecutivos),
        "KPI-03_unidades_por_informe": round(total_u / len(consecutivos), 2) if consecutivos else 0,
        "KPI-04_categorias_distintas": len(por_cat),
        "KPI-05_pct_categoria_top": round(100 * cat_top[1] / total_u, 1) if total_u else 0,
        "KPI-05_categoria_top": cat_top[0],
        "KPI-06_marcas_distintas": len(por_marca),
        "KPI-07_pct_marca_top": round(100 * marca_top[1] / total_u, 1) if total_u else 0,
        "KPI-07_marca_top": marca_top[0],
        "KPI-08_unidades_por_mes": dict(sorted(por_mes.items())),
        "KPI-09_variacion_anual_pct": round(100 * (u26 - u25) / u25, 1) if u25 else 0,
        "KPI-10_mes_pico": mes_pico[0],
        "KPI-11_unidades_mes_pico": mes_pico[1],
        "KPI-12_pct_sin_serie": round(100 * sin_serial / n, 1) if n else 0,
        "KPI-13_pct_sin_inventario": round(100 * sin_inv / n, 1) if n else 0,
        "KPI-14_seriales_duplicados": dup_serial,
    }
    logger.info(f"KPIs calculados: {total_u} unidades, {len(consecutivos)} informes, "
                f"score trazabilidad -> sin serie {kpis['KPI-12_pct_sin_serie']}%, "
                f"sin inventario {kpis['KPI-13_pct_sin_inventario']}%")
    return kpis
