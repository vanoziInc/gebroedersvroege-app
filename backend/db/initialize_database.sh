#! /bin/sh
# Create databases
psql -c "CREATE DATABASE dev;"
psql -c "CREATE DATABASE test;"
psql -c "CREATE DATABASE prod;"


for file in /sql_files/*; do
    psql test -f "$file"
done