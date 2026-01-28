import sys
import os
import argparse
import traceback
from urllib.parse import quote_plus

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from config import Config
except Exception as e:
    print('Error importing Config:', e)
    raise

try:
    from sqlalchemy import create_engine, text
except Exception as e:
    print('SQLAlchemy no disponible:', e)
    raise

try:
    from sshtunnel import SSHTunnelForwarder
except Exception:
    SSHTunnelForwarder = None

try:
    import paramiko
except Exception:
    paramiko = None


def build_uri(conf, local_port=None, overrides=None):
    if overrides is None:
        overrides = {}
    database_url = getattr(conf, 'database_url', None)
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url

    user = overrides.get('user') or conf.DATABASE_USER
    password = overrides.get('password') or conf.DATABASE_PASSWORD
    dbname = overrides.get('name') or conf.DATABASE_NAME
    host = '127.0.0.1' if local_port else (overrides.get('host') or conf.DATABASE_HOST)
    port = local_port or (overrides.get('port') or conf.DATABASE_PORT)

    return (
        'postgresql://'
        f"{quote_plus(str(user))}:{quote_plus(str(password))}@{host}:{port}/{quote_plus(str(dbname))}"
    )


def parse_args():
    p = argparse.ArgumentParser(description='Probar conexión a la BD (opcional túnel SSH)')
    p.add_argument('--use-ssh', action='store_true', help='Forzar uso de túnel SSH (ignora USE_SSH_TUNNEL)')
    p.add_argument('--local-port', type=int, help='Puerto local fijo para el túnel SSH')
    p.add_argument('--ssh-host')
    p.add_argument('--ssh-port', type=int)
    p.add_argument('--ssh-user')
    p.add_argument('--ssh-pkey')
    p.add_argument('--ssh-password')
    p.add_argument('--db-host')
    p.add_argument('--db-port')
    p.add_argument('--db-user')
    p.add_argument('--db-password')
    p.add_argument('--db-name')
    return p.parse_args()


def main():
    args = parse_args()
    conf = Config

    use_ssh = args.use_ssh or bool(conf.USE_SSH_TUNNEL)
    print('USE_SSH_TUNNEL (env/Config):', conf.USE_SSH_TUNNEL, '-> effective:', use_ssh)

    server = None
    local_port = None

    overrides = {
        'host': args.db_host,
        'port': args.db_port,
        'user': args.db_user,
        'password': args.db_password,
        'name': args.db_name,
    }

    try:
        if use_ssh:
            if SSHTunnelForwarder is None:
                print('sshtunnel no está instalado. Instala con: pip install sshtunnel')
                return

            # Check paramiko compatibility
            if paramiko is not None and not hasattr(paramiko, 'DSSKey'):
                print('Advertencia: la versión instalada de paramiko parece ser incompatible con sshtunnel.')
                print('Instala una versión compatible (por ejemplo: pip install "paramiko<3") y vuelve a intentarlo.')
                return

            ssh_host = args.ssh_host or conf.SSH_HOST
            ssh_port = args.ssh_port or conf.SSH_PORT or 22
            ssh_user = args.ssh_user or conf.SSH_USERNAME
            ssh_pkey = args.ssh_pkey or conf.SSH_PKEY
            ssh_password = args.ssh_password or conf.SSH_PASSWORD

            print(f'Iniciando túnel SSH a {ssh_host}:{ssh_port} como {ssh_user}')

            server_kwargs = {
                'remote_bind_address': (conf.DATABASE_HOST, int(conf.DATABASE_PORT)),
            }
            if args.local_port:
                server_kwargs['local_bind_address'] = ('127.0.0.1', int(args.local_port))

            server = SSHTunnelForwarder(
                (ssh_host, int(ssh_port)),
                ssh_username=ssh_user,
                ssh_password=ssh_password or None,
                ssh_pkey=ssh_pkey or None,
                **server_kwargs,
            )
            server.start()
            local_port = server.local_bind_port
            print('Túnel SSH iniciado en puerto local', local_port)

        uri = build_uri(conf, local_port=local_port, overrides=overrides)
        print('Probando conexión a:', uri)

        # Set PG client encoding env var to help decode server messages
        os.environ.setdefault('PGCLIENTENCODING', 'LATIN1')

        opts = getattr(conf, 'SQLALCHEMY_ENGINE_OPTIONS', {}) or {}
        print('Engine options:', opts)

        engine = create_engine(uri, **opts)
        with engine.connect() as conn:
            r = conn.execute(text('SELECT version();'))
            version = r.scalar()
            print('Versión de la base de datos:', version)

        print('Conexión OK')
    except Exception as e:
        print('Conexión FALLIDA:', repr(e))
        traceback.print_exc()
    finally:
        if server:
            print('Deteniendo túnel SSH')
            server.stop()


if __name__ == '__main__':
    main()
