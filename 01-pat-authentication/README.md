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
3. En **Repository access**, selecciona:
   - `All repositories` (o los repositorios específicos que necesites)
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

6. Haz clic en **Generate token**
7. **Copia el token** y guárdalo en tu archivo `.env`:
   ```
   GITHUB_TOKEN=github_pat_xxxxxxxxxxxxxxxxxxxxxxxx
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

## 📌 Consejos de seguridad

- ⚠️ **Nunca subas tu token a un repositorio**. Usa siempre el archivo `.env` (está en `.gitignore`).
- 🔄 Rota tus tokens periódicamente.
- 🎯 Usa fine-grained PATs siempre que sea posible para limitar el acceso.
- ⏰ Configura una fecha de expiración razonable.
