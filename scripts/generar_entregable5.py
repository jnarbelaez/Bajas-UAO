#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el ENTREGABLE 5 · Diseño de Visualizaciones como .docx (sin dependencias)."""
import os
import zipfile
from xml.sax.saxutils import escape

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "entregables", "Entregable5-Diseno-de-Visualizaciones.docx")
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')


def r(t, b=False, i=False, sz=None, col=None):
    rpr = "<w:rPr>"
    if b: rpr += "<w:b/>"
    if i: rpr += "<w:i/>"
    if col: rpr += f'<w:color w:val="{col}"/>'
    if sz: rpr += f'<w:sz w:val="{sz*2}"/><w:szCs w:val="{sz*2}"/>'
    rpr += "</w:rPr>"
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>'

def p(t="", style=None, b=False, i=False, sz=None, col=None, al=None, sa=120):
    pr = "<w:pPr>"
    if style: pr += f'<w:pStyle w:val="{style}"/>'
    if al: pr += f'<w:jc w:val="{al}"/>'
    pr += f'<w:spacing w:after="{sa}"/></w:pPr>'
    return f"<w:p>{pr}{r(t,b,i,sz,col) if t else ''}</w:p>"

def h(t, lvl=1):
    return p(t, style={1:"Heading1",2:"Heading2"}[lvl], sa=160)

def bul(t, bp=None):
    pr = ('<w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="0"/>'
          '<w:numId w:val="1"/></w:numPr><w:spacing w:after="60"/></w:pPr>')
    runs = (r(bp, b=True) if bp else "") + r(t)
    return f"<w:p>{pr}{runs}</w:p>"

def tbl(rows, widths=None, fs=9):
    nc = len(rows[0])
    widths = widths or [int(9200/nc)]*nc
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    o = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/>'
         '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="BFBFBF"/><w:left w:val="single" w:sz="4" w:color="BFBFBF"/>'
         '<w:bottom w:val="single" w:sz="4" w:color="BFBFBF"/><w:right w:val="single" w:sz="4" w:color="BFBFBF"/>'
         '<w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/>'
         f'</w:tblBorders></w:tblPr><w:tblGrid>{grid}</w:tblGrid>']
    for ri, row in enumerate(rows):
        o.append("<w:tr>")
        for j, c in enumerate(row):
            hd = ri == 0
            sh = '<w:shd w:val="clear" w:color="auto" w:fill="E2001A"/>' if hd else ""
            o.append(f'<w:tc><w:tcPr><w:tcW w:w="{widths[j]}" w:type="dxa"/>{sh}</w:tcPr>'
                     f'<w:p><w:pPr><w:spacing w:after="20"/></w:pPr>{r(c,b=hd,col="FFFFFF" if hd else None,sz=fs)}</w:p></w:tc>')
        o.append("</w:tr>")
    o.append("</w:tbl>")
    o.append(p("", sa=120))
    return "".join(o)

def pb():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

body = []
A = body.append

# Portada
A(p("UNIVERSIDAD AUTÓNOMA DE OCCIDENTE", al="center", b=True, sz=14, col="E2001A", sa=40))
A(p("Seminario de Inteligencia Artificial", al="center", i=True, sz=12, sa=400))
A(p("ENTREGABLE 5", al="center", b=True, sz=26, sa=80))
A(p("Diseño de Visualizaciones", al="center", b=True, sz=18, col="E2001A", sa=120))
A(p("Proyecto: Dashboard de Bajas de Activos de TI — UAO", al="center", sz=13, sa=40))
A(p("Complejidad: Media · Período 2025–2026", al="center", i=True, sz=11, col="6B7688", sa=400))
A(p("Nota: los wireframes, la paleta/tipografía y los mockups de alta fidelidad se entregan como",
    al="center", sz=10, col="6B7688", sa=20))
A(p("archivos vectoriales SVG en la carpeta diseno/ (equivalente a Figma, editables y nítidos).",
    al="center", sz=10, col="6B7688", sa=40))
A(pb())

# 1. Wireframes
A(h("1. Wireframes (boceto de layout)", 1))
A(p("El dashboard se organiza en un grid de 12 columnas y cuatro bandas horizontales, siguiendo "
    "un patrón de lectura en Z (lo más importante arriba-izquierda):"))
A(bul("barra con logo, título y acciones (tema, exportar).", "Banda 1 — Encabezado: "))
A(bul("fila de segmentadores (Año, Categoría, Marca, Mes, búsqueda).", "Banda 2 — Filtros: "))
A(bul("5 tarjetas con los KPIs primarios.", "Banda 3 — KPIs: "))
A(bul("barras, dona/treemap y serie temporal de ancho completo.", "Banda 4 — Visuales: "))
A(p("El boceto completo está en diseno/02-wireframe-layout.svg.", i=True, col="6B7688"))

# 2. Paleta
A(h("2. Paleta de colores", 1))
A(p("Paleta profesional y consistente, alineada a la identidad UAO (rojo institucional)."))
A(tbl([
    ["Uso", "Color", "Hex"],
    ["Marca principal", "Rojo UAO", "#E2001A"],
    ["Acento", "Azul", "#2563EB"],
    ["Texto principal", "Gris oscuro", "#1B2330"],
    ["Texto secundario", "Gris medio", "#6B7688"],
    ["Fondo", "Gris muy claro", "#F4F6FB"],
    ["Estado bueno", "Verde", "#10B981"],
    ["Estado alerta", "Ámbar", "#F59E0B"],
    ["Estado crítico", "Rojo", "#E2001A"],
], widths=[3200,3200,2800]))
A(p("La paleta categórica (9 colores) para series de datos está en diseno/01-paleta-tipografia.svg "
    "y en los temas Power BI (powerbi/tema-uao.json y tema-uao-oscuro.json).", i=True, col="6B7688"))

# 3. Tipografía
A(h("3. Tipografía y jerarquía visual", 1))
A(p("Familia única: Segoe UI (nativa en Windows/Power BI; alternativa: system-ui). Jerarquía:"))
A(tbl([
    ["Nivel", "Tamaño / peso", "Uso"],
    ["H1 Título", "30 px Bold", "Nombre del dashboard"],
    ["H2 Subtítulo", "22 px Semibold (rojo)", "Nombre de página"],
    ["H3 Título de visual", "16 px Semibold (azul)", "Encabezado de cada gráfico"],
    ["Valor KPI", "30 px Bold", "Cifra principal de las tarjetas"],
    ["Cuerpo", "13 px Regular", "Texto general"],
    ["Etiqueta / nota", "11 px (secundario)", "Encabezados de tabla y pies"],
], widths=[2400,3200,3600]))

# 4. Por cada KPI: tipo de gráfico
A(pb())
A(h("4. Tipo de gráfico elegido por KPI", 1))
A(p("Cada uno de los 14 KPIs (Entregable 3) se asocia al visual que mejor comunica su naturaleza:"))
A(tbl([
    ["KPI", "Visual elegido", "Por qué"],
    ["KPI-01 Total Unidades", "Tarjeta (card)", "Cifra única de alto impacto"],
    ["KPI-02 Total Informes", "Tarjeta", "Cifra única"],
    ["KPI-03 Unidades/Informe", "Tarjeta con sparkline", "Ratio + contexto"],
    ["KPI-04 Unidades por Categoría", "Barras horizontales", "Comparar muchas categorías ordenadas"],
    ["KPI-05 % Categoría Top", "Tarjeta / KPI visual", "Destacar concentración"],
    ["KPI-06 Unidades por Marca", "Treemap", "Jerarquía por área = peso"],
    ["KPI-07 Concentración Marca", "Dona (anillo)", "Participación sobre el total"],
    ["KPI-08 Unidades Mensuales", "Línea", "Evolución en el tiempo"],
    ["KPI-09 Variación Anual %", "Tarjeta con flecha ▲/▼", "Cambio direccional"],
    ["KPI-10 Mes Pico", "Marcador sobre la línea", "Resaltar máximo"],
    ["KPI-11 Unidades Mes Pico", "Etiqueta de dato", "Dimensión del pico"],
    ["KPI-12 % Sin Serie", "Barra de progreso / gauge", "Avance vs. meta"],
    ["KPI-13 % Sin Inventario", "Barra de progreso / gauge", "Avance vs. meta"],
    ["KPI-14 Seriales Duplicados", "Tabla + indicador", "Listado accionable"],
], widths=[2800,2800,3600], fs=8))

# 5. Interactividad
A(h("5. Interactividad (filtros / slicers)", 1))
A(p("El dashboard es interactivo mediante los siguientes controles, con resaltado cruzado entre "
    "visuales:"))
A(bul("segmentador 2025 / 2026 / ambos.", "Año: "))
A(bul("segmentador de categoría de activo.", "Categoría: "))
A(bul("segmentador de marca/fabricante.", "Marca: "))
A(bul("segmentador temporal de mes y de documento (DITI).", "Mes / Documento: "))
A(bul("cuadro de texto que filtra por descripción, serie o inventario.", "Búsqueda: "))
A(bul("al hacer clic en una categoría/marca, el resto de visuales se filtra automáticamente.", "Cross-filter: "))
A(bul("botón para alternar tema claro/oscuro y botón de exportar la vista a CSV.", "Acciones: "))

# 6. Ratios / dimensiones
A(pb())
A(h("6. Ratios y dimensiones de cada visual", 1))
A(p("Dimensiones de referencia sobre un lienzo de 1280×720 px (16:9, estándar de Power BI):"))
A(tbl([
    ["Visual", "Ancho × Alto (px)", "Proporción"],
    ["Tarjeta KPI", "230 × 90", "~2.5:1"],
    ["Barras por categoría", "620 × 300", "~2:1"],
    ["Dona / anillo", "300 × 300", "1:1"],
    ["Treemap de marcas", "560 × 250", "~2.2:1"],
    ["Serie temporal (línea)", "1240 × 260", "~4.8:1 (ancho completo)"],
    ["Barra de progreso / gauge", "230 × 110", "~2:1"],
    ["Tabla de detalle", "1240 × 300", "ancho completo"],
], widths=[3400,3200,2600]))
A(p("Regla: márgenes de 16 px entre visuales y esquinas redondeadas de 12 px para consistencia.",
    i=True, col="6B7688"))

# 7. Mockups
A(h("7. Mockups de alta fidelidad", 1))
A(p("El mockup de alta fidelidad de la página \u201cResumen Ejecutivo\u201d, con la paleta y tipografía "
    "aplicadas, se entrega en diseno/03-mockup-alta-fidelidad.svg. Adicionalmente, los mockups de las "
    "tres páginas del dashboard Power BI están en powerbi/mockups/ (Resumen Ejecutivo, Detalle por "
    "Activo y Calidad de Datos)."))
A(bul("diseno/03-mockup-alta-fidelidad.svg", "Mockup principal: "))
A(bul("powerbi/mockups/pagina1-resumen-ejecutivo.svg", "Página 1: "))
A(bul("powerbi/mockups/pagina2-detalle-por-activo.svg", "Página 2: "))
A(bul("powerbi/mockups/pagina3-calidad-datos.svg", "Página 3: "))

# 8. Guía de estilo
A(h("8. Guía de estilo (para futuros dashboards)", 1))
A(p("Lineamientos reutilizables para mantener consistencia en próximos tableros de la UAO:"))
A(bul("usar siempre la paleta institucional; el rojo (#E2001A) solo para marca y estados críticos, "
      "nunca para datos neutrales.", "Color: "))
A(bul("máximo 3 niveles de jerarquía tipográfica por pantalla; Segoe UI en todo el tablero.", "Tipografía: "))
A(bul("KPIs primarios arriba (tarjetas); tendencia temporal al pie; detalle en páginas aparte.", "Layout: "))
A(bul("1 visual = 1 idea; elegir el gráfico por la pregunta (comparar→barras, evolución→línea, "
      "parte-todo→dona/treemap, cifra→tarjeta).", "Gráficos: "))
A(bul("semáforo verde/ámbar/rojo para KPIs con meta; flechas ▲/▼ para variaciones.", "Estados: "))
A(bul("títulos claros en español, separador de miles, y nota de fuente al pie de cada página.", "Texto: "))
A(bul("filtros siempre visibles arriba; activar resaltado cruzado; no más de 6–7 visuales por página.", "Interacción: "))
A(p(""))
A(p("Fin del Entregable 5.", i=True, col="6B7688", al="center", sa=0))

doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>'
       + "".join(body)
       + '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" '
         'w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
         '</w:body></w:document>')

ct = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>'''
rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>'''
drels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''
styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/><w:lang w:val="es-CO"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:line="276" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="E2001A"/><w:sz w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="2563EB"/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720"/></w:pPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:color="BFBFBF"/><w:left w:val="single" w:sz="4" w:color="BFBFBF"/><w:bottom w:val="single" w:sz="4" w:color="BFBFBF"/><w:right w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/></w:tblBorders></w:tblPr></w:style>
</w:styles>'''
numbering = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#8226;"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr><w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'''
core = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>Entregable 5 - Diseno de Visualizaciones</dc:title><dc:creator>Proyecto Seminario IA</dc:creator></cp:coreProperties>'''

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", ct)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", doc)
    z.writestr("word/_rels/document.xml.rels", drels)
    z.writestr("word/styles.xml", styles)
    z.writestr("word/numbering.xml", numbering)
    z.writestr("docProps/core.xml", core)

print(f"[OK] Documento generado: {OUT} ({os.path.getsize(OUT):,} bytes)")
