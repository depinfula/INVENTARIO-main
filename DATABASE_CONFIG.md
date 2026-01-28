# Configuración de Base de Datos - Render

## Información de la Base de Datos

La aplicación está configurada para usar la siguiente base de datos PostgreSQL en Render:

- **Host**: `dpg-d4i7qo6mcj7s73cep8fg-a`
- **Usuario**: `inventario_0etk_user`
- **Base de Datos**: `inventario_0etk`
- **Puerto**: `5432` (por defecto)

## URL de Conexión

### Internal Database URL (para uso dentro de Render)
```
postgresql://inventario_0etk_user:cMmhn0IfeHBHr0hXQgoml2GUzqLICjpY@dpg-d4i7qo6mcj7s73cep8fg-a/inventario_0etk
```

Esta URL está configurada automáticamente en:
- `render.yaml` como variable de entorno `DATABASE_URL`
- `config.py` como valores por defecto (si no se encuentra `DATABASE_URL`)

## Configuración en Render Dashboard

Si necesitas configurar manualmente la variable de entorno en Render:

1. Ve a tu servicio web en Render Dashboard
2. Navega a "Environment"
3. Agrega o verifica la variable:
   - **Key**: `DATABASE_URL`
   - **Value**: `postgresql://inventario_0etk_user:cMmhn0IfeHBHr0hXQgoml2GUzqLICjpY@dpg-d4i7qo6mcj7s73cep8fg-a/inventario_0etk`

## Notas de Seguridad

⚠️ **IMPORTANTE**: 
- Esta URL contiene credenciales sensibles
- No compartas este archivo públicamente
- Considera usar variables de entorno en lugar de valores hardcodeados
- La URL interna solo funciona dentro de la red de Render

## Verificación de Conexión

La aplicación verificará automáticamente la conexión al iniciar y creará las tablas necesarias si no existen.

