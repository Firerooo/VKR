#!/bin/bash
set -e

echo "Импорт дампа базы данных через pg_restore..."
pg_restore -U postgres -d rental_db /docker-entrypoint-initdb.d/rental_db.dump
