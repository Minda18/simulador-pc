#!/bin/sh
set -e

# Espera a que PostgreSQL acepte conexiones antes de aplicar migraciones.
echo "Esperando a PostgreSQL en ${DB_HOST:-db}:${DB_PORT:-5432}..."
until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${POSTGRES_USER:-simulador}" >/dev/null 2>&1; do
  sleep 1
done

echo "Aplicando migraciones..."
python manage.py migrate --noinput

exec "$@"
