import os
from urllib.parse import quote_plus

try:
    from sshtunnel import SSHTunnelForwarder
except Exception:
    SSHTunnelForwarder = None

class Config:
    # Toma 'SECRET_KEY' de Render
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Datos de Base de Datos extraídos de tus variables de entorno en Render
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

    # URL de conexión para SQLAlchemy
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Si Render te da la DATABASE_URL directa, la usamos (corrigiendo el prefijo)
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Si no hay URL directa, la armamos con las variables de tu captura
        # quote_plus asegura que caracteres especiales en la contraseña no rompan la URL
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{quote_plus(DATABASE_USER)}:{quote_plus(DATABASE_PASSWORD)}@"
            f"{DATABASE_HOST}:{DATABASE_PORT}/{quote_plus(DATABASE_NAME)}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'options': '-c client_encoding=LATIN1'},
        # --- NUEVAS OPCIONES PARA EVITAR CAÍDAS ---
        'pool_pre_ping': True,       # Verifica si la conexión sirve antes de usarla
        'pool_recycle': 280,         # Recicla conexiones antes de los 5 min (Render suele matar a los 5)
        'pool_timeout': 30,          # No te quedes colgado esperando si el túnel murió
        'pool_size': 5,              # Mantén pocas conexiones para no saturar tu PC local
        'max_overflow': 2            # Permitir un pequeño margen extra
    }
