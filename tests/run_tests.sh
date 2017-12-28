#!/bin/bash

# Assume we are running with working directory in tests

# Exit on first occurrance of an error
set -e

export WEB2PY_CONFIG=test
# HINT: make sure that 1.py has something like the following, that reads this environment variable
#config = environ.get("WEB2PY_CONFIG","production")
#
#if config == "production":
#    settings.database_uri = environ["DBURL"]
#elif config == "development":
#    settings.database_uri = environ.get("DEV_DBURL")
#elif config == "test":
#    settings.database_uri = environ.get("TEST_DBURL")
#else:
#    raise ValueError("unknown value for WEB2PY_CONFIG")

# HINT: make sure that you export TEST_DBURL in your environment; not set here because it's specific to local
# setup, possibly with a password, and thus can't be committed to the repo.

# HINT: if using postgres, set an environment variable for PGUSER so that the database drops and creates will work
# export PGUSER=<dbusername>

# Ascend to the main web2py directory
cd ../../../

# To reset the unit test based on current grading code, uncomment these lines
# python web2py.py -S runestone -M -R applications/runestone/tests/make_clean_db_with_grades.py
# pg_dump runestone_test > runestone_test.sql

# make sure runestone_test is nice and clean

if [ "$1" != "--skipdbinit" ]; then
    dropdb --echo --if-exists runestone_test
    createdb --echo runestone_test
    psql runestone_test < runestone_test.sql
else
    echo "Skipping DB initialization"
fi

# Now run
python web2py.py -S runestone -M -R applications/runestone/tests/test_ajax.py
python web2py.py -S runestone -M -R applications/runestone/tests/test_assignments.py
