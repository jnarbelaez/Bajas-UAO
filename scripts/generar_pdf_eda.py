#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el informe EDA (Entregable 2) como HTML imprimible a PDF (8-10 páginas),
con las 12 figuras SVG embebidas y las 9 secciones. Sin dependencias externas.
"""
import os
from eda_motor import analizar

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(BASE, "entregables", "eda_figuras")
OUT = os.path.join(BASE, "entregables", "Entregable2-EDA-Informe.html")
R = analizar()


def svg_inline(nombre):
    p = os.path.join(FIG, nombre)
    with open(p, encoding="utf-8") as fh:
        return f'<div class="fig">{fh.read()}</div>'


sc = R["stats_cant"]
cal = R["calidad"]
ns = R["nulos"]["Serie No."]
ni = R["nulos"]["No. inventario"]

html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<title>Entregable 2 · Análisis Exploratorio de Datos</title>
<style>
  @page {{ size: A4; margin: 18mm 16mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; color:#1b2330; line-height:1.55; max-width: 820px; margin: 0 auto; padding: 24px; }}
  h1 {{ color:#e2001a; font-size: 26px; margin-bottom:4px; }}
  h2 {{ color:#e2001a; font-size: 18px; border-bottom:2px solid #f0e0e2; padding-bottom:4px; margin-top:28px; page-break-after: avoid; }}
  h3 {{ color:#2563eb; font-size:14px; }}
  .sub {{ color:#6b7688; font-size: 13px; }}
  table {{ border-collapse: collapse; width:100%; font-size:12px; margin:10px 0; }}
  th {{ background:#e2001a; color:#fff; text-align:left; padding:6px 8px; }}
  td {{ border:1px solid #e6eaf2; padding:6px 8px; }}
  .fig {{ margin:12px 0; page-break-inside: avoid; border:1px solid #eef1f6; border-radius:8px; padding:6px; }}
  .fig svg {{ width:100%; height:auto; }}
  .kpi-row {{ display:flex; gap:10px; flex-wrap:wrap; margin:12px 0; }}
  .kpi {{ flex:1; min-width:140px; border:1px solid #e6eaf2; border-radius:10px; padding:10px 14px; border-left:4px solid #e2001a; }}
  .kpi .v {{ font-size:22px; font-weight:800; }}
  .kpi .l {{ font-size:11px; color:#6b7688; text-transform:uppercase; }}
  .note {{ background:#f9fafc; border-left:3px solid #2563eb; padding:8px 12px; font-size:13px; margin:10px 0; }}
  code {{ background:#f4f6fb; padding:1px 5px; border-radius:4px; font-size:12px; }}
  footer {{ margin-top:30px; color:#93a0b5; font-size:11px; text-align:center; }}
  .pb {{ page-break-before: always; }}
</style></head><body>

<h1>Entregable 2 · Análisis Exploratorio de Datos (EDA)</h1>
<p class="sub">Proyecto: Dashboard de Bajas de Activos de TI — Universidad Autónoma de Occidente ·
Complejidad: Media · Fuente: Informes Técnicos DSU-3.1.3-FO15 · Período: 2025–2026</p>

<div class="kpi-row">
  <div class="kpi"><div class="l">Registros</div><div class="v">{R['n']:,}</div></div>
  <div class="kpi"><div class="l">Unidades</div><div class="v">{R['total_unidades']:,}</div></div>
  <div class="kpi"><div class="l">Variables</div><div class="v">{len(R['cols'])}</div></div>
  <div class="kpi"><div class="l">Score calidad</div><div class="v">{cal['score']}</div></div>
</div>

<h2>1. Carga de datos</h2>
<p>Se carga la tabla de hechos consolidada <code>bajas_consolidado.csv</code> (codificación UTF-8),
construida a partir de los informes técnicos de baja de 2025 y 2026. La carga se realiza con
<code>pandas.read_csv(...)</code> interpretando <code>Fecha</code> como tipo fecha. El notebook
adjunto (<code>Entregable2-EDA.ipynb</code>) contiene el código ejecutable.</p>

<h2>2. Dimensiones: tamaño, variables y tipos</h2>
<p>El conjunto tiene <strong>{R['n']} registros</strong> (líneas de activo) y
<strong>{len(R['cols'])} variables</strong>. Predominan variables categóricas y dos de tipo fecha;
la única métrica numérica continua es <code>Cantidad</code>.</p>
<table>
<tr><th>Variable</th><th>Tipo</th><th>Rol analítico</th></tr>
<tr><td>Fecha</td><td>Fecha</td><td>Dimensión temporal</td></tr>
<tr><td>Cantidad</td><td>Entero</td><td>Métrica numérica</td></tr>
<tr><td>Categoria</td><td>Texto</td><td>Dimensión categórica (derivada)</td></tr>
<tr><td>Marca</td><td>Texto</td><td>Dimensión categórica (derivada)</td></tr>
<tr><td>Serie No. / No. inventario</td><td>Texto</td><td>Identificadores de activo</td></tr>
<tr><td>TieneSerial / TieneInventario / EsLote</td><td>Si/No</td><td>Indicadores de calidad</td></tr>
</table>

<h2>3. Estadísticas descriptivas</h2>
<p>Estadísticos de la variable <code>Cantidad</code> (unidades por línea):</p>
<table>
<tr><th>Media</th><th>Mediana</th><th>Moda</th><th>Desv. Est.</th><th>Mín</th><th>Q1</th><th>Q3</th><th>Máx</th></tr>
<tr><td>{sc['media']}</td><td>{sc['mediana']}</td><td>{sc['moda']}</td><td>{sc['desv_std']}</td>
<td>{sc['min']}</td><td>{sc['q1']}</td><td>{sc['q3']}</td><td>{sc['max']}</td></tr>
</table>
<div class="note">La mayoría de registros corresponde a 1 unidad; la media de {sc['media']} y el máximo
de {sc['max']} evidencian registros de <strong>lote</strong>. Las distribuciones categóricas se
muestran en las figuras 1–4.</div>
{svg_inline('fig01_categorias.svg')}
{svg_inline('fig02_marcas.svg')}
<div class="pb"></div>
{svg_inline('fig03_anio.svg')}
{svg_inline('fig04_tendencia.svg')}

<h2>4. Valores nulos / faltantes</h2>
<p>Ubicación e impacto de los vacíos. Los campos identificadores son los más afectados:</p>
<table>
<tr><th>Columna</th><th>Faltantes</th><th>%</th></tr>
<tr><td>No. inventario</td><td>{ni['faltantes']}</td><td>{ni['pct']}%</td></tr>
<tr><td>Serie No.</td><td>{ns['faltantes']}</td><td>{ns['pct']}%</td></tr>
</table>
<div class="note"><strong>Impacto:</strong> el {ni['pct']}% de registros sin número de inventario y
el {ns['pct']}% sin serie limitan la trazabilidad patrimonial. No afectan el conteo de bajas, pero
sí la auditoría. Es el principal hallazgo de calidad.</div>
{svg_inline('fig06_nulos.svg')}

<h2>5. Duplicados</h2>
<p>Filas 100% idénticas: <strong>{R['filas_dup']}</strong>. Números de serie repetidos:
<strong>{len(R['dup_serial'])}</strong> (posibles dobles bajas o errores de digitación).</p>
<table>
<tr><th>Serie No.</th><th>Repeticiones</th></tr>
{''.join(f'<tr><td>{s}</td><td>{c}</td></tr>' for s,c in list(R['dup_serial'].items())[:6])}
</table>

<h2>6. Valores atípicos (outliers)</h2>
<p>Con la regla IQR (Q1={sc['q1']}, Q3={sc['q3']}, IQR={sc['iqr']}), todo valor &gt;
{R['lim_sup']} es atípico. Se detectaron <strong>{len(R['outliers'])} registros</strong>, todos
correspondientes a <strong>lotes legítimos</strong> (mouse, bases de teléfono, diademas en bloque),
no a errores.</p>
{svg_inline('fig05_histograma.svg')}
{svg_inline('fig09_outliers.svg')}
<div class="pb"></div>

<h2>7. Correlaciones entre variables</h2>
<p>Relaciones principales:</p>
<ul>
<li><strong>Mes ↔ Cantidad:</strong> {R['corr_mes_cant']} (prácticamente nula; el volumen no crece
linealmente con el mes, hay picos puntuales).</li>
<li><strong>Tiene serie ↔ Tiene inventario:</strong> {R['corr_ser_inv']} (positiva débil; los
registros bien documentados tienden a tener ambos campos).</li>
<li><strong>Cantidad ↔ tiene serie:</strong> negativa; los lotes grandes no listan serie individual.</li>
</ul>
{svg_inline('fig12_contingencia.svg')}
{svg_inline('fig07_anio_categoria.svg')}

<h2>8. Visualizaciones</h2>
<p>El entregable incluye <strong>12 gráficos</strong> (figuras 1–12). Las figuras 1–7, 9 y 12 ya
aparecen en las secciones anteriores. A continuación, las restantes de trazabilidad y origen.</p>
{svg_inline('fig08_trazabilidad.svg')}
{svg_inline('fig10_origen.svg')}

<h2>9. Calidad de datos: score general</h2>
<p>Score compuesto (0–100) promediando cinco dimensiones:</p>
<table>
<tr><th>Dimensión</th><th>Valor</th></tr>
<tr><td>Completitud de serie</td><td>{cal['completitud_serial']}%</td></tr>
<tr><td>Completitud de inventario</td><td>{cal['completitud_inv']}%</td></tr>
<tr><td>Unicidad (sin duplicados)</td><td>{cal['unicidad']}%</td></tr>
<tr><td>Validez de fecha</td><td>{cal['validez_fecha']}%</td></tr>
<tr><td>Consistencia de categoría</td><td>{cal['consistencia_cat']}%</td></tr>
<tr><td><strong>SCORE GENERAL</strong></td><td><strong>{cal['score']} / 100</strong></td></tr>
</table>
{svg_inline('fig11_score.svg')}
<div class="note"><strong>Conclusión:</strong> el dataset obtiene <strong>{cal['score']}/100</strong>
(calidad buena). Fortalezas: 0 duplicados, 100% de fechas válidas, alta consistencia de
categorización. Debilidad principal: completitud de inventario ({cal['completitud_inv']}%) y serie
({cal['completitud_serial']}%). Los outliers son lotes legítimos. <strong>El dataset es apto para
alimentar el dashboard</strong> de bajas de activos de TI.</div>

<footer>Entregable 2 · EDA · Universidad Autónoma de Occidente · Generado a partir de los Informes
Técnicos DSU-3.1.3-FO15 (Bajas 2025–2026). Para exportar a PDF: abrir en el navegador →
Imprimir → Guardar como PDF (A4).</footer>
</body></html>"""

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(html)

print(f"[OK] Informe HTML/PDF generado: {OUT}")
print(f"     Tamaño: {os.path.getsize(OUT):,} bytes")
