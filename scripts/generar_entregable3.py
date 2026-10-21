#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el ENTREGABLE 3 · Identificación de KPIs e Indicadores como documento Word (.docx)
sin dependencias externas. Reutiliza los helpers de construcción OOXML.

Salida: entregables/Entregable3-KPIs-e-Indicadores.docx
"""
import os
import zipfile
from xml.sax.saxutils import escape

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "entregables")
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "Entregable3-KPIs-e-Indicadores.docx")

NSMARKS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
           'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')

def _runs(text, bold=False, italic=False, size=None, color=None, mono=False):
    rpr = "<w:rPr>"
    if mono: rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
    if bold: rpr += "<w:b/>"
    if italic: rpr += "<w:i/>"
    if color: rpr += f'<w:color w:val="{color}"/>'
    if size: rpr += f'<w:sz w:val="{size*2}"/><w:szCs w:val="{size*2}"/>'
    rpr += "</w:rPr>"
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'

def para(text="", style=None, bold=False, italic=False, size=None, color=None,
         align=None, space_after=120, mono=False, shade=None):
    ppr = "<w:pPr>"
    if style: ppr += f'<w:pStyle w:val="{style}"/>'
    if align: ppr += f'<w:jc w:val="{align}"/>'
    if shade: ppr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
    ppr += f'<w:spacing w:after="{space_after}"/>'
    ppr += "</w:pPr>"
    run = _runs(text, bold, italic, size, color, mono) if text else ""
    return f"<w:p>{ppr}{run}</w:p>"

def code_block(lines, lang=""):
    out = []
    if lang:
        out.append(para(lang, mono=True, size=8, color="6B7688", space_after=0))
    for ln in lines:
        out.append(para(ln, mono=True, size=9, shade="F4F6FB", space_after=0))
    out.append(para("", space_after=100))
    return "".join(out)

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

def table(rows, header=True, widths=None, fontsize=9):
    ncols = len(rows[0])
    if not widths:
        widths = [int(9200 / ncols)] * ncols
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    out = ['<w:tbl>',
           '<w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:color="BFBFBF"/><w:left w:val="single" w:sz="4" w:color="BFBFBF"/>'
           '<w:bottom w:val="single" w:sz="4" w:color="BFBFBF"/><w:right w:val="single" w:sz="4" w:color="BFBFBF"/>'
           '<w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/>'
           '</w:tblBorders></w:tblPr>',
           f'<w:tblGrid>{grid}</w:tblGrid>']
    for i, row in enumerate(rows):
        out.append("<w:tr>")
        for j, cell in enumerate(row):
            is_head = header and i == 0
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="E2001A"/>' if is_head else ""
            tcpr = f'<w:tcPr><w:tcW w:w="{widths[j]}" w:type="dxa"/>{shd}</w:tcPr>'
            runs = _runs(cell, bold=is_head, color="FFFFFF" if is_head else None, size=fontsize)
            out.append(f'<w:tc>{tcpr}<w:p><w:pPr><w:spacing w:after="20"/></w:pPr>{runs}</w:p></w:tc>')
        out.append("</w:tr>")
    out.append("</w:tbl>")
    out.append(para("", space_after=120))
    return "".join(out)

def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

# =========================================================================
# CONTENIDO
# =========================================================================
body = []
A = body.append

# Portada
A(para("UNIVERSIDAD AUTÓNOMA DE OCCIDENTE", align="center", bold=True, size=14, color="E2001A", space_after=40))
A(para("Seminario de Inteligencia Artificial", align="center", italic=True, size=12, space_after=400))
A(para("ENTREGABLE 3", align="center", bold=True, size=26, space_after=80))
A(para("Identificación de KPIs e Indicadores", align="center", bold=True, size=18, color="E2001A", space_after=120))
A(para("Proyecto: Dashboard de Bajas de Activos de TI", align="center", size=13, space_after=40))
A(para("Universidad Autónoma de Occidente · Período 2025–2026", align="center", italic=True, size=11, color="6B7688", space_after=500))
A(para("Complejidad: Media", align="center", size=11, color="6B7688", space_after=40))
A(para("Propósito: traducir las preguntas de negocio en KPIs y métricas medibles", align="center", size=10, color="6B7688", space_after=40))
A(page_break())

# ---- 1. Mapeo pregunta -> KPI ----
A(heading("1. Mapeo pregunta → KPI", 1))
A(para("Cada pregunta de negocio definida en el Entregable 1 se traduce en uno o más KPIs medibles. "
       "Esta trazabilidad garantiza que el dashboard responda exactamente lo que el negocio necesita."))
A(table([
    ["Pregunta de negocio", "KPI(s) asociado(s)"],
    ["P1. ¿Cuántas unidades y cuántos informes se tramitaron?", "KPI-01 Total Unidades, KPI-02 Total Informes, KPI-03 Unidades por Informe"],
    ["P2. ¿Cómo se distribuyen por categoría?", "KPI-04 Unidades por Categoría, KPI-05 % Participación Categoría Top"],
    ["P3. ¿Qué marcas concentran las bajas?", "KPI-06 Unidades por Marca, KPI-07 Concentración de Marca (Top)"],
    ["P4. ¿Cómo evoluciona mes a mes y año a año?", "KPI-08 Unidades Mensuales, KPI-09 Variación Anual %"],
    ["P5. ¿En qué meses hay picos?", "KPI-10 Mes Pico, KPI-11 Unidades del Mes Pico"],
    ["P6. ¿Qué % carece de serie/inventario?", "KPI-12 % Sin Serie, KPI-13 % Sin Inventario"],
    ["P7. ¿Existen seriales duplicados?", "KPI-14 Seriales Duplicados"],
], widths=[4600, 4600]))

# ---- 2. KPIs identificados ----
A(heading("2. KPIs identificados (14 métricas clave)", 1))
A(para("Se identificaron 14 KPIs, clasificados por tipo. El valor \u201cactual\u201d corresponde al "
       "cálculo sobre la base consolidada 2025–2026."))
A(table([
    ["ID", "KPI", "Tipo", "Valor actual"],
    ["KPI-01", "Total Unidades dadas de baja", "Volumen", "1.322"],
    ["KPI-02", "Total Informes técnicos (DITI)", "Volumen", "104"],
    ["KPI-03", "Unidades por Informe", "Eficiencia", "12,7"],
    ["KPI-04", "Unidades por Categoría", "Distribución", "11 categorías"],
    ["KPI-05", "% Participación Categoría Top", "Concentración", "20,7% (Mouse)"],
    ["KPI-06", "Unidades por Marca", "Distribución", "27 marcas"],
    ["KPI-07", "Concentración de Marca Top", "Concentración", "33,7% (Dell)"],
    ["KPI-08", "Unidades Mensuales", "Tendencia", "promedio ~63/mes"],
    ["KPI-09", "Variación Anual %", "Tendencia", "+3,1% (26 vs 25)"],
    ["KPI-10", "Mes Pico", "Tendencia", "jul-2025"],
    ["KPI-11", "Unidades del Mes Pico", "Tendencia", "161"],
    ["KPI-12", "% Registros Sin Serie", "Calidad", "22,3%"],
    ["KPI-13", "% Registros Sin Inventario", "Calidad", "40,4%"],
    ["KPI-14", "Seriales Duplicados", "Calidad", "5"],
], widths=[900, 3600, 1800, 2900]))

# ---- 3. Definiciones claras ----
A(page_break())
A(heading("3. Definiciones claras de cada KPI", 1))
defs = [
    ("KPI-01 · Total Unidades", "Suma de la columna Cantidad en todos los registros de baja. Mide el volumen físico de activos retirados de servicio."),
    ("KPI-02 · Total Informes (DITI)", "Número de consecutivos únicos (documentos DITI). Mide la carga administrativa de trámites de baja."),
    ("KPI-03 · Unidades por Informe", "Promedio de unidades por documento. Indica el tamaño medio de cada trámite (individual vs. lote)."),
    ("KPI-04 · Unidades por Categoría", "Suma de unidades agrupada por categoría de activo (Mouse, Teléfono, Teclado, etc.)."),
    ("KPI-05 · % Participación Categoría Top", "Peso de la categoría con más bajas sobre el total. Señala dónde se concentra la obsolescencia."),
    ("KPI-06 · Unidades por Marca", "Suma de unidades agrupada por marca/fabricante. Apoya decisiones de proveedor."),
    ("KPI-07 · Concentración de Marca Top", "Peso de la marca con más bajas sobre el total. Mide dependencia de un fabricante."),
    ("KPI-08 · Unidades Mensuales", "Suma de unidades por mes calendario (AnioMes). Base de la serie temporal."),
    ("KPI-09 · Variación Anual %", "Cambio porcentual de unidades de 2026 frente a 2025. Mide la tendencia interanual."),
    ("KPI-10 · Mes Pico", "Mes con mayor número de unidades dadas de baja. Identifica estacionalidad/eventos."),
    ("KPI-11 · Unidades del Mes Pico", "Cantidad de unidades del mes pico. Dimensiona el máximo esfuerzo de disposición."),
    ("KPI-12 · % Sin Serie", "Proporción de registros sin número de serie. Indicador de trazabilidad."),
    ("KPI-13 · % Sin Inventario", "Proporción de registros sin número de inventario. Indicador de control patrimonial."),
    ("KPI-14 · Seriales Duplicados", "Cantidad de números de serie que aparecen más de una vez. Control de dobles registros."),
]
for nombre, desc in defs:
    A(para(nombre, bold=True, color="2563EB", space_after=20))
    A(para(desc, space_after=100))

# ---- 4. Fórmulas exactas ----
A(page_break())
A(heading("4. Fórmulas exactas (SQL y Python/DAX)", 1))
A(para("A continuación las fórmulas de los KPIs representativos. Se asume una tabla "
       "bajas_consolidado con las columnas definidas en el diccionario (sección 8)."))

A(para("KPI-01 · Total Unidades", bold=True, color="2563EB"))
A(code_block(["-- SQL", "SELECT SUM(Cantidad) AS total_unidades FROM bajas_consolidado;"], "SQL"))
A(code_block(["# Python (pandas)", "df['Cantidad'].sum()", "", "// DAX (Power BI)", "Total Unidades = SUM ( bajas_consolidado[Cantidad] )"], "Python / DAX"))

A(para("KPI-02 · Total Informes (DITI)", bold=True, color="2563EB"))
A(code_block(["-- SQL", "SELECT COUNT(DISTINCT Consecutivo) AS total_informes FROM bajas_consolidado;"], "SQL"))
A(code_block(["# Python", "df['Consecutivo'].nunique()", "", "// DAX", "Total Informes = DISTINCTCOUNT ( bajas_consolidado[Consecutivo] )"], "Python / DAX"))

A(para("KPI-03 · Unidades por Informe", bold=True, color="2563EB"))
A(code_block(["-- SQL", "SELECT SUM(Cantidad) * 1.0 / COUNT(DISTINCT Consecutivo)", "FROM bajas_consolidado;"], "SQL"))
A(code_block(["# Python", "df['Cantidad'].sum() / df['Consecutivo'].nunique()", "", "// DAX", "Unidades por Informe = DIVIDE ( [Total Unidades], [Total Informes] )"], "Python / DAX"))

A(para("KPI-09 · Variación Anual %", bold=True, color="2563EB"))
A(code_block(["-- SQL", "WITH t AS (",
              "  SELECT Anio, SUM(Cantidad) u FROM bajas_consolidado GROUP BY Anio)",
              "SELECT (MAX(CASE WHEN Anio=2026 THEN u END) -",
              "        MAX(CASE WHEN Anio=2025 THEN u END)) * 1.0 /",
              "        MAX(CASE WHEN Anio=2025 THEN u END) AS variacion FROM t;"], "SQL"))
A(code_block(["# Python", "u = df.groupby('Anio')['Cantidad'].sum()",
              "(u[2026] - u[2025]) / u[2025]", "", "// DAX",
              "Variacion % 25 vs 26 =", "VAR a = [Unidades 2025] VAR b = [Unidades 2026]",
              "RETURN DIVIDE ( b - a, a )"], "Python / DAX"))

A(para("KPI-13 · % Sin Inventario", bold=True, color="2563EB"))
A(code_block(["-- SQL",
              "SELECT AVG(CASE WHEN No_inventario IS NULL OR No_inventario='' ",
              "            THEN 1.0 ELSE 0 END) AS pct_sin_inventario",
              "FROM bajas_consolidado;"], "SQL"))
A(code_block(["# Python", "(df['TieneInventario'] == 'No').mean()", "", "// DAX",
              "% Sin Inventario =", "DIVIDE ( CALCULATE([Total Registros],",
              "  bajas_consolidado[TieneInventario]=\"No\"), [Total Registros] )"], "Python / DAX"))

A(para("KPI-14 · Seriales Duplicados", bold=True, color="2563EB"))
A(code_block(["-- SQL", "SELECT COUNT(*) FROM (",
              "  SELECT [Serie No.] FROM bajas_consolidado",
              "  WHERE [Serie No.] <> '' GROUP BY [Serie No.]",
              "  HAVING COUNT(*) > 1) t;"], "SQL"))
A(code_block(["# Python", "s = df.loc[df['Serie No.']!='', 'Serie No.']",
              "(s.value_counts() > 1).sum()"], "Python"))

# ---- 5. Frecuencia de actualización ----
A(page_break())
A(heading("5. Frecuencia de actualización", 1))
A(para("La cadencia de cálculo se alinea con el ritmo de los trámites de baja (no es tiempo real)."))
A(table([
    ["KPI", "Frecuencia recomendada"],
    ["KPI-01 a KPI-07 (volumen, distribución)", "Mensual (al cierre de mes)"],
    ["KPI-08 a KPI-11 (tendencia/temporales)", "Mensual"],
    ["KPI-12 a KPI-14 (calidad de datos)", "Mensual, con revisión al cargar nuevos informes"],
], widths=[5200, 4000]))
A(para("Mecanismo: el script procesar_bajas.py regenera la base consolidada a partir de los CSV; "
       "en Power BI basta pulsar \u201cActualizar\u201d. Si se publica en Power BI Service, puede "
       "programarse una actualización automática mensual.", space_after=120))

# ---- 6. Benchmarks ----
A(heading("6. Benchmarks: qué es bueno / malo", 1))
A(para("Umbrales de referencia para interpretar cada KPI de calidad y concentración. Los límites "
       "son metas de gestión propuestas para el área de activos de TI."))
A(table([
    ["KPI", "Bueno", "Aceptable", "Malo", "Actual"],
    ["KPI-05 % Categoría Top", "< 25%", "25–40%", "> 40%", "20,7% ✔"],
    ["KPI-07 Concentración Marca Top", "< 35%", "35–50%", "> 50%", "33,7% ✔"],
    ["KPI-09 Variación Anual %", "±10%", "±10–25%", "> 25%", "+3,1% ✔"],
    ["KPI-12 % Sin Serie", "< 10%", "10–20%", "> 20%", "22,3% ✘"],
    ["KPI-13 % Sin Inventario", "< 10%", "10–25%", "> 25%", "40,4% ✘"],
    ["KPI-14 Seriales Duplicados", "0", "1–5", "> 5", "5 ⚠"],
], widths=[3000, 1400, 1600, 1200, 2000]))
A(para("Lectura: los KPIs de concentración y tendencia están en zona saludable. Los indicadores de "
       "trazabilidad (serie e inventario) están en zona crítica y constituyen la principal "
       "oportunidad de mejora del proceso de registro de bajas.", space_after=120))

# ---- 7. Jerarquía ----
A(heading("7. Jerarquía: KPIs primarios vs. secundarios", 1))
A(para("KPIs primarios (tablero ejecutivo — primera mirada):", bold=True))
A(bullet("KPI-01 Total Unidades"))
A(bullet("KPI-02 Total Informes"))
A(bullet("KPI-09 Variación Anual %"))
A(bullet("KPI-05 % Participación Categoría Top"))
A(bullet("KPI-13 % Sin Inventario (señal de calidad crítica)"))
A(para("KPIs secundarios (análisis de detalle y soporte):", bold=True))
A(bullet("KPI-03 Unidades por Informe, KPI-04 Unidades por Categoría"))
A(bullet("KPI-06 Unidades por Marca, KPI-07 Concentración de Marca"))
A(bullet("KPI-08 Unidades Mensuales, KPI-10 Mes Pico, KPI-11 Unidades del Mes Pico"))
A(bullet("KPI-12 % Sin Serie, KPI-14 Seriales Duplicados"))

# ---- 8. Diccionario de datos ----
A(page_break())
A(heading("8. Diccionario de datos (métricas documentadas)", 1))
A(para("Ficha técnica de cada KPI: unidad de medida, origen y dirección deseada "
       "(↑ mejor subir / ↓ mejor bajar / = estable)."))
A(table([
    ["ID", "Métrica", "Unidad", "Origen (columnas)", "Dir."],
    ["KPI-01", "Total Unidades", "unidades", "Cantidad", "="],
    ["KPI-02", "Total Informes", "documentos", "Consecutivo", "="],
    ["KPI-03", "Unidades por Informe", "ratio", "Cantidad / Consecutivo", "="],
    ["KPI-04", "Unidades por Categoría", "unidades", "Cantidad × Categoria", "="],
    ["KPI-05", "% Categoría Top", "%", "Cantidad × Categoria", "↓"],
    ["KPI-06", "Unidades por Marca", "unidades", "Cantidad × Marca", "="],
    ["KPI-07", "Concentración Marca Top", "%", "Cantidad × Marca", "↓"],
    ["KPI-08", "Unidades Mensuales", "unidades", "Cantidad × AnioMes", "="],
    ["KPI-09", "Variación Anual %", "%", "Cantidad × Anio", "="],
    ["KPI-10", "Mes Pico", "texto (AnioMes)", "Cantidad × AnioMes", "="],
    ["KPI-11", "Unidades Mes Pico", "unidades", "Cantidad × AnioMes", "="],
    ["KPI-12", "% Sin Serie", "%", "TieneSerial", "↓"],
    ["KPI-13", "% Sin Inventario", "%", "TieneInventario", "↓"],
    ["KPI-14", "Seriales Duplicados", "conteo", "Serie No.", "↓"],
], widths=[900, 2500, 1500, 2800, 700], fontsize=8))
A(para(""))
A(para("Fin del Entregable 3.", italic=True, color="6B7688", align="center", space_after=0))

# =========================================================================
document_xml = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<w:document {NSMARKS}><w:body>'
                + "".join(body)
                + '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
                  '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
                  'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')

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
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>Entregable 3 - KPIs e Indicadores</dc:title>
<dc:subject>Dashboard Bajas de Activos TI - UAO</dc:subject>
<dc:creator>Proyecto Seminario IA</dc:creator>
</cp:coreProperties>'''

app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<Application>Python docx generator</Application><Company>Universidad Autonoma de Occidente</Company>
</Properties>'''

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
