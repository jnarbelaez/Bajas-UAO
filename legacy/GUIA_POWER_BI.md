# Guía de Construcción — Dashboard Profesional de Bajas de Activos de TI (Power BI)

**Proyecto:** Desarrollo de Dashboard Profesional
**Fuente de datos:** Informes Técnicos para Baja o Devolución de Activos (formato `DSU-3.1.3-FO15`)
**Alcance:** Consolidado **2025 + 2026** · Interactivo · Power BI Desktop
**Usuario final:** Responsable de la administración de los Activos del área de Tecnología (TI)

---

## 1. Archivo que debes cargar

Usa como única fuente la **tabla de hechos** ya limpia y consolidada:

```
data/processed/bajas_consolidado.csv
```

Está en **UTF-8 con BOM** y separador coma, por lo que Power BI reconoce las tildes y la coma automáticamente. Las tablas `resumen_*.csv` son opcionales (solo para validación cruzada).

### Columnas de la tabla de hechos

| Columna | Tipo en Power BI | Descripción |
|---|---|---|
| Archivo de Origen | Texto | PDF de donde proviene (Bajas 2025 / bajas 2026) |
| Fecha | **Fecha** | Fecha del informe técnico (ISO `aaaa-mm-dd`) |
| Anio | Número entero | Año de la baja |
| Mes | Número entero | Mes (1–12) |
| NombreMes | Texto | Nombre del mes en español |
| AnioMes | Texto | Clave `aaaa-mm` para ordenar |
| Trimestre | Texto | `aaaa-Tn` |
| Consecutivo | Texto | Nº de informe (ej. `DITI-4.6-64`) |
| Cantidad | Número entero | Unidades dadas de baja en la línea |
| Descripcion del elemento | Texto | Detalle del activo |
| **Categoria** | Texto | Clasificación TI derivada (Mouse, Teclados, Telefonía…) |
| **Marca** | Texto | Marca detectada (Dell, Apple, Avaya…) |
| Serie No. | Texto | Número de serie |
| No. inventario | Texto | Código de inventario institucional |
| IMEI | Texto | IMEI (solo celulares) |
| TieneSerial | Si/No | Indicador de calidad de dato |
| TieneInventario | Si/No | Indicador de calidad de dato |
| EsLote | Si/No | Línea con Cantidad > 1 |

---

## 2. Importar los datos

1. Abre **Power BI Desktop** → **Inicio → Obtener datos → Texto/CSV**.
2. Selecciona `bajas_consolidado.csv`.
3. En la vista previa, confirma **Origen de archivo = 65001: Unicode (UTF-8)**.
4. Pulsa **Transformar datos** para abrir Power Query y verifica tipos:
   - `Fecha` → **Fecha**
   - `Anio`, `Mes`, `Cantidad` → **Número entero**
   - El resto → **Texto**
5. **Cerrar y aplicar**.

---

## 3. Tabla Calendario (modelo profesional)

Crea una tabla de fechas para habilitar inteligencia de tiempo. En **Modelado → Nueva tabla**:

```DAX
Calendario =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2025, 1, 1 ), DATE ( 2026, 12, 31 ) ),
    "Anio", YEAR ( [Date] ),
    "NroMes", MONTH ( [Date] ),
    "NombreMes", FORMAT ( [Date], "MMMM", "es-ES" ),
    "AnioMes", FORMAT ( [Date], "YYYY-MM" ),
    "Trimestre", "T" & FORMAT ( [Date], "Q" ),
    "AnioTrimestre", FORMAT ( [Date], "YYYY" ) & "-T" & FORMAT ( [Date], "Q" )
)
```

Luego:
- **Modelo:** relaciona `Calendario[Date]` → `bajas_consolidado[Fecha]` (uno a varios).
- Marca la tabla como **tabla de fechas** (clic derecho → *Marcar como tabla de fechas* → `Date`).
- Ordena `NombreMes` por `NroMes` (seleccionar columna → *Ordenar por columna*).

---

## 4. Medidas DAX (crea una tabla "Medidas")

> Modelado → Nueva medida. Agrúpalas en una tabla vacía llamada `_Medidas` para mantener orden.

```DAX
-- KPIs base
Total Unidades = SUM ( bajas_consolidado[Cantidad] )

Total Registros = COUNTROWS ( bajas_consolidado )

Total Informes = DISTINCTCOUNT ( bajas_consolidado[Consecutivo] )

Unidades por Informe =
DIVIDE ( [Total Unidades], [Total Informes] )

-- Comparación entre años
Unidades 2025 =
CALCULATE ( [Total Unidades], bajas_consolidado[Anio] = 2025 )

Unidades 2026 =
CALCULATE ( [Total Unidades], bajas_consolidado[Anio] = 2026 )

Variacion % 25 vs 26 =
VAR a = [Unidades 2025]
VAR b = [Unidades 2026]
RETURN DIVIDE ( b - a, a )

-- Acumulado del año (inteligencia de tiempo)
Unidades YTD =
TOTALYTD ( [Total Unidades], Calendario[Date] )

-- Indicadores de calidad de datos
% Sin Serial =
DIVIDE (
    CALCULATE ( [Total Registros], bajas_consolidado[TieneSerial] = "No" ),
    [Total Registros]
)

% Sin Inventario =
DIVIDE (
    CALCULATE ( [Total Registros], bajas_consolidado[TieneInventario] = "No" ),
    [Total Registros]
)

-- Categoría líder (dinámica según filtros)
Categoria Top =
CALCULATE (
    FIRSTNONBLANK ( bajas_consolidado[Categoria], 1 ),
    TOPN ( 1, VALUES ( bajas_consolidado[Categoria] ), [Total Unidades], DESC )
)
```

---

## 5. Diseño del Dashboard (3 páginas)

### Página 1 — "Resumen Ejecutivo"
Pensada para una mirada de 10 segundos del responsable de activos.

| Zona | Visual | Campos |
|---|---|---|
| Fila de **tarjetas (KPI)** arriba | 5 × *Tarjeta* | `Total Unidades`, `Total Registros`, `Total Informes`, `Unidades por Informe`, `Variacion % 25 vs 26` |
| Izquierda | **Gráfico de columnas** | Eje: `NombreMes`; Valor: `Total Unidades`; Leyenda: `Anio` |
| Centro | **Gráfico de barras** (Top categorías) | Eje: `Categoria`; Valor: `Total Unidades` |
| Derecha | **Gráfico de anillo (dona)** | Leyenda: `Anio`; Valor: `Total Unidades` |
| Inferior | **Treemap** | Grupo: `Marca`; Valor: `Total Unidades` |

### Página 2 — "Detalle por Activo"
Para análisis operativo y búsqueda.

- **Segmentaciones (slicers):** `Anio`, `Categoria`, `Marca`, `EsLote`.
- **Matriz:** Filas → `Categoria` ▸ `Descripcion del elemento`; Columnas → `Anio`; Valores → `Total Unidades`.
- **Tabla detalle:** `Fecha`, `Consecutivo`, `Descripcion del elemento`, `Marca`, `Serie No.`, `No. inventario`, `Cantidad`.
- **Gráfico de líneas:** Eje `AnioMes`, Valor `Total Unidades` (tendencia mensual).

### Página 3 — "Calidad de Datos y Trazabilidad"
Clave para administración de activos: detectar registros sin serial/inventario y posibles duplicados.

- Tarjetas: `% Sin Serial`, `% Sin Inventario`.
- Gráfico de columnas apiladas: `Categoria` × `TieneInventario`.
- Tabla filtrada: registros con `TieneSerial = No` o `TieneInventario = No`.
- Tabla de **seriales duplicados** (filtra `Serie No.` que se repite) → control de doble baja.

---

## 6. Interactividad recomendada

- **Panel de filtros** fijo a la izquierda con `Anio`, `Categoria`, `Marca`.
- Activa **Interacciones de objetos visuales** (Formato → Editar interacciones) para que al hacer clic en una categoría se filtren los demás visuales.
- Agrega **Botones de marcadores** para alternar "Vista 2025", "Vista 2026", "Comparativo".
- Habilita **Información sobre herramientas (tooltips)** personalizados mostrando `Total Informes` y `Unidades por Informe`.

---

## 7. Formato profesional

- **Tema:** Vista → Temas → uno sobrio (ej. "Innovación" o importa un JSON corporativo).
- **Paleta por Año:** 2025 = azul, 2026 = naranja (consistente en todos los visuales).
- Títulos claros en español, formato de miles con separador, y **nota de fuente** al pie: *"Fuente: Informes Técnicos DSU-3.1.3-FO15 — Bajas 2025–2026"*.

---

## 8. Reproducibilidad

Si los PDF de bajas se actualizan, reemplaza/añade los CSV en `data/raw/` y ejecuta:

```bash
python3 scripts/procesar_bajas.py
```

Esto regenera `bajas_consolidado.csv`. En Power BI solo pulsa **Actualizar** y el dashboard se refresca.
