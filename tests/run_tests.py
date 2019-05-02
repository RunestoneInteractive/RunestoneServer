import os
import sys
import argparse
import re
from shutil import rmtree, copytree
from ci_utils import xqt, pushd

COVER_DIRS = 'applications/runestone/tests,applications/runestone/controllers,applications/runestone/models'

# Assume we are running with working directory in tests

if __name__ == '__main__':
    os.environ['WEB2PY_CONFIG'] = 'test'
    # HINT: make sure that ``0.py`` has something like the following, that reads this environment variable:
    #
    # .. code:: Python
    #   :number-lines:
    #
    #   config = environ.get("WEB2PY_CONFIG","production")
    #
    #   if config == "production":
    #       settings.database_uri = environ["DBURL"]
    #   elif config == "development":
    #       settings.database_uri = environ.get("DEV_DBURL")
    #   elif config == "test":
    #       settings.database_uri = environ.get("TEST_DBURL")
    #   else:
    #       raise ValueError("unknown value for WEB2PY_CONFIG")

    # HINT: make sure that you export ``TEST_DBURL`` in your environment; it is
    # not set here because it's specific to the local setup, possibly with a
    # password, and thus can't be committed to the repo.
    assert os.environ['TEST_DBURL']

    # Extract the components of the DBURL. The expected format is ``postgresql://user:password@netloc/dbname``, a simplified form of the `connection URI <https://www.postgresql.org/docs/9.6/static/libpq-connect.html#LIBPQ-CONNSTRING>`_.
    empty1, postgres_ql, pguser, pgpassword, pgnetloc, dbname, empty2 = re.split('^postgres(ql)?://(.*):(.*)@(.*)/(.*)$', os.environ['TEST_DBURL'])
    assert (not empty1) and (not empty2)
    os.environ['PGPASSWORD'] = pgpassword
    os.environ['PGUSER'] = pguser
    os.environ['DBHOST'] = pgnetloc

    parser = argparse.ArgumentParser(description='Run tests on the Web2Py Runestone server.')
    parser.add_argument('--rebuildgrades', action='store_true',
        help='Reset the unit test based on current grading code.')
    parser.add_argument('--skipdbinit', action='store_true',
        help='Skip initialization of the test database.')
    # Per https://docs.python.org/2/library/argparse.html#partial-parsing, gather any known args. These will be passed to pytest.
    parsed_args, extra_args = parser.parse_known_args()

    if parsed_args.rebuildgrades:
        with pushd('../../..'):
            print("recalculating grades tables")
            xqt('{} web2py.py -S runestone -M -R applications/runestone/tests/make_clean_db_with_grades.py'.format(sys.executable))
            print("dumping the data")
            xqt('pg_dump --no-owner runestone_test > applications/runestone/tests/runestone_test.sql')
        sys.exit(0)

    if parsed_args.skipdbinit:
        print('Skipping DB initialization.')
    else:
        # make sure runestone_test is nice and clean.
        xqt('dropdb --echo --if-exists --host={} --user={} "{}"'.format(pgnetloc, pguser, dbname),
            'createdb --echo --host={} --user={} "{}"'.format(pgnetloc, pguser, dbname),
            'psql  --host={} --user={} "{}" < runestone_test.sql'.format(pgnetloc, pguser, dbname))
        # Copy the test book to the books directory.
        rmtree('../books/test_course_1', ignore_errors=True)
        # Sometimes this fails for no good reason on Windows. Retry.
        for retry in range(100):
            try:
                copytree('test_course_1', '../books/test_course_1')
                break
            except WindowsError:
                if retry == 99:
                    raise
        # Build the test book to add in db fields needed.
        with pushd('../books/test_course_1'):
            # The runestone build process only looks at ``DBURL``.
            os.environ['DBURL'] = os.environ['TEST_DBURL']
            xqt('{} -m runestone build --all'.format(sys.executable),
                '{} -m runestone deploy'.format(sys.executable))

    with pushd('../../..'):
        if extra_args:
            print('Passing the additional arguments {} to pytest.'.format(' '.join(extra_args)))
        # Now run tests.
        xqt('{} -m coverage erase'.format(sys.executable),
            '{} -m pytest -v applications/runestone/tests/test_server.py {}'.format(sys.executable, ' '.join(extra_args)),
            *['{} -m coverage run --append --source={} web2py.py -S runestone -M -R applications/runestone/tests/{}'.format(sys.executable, COVER_DIRS, x)
              for x in ['test_ajax.py', 'test_dashboard.py', 'test_admin.py', 'test_assignments.py']]
            )
        xqt('{} -m coverage report'.format(sys.executable))
