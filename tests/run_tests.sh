#!/bin/bash

# Assume we are running with working directory in tests

# Exit on first occurrance of an error
set -e

export WEB2PY_CONFIG=test
export TEST_DBURL=postgres://bmiller:@localhost/runestone_test

# make sure runestone_test is nice and clean

dropdb --echo runestone_test
createdb --echo runestone_test
psql runestone_test < runestone_test.sql

# Ascend to the main web2py directory
cd ../../../

# Now run
python web2py.py -S runestone -M -R applications/runestone/tests/test_ajax.py
