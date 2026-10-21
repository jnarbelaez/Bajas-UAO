# Scheduler — Automatización del Pipeline ETL (Sección 7, opcional)

El pipeline (`run_pipeline.py`) es un proceso por lotes idempotente: cada ejecución
reconstruye la tabla de hechos y los KPIs desde las fuentes. Por eso puede programarse
sin riesgo de duplicar datos. A continuación, tres formas de automatizarlo.

## Opción A · cron (Linux/macOS)

Ejecutar el día 1 de cada mes a las 06:00:

```cron
# crontab -e
0 6 1 * * cd /ruta/al/repo/etl && /usr/bin/python3 run_pipeline.py >> cron.out 2>&1
```

El pipeline ya escribe su propia bitácora con marca de tiempo en `etl/logs/`;
el `>> cron.out` captura además la salida estándar por si cron falla antes de iniciar.

## Opción B · Programador de tareas de Windows

```powershell
# Crear tarea mensual (día 1, 06:00)
schtasks /Create /SC MONTHLY /D 1 /ST 06:00 /TN "ETL_Bajas_UAO" ^
  /TR "python C:\ruta\al\repo\etl\run_pipeline.py"
```

## Opción C · GitHub Actions (nube, sin servidor propio)

El archivo `etl-schedule.yml` (en esta carpeta) ejecuta el pipeline mensualmente y
sube los resultados como artefactos. Para activarlo, cópialo a `.github/workflows/`.

## Recomendaciones de operación

- **Frecuencia:** mensual, alineada con el cierre de trámites de baja (ver Entregable 3).
- **Monitoreo:** revisar el último archivo en `etl/logs/`; un código de salida ≠ 0 indica fallo.
- **Alertas:** en producción, enviar el log por correo o a un canal si el `exit code` es 1 o 2.
- **Reintentos:** al ser idempotente, re-ejecutar es seguro ante un fallo transitorio.
