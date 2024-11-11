#!/bin/bash
# Esperar a que la base de datos esté lista
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Ejecutar migraciones
alembic upgrade head

# Iniciar la aplicación
uvicorn app.main:app --host 0.0.0.0 --port 8000
