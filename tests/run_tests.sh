#!/bin/bash

# Assume we are running with working directory in tests

# Exit on first occurrance of an error
set -e

export WEB2PY_CONFIG=test
# HINT: make sure that 1.py has something like the following, that reads this environment variable
#if os.environ.get("WEB2PY_CONFIG", None) == "test":
#    settings.database_uri = 'postgres://dbusername:dbpassword@localhost/runestone_test'
#else:
#    settings.database_uri = 'your regular db string'

# HINT: if using postgres, set an environment variable for PGUSER so that the database drops and creates will work
# export PGUSER=dbusername

# make sure runestone_test is nice and clean

if [ "$1" != "--skipdbinit" ]; then
    dropdb --echo --if-exists runestone_test
    createdb --echo runestone_test
    psql runestone_test < runestone_test.sql
else
    echo "Skipping DB initialization"
fi

# Ascend to the main web2py directory
cd ../../../

# Now run
python web2py.py -S runestone -M -R applications/runestone/tests/test_ajax.py
