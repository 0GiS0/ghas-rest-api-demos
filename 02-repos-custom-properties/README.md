# Demo 2: Agrupar repositorios por Custom Properties

Los **Custom Properties** de GitHub permiten añadir metadatos personalizados a los repositorios de tu organización. Esto te permite clasificarlos y agruparlos por tipo de aplicación, plataforma móvil, o cualquier criterio que necesites.

## 🏷️ ¿Qué son los Custom Properties?

Son pares clave-valor que defines a nivel de organización y asignas a cada repositorio. Por ejemplo:

| Propiedad | Valores posibles | Descripción |
|-----------|-----------------|-------------|
| `application_type` | `mobile`, `web`, `desktop` | Tipo de aplicación del repositorio |
| `mobile_platform` | `android`, `ios` | Plataforma de la app móvil |

La property `mobile_platform` solo aplica a repositorios cuyo `application_type` sea `mobile`. En repos web o desktop se puede dejar sin valor.

## 🧪 Casos de uso

- **Filtrar alertas de seguridad**: Obtener alertas solo de repos de producción (ver [Demo 3](../03-alerts-by-custom-properties/))
- **Filtrar alertas de seguridad**: Obtener alertas solo de apps móviles Android o iOS (ver [Demo 3](../03-alerts-by-custom-properties/))
- **Aplicar rulesets**: GitHub permite usar custom properties en los rulesets para aplicar reglas solo a repos que cumplan ciertos criterios
- **Reporting**: Generar reportes de seguridad agrupados por tipo de aplicación o plataforma móvil (ver [Demo 4](../04-pdf-report/))

## 📖 Cómo usar esta demo

1. Abre el archivo [`custom-properties.http`](./custom-properties.http) en VS Code
2. Asegúrate de tener tu `.env` configurado con `GITHUB_TOKEN_DEMO_02` y `GITHUB_ORG`
3. Ejecuta las peticiones en orden:
   - Primero **crea el esquema** de custom properties en la org
   - Luego **asigna valores** a tus repositorios según sean mobile, web o desktop
   - Finalmente **consulta** los valores asignados

## ⚠️ Permisos necesarios

Para gestionar custom properties necesitas:
- **Variable usada en esta demo**: `GITHUB_TOKEN_DEMO_02`
- **Fine-grained PAT**: Permiso `Custom properties: Read and write` tanto a nivel de repositorio como de organización
- **Classic PAT**: Scope `repo` + `admin:org`
