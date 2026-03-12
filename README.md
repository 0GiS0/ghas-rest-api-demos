# GHAS REST API Demos

<div align="center">

[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC140iBrEZbOtvxWsJ-Tb0lQ?style=for-the-badge&logo=youtube&logoColor=white&color=red)](https://www.youtube.com/c/GiselaTorres?sub_confirmation=1)
[![GitHub followers](https://img.shields.io/github/followers/0GiS0?style=for-the-badge&logo=github&logoColor=white)](https://github.com/0GiS0)
[![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-Sígueme-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/giselatorresbuitrago/)
[![X Follow](https://img.shields.io/badge/X-Sígueme-black?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/0GiS0)

</div>

---

¡Hola developer 👋🏻! Este repositorio contiene demos prácticas para consumir las **APIs REST de GitHub Advanced Security (GHAS)**. Aprenderás a autenticarte con PATs, filtrar repositorios por custom properties, obtener alertas de seguridad y generar reportes en PDF.

---

## 📑 Tabla de Contenidos

<div align="center">

|  |  |  |
|:---:|:---:|:---:|
| [✨ Características](#-características) | [📋 Demos Incluidas](#-demos-incluidas) | [🛠️ Tecnologías](#️-tecnologías-utilizadas) |
| [📝 Requisitos Previos](#-requisitos-previos) | [🚀 Instalación](#-instalación) | [💻 Uso](#-uso) |
| [🔐 PATs por Demo](#-pats-por-demo) | [📁 Estructura](#-estructura-del-proyecto) | [📸 Capturas](#-capturas) |

</div>

<p align="center">
  <a href="#-sígueme-en-mis-redes-sociales">🌐 <strong>Sígueme en Mis Redes Sociales</strong></a>
</p>

---

## ✨ Características

- **5 demos progresivas** que cubren desde autenticación hasta generación de reportes
- Archivos `.http` listos para usar con la extensión REST Client de VS Code
- **Colecciones de Postman** incluidas para fácil importación
- Scripts en Python para filtrado avanzado y generación de PDFs
- Documentación detallada de permisos necesarios para cada demo
- Ejemplos reales de integración con la API de GHAS

---

## 📋 Demos Incluidas

| # | Demo | Descripción |
|---|------|-------------|
| 1 | [Autenticación con PAT](./01-pat-authentication/) | Cómo crear un PAT y usarlo para consultar las APIs de GHAS |
| 2 | [Repos y Custom Properties](./02-repos-custom-properties/) | Agrupar repositorios usando custom properties |
| 3 | [Alertas por Custom Properties](./03-alerts-by-custom-properties/) | Obtener alertas de GHAS filtradas por custom properties |
| 4 | [Reporte en PDF](./04-pdf-report/) | Generar un reporte PDF con las alertas de GHAS |
| 5 | [Autenticación con GitHub App](./05-github-app-authentication/) | Usar una GitHub App para autenticarse en lugar de PAT |

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.9+** - Scripts de filtrado y generación de reportes
- **GitHub REST API** - API de GitHub Advanced Security
- **VS Code REST Client** - Para probar las llamadas HTTP
- **Postman** - Colecciones alternativas para testing
- **FPDF2** - Generación de reportes PDF
- **python-dotenv** - Gestión de variables de entorno
- **PyJWT** - Generación de tokens JWT para GitHub App

---

## 📋 Requisitos Previos

- **Python 3.9+** instalado
- **VS Code** con la extensión [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) (o [Postman](https://marketplace.visualstudio.com/items?itemName=Postman.postman-for-vscode))
- Una **organización de GitHub** con GitHub Advanced Security habilitado
- Un **Personal Access Token (PAT)** con los permisos adecuados (ver [Demo 1](./01-pat-authentication/))

---

## 🚀 Instalación

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/0GiS0/ghas-rest-api-demos.git
cd ghas-rest-api-demos
```

### Paso 2: Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` y añade tus valores.

### Paso 3: Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

> **Nota:** Las dependencias de Python son necesarias para las demos 3 y 4.

---

## 💻 Uso

### Opción 1: REST Client (VS Code)

Los archivos `.http` de este repo están pensados para la extensión **REST Client**. Simplemente abre cualquier archivo `.http` y haz clic en "Send Request".

### Opción 2: Postman para VS Code

1. Abre la extensión de Postman en VS Code
2. Importa `postman/ghas-rest-api-demos.postman_environment.json` como Environment
3. Rellena `GITHUB_ORG` y los `GITHUB_TOKEN_DEMO_*` que vayas a usar
4. Importa una o varias colecciones desde la carpeta `postman/`
5. Selecciona ese Environment antes de enviar las requests

### ⚠️ Notas importantes sobre PATs

> **Importante para fine-grained PATs:**
> - Si vas a consultar una organización, crea el PAT con esa organización seleccionada en `Resource owner`
> - No basta con crear el token desde las settings de un usuario que sea `Owner` de la org
> - Si el `Resource owner` es tu cuenta personal en vez de la org, GitHub puede responder `[]` en `/orgs/{org}/repos` y `404` en los endpoints GHAS de organización
> - Este repo usa un PAT distinto por demo para que quede claro qué permisos necesita cada flujo
> - La API de GHAS **no soporta filtrado directo por custom properties**. La demo 3 muestra cómo resolver esto con un script que hace el filtrado en dos pasos

⚠️ **Recuerda que los PATs son sensibles. ¡Nunca los subas a un repositorio!** Usa siempre el archivo `.env`.

---

## 🔐 PATs por Demo

| Demo | Variable en `.env` | Uso | Permisos principales |
|---|---|---|---|
| 1 | `GITHUB_TOKEN_DEMO_01` | Validar autenticación y consultar GHAS directamente | `Code scanning alerts: Read`, `Secret scanning alerts: Read`, `Dependabot alerts: Read`, `Metadata: Read` |
| 2 | `GITHUB_TOKEN_DEMO_02` | Crear y consultar custom properties | `Custom properties: Read and write` |
| 3 | `GITHUB_TOKEN_DEMO_03` | Filtrar repos por properties y leer alertas GHAS | `Custom properties: Read`, `Code scanning alerts: Read`, `Secret scanning alerts: Read`, `Dependabot alerts: Read`, `Metadata: Read` |
| 4 | `GITHUB_TOKEN_DEMO_04` | Generar el PDF con alertas y filtros por properties | mismos permisos que Demo 3 |
| 5 | `GITHUB_APP_ID` + `GITHUB_APP_INSTALLATION_ID` | Autenticación con GitHub App | Ver [Demo 5](./05-github-app-authentication/) para permisos de la App |

---

## 📁 Estructura del Proyecto

```
ghas-rest-api-demos/
├── 01-pat-authentication/      # Demo 1: Autenticación con PAT
│   ├── ghas-api.http
│   └── README.md
├── 02-repos-custom-properties/ # Demo 2: Custom Properties
│   ├── custom-properties.http
│   └── README.md
├── 03-alerts-by-custom-properties/ # Demo 3: Alertas filtradas
│   ├── alerts-api.http
│   ├── get_alerts_by_properties.py
│   └── README.md
├── 04-pdf-report/              # Demo 4: Reporte PDF
│   ├── generate_report.py
│   └── README.md
├── 05-github-app-authentication/ # Demo 5: GitHub App Auth
│   ├── ghas-api.http
│   ├── get_installation_token.py
│   └── README.md
├── docs/
│   └── images/
│       └── pat-setup/          # Capturas de configuración PAT
├── postman/                    # Colecciones de Postman
│   ├── 01-pat-authentication.postman_collection.json
│   ├── 02-repos-custom-properties.postman_collection.json
│   ├── 03-alerts-by-custom-properties.postman_collection.json
│   └── ghas-rest-api-demos.postman_environment.json
├── .env.example
├── requirements.txt
└── README.md
```

---

## 📸 Capturas

### Captura 1: Resource owner del PAT

![Resource owner del PAT](./docs/images/pat-setup/PAT%20-%20Resource%20owner.png)

### Captura 2: Permisos del PAT

![Permisos del PAT](./docs/images/pat-setup/PAT%20-%20Permissions.png)

---

## 🌐 Sígueme en Mis Redes Sociales

Si te ha gustado este proyecto y quieres ver más contenido como este, no olvides suscribirte a mi canal de YouTube y seguirme en mis redes sociales:

<div align="center">

[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC140iBrEZbOtvxWsJ-Tb0lQ?style=for-the-badge&logo=youtube&logoColor=white&color=red)](https://www.youtube.com/c/GiselaTorres?sub_confirmation=1)
[![GitHub followers](https://img.shields.io/github/followers/0GiS0?style=for-the-badge&logo=github&logoColor=white)](https://github.com/0GiS0)
[![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-Sígueme-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/giselatorresbuitrago/)
[![X Follow](https://img.shields.io/badge/X-Sígueme-black?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/0GiS0)

</div>
