-- Script SQL para crear la base de datos de PostgreSQL
-- Ejecutar desde psql o pgAdmin:
-- psql -U postgres -f create_db.sql

-- Crear la base de datos (si no existe)
SELECT 'CREATE DATABASE inventario'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'inventario')\gexec

-- Conectar a la base de datos creada
\c inventario

-- Mensaje de confirmación
SELECT 'Base de datos inventario creada exitosamente' AS mensaje;

