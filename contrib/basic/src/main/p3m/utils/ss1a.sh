#!/bin/bash

export MEDOC_SQL_FILE='database_creation.sql'
sed -i'' -e "s/\bdb_user\b/root/g" $MEDOC_SQL_FILE
sed -i'' -e "s/\bDB_PASSWORD\b//g" $MEDOC_SQL_FILE