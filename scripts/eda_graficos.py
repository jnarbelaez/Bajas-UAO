#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera los gráficos del EDA (Entregable 2) como archivos SVG, sin matplotlib.
Produce 10 visualizaciones en entregables/eda_figuras/.
"""
import os
from eda_motor import analizar

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(BASE, "entregables", "eda_figuras")
os.makedirs(FIG, exist_ok=True)

PAL = ["#e2001a", "#2563eb", "#f59e0b", "#10b981", "#8b5cf6", "#06b6d4",
       "#ec4899", "#64748b", "#f97316", "#14b8a6", "#a855f7", "#0ea5e9"]


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _svg(w, h, body, title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="Segoe UI, sans-serif">'
            f'<rect width="{w}" height="{h}" fill="#ffffff"/>'
            f'<text x="20" y="28" font-size="15" font-weight="700" fill="#1b2330">{_esc(title)}</text>'
            f'{body}</svg>')


def barras_h(datos, titulo, archivo, top=None, unidad="u."):
    """datos: lista de (label, valor) ya ordenada desc."""
    if top:
        datos = datos[:top]
    w, h = 720, 60 + len(datos) * 34
    maxv = max(v for _, v in datos) or 1
    x0, barw = 230, 420
    body = []
    y = 56
    for i, (lab, v) in enumerate(datos):
        bw = barw * v / maxv
        body.append(f'<text x="20" y="{y+14}" font-size="12" fill="#1b2330">{_esc(lab[:30])}</text>')
        body.append(f'<rect x="{x0}" y="{y}" width="{bw:.1f}" height="20" rx="3" fill="{PAL[i%len(PAL)]}"/>')
        body.append(f'<text x="{x0+bw+6:.1f}" y="{y+15}" font-size="11" fill="#6b7688">{v:,} {unidad}</text>')
        y += 34
    _write(archivo, _svg(w, h, "".join(body), titulo))


def columnas_pareadas(cats, serieA, serieB, labA, labB, titulo, archivo):
    w, h = 720, 340
    maxv = max(max(serieA or [1]), max(serieB or [1])) or 1
    x0, y0, plot_h = 60, 60, 220
    bw = (w - x0 - 30) / (len(cats) * 2.4)
    body = [f'<line x1="{x0}" y1="{y0+plot_h}" x2="{w-20}" y2="{y0+plot_h}" stroke="#e6eaf2"/>']
    for i, c in enumerate(cats):
        gx = x0 + i * (w - x0 - 30) / len(cats) + 10
        ha = plot_h * serieA[i] / maxv
        hb = plot_h * serieB[i] / maxv
        body.append(f'<rect x="{gx:.1f}" y="{y0+plot_h-ha:.1f}" width="{bw:.1f}" height="{ha:.1f}" fill="#2563eb"/>')
        body.append(f'<rect x="{gx+bw:.1f}" y="{y0+plot_h-hb:.1f}" width="{bw:.1f}" height="{hb:.1f}" fill="#f59e0b"/>')
        body.append(f'<text x="{gx+bw:.1f}" y="{y0+plot_h+16}" font-size="9" fill="#6b7688" text-anchor="middle" transform="rotate(35 {gx+bw:.1f} {y0+plot_h+16})">{_esc(c[:12])}</text>')
    body.append(f'<rect x="{w-180}" y="30" width="12" height="12" fill="#2563eb"/><text x="{w-162}" y="40" font-size="11" fill="#6b7688">{labA}</text>')
    body.append(f'<rect x="{w-110}" y="30" width="12" height="12" fill="#f59e0b"/><text x="{w-92}" y="40" font-size="11" fill="#6b7688">{labB}</text>')
    _write(archivo, _svg(w, h, "".join(body), titulo))


def linea(puntos, titulo, archivo, color="#e2001a"):
    """puntos: lista de (label, valor)"""
    w, h = 720, 320
    x0, y0, pw, ph = 60, 60, w - 90, 200
    maxv = max(v for _, v in puntos) or 1
    n = len(puntos)
    coords = []
    for i, (lab, v) in enumerate(puntos):
        x = x0 + (pw * i / max(n - 1, 1))
        y = y0 + ph - (ph * v / maxv)
        coords.append((x, y, lab, v))
    body = [f'<line x1="{x0}" y1="{y0+ph}" x2="{x0+pw}" y2="{y0+ph}" stroke="#e6eaf2"/>',
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+ph}" stroke="#e6eaf2"/>']
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y, _, _ in coords)
    body.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.5" points="{poly}"/>')
    for i, (x, y, lab, v) in enumerate(coords):
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{color}"/>')
        if i % 2 == 0:
            body.append(f'<text x="{x:.1f}" y="{y0+ph+16}" font-size="8" fill="#6b7688" text-anchor="middle" transform="rotate(40 {x:.1f} {y0+ph+16})">{_esc(lab)}</text>')
    _write(archivo, _svg(w, h, "".join(body), titulo))


def histograma(valores, titulo, archivo, bins=None):
    w, h = 720, 320
    from collections import Counter
    c = Counter(valores)
    items = sorted(c.items())
    x0, y0, ph = 60, 60, 200
    maxv = max(c.values()) or 1
    bw = (w - x0 - 40) / max(len(items), 1)
    body = [f'<line x1="{x0}" y1="{y0+ph}" x2="{w-20}" y2="{y0+ph}" stroke="#e6eaf2"/>']
    for i, (val, cnt) in enumerate(items):
        gx = x0 + i * bw
        bh = ph * cnt / maxv
        body.append(f'<rect x="{gx:.1f}" y="{y0+ph-bh:.1f}" width="{bw*0.8:.1f}" height="{bh:.1f}" fill="#2563eb"/>')
        body.append(f'<text x="{gx+bw*0.4:.1f}" y="{y0+ph+16}" font-size="9" fill="#6b7688" text-anchor="middle">{_esc(val)}</text>')
        body.append(f'<text x="{gx+bw*0.4:.1f}" y="{y0+ph-bh-4:.1f}" font-size="9" fill="#6b7688" text-anchor="middle">{cnt}</text>')
    body.append(f'<text x="{(w)/2:.0f}" y="{h-8}" font-size="10" fill="#93a0b5" text-anchor="middle">Valor de Cantidad por registro</text>')
    _write(archivo, _svg(w, h, "".join(body), titulo))


def dona(datos, titulo, archivo):
    import math
    w, h = 720, 320
    total = sum(v for _, v in datos) or 1
    cx, cy, r = 200, 170, 110
    body, ang = [], -90
    for i, (lab, v) in enumerate(datos):
        frac = v / total
        a2 = ang + frac * 360
        large = 1 if frac > 0.5 else 0
        x1 = cx + r * math.cos(math.radians(ang)); y1 = cy + r * math.sin(math.radians(ang))
        x2 = cx + r * math.cos(math.radians(a2)); y2 = cy + r * math.sin(math.radians(a2))
        body.append(f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large} 1 {x2:.1f},{y2:.1f} Z" fill="{PAL[i%len(PAL)]}"/>')
        ly = 70 + i * 26
        body.append(f'<rect x="370" y="{ly}" width="14" height="14" fill="{PAL[i%len(PAL)]}"/>')
        body.append(f'<text x="392" y="{ly+12}" font-size="12" fill="#1b2330">{_esc(lab)} — {v:,} ({frac*100:.1f}%)</text>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="55" fill="#ffffff"/>')
    body.append(f'<text x="{cx}" y="{cy+5}" font-size="16" font-weight="800" fill="#1b2330" text-anchor="middle">{total:,}</text>')
    _write(archivo, _svg(w, h, "".join(body), titulo))


def nulos_chart(nulos, titulo, archivo):
    items = sorted(((c, d["pct"]) for c, d in nulos.items() if d["pct"] > 0), key=lambda x: -x[1])
    w, h = 720, 60 + max(len(items), 1) * 30
    x0, barw = 230, 400
    body, y = [], 50
    for c, pct in items:
        bw = barw * pct / 100
        col = "#e2001a" if pct >= 40 else ("#f59e0b" if pct >= 20 else "#10b981")
        body.append(f'<text x="20" y="{y+13}" font-size="11" fill="#1b2330">{_esc(c[:28])}</text>')
        body.append(f'<rect x="{x0}" y="{y}" width="{bw:.1f}" height="18" rx="3" fill="{col}"/>')
        body.append(f'<text x="{x0+bw+6:.1f}" y="{y+13}" font-size="11" fill="#6b7688">{pct}%</text>')
        y += 30
    _write(archivo, _svg(w, h, "".join(body), titulo))


def gauge_score(score, titulo, archivo):
    import math
    w, h = 480, 300
    cx, cy, r = 240, 200, 140
    body = []
    # arco de fondo (semicírculo)
    for i in range(0, 180, 2):
        a1 = math.radians(180 - i); a2 = math.radians(180 - (i + 2))
        frac = i / 180
        col = "#e2001a" if frac < .5 else ("#f59e0b" if frac < .75 else "#10b981")
        x1 = cx + r*math.cos(a1); y1 = cy - r*math.sin(a1)
        x2 = cx + r*math.cos(a2); y2 = cy - r*math.sin(a2)
        x3 = cx + (r-26)*math.cos(a2); y3 = cy - (r-26)*math.sin(a2)
        x4 = cx + (r-26)*math.cos(a1); y4 = cy - (r-26)*math.sin(a1)
        body.append(f'<polygon points="{x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f} {x3:.1f},{y3:.1f} {x4:.1f},{y4:.1f}" fill="{col}" opacity="0.9"/>')
    # aguja
    a = math.radians(180 - (score/100*180))
    nx = cx + (r-40)*math.cos(a); ny = cy - (r-40)*math.sin(a)
    body.append(f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#1b2330" stroke-width="4"/>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="#1b2330"/>')
    body.append(f'<text x="{cx}" y="{cy+45}" font-size="40" font-weight="800" fill="#1b2330" text-anchor="middle">{score}</text>')
    body.append(f'<text x="{cx}" y="{cy+68}" font-size="13" fill="#6b7688" text-anchor="middle">/ 100 puntos</text>')
    _write(archivo, _svg(w, h, "".join(body), titulo))


def _write(nombre, contenido):
    with open(os.path.join(FIG, nombre), "w", encoding="utf-8") as fh:
        fh.write(contenido)
    print("  ✔", nombre)


def generar_todos():
    R = analizar()
    print("Generando figuras EDA...")
    # 1. Distribución por categoría (barras)
    cat = sorted(R["por_cat_u"].items(), key=lambda x: -x[1])
    barras_h(cat, "Fig. 1 — Unidades por categoría de activo", "fig01_categorias.svg")
    # 2. Top marcas
    mar = sorted(R["por_marca_u"].items(), key=lambda x: -x[1])
    barras_h(mar, "Fig. 2 — Top marcas / fabricantes (unidades)", "fig02_marcas.svg", top=10)
    # 3. Comparativo por año (dona)
    an = sorted(R["por_anio_u"].items())
    dona(an, "Fig. 3 — Participación de unidades por año", "fig03_anio.svg")
    # 4. Tendencia mensual (línea)
    mes = sorted(R["por_mes_u"].items())
    linea(mes, "Fig. 4 — Tendencia mensual de unidades (2025–2026)", "fig04_tendencia.svg")
    # 5. Histograma de 'Cantidad'
    import csv as _csv
    filas = list(_csv.DictReader(open(os.path.join(BASE,"data","processed","bajas_consolidado.csv"), encoding="utf-8-sig")))
    cants = [int(float(f["Cantidad"])) for f in filas]
    histograma(cants, "Fig. 5 — Distribución de 'Cantidad' (detección de lotes/outliers)", "fig05_histograma.svg")
    # 6. Valores nulos por columna
    nulos_chart(R["nulos"], "Fig. 6 — Porcentaje de valores faltantes por columna", "fig06_nulos.svg")
    # 7. Comparativo 2025 vs 2026 por categoría (columnas pareadas)
    cats_top = [c for c, _ in cat[:8]]
    s25 = [sum(int(float(f["Cantidad"])) for f in filas if f["Anio"]=="2025" and f["Categoria"]==c) for c in cats_top]
    s26 = [sum(int(float(f["Cantidad"])) for f in filas if f["Anio"]=="2026" and f["Categoria"]==c) for c in cats_top]
    columnas_pareadas(cats_top, s25, s26, "2025", "2026", "Fig. 7 — Comparativo 2025 vs 2026 por categoría", "fig07_anio_categoria.svg")
    # 8. Trazabilidad: tiene serial / inventario (barras)
    traz = [("Con serie", R["calidad"]["completitud_serial"]),
            ("Sin serie", 100 - R["calidad"]["completitud_serial"]),
            ("Con inventario", R["calidad"]["completitud_inv"]),
            ("Sin inventario", 100 - R["calidad"]["completitud_inv"])]
    barras_h(traz, "Fig. 8 — Trazabilidad: completitud de serie e inventario (%)", "fig08_trazabilidad.svg", unidad="%")
    # 9. Outliers / lotes top
    out = [(f["Descripcion del elemento"][:26], int(float(f["Cantidad"]))) for f in R["outliers_top"]]
    barras_h(out, "Fig. 9 — Top valores atípicos (lotes de mayor cantidad)", "fig09_outliers.svg")
    # 10. Registros por documento origen
    org = sorted(R["por_origen"].items(), key=lambda x: -x[1])
    barras_h([(k, v) for k, v in org], "Fig. 10 — Registros por archivo de origen", "fig10_origen.svg", unidad="reg.")
    # 11. Score de calidad (gauge)
    gauge_score(R["calidad"]["score"], "Fig. 11 — Score general de calidad de datos", "fig11_score.svg")
    # 12. Correlación serial~inventario (tabla de contingencia como barras)
    cont = R["contingencia"]
    pares = [(f"Serie={k[0]}, Inv={k[1]}", v) for k, v in sorted(cont.items(), key=lambda x: -x[1])]
    barras_h(pares, "Fig. 12 — Contingencia Serie × Inventario (correlación)", "fig12_contingencia.svg", unidad="reg.")
    print("Figuras generadas en:", FIG)


if __name__ == "__main__":
    generar_todos()
