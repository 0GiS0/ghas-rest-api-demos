# Demo 1: Autenticación con PAT (Personal Access Token)

En esta demo aprenderás a crear un **Personal Access Token** para autenticarte contra las APIs REST de GitHub Advanced Security.

## 🔑 Crear un Personal Access Token

### Opción A: Fine-grained PAT (Recomendado)

Los **fine-grained PATs** permiten controlar los permisos de forma granular y limitar el acceso a repositorios específicos.

1. Ve a [GitHub Settings > Developer settings > Personal access tokens > Fine-grained tokens](https://github.com/settings/personal-access-tokens/new)
2. Configura los campos básicos:
   - **Token name**: `ghas-api-demos`
   - **Expiration**: Elige una fecha de expiración adecuada
   - **Resource owner**: Selecciona la **organización** que tiene GHAS habilitado
   - **Warning**: no basta con crear el token desde las settings de un usuario que sea `Owner` de la org. El PAT tiene que quedar creado con la org como **Resource owner**. Si lo creas con tu cuenta personal como resource owner, las llamadas a `/orgs/{org}/repos` pueden devolver `[]` y las llamadas GHAS org-level pueden devolver `404`.
3. En **Repository access**, selecciona:
   - `All repositories` (o los repositorios específicos que necesites)
   - Si eliges repositorios concretos, asegúrate de incluir el repo que vayas a consultar en `ghas-api.http`
4. En **Permissions > Repository permissions**, asigna:

   | Permiso | Nivel | Para qué |
   |---------|-------|----------|
   | **Code scanning alerts** | `Read` | Consultar alertas de code scanning |
   | **Secret scanning alerts** | `Read` | Consultar alertas de secret scanning |
   | **Dependabot alerts** | `Read` | Consultar alertas de Dependabot |
   | **Custom properties** | `Read and write` | Gestionar custom properties de repos |
   | **Metadata** | `Read` | Acceso básico a la metadata del repo (se selecciona automáticamente) |
   | **Administration** | `Read` | Listar repos de la organización |

5. En **Permissions > Organization permissions**, asigna:

   | Permiso | Nivel | Para qué |
   |---------|-------|----------|
   | **Custom properties** | `Read and write` | Gestionar el esquema de custom properties de la org |

> Importante: para consultar alertas GHAS a nivel de organización no basta con que el token sea válido. El usuario autenticado debe ser **owner** o **security manager** de la organización. Si no, GitHub suele responder **404** aunque el endpoint exista.

> Importante: además del rol del usuario, el fine-grained PAT debe estar asociado a la organización correcta en **Resource owner**. Si el token está asociado a tu cuenta personal, no heredará automáticamente el acceso por ser owner de la org.

6. Haz clic en **Generate token**
7. **Copia el token** y guárdalo en tu archivo `.env` como `GITHUB_TOKEN_DEMO_01`:
   ```
   GITHUB_TOKEN_DEMO_01=github_pat_xxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Opción B: Classic PAT

Si prefieres un PAT clásico (más simple pero con permisos más amplios):

1. Ve a [GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)](https://github.com/settings/tokens/new)
2. Configura:
   - **Note**: `ghas-api-demos`
   - **Expiration**: Elige una fecha de expiración
3. Selecciona los **scopes**:

   | Scope | Para qué |
   |-------|----------|
   | `repo` | Acceso completo a repositorios (incluye alertas de Dependabot) |
   | `security_events` | Leer alertas de code scanning y secret scanning |
   | `read:org` | Leer información de la organización |

4. Haz clic en **Generate token**
5. **Copia el token** y guárdalo en tu archivo `.env`

## 🧪 Probar la autenticación

Una vez tengas el token, abre el archivo [`ghas-api.http`](./ghas-api.http) en VS Code y haz clic en **Send Request** encima de cualquier petición para verificar que funciona.

Esta demo usa la variable `GITHUB_TOKEN_DEMO_01`.

Empieza por este orden:

1. `GET /user`
2. `GET /orgs/{org}`
3. `GET /orgs/{org}/repos`
4. Ajusta `@repo` a un repo real visible para tu token
5. Prueba las llamadas de GHAS

Si una llamada devuelve **404**, normalmente significa una de estas cosas:

- El repo no existe en esa organización o el nombre no coincide exactamente
- El token no tiene acceso a ese repo
- No eres **owner** o **security manager** de la organización para consultas org-level
- El PAT fue creado con tu usuario personal como **Resource owner** en vez de con la organización
- La feature no está habilitada en ese repo, por ejemplo secret scanning o code scanning

## 📸 Capturas

Puedes pegar aquí un par de capturas para dejar documentada la configuración del token:

### Captura 1: Resource owner correcto

![Resource owner del PAT](../docs/images/pat-setup/PAT%20-%20Resource%20owner.png)

### Captura 2: Permisos del PAT

![Permisos del PAT](../docs/images/pat-setup/PAT%20-%20Permissions.png)

## 📌 Consejos de seguridad

- ⚠️ **Nunca subas tu token a un repositorio**. Usa siempre el archivo `.env` (está en `.gitignore`).
- 🔄 Rota tus tokens periódicamente.
- 🎯 Usa fine-grained PATs siempre que sea posible para limitar el acceso.
- ⏰ Configura una fecha de expiración razonable.
