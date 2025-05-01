#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Wait for postgres to be ready
if [ -z "${DATABASE_URL:-}" ]; then
    export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
fi

postgres_ready() {
    python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
done

echo >&2 "Postgres is up - continuing..."

# Apply database migrations
echo >&2 "Applying database migrations..."
python manage.py migrate

# Create superuser if needed
if [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    echo >&2 "Creating superuser..."
    python manage.py createsuperuser --noinput \
        --email "${DJANGO_SUPERUSER_EMAIL}" \
        || echo "Superuser already exists."
fi

exec "$@"
