import os
from urllib.parse import quote_plus

try:
    from sshtunnel import SSHTunnelForwarder
except Exception:
    SSHTunnelForwarder = None


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_PORT = os.environ.get('DATABASE_PORT')
    DATABASE_NAME = os.environ.get('DATABASE_NAME')

    # SSH Tunnel - Configurado según tus Keys de la imagen
    # Agregamos un valor por defecto False para evitar errores si no se define
    USE_SSH_TUNNEL = os.environ.get('USE_SSH_TUNNEL', 'False').lower() == 'true'
    SSH_HOST = os.environ.get('SSH_HOST')
    SSH_PORT = int(os.environ.get('SSH_PORT', 22))
    SSH_USERNAME = os.environ.get('SSH_USERNAME', 'librum') # Puedes subir esta a Render también
    SSH_PASSWORD = os.environ.get('SSH_PASSWORD')
    SSH_PKEY = os.environ.get('SSH_PKEY') 

    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = (
            'postgresql://'
            f"{quote_plus(DATABASE_USER)}:{quote_plus(DATABASE_PASSWORD)}@{DATABASE_HOST}:{DATABASE_PORT}/{quote_plus(DATABASE_NAME)}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'options': '-c client_encoding=LATIN1'}
    }

