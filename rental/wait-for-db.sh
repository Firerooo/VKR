#!/bin/bash
# wait-for-db.sh
set -e

DB_HOST=$1
shift

echo "Waiting for Postgres at ${DB_HOST}:5432..."
while ! nc -z "$DB_HOST" 5432; do
  sleep 1
done
echo "Postgres is up."

exec "$@"
