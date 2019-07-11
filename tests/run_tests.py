# ***********************
# |docname| - Test runner
# ***********************
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
import os
import sys
import argparse
import re
from shutil import rmtree, copytree

# Third-party imports
# -------------------
# None.
#
#
# Local imports
# -------------
from ci_utils import xqt, pushd
from utils import COVER_DIRS


# main
# ====
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
    parser.add_argument('--skipdbinit', action='store_true',
        help='Skip initialization of the test database.')
    parser.add_argument('--runold', action='store_true',
        help='Force old tests to run ')

    # Per https://docs.python.org/2/library/argparse.html#partial-parsing, gather any known args. These will be passed to pytest.
    parsed_args, extra_args = parser.parse_known_args()

    if parsed_args.skipdbinit:
        print('Skipping DB initialization.')
    else:
        # Make sure runestone_test is nice and clean -- this will remove many
        # tables that web2py will then re-create.
        xqt('rsmanage --verbose initdb --reset --force')

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
        #xqt('rsmanage addcourse --course-name=test_course_1 --basecourse=test_course_1')
        with pushd('../books/test_course_1'):
            # The runestone build process only looks at ``DBURL``.
            os.environ['DBURL'] = os.environ['TEST_DBURL']
            xqt('{} -m runestone build --all'.format(sys.executable),
                '{} -m runestone deploy'.format(sys.executable))


    with pushd('../../..'):
        if extra_args:
            print(extra_args)
            print('Passing the additional arguments {} to pytest.'.format(' '.join(extra_args)))
        # Now run tests.
        test_files = ["test_server.py", "test_admin.py", "test_dashboard.py", "test_ajax2.py", "test_designer.py", "test_autograder.py"]
        testf_string = " ".join(['applications/runestone/tests/{}'.format(i) for i in test_files])
        xqt('{} -m coverage erase'.format(sys.executable),
            '{} -m pytest -v {} {}'.format(sys.executable, testf_string, ' '.join(extra_args)),
            '{} -m coverage report'.format(sys.executable)
        )
