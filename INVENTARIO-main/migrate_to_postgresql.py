"""
Script para migrar datos de SQLite a PostgreSQL
Ejecutar: python migrate_to_postgresql.py
"""
import os
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import Config

# Configuración de SQLite (origen)
SQLITE_DB_PATH = 'instance/inventario.db'

# Configuración de PostgreSQL (destino)
POSTGRES_URI = Config.SQLALCHEMY_DATABASE_URI

def migrate_data():
    """Migra los datos de SQLite a PostgreSQL"""
    
    print("Iniciando migración de SQLite a PostgreSQL...")
    
    # Conectar a SQLite
    if not os.path.exists(SQLITE_DB_PATH):
        print(f"Error: No se encontró la base de datos SQLite en {SQLITE_DB_PATH}")
        return
    
    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()
    
    # Conectar a PostgreSQL
    try:
        postgres_engine = create_engine(POSTGRES_URI)
        postgres_conn = postgres_engine.connect()
        print("✓ Conexión a PostgreSQL establecida")
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        print("\nAsegúrate de que:")
        print("1. PostgreSQL esté instalado y corriendo")
        print("2. La base de datos 'inventario' exista")
        print("3. Las credenciales en config.py sean correctas")
        sqlite_conn.close()
        return
    
    # Lista de tablas a migrar (en orden de dependencias)
    tables = ['user', 'department', 'area', 'personnel', 'equipment', 'assignment']
    
    try:
        # Crear las tablas en PostgreSQL si no existen
        print("\nCreando tablas en PostgreSQL...")
        from app import app, db
        with app.app_context():
            db.create_all()
        print("✓ Tablas creadas/verificadas")
        
        # Migrar datos de cada tabla
        for table in tables:
            print(f"\nMigrando tabla: {table}")
            
            # Obtener datos de SQLite
            sqlite_cursor.execute(f"SELECT * FROM {table}")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                print(f"  - Tabla {table} está vacía, saltando...")
                continue
            
            # Limpiar tabla en PostgreSQL (opcional, comentar si quieres mantener datos existentes)
            # postgres_conn.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
            
            # Insertar datos en PostgreSQL
            inserted = 0
            for row in rows:
                try:
                    # Construir query de inserción
                    columns = ', '.join(row.keys())
                    placeholders = ', '.join([f':{key}' for key in row.keys()])
                    values = {key: row[key] for key in row.keys()}
                    
                    query = text(f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING")
                    postgres_conn.execute(query, values)
                    postgres_conn.commit()
                    inserted += 1
                except Exception as e:
                    print(f"  - Error al insertar fila: {e}")
                    postgres_conn.rollback()
                    continue
            
            print(f"  ✓ {inserted} registros migrados de {table}")
        
        print("\n✓ Migración completada exitosamente!")
        print(f"\nDatos migrados a: {POSTGRES_URI}")
        
    except Exception as e:
        print(f"\nError durante la migración: {e}")
        import traceback
        traceback.print_exc()
    finally:
        sqlite_conn.close()
        postgres_conn.close()
        print("\nConexiones cerradas")

if __name__ == '__main__':
    migrate_data()

