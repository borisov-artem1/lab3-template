#!/usr/bin/env bash
set -e

# TODO для создания баз прописать свой вариант
export VARIANT="v4"
export SCRIPT_PATH=/docker-entrypoint-initdb.d/
export PGPASSWORD=password
psql -f "$SCRIPT_PATH/sql/db-$VARIANT.sql"
psql -f "$SCRIPT_PATH/sql/db/all.sql"
