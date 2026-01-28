import os
from urllib.parse import quote_plus

try:
    from sshtunnel import SSHTunnelForwarder
except Exception:
    SSHTunnelForwarder = None


class Config:
    """
    Configuración de la aplicación.

    IMPORTANTE:
    - NUNCA guardes credenciales reales (usuario, contraseña, host, etc.) en este archivo.
    - Usa SIEMPRE variables de entorno en tu máquina, en Render o en cualquier otro servidor.
    - Este archivo puede estar en un repositorio público sin exponer datos sensibles.
    """

    # Clave secreta de Flask
    # En producción DEFINIR siempre la variable de entorno SECRET_KEY.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Datos de base de datos (SIEMPRE desde variables de entorno en producción)
    DATABASE_USER = os.environ.get('DATABASE_USER', 'postgres')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'postgres')
    DATABASE_HOST = os.environ.get('DATABASE_HOST', '127.0.0.1')
    DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'inventario')

    # Opciones de túnel SSH (también SIEMPRE desde variables de entorno)
    # En producción, define USE_SSH_TUNNEL=true si quieres usar el túnel.
    USE_SSH_TUNNEL = os.environ.get('USE_SSH_TUNNEL', 'false').lower() == 'true'
    SSH_HOST = os.environ.get('SSH_HOST', '')
    SSH_PORT = int(os.environ.get('SSH_PORT', '22'))
    SSH_USERNAME = os.environ.get('SSH_USERNAME', '')
    SSH_PASSWORD = os.environ.get('SSH_PASSWORD', '')
    # Ruta a clave privada (si se usa). También se pasa por variable de entorno.
    SSH_PKEY = os.environ.get('SSH_PKEY')

    # Si el proveedor (por ejemplo Render) expone DATABASE_URL, la respetamos.
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = (
            'postgresql://'
            f"{quote_plus(DATABASE_USER)}:{quote_plus(DATABASE_PASSWORD)}"
            f"@{DATABASE_HOST}:{DATABASE_PORT}/{quote_plus(DATABASE_NAME)}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'options': '-c client_encoding=LATIN1'}
    }
