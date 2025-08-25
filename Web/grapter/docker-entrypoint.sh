#!/bin/sh
set -e

DB_PATH=${DB_PATH:-/app/data/app.db}
mkdir -p "$(dirname "$DB_PATH")"

if [ ! -f "$DB_PATH" ]; then
  echo "[entrypoint] No DB found at $DB_PATH, seeding initial data..."
  python -m src.seed || true
else
  echo "[entrypoint] DB exists at $DB_PATH, skipping seed"
fi

exec "$@"

