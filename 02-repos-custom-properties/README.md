# Demo 2: Agrupar repositorios por Custom Properties

Los **Custom Properties** de GitHub permiten añadir metadatos personalizados a los repositorios de tu organización. Esto te permite clasificarlos y agruparlos por equipo, entorno, criticidad, o cualquier criterio que necesites.

## 🏷️ ¿Qué son los Custom Properties?

Son pares clave-valor que defines a nivel de organización y asignas a cada repositorio. Por ejemplo:

| Propiedad | Valores posibles | Descripción |
|-----------|-----------------|-------------|
| `environment` | `production`, `staging`, `development` | Entorno del servicio |
| `team` | `backend`, `frontend`, `platform` | Equipo responsable |
| `criticality` | `high`, `medium`, `low` | Nivel de criticidad |

## 🧪 Casos de uso

- **Filtrar alertas de seguridad**: Obtener alertas solo de repos de producción (ver [Demo 3](../03-alerts-by-custom-properties/))
- **Aplicar rulesets**: GitHub permite usar custom properties en los rulesets para aplicar reglas solo a repos que cumplan ciertos criterios
- **Reporting**: Generar reportes de seguridad agrupados por equipo o criticidad (ver [Demo 4](../04-pdf-report/))

## 📖 Cómo usar esta demo

1. Abre el archivo [`custom-properties.http`](./custom-properties.http) en VS Code
2. Asegúrate de tener tu `.env` configurado con `GITHUB_TOKEN` y `GITHUB_ORG`
3. Ejecuta las peticiones en orden:
   - Primero **crea el esquema** de custom properties en la org
   - Luego **asigna valores** a tus repositorios
   - Finalmente **consulta** los valores asignados

## ⚠️ Permisos necesarios

Para gestionar custom properties necesitas:
- **Fine-grained PAT**: Permiso `Custom properties: Read and write` tanto a nivel de repositorio como de organización
- **Classic PAT**: Scope `repo` + `admin:org`
