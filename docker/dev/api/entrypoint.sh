#!/bin/sh
set -e

alembic -c /app/alembic.ini upgrade head

python /app/scripts/create_short_link_partitions.py --ahead 2

exec uvicorn main.server.index:app --host 0.0.0.0 --port 8000 --workers 6
