#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE DATABASE nutrition;
GRANT ALL PRIVILEGES ON DATABASE nutrition TO postgres;

EOSQL