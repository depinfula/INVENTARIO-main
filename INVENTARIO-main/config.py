import os
from urllib.parse import quote_plus

try:
    from sshtunnel import SSHTunnelForwarder
except Exception:
    SSHTunnelForwarder = None


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    DATABASE_USER =  'librum'
    DATABASE_PASSWORD = 't0npl4*2020'
    DATABASE_HOST = os.environ.get('DATABASE_HOST') or '127.0.0.1'
    DATABASE_PORT = os.environ.get('DATABASE_PORT') or '5432'
    DATABASE_NAME = 'inventario'

    # SSH tunnel options
    USE_SSH_TUNNEL = True
    SSH_HOST = '190.168.74.199'
    SSH_PORT =  22
    SSH_USERNAME='librum'
    SSH_PASSWORD='t0npl4*2020'
    SSH_PKEY = os.environ.get('SSH_PKEY')  # path to private key file, optional

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

