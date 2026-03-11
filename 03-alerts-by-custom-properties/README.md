# Demo 3: Obtener alertas de GHAS filtradas por Custom Properties

## 🎯 El problema

La API de GitHub Advanced Security permite obtener alertas a nivel de **organización** o de **repositorio individual**, pero **no permite filtrar alertas directamente por custom properties**.

En la UI de GitHub sí es posible usar los custom properties como filtro en el Security Overview, pero la API REST no expone este filtrado de forma nativa.

## 💡 La solución

La solución es un flujo de **dos pasos**:

```
1. Obtener repos que cumplan el filtro de custom properties
   GET /orgs/{org}/properties/values?repository_query=props.environment:production

2. Para cada repo filtrado, obtener sus alertas de GHAS
   GET /repos/{org}/{repo}/code-scanning/alerts
   GET /repos/{org}/{repo}/secret-scanning/alerts
   GET /repos/{org}/{repo}/dependabot/alerts
```

## 📖 Contenido de esta demo

### Archivo `.http`
El archivo [`alerts-api.http`](./alerts-api.http) contiene los endpoints individuales para consultar alertas de GHAS directamente.

### Script Python
El script [`get_alerts_by_properties.py`](./get_alerts_by_properties.py) automatiza el flujo completo:
1. Consulta los repos que cumplen un filtro de custom properties
2. Para cada repo, obtiene las alertas de code scanning, secret scanning y dependabot
3. Muestra un resumen en consola

## 🚀 Uso

```bash
# Asegúrate de tener el .env configurado y las dependencias instaladas
pip install -r ../requirements.txt

# Obtener alertas de repos con environment=production
python get_alerts_by_properties.py --property environment --value production

# Filtrar por equipo
python get_alerts_by_properties.py --property team --value backend

# Filtrar por múltiples properties (AND)
python get_alerts_by_properties.py --property environment --value production --property team --value backend

# Mostrar solo alertas abiertas (por defecto)
python get_alerts_by_properties.py --property criticality --value high --state open

# Exportar resultado como JSON
python get_alerts_by_properties.py --property environment --value production --output json
```
