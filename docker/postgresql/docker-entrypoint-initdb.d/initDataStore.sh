#!/bin/bash

set -e

psql -U "$POSTGRES_USER" <<-EOSQL

	CREATE ROLE datastore_default NOSUPERUSER NOCREATEDB NOCREATEROLE LOGIN PASSWORD '333';
	CREATE DATABASE datastore_default OWNER ckan_default ENCODING 'utf-8';
	GRANT ALL PRIVILEGES ON DATABASE datastore_default TO ckan_default;
	


EOSQL


