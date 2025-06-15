#!/bin/bash
# Helper script to run Alembic from the api directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/sql"
cd "$SCRIPT_DIR/sql"
alembic "$@"
