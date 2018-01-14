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

if [ "$1" == "--help" ]; then
    echo "Options are --rebuildgrades or --skipdbinit"
    exit
fi

# To reset the unit test based on current grading code, uncomment these lines
if [ "$1" == "--rebuildgrades" ]; then
    cd ../../..
    echo "recalculating grades tables"
    python web2py.py -S runestone -M -R applications/runestone/tests/make_clean_db_with_grades.py
    echo "dumping the data"
    pg_dump runestone_test --no-owner > applications/runestone/tests/runestone_test.sql
    exit
fi

# make sure runestone_test is nice and clean

if [ "$1" != "--skipdbinit" ]; then
    dbname=`basename "$TEST_DBURL"`
    dropdb --echo --if-exists "$dbname"
    createdb --echo "$dbname"
    psql "$dbname" < runestone_test.sql
else
    echo "Skipping DB initialization"
fi

cd ../../..
# Now run
COVER_DIRS=applications/runestone/tests,applications/runestone/controllers,applications/runestone/models
coverage run --source=$COVER_DIRS web2py.py -S runestone -M -R applications/runestone/tests/test_ajax.py
coverage run --append --source=$COVER_DIRS web2py.py -S runestone -M -R applications/runestone/tests/test_dashboard.py
coverage run --append --source=$COVER_DIRS web2py.py -S runestone -M -R applications/runestone/tests/test_admin.py
coverage run --append --source=$COVER_DIRS web2py.py -S runestone -M -R applications/runestone/tests/test_assignments.py
coverage report
