#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el ENTREGABLE 7 · Documentación (.docx): componentes 1-5."""
import os, zipfile
from xml.sax.saxutils import escape

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "entregables", "Entregable7-Documentacion.docx")
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')

def r(t,b=False,i=False,sz=None,col=None):
    rp="<w:rPr>"+("<w:b/>" if b else "")+("<w:i/>" if i else "")
    rp+=(f'<w:color w:val="{col}"/>' if col else "")+(f'<w:sz w:val="{sz*2}"/>' if sz else "")+"</w:rPr>"
    return f'<w:r>{rp}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>'
def p(t="",style=None,b=False,i=False,sz=None,col=None,al=None,sa=120):
    pr="<w:pPr>"+(f'<w:pStyle w:val="{style}"/>' if style else "")+(f'<w:jc w:val="{al}"/>' if al else "")
    pr+=f'<w:spacing w:after="{sa}"/></w:pPr>'
    return f"<w:p>{pr}{r(t,b,i,sz,col) if t else ''}</w:p>"
def h(t,l=1): return p(t,style={1:"Heading1",2:"Heading2"}[l],sa=160)
def bul(t,bp=None):
    pr='<w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr><w:spacing w:after="60"/></w:pPr>'
    return f"<w:p>{pr}{(r(bp,b=True) if bp else '')+r(t)}</w:p>"
def tbl(rows,widths=None,fs=9):
    nc=len(rows[0]);widths=widths or [int(9200/nc)]*nc
    grid="".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    o=['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/>'
       '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="BFBFBF"/><w:left w:val="single" w:sz="4" w:color="BFBFBF"/>'
       '<w:bottom w:val="single" w:sz="4" w:color="BFBFBF"/><w:right w:val="single" w:sz="4" w:color="BFBFBF"/>'
       '<w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/>'
       f'</w:tblBorders></w:tblPr><w:tblGrid>{grid}</w:tblGrid>']
    for ri,row in enumerate(rows):
        o.append("<w:tr>")
        for j,c in enumerate(row):
            hd=ri==0;sh='<w:shd w:val="clear" w:color="auto" w:fill="E2001A"/>' if hd else ""
            o.append(f'<w:tc><w:tcPr><w:tcW w:w="{widths[j]}" w:type="dxa"/>{sh}</w:tcPr>'
                     f'<w:p><w:pPr><w:spacing w:after="20"/></w:pPr>{r(c,b=hd,col="FFFFFF" if hd else None,sz=fs)}</w:p></w:tc>')
        o.append("</w:tr>")
    o.append("</w:tbl>");o.append(p("",sa=120));return "".join(o)
def pb(): return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

B=[];A=B.append
# Portada
A(p("UNIVERSIDAD AUTÓNOMA DE OCCIDENTE",al="center",b=True,sz=14,col="E2001A",sa=40))
A(p("Seminario de Inteligencia Artificial",al="center",i=True,sz=12,sa=400))
A(p("ENTREGABLE 7",al="center",b=True,sz=26,sa=80))
A(p("Documentación y Presentación",al="center",b=True,sz=18,col="E2001A",sa=120))
A(p("Proyecto: Dashboard de Bajas de Activos de TI — UAO",al="center",sz=13,sa=40))
A(p("Complejidad: Media · Período 2025–2026",al="center",i=True,sz=11,col="6B7688",sa=200))
A(p("Este documento reúne los componentes 1–5 del Entregable 7. La presentación ejecutiva (PPTX),",al="center",sz=10,col="6B7688",sa=20))
A(p("el guion del video tutorial y el README de setup se entregan como archivos aparte.",al="center",sz=10,col="6B7688",sa=40))
A(pb())

# 1. Documentación técnica
A(h("1. Documentación técnica",1))
A(p("El proyecto transforma los informes técnicos de baja de activos (formato DSU-3.1.3-FO15) en un "
    "dashboard interactivo, mediante una arquitectura de datos reproducible."))
A(p("Arquitectura general",b=True))
A(p("Fuentes (CSV de bajas 2025/2026) → Pipeline ETL (Extract, Transform, Validate, Load) → Tabla de "
    "hechos consolidada (bajas_consolidado.csv) + KPIs (kpis.json) → Dashboard (web o Power BI)."))
A(p("Componentes técnicos",b=True))
A(bul("archivos CSV en data/raw/ con el esquema del informe técnico.","Fuentes de datos: "))
A(bul("paquete modular en etl/ (config, logger, extract, transform, validate, load, run_pipeline).","Pipeline ETL: "))
A(bul("924 registros × 18 columnas; una fila por línea de activo dado de baja.","Modelo de datos: "))
A(bul("dashboard web (Chart.js, 3 páginas) y plantilla Power BI (tema + medidas DAX).","Capa de visualización: "))
A(bul("solo librería estándar de Python 3.8+ para el ETL; navegador para el dashboard.","Tecnologías: "))
A(p("Flujo de actualización",b=True))
A(p("Al recibir nuevos informes, se añaden/reemplazan los CSV en data/raw/ y se ejecuta "
    "run_pipeline.py, que regenera la tabla de hechos y los KPIs con validación de integridad. "
    "El dashboard se refresca recargando (web) o con Actualizar (Power BI)."))

# 2. Guía de usuario
A(pb())
A(h("2. Guía de usuario: cómo interpretar el dashboard",1))
A(p("El dashboard tiene tres páginas, accesibles desde las pestañas superiores:"))
A(p("Página 1 · Visión general",b=True,col="2563EB"))
A(bul("muestran las cifras clave: unidades dadas de baja, informes (DITI), unidades por año y variación.","Tarjetas KPI: "))
A(bul("barras por categoría, dona de participación por año y la tendencia mensual.","Gráficos: "))
A(bul("al hacer clic en una barra de categoría, el tablero navega a la Página 2 ya filtrada.","Drilldown: "))
A(p("Página 2 · Detalle operacional",b=True,col="2563EB"))
A(bul("top de marcas, top de documentos y la tabla detallada de activos.","Contenido: "))
A(bul("clic en una marca filtra la tabla; doble clic en una fila copia el número de serie.","Interacción: "))
A(p("Página 3 · Análisis comparativo",b=True,col="2563EB"))
A(bul("comparación 2025 vs 2026 por categoría, indicadores de calidad/trazabilidad y estacionalidad.","Contenido: "))
A(p("Filtros globales (aplican a las 3 páginas)",b=True,col="2563EB"))
A(bul("selectores \u201cDesde\u201d y \u201cHasta\u201d acotan el período.","Rango de fechas: "))
A(bul("Año, Categoría, Marca y un buscador por texto libre.","Segmentadores: "))
A(bul("el botón \u201cLimpiar\u201d restablece todos los filtros; \u201cExportar CSV\u201d descarga la vista filtrada.","Acciones: "))

# 3. Diccionario de datos
A(pb())
A(h("3. Diccionario de datos (variables y KPIs)",1))
A(p("Variables de la tabla de hechos:",b=True))
A(tbl([
    ["Variable","Tipo","Descripción"],
    ["Archivo de Origen","Texto","PDF de origen (Bajas 2025 / 2026)"],
    ["Fecha / Anio / Mes","Fecha/Entero","Fecha del trámite y derivados"],
    ["NombreMes / AnioMes / Trimestre","Texto","Dimensiones de tiempo derivadas"],
    ["Consecutivo","Texto","Número de documento (DITI)"],
    ["Cantidad","Entero","Unidades dadas de baja en la línea"],
    ["Descripcion del elemento","Texto","Detalle del activo"],
    ["Categoria","Texto","Clasificación derivada (Mouse, Teléfono…)"],
    ["Marca","Texto","Fabricante derivado (Dell, Avaya…)"],
    ["Serie No. / No. inventario / IMEI","Texto","Identificadores del activo"],
    ["TieneSerial / TieneInventario / EsLote","Si/No","Indicadores de calidad"],
],widths=[3000,1700,4500],fs=8))
A(p("KPIs principales (detalle completo en el Entregable 3):",b=True))
A(tbl([
    ["KPI","Definición","Valor actual"],
    ["Total Unidades","Suma de Cantidad","1.322"],
    ["Total Informes","Consecutivos únicos","104"],
    ["Variación Anual %","Cambio 2026 vs 2025","+3,1%"],
    ["% Categoría Top","Peso de la categoría líder","20,7% (Mouse)"],
    ["% Sin Inventario","Registros sin inventario","40,4%"],
    ["% Sin Serie","Registros sin serie","22,3%"],
],widths=[2600,4000,2600],fs=8))

# 4. Limitaciones
A(pb())
A(h("4. Limitaciones (qué puede mejorar)",1))
A(bul("el 40,4% de registros no tiene número de inventario y el 22,3% carece de serie, lo que limita "
      "la trazabilidad patrimonial individual.","Trazabilidad incompleta: "))
A(bul("no se registra el campo \u201cEstado\u201d (Dañado/Obsoleto/Bueno) del formato original, por lo que "
      "no se analizan los motivos de baja.","Sin motivo de baja: "))
A(bul("la Categoría y la Marca se derivan por reglas sobre la descripción; textos atípicos pueden caer "
      "en \u201cOtros\u201d o \u201cSin marca\u201d.","Clasificación por reglas: "))
A(bul("no hay valor contable ni fecha de compra, por lo que no se calcula vida útil ni depreciación.","Sin datos económicos: "))
A(bul("la actualización es manual (ejecutar el ETL); no hay ingesta en tiempo real.","Actualización por lotes: "))
A(bul("se detectaron 5 seriales repetidos que requieren revisión de posibles dobles registros.","Posibles duplicados: "))

# 5. Roadmap
A(h("5. Roadmap (mejoras futuras)",1))
A(p("Corto plazo",b=True,col="2563EB"))
A(bul("reforzar el registro de serie e inventario en el origen para subir la trazabilidad por encima del 90%."))
A(bul("incorporar el campo Estado (Dañado/Obsoleto/Bueno) para analizar motivos de baja."))
A(p("Mediano plazo",b=True,col="2563EB"))
A(bul("automatizar el ETL con el scheduler (cron o GitHub Actions) para actualización mensual sin intervención."))
A(bul("publicar el .pbix en Power BI Service con actualización programada y control de acceso por roles."))
A(p("Largo plazo",b=True,col="2563EB"))
A(bul("enlazar con el inventario general para analizar el ciclo de vida completo (alta → uso → baja)."))
A(bul("añadir valor contable y fecha de compra para estimar depreciación y planear reposiciones con presupuesto."))
A(bul("modelo predictivo de reposición basado en la estacionalidad detectada (picos de jul-2025 y abr-2026)."))
A(p(""))
A(p("Continúa en los archivos: presentación ejecutiva (PPTX), guion del video y README de setup.",i=True,col="6B7688",al="center",sa=0))

doc=(f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>'
     +"".join(B)+'<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" '
     'w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')
ct='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>'''
rels='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>'''
drels='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/></Relationships>'''
styles='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/><w:lang w:val="es-CO"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:line="276" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="E2001A"/><w:sz w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="2563EB"/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720"/></w:pPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:color="BFBFBF"/><w:left w:val="single" w:sz="4" w:color="BFBFBF"/><w:bottom w:val="single" w:sz="4" w:color="BFBFBF"/><w:right w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/></w:tblBorders></w:tblPr></w:style></w:styles>'''
numbering='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#8226;"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr><w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>'''
core='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>Entregable 7 - Documentacion</dc:title><dc:creator>Proyecto Seminario IA</dc:creator></cp:coreProperties>'''

with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml",ct);z.writestr("_rels/.rels",rels)
    z.writestr("word/document.xml",doc);z.writestr("word/_rels/document.xml.rels",drels)
    z.writestr("word/styles.xml",styles);z.writestr("word/numbering.xml",numbering)
    z.writestr("docProps/core.xml",core)
print(f"[OK] {OUT} ({os.path.getsize(OUT):,} bytes)")
