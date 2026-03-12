# Demo 5: Autenticación con GitHub App

En esta demo aprenderás a autenticarte contra las APIs REST de GitHub Advanced Security usando una **GitHub App** en lugar de un Personal Access Token.

## 🤖 ¿Por qué usar una GitHub App?

Las GitHub Apps ofrecen varias ventajas sobre los PATs:

| GitHub App | Personal Access Token |
|------------|----------------------|
| ✅ No asociada a un usuario específico | ❌ Vinculado a un usuario |
| ✅ Permisos granulares y auditables | ⚠️ Scopes más amplios (classic) |
| ✅ Tokens de corta duración (1 hora) | ⚠️ Tokens de larga duración |
| ✅ Rate limits más altos | ⚠️ Rate limits estándar |
| ✅ Ideal para automatización y CI/CD | ⚠️ Problemas si el usuario deja la org |

## 🔑 Crear una GitHub App

### Paso 1: Crear la App

1. Ve a [GitHub Settings > Developer settings > GitHub Apps > New GitHub App](https://github.com/settings/apps/new)
   - Si quieres crear la app a nivel de **organización**: `https://github.com/organizations/{org}/settings/apps/new`
2. Configura los campos básicos:
   - **GitHub App name**: `ghas-api-demo-app` (debe ser único en todo GitHub)
   - **Homepage URL**: `https://github.com/0GiS0/ghas-rest-api-demos` (o cualquier URL válida)
   - **Webhook**: Desmarca `Active` (no necesitamos webhooks para esta demo)

### Paso 2: Configurar permisos

En **Repository permissions**, asigna:

| Permiso | Nivel | Para qué |
|---------|-------|----------|
| **Code scanning alerts** | `Read` | Consultar alertas de code scanning |
| **Secret scanning alerts** | `Read` | Consultar alertas de secret scanning |
| **Dependabot alerts** | `Read` | Consultar alertas de Dependabot |
| **Metadata** | `Read` | Acceso básico a la metadata del repo |

En **Organization permissions**, asigna:

| Permiso | Nivel | Para qué |
|---------|-------|----------|
| **Administration** | `Read` | Listar repositorios de la organización |

### Paso 3: Elegir dónde se puede instalar

En **Where can this GitHub App be installed?**:
- Selecciona `Only on this account` si solo la usarás en tu organización
- Selecciona `Any account` si quieres que otras organizaciones puedan instalarla

### Paso 4: Crear y descargar la clave privada

1. Haz clic en **Create GitHub App**
2. Ve a la sección **Private keys** y haz clic en **Generate a private key**
3. Se descargará un archivo `.pem`. **Guárdalo de forma segura**.
4. Mueve el archivo `.pem` a la raíz del proyecto y renómbralo a `github-app.pem`:
   ```bash
   mv ~/Downloads/ghas-api-demo-app.*.private-key.pem ./c
   ```

### Paso 5: Anotar el App ID

1. En la página de configuración de tu GitHub App, copia el **App ID** (un número)
2. Guárdalo en tu archivo `.env`:
   ```
   GITHUB_APP_ID=123456
   ```

### Paso 6: Instalar la App en tu organización

1. Ve a la pestaña **Install App** en la configuración de tu GitHub App
2. Haz clic en **Install** junto a tu organización
3. Selecciona:
   - `All repositories` para acceso a todos los repos
   - `Only select repositories` para limitar el acceso
4. Haz clic en **Install**
5. Copia el **Installation ID** de la URL resultante:
   - URL: `https://github.com/organizations/{org}/settings/installations/12345678`
   - El Installation ID es `12345678`
6. Guárdalo en tu archivo `.env`:
   ```
   GITHUB_APP_INSTALLATION_ID=12345678
   ```

## 🔐 Cómo funciona la autenticación

La autenticación con GitHub App tiene dos pasos:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FLUJO DE AUTENTICACIÓN                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. GENERAR JWT                                                     │
│     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │
│     │ App ID      │ + │ Private Key │ ──▶ │    JWT      │        │
│     │             │     │   (.pem)    │     │ (10 min)    │        │
│     └─────────────┘     └─────────────┘     └─────────────┘        │
│                                                    │                │
│                                                    ▼                │
│  2. OBTENER INSTALLATION TOKEN                                      │
│     ┌─────────────┐     ┌─────────────────────────────────┐        │
│     │    JWT      │ ──▶ │ POST /app/installations/{id}/   │        │
│     │             │     │      access_tokens              │        │
│     └─────────────┘     └─────────────────────────────────┘        │
│                                         │                           │
│                                         ▼                           │
│     ┌───────────────────────────────────────────────────────┐      │
│     │         Installation Access Token (1 hora)            │      │
│     │         Usar como: Bearer {token}                     │      │
│     └───────────────────────────────────────────────────────┘      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 🧪 Generar el token de instalación

### Opción 1: Usando el script Python

```bash
# Asegúrate de tener las dependencias instaladas
pip install -r requirements.txt

# Ejecutar el script
cd 05-github-app-authentication
python3 get_installation_token.py
```

El script:
1. Lee la clave privada de `github-app.pem`
2. Genera un JWT firmado con RS256
3. Llama a la API de GitHub para obtener el installation token
4. Muestra el token y su fecha de expiración

### Opción 2: Usando GitHub CLI

Si tienes `gh` instalado:

```bash
# Autenticarte como GitHub App
gh auth login --with-token < github-app.pem

# O usar gh api directamente con el JWT
# (requiere generar el JWT manualmente primero)
```

## 🔍 Probar las llamadas a la API

Una vez tengas el installation token, puedes:

1. **Usar el archivo [`ghas-api.http`](./ghas-api.http)**:
   - Primero ejecuta el script Python para obtener el token
   - Copia el token en la variable `@token` del archivo `.http`
   - Ejecuta las peticiones con REST Client

2. **Usar el script directamente**:
   - El script `get_installation_token.py` incluye ejemplos de llamadas a la API

## 📝 Variables de entorno necesarias

Añade estas variables a tu archivo `.env`:

```bash
# GitHub App configuration
GITHUB_APP_ID=123456
GITHUB_APP_INSTALLATION_ID=12345678
GITHUB_APP_PRIVATE_KEY_PATH=./github-app.pem

# Organización para las consultas
GITHUB_ORG=mi-organizacion
```

## ⚠️ Consideraciones de seguridad

1. **Nunca subas la clave privada `.pem` al repositorio**
   - Está incluida en `.gitignore`
   - Guárdala en un lugar seguro (vault, secrets manager, etc.)

2. **Los tokens de instalación expiran en 1 hora**
   - Tu código debe renovar el token cuando sea necesario
   - El script incluye un ejemplo de cómo verificar la expiración

3. **Rota las claves privadas periódicamente**
   - Puedes generar nuevas claves desde la configuración de la App
   - Las claves antiguas seguirán funcionando hasta que las revoques

## 🔗 Recursos adicionales

- [Documentación oficial: Authenticating as a GitHub App](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app)
- [Documentación oficial: Generating a JWT](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-json-web-token-jwt-for-a-github-app)
- [API: Create installation access token](https://docs.github.com/en/rest/apps/apps#create-an-installation-access-token-for-an-app)
