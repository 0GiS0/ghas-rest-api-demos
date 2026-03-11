# GHAS REST API Demos

> Demos prácticas para consumir las APIs REST de **GitHub Advanced Security (GHAS)**.

## 📋 Contenido

| # | Demo | Descripción |
|---|------|-------------|
| 1 | [Autenticación con PAT](./01-pat-authentication/) | Cómo crear un PAT y usarlo para consultar las APIs de GHAS |
| 2 | [Repos y Custom Properties](./02-repos-custom-properties/) | Agrupar repositorios usando custom properties |
| 3 | [Alertas por Custom Properties](./03-alerts-by-custom-properties/) | Obtener alertas de GHAS filtradas por custom properties |
| 4 | [Reporte en PDF](./04-pdf-report/) | Generar un reporte PDF con las alertas de GHAS |

## 🚀 Prerrequisitos

- **Python 3.9+**
- **VS Code** con la extensión [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) (o [Postman](https://marketplace.visualstudio.com/items?itemName=Postman.postman-for-vscode))
- Una **organización de GitHub** con GitHub Advanced Security habilitado
- Un **Personal Access Token (PAT)** con los permisos adecuados (ver [Demo 1](./01-pat-authentication/))

## ⚙️ Setup

1. Clona el repositorio:

```bash
git clone https://github.com/<tu-usuario>/ghas-rest-api-demos.git
cd ghas-rest-api-demos
```

2. Copia el archivo de configuración y añade tus valores:

```bash
cp .env.example .env
```

3. Instala las dependencias de Python (necesarias para las demos 3 y 4):

```bash
pip install -r requirements.txt
```

## ⚠️ Notas importantes

- Los archivos `.http` son compatibles tanto con la extensión **REST Client** como con **Postman** para VS Code.
- La API de GHAS **no soporta filtrado directo por custom properties**. La demo 3 muestra cómo resolver esto con un script que hace el filtrado en dos pasos.
- Recuerda que los PATs son sensibles. **Nunca los subas a un repositorio**. Usa siempre el archivo `.env`.
