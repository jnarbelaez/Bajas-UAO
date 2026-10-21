#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el ENTREGABLE 1 · Especificación de Requisitos como documento Word (.docx)
sin dependencias externas (construye el OOXML con zipfile + XML).

Salida: entregables/Entregable1-Especificacion-de-Requisitos.docx
"""
import os
import zipfile
from xml.sax.saxutils import escape

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "entregables")
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "Entregable1-Especificacion-de-Requisitos.docx")

# -------------------------------------------------------------------------
# Helpers para construir párrafos / encabezados / tablas en WordprocessingML
# -------------------------------------------------------------------------
NSMARKS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
           'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')

def _runs(text, bold=False, italic=False, size=None, color=None):
    rpr = "<w:rPr>"
    if bold: rpr += "<w:b/>"
    if italic: rpr += "<w:i/>"
    if color: rpr += f'<w:color w:val="{color}"/>'
    if size: rpr += f'<w:sz w:val="{size*2}"/><w:szCs w:val="{size*2}"/>'
    rpr += "</w:rPr>"
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'

def para(text="", style=None, bold=False, italic=False, size=None, color=None,
         align=None, space_after=120):
    ppr = "<w:pPr>"
    if style: ppr += f'<w:pStyle w:val="{style}"/>'
    if align: ppr += f'<w:jc w:val="{align}"/>'
    ppr += f'<w:spacing w:after="{space_after}"/>'
    ppr += "</w:pPr>"
    run = _runs(text, bold, italic, size, color) if text else ""
    return f"<w:p>{ppr}{run}</w:p>"

def heading(text, level=1):
    style = {1: "Heading1", 2: "Heading2", 3: "Heading3"}[level]
    return para(text, style=style, space_after=160)

def bullet(text, bold_prefix=None):
    ppr = ('<w:pPr><w:pStyle w:val="ListParagraph"/>'
           '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
           '<w:spacing w:after="60"/></w:pPr>')
    runs = ""
    if bold_prefix:
        runs += _runs(bold_prefix, bold=True)
    runs += _runs(text)
    return f"<w:p>{ppr}{runs}</w:p>"

def table(rows, header=True, widths=None):
    """rows: lista de listas de strings. Primera fila = encabezado si header=True."""
    ncols = len(rows[0])
    if not widths:
        widths = [int(9000 / ncols)] * ncols
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    out = ['<w:tbl>',
           '<w:tblPr>'
           '<w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="0" w:type="auto"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:color="BFBFBF"/>'
           '<w:left w:val="single" w:sz="4" w:color="BFBFBF"/>'
           '<w:bottom w:val="single" w:sz="4" w:color="BFBFBF"/>'
           '<w:right w:val="single" w:sz="4" w:color="BFBFBF"/>'
           '<w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/>'
           '<w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/>'
           '</w:tblBorders></w:tblPr>',
           f'<w:tblGrid>{grid}</w:tblGrid>']
    for i, row in enumerate(rows):
        out.append("<w:tr>")
        for j, cell in enumerate(row):
            is_head = header and i == 0
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="E2001A"/>' if is_head else ""
            tcpr = f'<w:tcPr><w:tcW w:w="{widths[j]}" w:type="dxa"/>{shade}</w:tcPr>'
            runs = _runs(cell, bold=is_head, color="FFFFFF" if is_head else None)
            out.append(f'<w:tc>{tcpr}<w:p><w:pPr><w:spacing w:after="20"/></w:pPr>{runs}</w:p></w:tc>')
        out.append("</w:tr>")
    out.append("</w:tbl>")
    out.append(para("", space_after=120))  # espacio tras tabla
    return "".join(out)

# -------------------------------------------------------------------------
# CONTENIDO DEL ENTREGABLE 1
# -------------------------------------------------------------------------
body = []
A = body.append

# ---- Portada ----
A(para("UNIVERSIDAD AUTÓNOMA DE OCCIDENTE", align="center", bold=True, size=14, color="E2001A", space_after=40))
A(para("Seminario de Inteligencia Artificial", align="center", italic=True, size=12, space_after=400))
A(para("ENTREGABLE 1", align="center", bold=True, size=26, space_after=80))
A(para("Especificación de Requisitos", align="center", bold=True, size=18, color="E2001A", space_after=120))
A(para("Proyecto: Desarrollo de Dashboard Profesional", align="center", size=13, space_after=40))
A(para("Bajas de Activos del Área de Tecnología (TI)", align="center", italic=True, size=12, space_after=600))
A(para("Complejidad: Básica", align="center", size=11, color="6B7688", space_after=40))
A(para("Fuente de datos: Informes Técnicos de Baja o Devolución de Activos (DSU-3.1.3-FO15)",
       align="center", size=10, color="6B7688", space_after=40))
A(para("Período analizado: 2025–2026", align="center", size=10, color="6B7688", space_after=200))
A('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

# ---- Sección 1 ----
A(heading("1. Contexto empresarial", 1))
A(para("La organización objeto de este proyecto es la Universidad Autónoma de Occidente (UAO), "
       "institución de educación superior ubicada en Cali, Colombia (Campus Valle del Lili), vigilada "
       "por el Ministerio de Educación Nacional. Como toda institución educativa de gran escala, la UAO "
       "administra un parque tecnológico amplio y heterogéneo que da soporte a labores académicas, "
       "administrativas y de investigación."))
A(para("El área responsable de este dashboard es la gestión de activos del Departamento de Tecnologías "
       "de la Información (TI), adscrita a la Vicerrectoría Administrativa y Financiera "
       "(Departamento de Compras y Suministros). Funcionalmente corresponde a un área de Operaciones / "
       "TI, encargada del ciclo de vida de los equipos: adquisición, asignación, mantenimiento y, en "
       "particular, la BAJA o devolución de activos que llegan al final de su vida útil."))
A(para("El dominio de datos de este proyecto son los registros de bajas de activos tecnológicos: "
       "teléfonos IP (Avaya, Yealink), computadores de escritorio y todo-en-uno (Dell OptiPlex, iMac), "
       "portátiles (Latitude, MacBook), periféricos (teclados, mouse, diademas), monitores, tabletas, "
       "equipos de red (Cisco) y accesorios. Cada baja se documenta en un formato institucional "
       "estandarizado (DSU-3.1.3-FO15 — \u201cInforme Técnico para Baja o Devolución de Activos\u201d)."))

# ---- Sección 2 ----
A(heading("2. Problemas actuales", 1))
A(para("La gestión de bajas se registra hoy en documentos individuales (informes técnicos en PDF), lo "
       "que genera varias dificultades que justifican la construcción del dashboard:"))
A(bullet("los datos están dispersos en múltiples archivos PDF por fecha, sin una vista consolidada "
         "que permita analizar tendencias.", "Información fragmentada: "))
A(bullet("responder preguntas simples (cuántos equipos se dieron de baja, de qué tipo, en qué mes) "
         "exige revisar manualmente decenas de documentos.", "Análisis manual y lento: "))
A(bullet("se detectó que el 22% de los registros no tiene número de serie y el 40% carece de número "
         "de inventario, lo que dificulta la auditoría y el control patrimonial.", "Baja trazabilidad: "))
A(bullet("sin consolidación es difícil comparar el comportamiento de un año frente a otro o anticipar "
         "picos de reposición de equipos.", "Sin visión comparativa ni histórica: "))
A(bullet("existen seriales que aparecen repetidos, lo que puede indicar dobles registros o errores que "
         "pasan desapercibidos sin una herramienta de control.", "Riesgo de duplicidad: "))
A(para("El dashboard resuelve estos problemas al centralizar la información, automatizar el análisis y "
       "aportar indicadores de calidad de datos que apoyan la toma de decisiones y la auditoría."))

# ---- Sección 3 ----
A(heading("3. Usuarios finales", 1))
A(para("El dashboard está dirigido principalmente al empleado responsable de la administración de los "
       "activos del área de Tecnología, pero sirve a varios perfiles:"))
A(table([
    ["Usuario", "Rol / interés en el dashboard"],
    ["Administrador de activos de TI", "Usuario principal. Controla el inventario de bajas, verifica trazabilidad (serie/inventario) y gestiona la disposición de equipos."],
    ["Jefe del Departamento de TI", "Visión ejecutiva: volúmenes, tendencias y comparación año a año para planear reposiciones y presupuesto."],
    ["Departamento de Compras y Suministros", "Apoya la planeación de adquisiciones con base en los equipos que salen de servicio."],
    ["Auditoría / Control Interno", "Verifica el cumplimiento documental y detecta inconsistencias (registros sin serie/inventario, duplicados)."],
], widths=[2600, 6400]))

# ---- Sección 4 ----
A(heading("4. Preguntas de negocio específicas", 1))
A(para("El dashboard debe responder, de forma interactiva, las siguientes preguntas de negocio:"))
A(bullet("¿Cuántas unidades de activos se dieron de baja en total y cuántos informes técnicos (DITI) se tramitaron en el período 2025–2026?",
         "P1. "))
A(bullet("¿Cómo se distribuyen las bajas por categoría de activo (computadores, teléfonos, teclados, mouse, diademas, monitores, etc.)?",
         "P2. "))
A(bullet("¿Qué marcas o fabricantes concentran la mayor cantidad de bajas (Dell, Avaya, Apple, Cisco, etc.)?",
         "P3. "))
A(bullet("¿Cómo evoluciona el volumen de bajas mes a mes y cómo se compara el año 2026 frente al 2025 (variación %)?",
         "P4. "))
A(bullet("¿En qué meses se concentran los picos de baja de activos y qué categorías los explican?",
         "P5. "))
A(bullet("¿Qué porcentaje de los registros carece de número de serie o de número de inventario (indicador de calidad y trazabilidad)?",
         "P6. "))
A(bullet("¿Existen seriales duplicados que sugieran dobles registros o errores que requieran revisión?",
         "P7. "))

# ---- Sección 5 ----
A(heading("5. Fuentes de datos", 1))
A(para("Los datos tienen su origen en el formato institucional DSU-3.1.3-FO15 "
       "(\u201cInforme Técnico para Baja o Devolución de Activos\u201d), diligenciado por el área de TI "
       "para cada trámite de baja. Estos informes se consolidaron en archivos CSV anuales "
       "(Bajas 2025 y bajas 2026), que constituyen la fuente directa del dashboard."))
A(para("Correspondencia entre el formato de origen y los campos de datos:", bold=True))
A(table([
    ["Campo del Informe Técnico", "Columna de datos", "Descripción"],
    ["Fecha", "Fecha", "Fecha del trámite de baja (dd/mm/aaaa)"],
    ["Consecutivo", "Consecutivo", "Código del documento (ej. DITI-4.6-64)"],
    ["Cantidad", "Cantidad", "Número de unidades dadas de baja en la línea"],
    ["Descripción del Elemento", "Descripción del elemento", "Detalle del activo"],
    ["Serie No.", "Serie No.", "Número de serie del equipo"],
    ["No. Inventario", "No. inventario", "Código de inventario institucional"],
    ["(archivo PDF de origen)", "Archivo de Origen", "Documento fuente (Bajas 2025 / 2026)"],
], widths=[3000, 2600, 3400]))
A(para("Sobre esta base se construyó una tabla de hechos consolidada "
       "(bajas_consolidado.csv) enriquecida con columnas derivadas de análisis: Año, Mes, Trimestre, "
       "Categoría de activo, Marca e indicadores de calidad (TieneSerial, TieneInventario, EsLote). "
       "Este archivo es el que alimenta el dashboard en Power BI."))

# ---- Sección 6 ----
A(heading("6. Frecuencia de actualización", 1))
A(para("Dado que las bajas de activos no ocurren en tiempo real sino mediante trámites periódicos, se "
       "propone la siguiente frecuencia de actualización:"))
A(bullet("se recomienda actualizar la base consolidada al cierre de cada mes, incorporando los nuevos "
         "informes técnicos tramitados.", "Actualización mensual: "))
A(bullet("el proceso de transformación (script procesar_bajas.py) regenera la tabla de hechos a partir "
         "de los CSV; en Power BI basta con pulsar \u201cActualizar\u201d.", "Mecanismo: "))
A(bullet("los datos actuales abarcan de enero de 2025 a octubre de 2026 y se amplían a medida que se "
         "generan nuevos informes.", "Cobertura: "))
A(para("Para un entorno productivo, el archivo puede publicarse en Power BI Service y programarse una "
       "actualización automática, manteniendo el histórico para el análisis de tendencias."))

# ---- Sección 7 ----
A(heading("7. Restricciones: seguridad y privacidad", 1))
A(para("El manejo de la información está sujeto a las siguientes restricciones:"))
A(bullet("aunque se trata de activos institucionales, algunos registros incluyen datos sensibles como "
         "IMEI de celulares corporativos y líneas telefónicas asignadas a personas; estos deben "
         "tratarse conforme a la Ley 1581 de 2012 (protección de datos personales en Colombia).",
         "Privacidad: "))
A(bullet("el acceso al dashboard debe restringirse al personal autorizado del área de TI, compras y "
         "auditoría; se recomienda control por roles si se publica en Power BI Service.",
         "Seguridad / acceso: "))
A(bullet("el dashboard es de uso interno y administrativo; no debe exponerse públicamente ni "
         "compartirse con terceros sin autorización.", "Confidencialidad: "))
A(bullet("los seriales e inventarios son datos de control patrimonial; su alteración o divulgación "
         "indebida puede afectar procesos de auditoría.", "Integridad: "))
A(bullet("se recomienda conservar el histórico de bajas por el período que establezcan las políticas "
         "institucionales de retención documental, dado su valor para auditoría.",
         "Retención: "))
A(para(""))
A(para("Fin del Entregable 1.", italic=True, color="6B7688", align="center", space_after=0))

document_xml = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<w:document {NSMARKS}><w:body>'
                + "".join(body)
                + '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                  '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
                  'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
                  '</w:body></w:document>')

# -------------------------------------------------------------------------
# Archivos auxiliares del paquete .docx
# -------------------------------------------------------------------------
content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''

rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''

doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''

styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="es-CO"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:line="276" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="E2001A"/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="2563EB"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="160" w:after="60"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720"/></w:pPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:color="BFBFBF"/><w:left w:val="single" w:sz="4" w:color="BFBFBF"/><w:bottom w:val="single" w:sz="4" w:color="BFBFBF"/><w:right w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/></w:tblBorders></w:tblPr></w:style>
</w:styles>'''

numbering = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#8226;"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr><w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>'''

core = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>Entregable 1 - Especificacion de Requisitos</dc:title>
<dc:subject>Dashboard Bajas de Activos TI - UAO</dc:subject>
<dc:creator>Proyecto Seminario IA</dc:creator>
<cp:keywords>dashboard, bajas, activos, TI, Power BI</cp:keywords>
</cp:coreProperties>'''

app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<Application>Python docx generator</Application><Company>Universidad Autonoma de Occidente</Company>
</Properties>'''

# -------------------------------------------------------------------------
# Empaquetar en .docx (ZIP)
# -------------------------------------------------------------------------
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    z.writestr("word/styles.xml", styles)
    z.writestr("word/numbering.xml", numbering)
    z.writestr("docProps/core.xml", core)
    z.writestr("docProps/app.xml", app)

print(f"[OK] Documento generado: {OUT}")
print(f"     Tamaño: {os.path.getsize(OUT):,} bytes")
