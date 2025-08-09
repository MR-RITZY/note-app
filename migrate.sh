#!/usr/bin/env bash
# Run Alembic migrations
alembic upgrade head

# Then start your app
exec "$@"