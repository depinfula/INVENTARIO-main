"""
Script para crear la base de datos de PostgreSQL automáticamente
Ejecutar: python create_postgres_db_auto.py
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Crea la base de datos de PostgreSQL"""
    
    print("=" * 60)
    print("Creación de Base de Datos PostgreSQL para Inventario")
    print("=" * 60)
    
    # Configuración por defecto
    host = "localhost"
    port = "5432"
    user = "postgres"
    password = "dimasoftwares"
    database_name = "inventario"
    
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
        
        print("[OK] Conexion establecida")
        
        # Verificar si la base de datos ya existe
        cursor.execute("""
            SELECT 1 FROM pg_database WHERE datname = %s
        """, (database_name,))
        
        exists = cursor.fetchone()
        
        if exists:
            print(f"\n[INFO] La base de datos '{database_name}' ya existe.")
            print("Eliminando base de datos existente...")
            
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
            print(f"[OK] Base de datos '{database_name}' eliminada")
        
        # Crear la base de datos
        print(f"\nCreando base de datos '{database_name}'...")
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(database_name)
        ))
        print(f"[OK] Base de datos '{database_name}' creada exitosamente")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        # Probar conexión a la nueva base de datos
        print(f"\nVerificando conexion a la base de datos '{database_name}'...")
        test_conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database_name
        )
        test_conn.close()
        print("[OK] Conexion verificada")
        
        print("\n" + "=" * 60)
        print("[OK] Base de datos creada exitosamente!")
        print("=" * 60)
        print(f"\nConfiguración aplicada:")
        print(f"  Host: {host}")
        print(f"  Puerto: {port}")
        print(f"  Usuario: {user}")
        print(f"  Base de datos: {database_name}")
        print("\n[OK] La aplicacion esta lista para usar PostgreSQL")
        print("\nProximos pasos:")
        print("  1. Ejecuta: python app.py")
        print("  2. Las tablas se crearan automaticamente")
        print("  3. Si tienes datos en SQLite, ejecuta: python migrate_to_postgresql.py")
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n[ERROR] Error de conexion: {e}")
        print("\nVerifica que:")
        print("  1. PostgreSQL este instalado y corriendo")
        print("  2. El servicio de PostgreSQL este activo")
        print("  3. Las credenciales sean correctas")
        print("\nEn Windows, verifica el servicio:")
        print("  - Abre 'Servicios' (services.msc)")
        print("  - Busca 'postgresql' y verifica que este 'En ejecucion'")
        return False
        
    except psycopg2.Error as e:
        print(f"\n[ERROR] Error de PostgreSQL: {e}")
        return False
        
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = create_database()
    if not success:
        print("\n[ERROR] El proceso fallo. Revisa los errores arriba.")
        exit(1)

