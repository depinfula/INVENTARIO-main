"""
Script para crear la base de datos de PostgreSQL automáticamente
Ejecutar: python create_postgres_db.py
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

def create_database():
    """Crea la base de datos de PostgreSQL"""
    
    print("=" * 60)
    print("Creación de Base de Datos PostgreSQL para Inventario")
    print("=" * 60)
    
    # Solicitar credenciales
    print("\nPor favor, ingresa las credenciales de PostgreSQL:")
    host = input("Host (localhost): ").strip() or "localhost"
    port = input("Puerto (5432): ").strip() or "5432"
    user = input("Usuario (postgres): ").strip() or "postgres"
    password = input("Contraseña: ").strip()
    database_name = input("Nombre de la base de datos (inventario): ").strip() or "inventario"
    
    if not password:
        print("\n❌ Error: La contraseña es requerida")
        return False
    
    try:
        # Conectar a PostgreSQL (a la base de datos 'postgres' por defecto)
        print(f"\nConectando a PostgreSQL en {host}:{port}...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres'  # Conectamos a la BD por defecto para crear la nueva
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✓ Conexión establecida")
        
        # Verificar si la base de datos ya existe
        cursor.execute("""
            SELECT 1 FROM pg_database WHERE datname = %s
        """, (database_name,))
        
        exists = cursor.fetchone()
        
        if exists:
            print(f"\n⚠ La base de datos '{database_name}' ya existe.")
            respuesta = input("¿Deseas eliminarla y crearla de nuevo? (s/N): ").strip().lower()
            
            if respuesta == 's':
                # Terminar conexiones activas
                cursor.execute("""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = %s
                    AND pid <> pg_backend_pid();
                """, (database_name,))
                
                # Eliminar la base de datos
                cursor.execute(sql.SQL("DROP DATABASE {}").format(
                    sql.Identifier(database_name)
                ))
                print(f"✓ Base de datos '{database_name}' eliminada")
            else:
                print(f"✓ Usando la base de datos existente '{database_name}'")
                cursor.close()
                conn.close()
                return True
        
        # Crear la base de datos
        print(f"\nCreando base de datos '{database_name}'...")
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(database_name)
        ))
        print(f"✓ Base de datos '{database_name}' creada exitosamente")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        # Probar conexión a la nueva base de datos
        print(f"\nVerificando conexión a la base de datos '{database_name}'...")
        test_conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database_name
        )
        test_conn.close()
        print("✓ Conexión verificada")
        
        print("\n" + "=" * 60)
        print("✓ Base de datos creada exitosamente!")
        print("=" * 60)
        print(f"\nConfiguración para config.py:")
        print(f"  DATABASE_USER = '{user}'")
        print(f"  DATABASE_PASSWORD = '{password}'")
        print(f"  DATABASE_HOST = '{host}'")
        print(f"  DATABASE_PORT = '{port}'")
        print(f"  DATABASE_NAME = '{database_name}'")
        print("\nO usa variables de entorno:")
        print(f"  $env:DATABASE_USER='{user}'")
        print(f"  $env:DATABASE_PASSWORD='{password}'")
        print(f"  $env:DATABASE_HOST='{host}'")
        print(f"  $env:DATABASE_PORT='{port}'")
        print(f"  $env:DATABASE_NAME='{database_name}'")
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Error de conexión: {e}")
        print("\nVerifica que:")
        print("  1. PostgreSQL esté instalado y corriendo")
        print("  2. Las credenciales sean correctas")
        print("  3. El servicio de PostgreSQL esté activo")
        return False
        
    except psycopg2.Error as e:
        print(f"\n❌ Error de PostgreSQL: {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = create_database()
    if success:
        print("\n✓ Proceso completado. Puedes ejecutar la aplicación ahora.")
    else:
        print("\n❌ El proceso falló. Revisa los errores arriba.")
        sys.exit(1)

