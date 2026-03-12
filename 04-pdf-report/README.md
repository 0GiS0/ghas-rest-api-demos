# Demo 4: Generar reporte en PDF

Genera un reporte PDF con las alertas de GitHub Advanced Security de tu organización. Opcionalmente puedes filtrar por custom properties para generar reportes segmentados.

## 🚀 Uso

```bash
# Asegúrate de tener las dependencias instaladas
pip install -r ../requirements.txt

# Generar reporte de TODA la organización
python 04-pdf-report/generate_report.py

# Generar reporte filtrado por custom properties
python 04-pdf-report/generate_report.py --property application_type --value mobile

# Filtrar por múltiples properties
python 04-pdf-report/generate_report.py --property application_type --value mobile --property mobile_platform --value android

# Especificar nombre de archivo de salida
python 04-pdf-report/generate_report.py --output mi-reporte.pdf

# Incluir alertas cerradas
python 04-pdf-report/generate_report.py --state open
```

Esta demo usa la variable `GITHUB_TOKEN_DEMO_04`.

## ⚠️ Permisos necesarios

- **Fine-grained PAT** en `GITHUB_TOKEN_DEMO_04`
- `Custom properties: Read` si vas a filtrar por properties
- `Code scanning alerts: Read`
- `Secret scanning alerts: Read`
- `Dependabot alerts: Read`
- `Metadata: Read`

## 📄 Contenido del reporte

El PDF generado incluye:

1. **Portada** — Nombre de la organización, fecha de generación y filtros aplicados
2. **Resumen ejecutivo** — Total de alertas por tipo (Code Scanning, Secret Scanning, Dependabot) y por severidad
3. **Detalle por repositorio** — Tabla con las alertas de cada repo, organizadas por tipo

## 📋 Ejemplo de salida

El reporte se genera en el directorio actual con el nombre `ghas-report-YYYY-MM-DD.pdf` (o el nombre que especifiques con `--output`).
