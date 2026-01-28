import paramiko
import psycopg2
from sshtunnel import SSHTunnelForwarder
import sys
import time
from datetime import datetime

class ValidadorPostgresActualizado:
    def __init__(self):
        # Configuración SSH (actualizada)
        self.ssh_host = '190.168.74.199'
        self.ssh_port = 22
        self.ssh_user = 'librum'
        self.ssh_password = 't0npl4*2020'  # CLAVE ACTUALIZADA
        
        # Configuraciones PostgreSQL a probar
        self.configuraciones = [
            # Configuración 1: Mismo usuario SSH
            {
                'nombre': 'Usuario librum - misma clave',
                'postgres_user': 'librum',
                'postgres_password': 't0npl4*2020',  # misma clave SSH
                'postgres_database': 'inventario',
                'postgres_host': 'localhost',
                'postgres_port': 5432
            },
            # Configuración 2: Usuario PostgreSQL por defecto
            {
                'nombre': 'Usuario postgres - clave SSH',
                'postgres_user': 'postgres',
                'postgres_password': 't0npl4*2020',
                'postgres_database': 'inventario',
                'postgres_host': 'localhost',
                'postgres_port': 5432
            },
            # Configuración 3: Usuario postgres sin contraseña
            {
                'nombre': 'Usuario postgres sin contraseña',
                'postgres_user': 'postgres',
                'postgres_password': '',
                'postgres_database': 'inventario',
                'postgres_host': 'localhost',
                'postgres_port': 5432
            },
            # Configuración 4: Clave PostgreSQL común
            {
                'nombre': 'Clave PostgreSQL común',
                'postgres_user': 'postgres',
                'postgres_password': 'postgres',
                'postgres_database': 'inventario',
                'postgres_host': 'localhost',
                'postgres_port': 5432
            },
            # Configuración 5: Base de datos postgres por defecto
            {
                'nombre': 'Base de datos postgres',
                'postgres_user': 'postgres',
                'postgres_password': 't0npl4*2020',
                'postgres_database': 'postgres',
                'postgres_host': 'localhost',
                'postgres_port': 5432
            },
            # Configuración 6: Probando usuario librum en BD postgres
            {
                'nombre': 'Usuario librum en BD postgres',
                'postgres_user': 'librum',
                'postgres_password': 't0npl4*2020',
                'postgres_database': 'postgres',
                'postgres_host': 'localhost',
                'postgres_port': 5432
            }
        ]
        
        self.tunnel = None
        self.connection = None
    
    def crear_tunnel_ssh(self):
        """Crea un túnel SSH confiable"""
        print("=" * 60)
        print("CREANDO TÚNEL SSH")
        print("=" * 60)
        print(f"Host: {self.ssh_user}@{self.ssh_host}:{self.ssh_port}")
        print(f"Clave: {self.ssh_password}")
        
        try:
            self.tunnel = SSHTunnelForwarder(
                ssh_address_or_host=(self.ssh_host, self.ssh_port),
                ssh_username=self.ssh_user,
                ssh_password=self.ssh_password,
                remote_bind_address=('localhost', 5432),
                local_bind_address=('127.0.0.1', 0),
                set_keepalive=5,
                ssh_proxy=None
            )
            
            inicio = time.time()
            self.tunnel.start()
            tiempo = time.time() - inicio
            
            local_port = self.tunnel.local_bind_port
            print(f"✅ Túnel SSH creado exitosamente")
            print(f"   Puerto local: 127.0.0.1:{local_port}")
            print(f"   Tiempo: {tiempo:.2f} segundos")
            print("=" * 60)
            
            return local_port
            
        except Exception as e:
            print(f"❌ Error creando túnel SSH: {e}")
            print("\n⚠️  Posibles problemas:")
            print("   1. Caracteres especiales en la contraseña")
            print("   2. La contraseña contiene caracteres que necesitan escape")
            print("   3. Problemas de codificación")
            print("\n💡 Solución: Conecta manualmente primero:")
            print(f"   ssh {self.ssh_user}@{self.ssh_host}")
            return None
    
    def verificar_usuario_postgres_via_ssh(self):
        """Verifica usuarios PostgreSQL via SSH directo"""
        print("\n" + "=" * 60)
        print("VERIFICANDO USUARIOS POSTGRESQL VÍA SSH")
        print("=" * 60)
        
        ssh = None
        try:
            # Conectar via SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=self.ssh_host,
                port=self.ssh_port,
                username=self.ssh_user,
                password=self.ssh_password,
                timeout=10
            )
            
            # Comando para listar usuarios PostgreSQL
            comando = """
            sudo -u postgres psql -t -c "SELECT usename FROM pg_user WHERE usename NOT LIKE 'postgres%';"
            """
            
            stdin, stdout, stderr = ssh.exec_command(comando, timeout=5)
            usuarios = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if usuarios:
                print("📋 Usuarios PostgreSQL encontrados:")
                for usuario in usuarios.split('\n'):
                    usuario = usuario.strip()
                    if usuario:
                        print(f"   • {usuario}")
            else:
                print("ℹ️  No se pudieron obtener usuarios PostgreSQL")
            
            # Verificar si existe la base de datos 'inventario'
            print("\n🔍 Verificando base de datos 'inventario'...")
            comando_bd = """
            sudo -u postgres psql -t -c "SELECT datname FROM pg_database WHERE datname = 'inventario';"
            """
            
            stdin, stdout, stderr = ssh.exec_command(comando_bd, timeout=5)
            bd_result = stdout.read().decode().strip()
            
            if bd_result and 'inventario' in bd_result:
                print("✅ Base de datos 'inventario' encontrada")
            else:
                print("❌ Base de datos 'inventario' NO encontrada")
                print("   Listando bases de datos disponibles...")
                
                comando_all_bd = """
                sudo -u postgres psql -t -c "SELECT datname FROM pg_database WHERE datistemplate = false;"
                """
                stdin, stdout, stderr = ssh.exec_command(comando_all_bd, timeout=5)
                all_bd = stdout.read().decode().strip()
                
                if all_bd:
                    print("   Bases de datos disponibles:")
                    for bd in all_bd.split('\n'):
                        bd = bd.strip()
                        if bd:
                            print(f"   • {bd}")
            
            ssh.close()
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error verificando PostgreSQL via SSH: {e}")
            if ssh:
                ssh.close()
    
    def probar_conexion_postgres(self, config, local_port):
        """Prueba conexión a PostgreSQL con configuración específica"""
        print(f"\n🔧 Probando configuración: {config['nombre']}")
        print(f"   Usuario: {config['postgres_user']}")
        print(f"   Base de datos: {config['postgres_database']}")
        
        conn = None
        try:
            # Intentar conexión
            conn = psycopg2.connect(
                host='127.0.0.1',
                port=local_port,
                user=config['postgres_user'],
                password=config['postgres_password'],
                database=config['postgres_database'],
                connect_timeout=5
            )
            
            cursor = conn.cursor()
            
            # 1. Verificar versión
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            pg_version = version.split(',')[0]
            
            # 2. Obtener información de conexión
            cursor.execute("SELECT current_user, current_database();")
            usuario_actual, bd_actual = cursor.fetchone()
            
            # 3. Verificar tablas en la base de datos
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            num_tablas = cursor.fetchone()[0]
            
            print(f"   ✅ CONEXIÓN EXITOSA")
            print(f"      Usuario actual: {usuario_actual}")
            print(f"      Base de datos: {bd_actual}")
            print(f"      PostgreSQL: {pg_version}")
            print(f"      Tablas en esquema público: {num_tablas}")
            
            # 4. Listar algunas tablas si existen
            if num_tablas > 0:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    LIMIT 5
                """)
                tablas = cursor.fetchall()
                print(f"      Primeras tablas: {', '.join([t[0] for t in tablas])}")
            
            cursor.close()
            conn.close()
            
            return True
            
        except psycopg2.OperationalError as e:
            mensaje_error = str(e)
            print(f"   ❌ Error de conexión")
            
            if "password authentication failed" in mensaje_error:
                print(f"      Error de autenticación: usuario/clave incorrectos")
            elif "database \"" in mensaje_error and "\" does not exist" in mensaje_error:
                print(f"      La base de datos no existe")
            elif "role \"" in mensaje_error and "\" does not exist" in mensaje_error:
                print(f"      El usuario no existe")
            else:
                print(f"      {mensaje_error}")
            
            return False
            
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")
            return False
            
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    def ejecutar_pruebas_automaticas(self):
        """Ejecuta todas las pruebas automáticamente"""
        print("""
╔══════════════════════════════════════════════════════════╗
║      VALIDADOR POSTGRESQL - CLAVE ACTUALIZADA           ║
║                 t0npl4*2020                             ║
╚══════════════════════════════════════════════════════════╝
""")
        
        # Paso 1: Verificar usuarios y bases de datos via SSH
        self.verificar_usuario_postgres_via_ssh()
        
        # Paso 2: Crear túnel SSH
        local_port = self.crear_tunnel_ssh()
        if not local_port:
            print("\n❌ No se pudo crear el túnel SSH. Abortando...")
            return
        
        # Paso 3: Probar todas las configuraciones
        print("\n" + "=" * 60)
        print("PROBANDO CONFIGURACIONES POSTGRESQL")
        print("=" * 60)
        
        configuraciones_exitosas = []
        
        for config in self.configuraciones:
            exito = self.probar_conexion_postgres(config, local_port)
            if exito:
                configuraciones_exitosas.append(config)
        
        # Resumen
        print("\n" + "=" * 60)
        print("RESUMEN DE PRUEBAS")
        print("=" * 60)
        
        if configuraciones_exitosas:
            print(f"✅ {len(configuraciones_exitosas)} configuración(es) exitosa(s):")
            for config in configuraciones_exitosas:
                print(f"   • {config['nombre']}")
                print(f"     Usuario: {config['postgres_user']}")
                print(f"     Base de datos: {config['postgres_database']}")
        else:
            print("❌ Ninguna configuración funcionó")
            print("\n💡 Recomendaciones:")
            print("   1. Verifica los usuarios PostgreSQL en el servidor")
            print("   2. Crea el usuario y la base de datos si no existen")
            print("   3. Asegúrate de que el usuario tenga permisos")
        
        # Cerrar túnel
        print("\n" + "=" * 60)
        print("CERRANDO CONEXIONES")
        print("=" * 60)
        
        if self.tunnel:
            self.tunnel.stop()
            print("✅ Túnel SSH cerrado")
    
    def generar_script_conexion_final(self, config_exitosa):
        """Genera un script final con la configuración exitosa"""
        if not config_exitosa:
            return
        
        script = f'''"""
conexion_postgres_exitosa.py
Script final con configuración exitosa
Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

from sshtunnel import SSHTunnelForwarder
import psycopg2
import pandas as pd

class ConexionPostgresInventario:
    def __init__(self):
        # Configuración SSH
        self.ssh_host = '190.168.74.199'
        self.ssh_port = 22
        self.ssh_user = 'librum'
        self.ssh_password = 't0npl4*2020'
        
        # Configuración PostgreSQL exitosa
        self.pg_user = '{config_exitosa['postgres_user']}'
        self.pg_password = '{config_exitosa['postgres_password']}'
        self.pg_database = '{config_exitosa['postgres_database']}'
        self.pg_host = 'localhost'
        self.pg_port = 5432
        
        self.tunnel = None
        self.connection = None
    
    def conectar(self):
        """Establece conexión a PostgreSQL via SSH"""
        try:
            # Crear túnel SSH
            self.tunnel = SSHTunnelForwarder(
                ssh_address_or_host=(self.ssh_host, self.ssh_port),
                ssh_username=self.ssh_user,
                ssh_password=self.ssh_password,
                remote_bind_address=(self.pg_host, self.pg_port),
                local_bind_address=('127.0.0.1', 0)
            )
            
            self.tunnel.start()
            local_port = self.tunnel.local_bind_port
            print(f"✅ Túnel SSH creado en puerto: {{local_port}}")
            
            # Conectar a PostgreSQL
            self.connection = psycopg2.connect(
                host='127.0.0.1',
                port=local_port,
                user=self.pg_user,
                password=self.pg_password,
                database=self.pg_database
            )
            
            print(f"✅ Conectado a PostgreSQL: {{self.pg_database}}")
            return True
            
        except Exception as e:
            print(f"❌ Error de conexión: {{e}}")
            return False
    
    def ejecutar_consulta(self, sql, params=None):
        """Ejecuta una consulta SQL"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params or ())
            
            if sql.strip().upper().startswith('SELECT'):
                resultados = cursor.fetchall()
                columnas = [desc[0] for desc in cursor.description]
                cursor.close()
                return columnas, resultados
            else:
                self.connection.commit()
                cursor.close()
                return None
                
        except Exception as e:
            print(f"❌ Error en consulta: {{e}}")
            return None
    
    def listar_tablas(self):
        """Lista todas las tablas de la base de datos"""
        sql = """
        SELECT table_name, table_type 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
        """
        return self.ejecutar_consulta(sql)
    
    def cerrar(self):
        """Cierra la conexión"""
        if self.connection:
            self.connection.close()
        if self.tunnel:
            self.tunnel.stop()
        print("✅ Conexiones cerradas")

# Ejemplo de uso
if __name__ == "__main__":
    conexion = ConexionPostgresInventario()
    
    if conexion.conectar():
        # Listar tablas
        print("\\n📋 Tablas en la base de datos:")
        resultado = conexion.listar_tablas()
        if resultado:
            columnas, datos = resultado
            for fila in datos:
                print(f"  • {{fila[0]}} ({{fila[1]}})")
        
        # Ejemplo de consulta personalizada
        # resultado = conexion.ejecutar_consulta("SELECT * FROM mi_tabla LIMIT 5")
        
        conexion.cerrar()
'''
        
        with open('conexion_exitosa.py', 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"\n✅ Script de conexión guardado como 'conexion_exitosa.py'")


def main():
    """Función principal"""
    # Verificar dependencias
    try:
        import paramiko
        import psycopg2
        from sshtunnel import SSHTunnelForwarder
    except ImportError:
        print("❌ Faltan dependencias")
        print("   Ejecuta: pip install paramiko sshtunnel psycopg2-binary")
        sys.exit(1)
    
    # Ejecutar validador
    validador = ValidadorPostgresActualizado()
    validador.ejecutar_pruebas_automaticas()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Programa interrumpido")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")