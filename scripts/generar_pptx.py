#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la presentación ejecutiva (.pptx) del Entregable 7 — 13 slides.
Construye el OOXML de PowerPoint con la librería estándar (zipfile + XML)."""
import os, zipfile
from xml.sax.saxutils import escape

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "entregables", "Entregable7-Presentacion-Ejecutiva.pptx")

# Dimensiones de diapositiva 16:9 en EMU
CX, CY = 12192000, 6858000

def _tx(text, x, y, w, h, size, bold=False, color="1B2330", align="l", anchor="t"):
    """Crea un cuadro de texto. Soporta varias líneas separadas por '\n'."""
    paras = ""
    for ln in text.split("\n"):
        bullet = ln.startswith("• ")
        content = ln[2:] if bullet else ln
        buNone = '' if bullet else '<a:buNone/>'
        ind = '<a:pPr marL="285750" indent="-285750" algn="%s"/>' % align if bullet else '<a:pPr algn="%s">%s</a:pPr>' % (align, buNone)
        run = (f'<a:r><a:rPr lang="es-CO" sz="{size}" b="{1 if bold else 0}" dirty="0">'
               f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
               f'<a:latin typeface="Segoe UI"/></a:rPr><a:t>{escape(content)}</a:t></a:r>')
        paras += f'<a:p>{ind}{run}</a:p>'
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="0" name="t"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            f'<p:txBody><a:bodyPr anchor="{anchor}" wrap="square"/><a:lstStyle/>{paras}</p:txBody></p:sp>')

def _rect(x, y, w, h, color):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="0" name="r"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>')

def slide(shapes):
    sp = "".join(shapes)
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            f'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            f'<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            f'<p:grpSpPr/>{sp}</p:spTree></p:cSld><p:clrMapOvr><a:overrideClrMapping '
            f'bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" '
            f'accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
            f'</p:clrMapOvr></p:sld>')

def titulo_slide(titulo, subtitulo):
    return slide([
        _rect(0, 0, CX, 180000, "E2001A"),
        _rect(0, CY-120000, CX, 120000, "E2001A"),
        _tx(titulo, 900000, 2200000, CX-1800000, 1400000, 4000, True, "E2001A", "ctr"),
        _tx(subtitulo, 900000, 3700000, CX-1800000, 900000, 2000, False, "6B7688", "ctr"),
    ])

def contenido_slide(titulo, lineas, kpi=None):
    shapes = [
        _rect(0, 0, CX, 120000, "E2001A"),
        _tx(titulo, 600000, 450000, CX-1200000, 800000, 2800, True, "1B2330"),
        _tx("\n".join(lineas), 700000, 1500000, CX-1400000, 4600000, 1800, False, "1B2330"),
    ]
    if kpi:
        shapes.append(_rect(CX-3400000, 1500000, 2800000, 1500000, "F4F6FB"))
        shapes.append(_tx(kpi[0], CX-3300000, 1700000, 2600000, 700000, 4400, True, "E2001A", "ctr"))
        shapes.append(_tx(kpi[1], CX-3300000, 2550000, 2600000, 400000, 1400, False, "6B7688", "ctr"))
    return slide(shapes)

# --------- 13 diapositivas ---------
slides = [
    titulo_slide("Dashboard de Bajas de Activos de TI",
                 "Universidad Autónoma de Occidente · Presentación ejecutiva · 2025–2026"),
    contenido_slide("1. Contexto", [
        "• Área de gestión de activos de Tecnología (TI) de la UAO.",
        "• Las bajas de equipos se documentan en informes técnicos (formato DSU-3.1.3-FO15).",
        "• Reto: la información estaba dispersa en múltiples PDF, sin vista consolidada.",
        "• Solución: un dashboard interactivo alimentado por un pipeline de datos automatizado."]),
    contenido_slide("2. Objetivo del proyecto", [
        "• Centralizar y analizar las bajas de activos tecnológicos.",
        "• Responder 7 preguntas de negocio clave de forma visual e interactiva.",
        "• Aportar indicadores de calidad para fortalecer la trazabilidad patrimonial.",
        "• Entregar una herramienta que el equipo de TI pueda usar y mantener."]),
    contenido_slide("3. Los datos en cifras", [
        "• 924 registros de baja en 104 informes técnicos (DITI).",
        "• 1.322 unidades de activos retiradas de servicio.",
        "• Período: enero 2025 – octubre 2026.",
        "• 18 variables por registro, incluyendo categoría y marca derivadas."],
        kpi=("1.322", "unidades dadas de baja")),
    contenido_slide("4. Qué se da de baja (categorías)", [
        "• Mouse: 20,7% del total (274 u.) — la categoría líder.",
        "• Telefonía IP: 18,8% (249 u.).",
        "• Teclados: 16,9% (223 u.).",
        "• Computadores: 11,1% (147 u.).",
        "• Los periféricos concentran más de la mitad de las bajas."],
        kpi=("20,7%", "categoría top: Mouse")),
    contenido_slide("5. Marcas y evolución anual", [
        "• Dell concentra el 33,7% de las unidades; Avaya el 11,9%.",
        "• 2025: 651 unidades · 2026: 671 unidades.",
        "• Variación interanual: +3,1% (volumen estable).",
        "• Picos de baja: julio 2025 (161 u.) y abril 2026 (135 u.)."],
        kpi=("+3,1%", "variación 2026 vs 2025")),
    contenido_slide("6. Calidad de los datos", [
        "• Score general de calidad: 87,2 / 100 (bueno).",
        "• Fortalezas: 0 registros duplicados, 100% de fechas válidas.",
        "• Debilidad: 40,4% sin número de inventario y 22,3% sin serie.",
        "• 5 seriales repetidos a revisar (posibles dobles bajas)."],
        kpi=("87,2", "score de calidad / 100")),
    contenido_slide("7. Arquitectura de la solución", [
        "• Fuentes CSV → Pipeline ETL → Tabla de hechos + KPIs → Dashboard.",
        "• ETL modular en Python: Extract, Transform, Validate, Load.",
        "• Validación de integridad con 7 checks antes de cargar.",
        "• Salida lista para el dashboard web y para Power BI."]),
    contenido_slide("8. El dashboard interactivo", [
        "• 3 páginas: Visión general, Detalle operacional y Análisis comparativo.",
        "• Filtros globales: rango de fechas, año, categoría, marca y búsqueda.",
        "• Drilldowns: del resumen al detalle con un clic.",
        "• Tema claro/oscuro, exportación a CSV y diseño profesional UAO."]),
    contenido_slide("9. Preguntas de negocio respondidas", [
        "• ¿Cuánto y qué se da de baja? → KPIs y gráficos por categoría.",
        "• ¿Qué marcas y cómo evoluciona? → treemap y tendencia mensual.",
        "• ¿Dónde están los picos? → serie temporal y estacionalidad.",
        "• ¿Qué tan trazable es? → indicadores de calidad en la página 3."]),
    contenido_slide("10. Hallazgos para la gestión", [
        "• Reforzar el registro de serie e inventario en el origen (trazabilidad).",
        "• Planear reposiciones anticipando los picos estacionales detectados.",
        "• Revisar los seriales duplicados para depurar el inventario.",
        "• Oportunidad: incorporar el motivo de baja (Dañado/Obsoleto/Bueno)."]),
    contenido_slide("11. Roadmap de mejoras", [
        "• Corto plazo: subir trazabilidad > 90%; añadir campo Estado.",
        "• Mediano plazo: automatizar el ETL (scheduler) y publicar en Power BI Service.",
        "• Largo plazo: enlazar con el inventario general y el valor contable.",
        "• Futuro: modelo predictivo de reposición basado en estacionalidad."]),
    contenido_slide("12. Conclusión", [
        "• Proyecto completo: de los datos crudos a un dashboard funcionando.",
        "• Pipeline reproducible, documentado y fácil de mantener.",
        "• Entrega valor inmediato al administrador de activos de TI.",
        "• Base sólida para evolucionar hacia analítica predictiva.",
        "",
        "Gracias. · Universidad Autónoma de Occidente"]),
]

# --------- Empaquetado OOXML de PowerPoint ---------
n = len(slides)
sldIds = "".join(f'<p:sldId id="{256+i}" r:id="rId{i+1}"/>' for i in range(n))
presentation = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    f'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
    f'<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId{n+1}"/></p:sldMasterIdLst>'
    f'<p:sldIdLst>{sldIds}</p:sldIdLst>'
    f'<p:sldSz cx="{CX}" cy="{CY}"/><p:notesSz cx="{CY}" cy="{CX}"/></p:presentation>')

pres_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
for i in range(n):
    pres_rels.append(f'<Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i+1}.xml"/>')
pres_rels.append(f'<Relationship Id="rId{n+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>')
pres_rels.append(f'<Relationship Id="rId{n+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>')
pres_rels.append('</Relationships>')
pres_rels = "".join(pres_rels)

theme = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="UAO">'
    '<a:themeElements><a:clrScheme name="UAO"><a:dk1><a:srgbClr val="1B2330"/></a:dk1>'
    '<a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="6B7688"/></a:dk2>'
    '<a:lt2><a:srgbClr val="F4F6FB"/></a:lt2><a:accent1><a:srgbClr val="E2001A"/></a:accent1>'
    '<a:accent2><a:srgbClr val="2563EB"/></a:accent2><a:accent3><a:srgbClr val="F59E0B"/></a:accent3>'
    '<a:accent4><a:srgbClr val="10B981"/></a:accent4><a:accent5><a:srgbClr val="8B5CF6"/></a:accent5>'
    '<a:accent6><a:srgbClr val="06B6D4"/></a:accent6><a:hlink><a:srgbClr val="2563EB"/></a:hlink>'
    '<a:folHlink><a:srgbClr val="8B5CF6"/></a:folHlink></a:clrScheme>'
    '<a:fontScheme name="UAO"><a:majorFont><a:latin typeface="Segoe UI"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
    '<a:minorFont><a:latin typeface="Segoe UI"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>'
    '<a:fmtScheme name="UAO"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
    '<a:lnStyleLst><a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
    '<a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
    '<a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
    '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle>'
    '<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
    '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>'
    '</a:fmtScheme></a:themeElements></a:theme>')

sm = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
    '<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'
    '<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>'
    '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" '
    'accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
    '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>')
sm_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>')
layout = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">'
    '<p:cSld name="En blanco"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
    '<p:grpSpPr/></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
layout_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>')

def slide_rels():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>')

ctypes = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
    '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
    '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
    '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>']
for i in range(n):
    ctypes.append(f'<Override PartName="/ppt/slides/slide{i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
ctypes.append('</Types>')
ctypes = "".join(ctypes)

root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>')
core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Entregable 7 - Presentacion Ejecutiva</dc:title>'
    '<dc:creator>Proyecto Seminario IA</dc:creator></cp:coreProperties>')

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", ctypes)
    z.writestr("_rels/.rels", root_rels)
    z.writestr("docProps/core.xml", core)
    z.writestr("ppt/presentation.xml", presentation)
    z.writestr("ppt/_rels/presentation.xml.rels", pres_rels)
    z.writestr("ppt/theme/theme1.xml", theme)
    z.writestr("ppt/slideMasters/slideMaster1.xml", sm)
    z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", sm_rels)
    z.writestr("ppt/slideLayouts/slideLayout1.xml", layout)
    z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", layout_rels)
    for i, s in enumerate(slides):
        z.writestr(f"ppt/slides/slide{i+1}.xml", s)
        z.writestr(f"ppt/slides/_rels/slide{i+1}.xml.rels", slide_rels())

print(f"[OK] Presentación generada: {OUT} ({n} slides, {os.path.getsize(OUT):,} bytes)")
