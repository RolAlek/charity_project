#!/bin/bash

echo "Applying Alembic migrations..."
alembic upgrade head && exec "$@"