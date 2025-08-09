#!/usr/bin/env bash

echo "🚀 Running migrations..."
alembic upgrade head
if [ $? -ne 0 ]; then
    echo "❌ Alembic migration failed. Aborting startup."
    exit 1
fi

echo "✅ Migrations complete. Starting app..."
exec "$@"