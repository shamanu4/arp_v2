#!/usr/bin/env bash
#POSTGIS_SQL_PATH=`pg_config --sharedir`/contrib/postgis-1.5
POSTGIS_SQL_PATH=/usr/pgsql-9.0/share/contrib/postgis-1.5
PSQL_ADV_LIB_PATH=/usr/pgsql-9.0/lib/
PSQL_LIB_PATH=`pg_config --libdir`

cd -- "PSQL_ADV_LIB_PATH"
find -type f -exec ln --symbolic -- "$PSQL_ADV_LIB_PATH"/{} "$PSQL_LIB_PATH"/{} \;

createdb -E UTF8 template_postgis # Create the template spatial database.
createlang -d template_postgis plpgsql # Adding PLPGSQL language support.
psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"
psql -d template_postgis -f $POSTGIS_SQL_PATH/postgis.sql # Loading the PostGIS SQL routines
psql -d template_postgis -f $POSTGIS_SQL_PATH/spatial_ref_sys.sql
psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;" # Enabling users to alter spatial tables.
psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
