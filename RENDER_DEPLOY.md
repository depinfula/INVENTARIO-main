# Guía de Despliegue en Render

Esta guía te ayudará a desplegar tu aplicación de inventario en Render.

## Pasos para Desplegar

### Opción 1: Despliegue Automático con render.yaml (Recomendado)

1. **Sube tu código a GitHub**
   - Crea un repositorio en GitHub
   - Sube todos los archivos del proyecto

2. **Conecta con Render**
   - Ve a [Render Dashboard](https://dashboard.render.com)
   - Haz clic en "New +" y selecciona "Blueprint"
   - Conecta tu repositorio de GitHub
   - Render detectará automáticamente el archivo `render.yaml` y creará los servicios

3. **Configuración Automática**
   - Render creará automáticamente:
     - Un servicio web (aplicación Flask)
     - Una base de datos PostgreSQL
   - Las variables de entorno se configurarán automáticamente

### Opción 2: Despliegue Manual

1. **Crear Base de Datos PostgreSQL**
   - En Render Dashboard, haz clic en "New +" → "PostgreSQL"
   - Nombre: `inventario-db`
   - Plan: Free
   - Anota la **Internal Database URL** (se usará más adelante)

2. **Crear Servicio Web**
   - En Render Dashboard, haz clic en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Configuración:
     - **Name**: `inventario-web`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
   
3. **Variables de Entorno**
   - En la sección "Environment Variables" del servicio web, agrega:
     - `SECRET_KEY`: Genera una clave secreta (puedes usar: `python -c "import secrets; print(secrets.token_hex(32))"`)
     - `DATABASE_URL`: Copia la **Internal Database URL** de la base de datos creada
     - `PYTHON_VERSION`: `3.11.0`

4. **Desplegar**
   - Haz clic en "Create Web Service"
   - Render comenzará a construir y desplegar tu aplicación

## Configuración Post-Despliegue

### Inicializar la Base de Datos

Después del primer despliegue, la aplicación creará automáticamente las tablas y un usuario administrador:

- **Usuario**: `admin`
- **Contraseña**: `admin123`

**⚠️ IMPORTANTE**: Cambia la contraseña del administrador inmediatamente después del primer inicio de sesión.

### Variables de Entorno Importantes

- `SECRET_KEY`: Clave secreta para sesiones Flask (generada automáticamente en render.yaml)
- `DATABASE_URL`: URL de conexión a PostgreSQL (configurada automáticamente)
- `PORT`: Puerto donde corre la aplicación (configurado automáticamente por Render)

## Solución de Problemas

### Error de Conexión a la Base de Datos

Si ves errores de conexión:
1. Verifica que `DATABASE_URL` esté configurada correctamente
2. Asegúrate de que la base de datos esté en el mismo plan que el servicio web
3. Usa la **Internal Database URL** (no la externa) para mejor rendimiento

### Error en el Build

Si el build falla:
1. Verifica que `requirements.txt` tenga todas las dependencias
2. Revisa los logs de build en Render Dashboard
3. Asegúrate de que Python 3.11 esté disponible

### La Aplicación no Inicia

1. Verifica que el comando de inicio sea: `gunicorn app:app`
2. Revisa los logs del servicio en Render Dashboard
3. Asegúrate de que el puerto esté configurado correctamente (Render lo hace automáticamente)

## Notas Importantes

- **Plan Free**: Render ofrece un plan gratuito, pero el servicio puede "dormir" después de 15 minutos de inactividad
- **Base de Datos**: El plan gratuito de PostgreSQL tiene límites de almacenamiento (1 GB)
- **Archivos Subidos**: Los archivos subidos se guardan en el sistema de archivos del contenedor. Considera usar un servicio de almacenamiento (S3, Cloudinary) para producción
- **HTTPS**: Render proporciona HTTPS automáticamente para todos los servicios

## Actualizaciones

Para actualizar la aplicación:
1. Haz push de tus cambios a GitHub
2. Render detectará automáticamente los cambios y desplegará una nueva versión

## Recursos Adicionales

- [Documentación de Render](https://render.com/docs)
- [Guía de Python en Render](https://render.com/docs/deploy-python)
- [Guía de PostgreSQL en Render](https://render.com/docs/databases)

