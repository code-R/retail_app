#!/bin/bash

set -ex
export HOME=/tmp

pgsql_superuser_cmd () {
  DB_COMMAND="$1"

  psql \
  -U ${DB_ADMIN_USER} \
  -d ${ADMIN_DB} \
  -h ${DB_FQDN} \
  -c "${DB_COMMAND}"
}

# Drop database if present
pgsql_superuser_cmd "DROP DATABASE IF EXISTS $DB_NAME;"

# Create database if present
pgsql_superuser_cmd "CREATE DATABASE $DB_NAME;"

# Remove db user if present
pgsql_superuser_cmd "DROP ROLE IF EXISTS $DB_SERVICE_USER;"

# Create db user
pgsql_superuser_cmd "CREATE ROLE ${DB_SERVICE_USER} LOGIN PASSWORD '$DB_SERVICE_PASSWORD';"

# Grant permissions to user
pgsql_superuser_cmd "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME to $DB_SERVICE_USER;"

# Run migrations
alembic upgrade head
