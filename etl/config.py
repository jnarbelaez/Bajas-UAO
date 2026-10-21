#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración central del pipeline ETL de Bajas de Activos TI (UAO).
Centraliza rutas, nombres de columnas y parámetros de negocio para que el
resto de módulos no tengan valores "hardcodeados".
"""
import os

# --- Rutas base (relativas a la raíz del repositorio) ---
ETL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ETL_DIR)

RAW_DIR = os.path.join(ROOT, "data", "raw")              # CSV de origen
PROCESSED_DIR = os.path.join(ROOT, "data", "processed")  # salida limpia
KPI_DIR = os.path.join(ROOT, "data", "kpis")             # KPIs calculados
LOG_DIR = os.path.join(ROOT, "etl", "logs")              # bitácoras de ejecución

# --- Archivos de origen esperados ---
SOURCE_FILES = ["bajas_2025.csv", "bajas_2026.csv"]

# --- Salidas ---
OUTPUT_FACT = os.path.join(PROCESSED_DIR, "bajas_consolidado.csv")
OUTPUT_KPIS = os.path.join(KPI_DIR, "kpis.json")

# --- Esquema esperado del origen (validación de contrato) ---
EXPECTED_SOURCE_COLUMNS = [
    "Archivo de Origen", "Fecha", "Consecutivo", "Cantidad",
    "Descripción del elemento", "Serie No.", "No. inventario",
]

# --- Columnas de la tabla de hechos de salida ---
FACT_COLUMNS = [
    "Archivo de Origen", "Fecha", "Anio", "Mes", "NombreMes", "AnioMes", "Trimestre",
    "Consecutivo", "Cantidad", "Descripcion del elemento", "Categoria", "Marca",
    "Serie No.", "No. inventario", "IMEI", "TieneSerial", "TieneInventario", "EsLote",
]

# --- Parámetros de negocio ---
VALORES_NO_INFORMATIVOS = {"", "ng", "n/n", "n/a", "sin código", "sin codigo", "na", "nn"}
ANIOS_VALIDOS = {2025, 2026}

# --- Umbrales de validación (fallan el pipeline si se superan) ---
MAX_PCT_FECHAS_INVALIDAS = 5.0     # % máximo de fechas no parseables tolerado
MIN_REGISTROS_ESPERADOS = 100      # mínimo de filas para considerar carga válida

MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}
