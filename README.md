# Sistema de Inventario de Equipos Informáticos

Aplicación web desarrollada en Flask para la gestión de inventario de equipos informáticos por departamento.

## Características

- ✅ **Sistema de autenticación**: Login y registro de usuarios
- ✅ **Gestión de Departamentos**: Crear, editar y eliminar departamentos
- ✅ **Gestión de Equipos**: Registrar equipos con código, serial, tipo, marca, modelo, estatus, asignación, fechas, etc.
- ✅ **Gestión de Personal**: Registrar personal por departamento
- ✅ **Dashboard**: Vista general con estadísticas del inventario

## Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)
- PostgreSQL 12 o superior (recomendado) o SQLite (desarrollo)

## Instalación

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Configuración de Base de Datos

### PostgreSQL (Recomendado para Producción)

1. **Instalar PostgreSQL** desde https://www.postgresql.org/download/

2. **Crear la base de datos:**
```sql
CREATE DATABASE inventario;
```

3. **Configurar credenciales** en `config.py` o usar variables de entorno:
```bash
# Windows PowerShell
$env:DATABASE_USER="postgres"
$env:DATABASE_PASSWORD="tu_contraseña"
$env:DATABASE_HOST="localhost"
$env:DATABASE_PORT="5432"
$env:DATABASE_NAME="inventario"
```

4. **Migrar datos de SQLite (si aplica):**
```bash
python migrate_to_postgresql.py
```

Ver `setup_postgresql.md` para instrucciones detalladas.

### SQLite (Desarrollo)

La aplicación puede usar SQLite para desarrollo. Simplemente ejecuta la aplicación y se creará automáticamente.

## Ejecución

Para iniciar la aplicación:

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Usuario por Defecto

Al iniciar la aplicación por primera vez, se crea automáticamente un usuario administrador:

- **Usuario**: `admin`
- **Contraseña**: `admin123`

**¡Importante!** Cambia la contraseña después del primer inicio de sesión.

## Estructura del Proyecto

```
inventario/
├── app.py              # Aplicación principal Flask
├── models.py           # Modelos de base de datos
├── forms.py            # Formularios WTForms
├── config.py           # Configuración
├── requirements.txt    # Dependencias
├── templates/          # Plantillas HTML
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── departments.html
│   ├── department_form.html
│   ├── equipment.html
│   ├── equipment_form.html
│   ├── personnel.html
│   └── personnel_form.html
└── static/             # Archivos estáticos (CSS, JS)
    └── style.css
```

## Funcionalidades Detalladas

### Equipos Informáticos

Cada equipo puede tener:
- Código único
- Serial único
- Tipo de equipo (Laptop, Desktop, Monitor, Impresora, etc.)
- Marca y modelo
- Estatus (Disponible, Asignado, Mantenimiento, Baja)
- Departamento asignado
- Personal asignado
- Fecha de registro
- Fecha de compra
- Fecha de vencimiento de garantía
- Notas adicionales

### Personal

Cada miembro del personal puede tener:
- Nombre y apellido
- Email y teléfono
- Cargo/Posición
- ID de empleado
- Departamento asignado

## Notas de Seguridad

- En producción, cambia la `SECRET_KEY` en `config.py`
- Usa una base de datos más robusta (PostgreSQL, MySQL) en producción
- Implementa HTTPS en producción
- Considera agregar roles y permisos de usuario

## Licencia

Este proyecto es de código abierto y está disponible para uso personal y comercial.

