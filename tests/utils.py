# ***********************************
# |docname| - utilities used by tests
# ***********************************

# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
# None.
#
#
# Third-party imports
# -------------------
import six
import os
from contextlib import contextmanager

# Local imports
# -------------
# None.
#
# Globals
# =======
COVER_DIRS = "applications/runestone/modules,applications/runestone/controllers,applications/runestone/models"


# Classes
# =======
# Given a dictionary, convert it to an object. For example, if ``d['one'] == 1``, then after ``do = DictToObject(d)``, ``do.one == 1``.
class DictToObject(object):
    def __init__(self, _dict):
        self.__dict__.update(_dict)


# Functions
# =========
# Import from a web2py controller. It returns a object of imported names, which also included standard web2py names (``request``, etc.). For example, ``d = web2py_controller_import('application', 'controller')`` then allows ``d.foo()``, assuming ``controller`` defined a ``foo()`` function.
def web2py_controller_import(
    # The ``runestone_env`` fixture.
    runestone_env,
    # The controller, as a string.
    controller,
):

    exec_file = "applications/{}/controllers/{}.py".format(
        runestone_env["request"].application, controller
    )
    exec(
        compile(open(exec_file, "r" if six.PY3 else "rb").read(), exec_file, "exec"),
        runestone_env,
    )
    # Note: `exec_environment <http://web2py.com/books/default/chapter/29/04/the-core#Execution-environment>`_ seems like the obvious tool. However, ``exec_environment('applications/{}/controllers/{}.py'.format(runestone_controller.request.application, controller)) fails with:
    ## >   logger = logging.getLogger(settings.logger)
    ## E   NameError: name 'settings' is not defined
    ##
    ## applications\runestone\controllers\default.py:12: NameError
    return DictToObject(runestone_env)


@contextmanager
def settings_context(settings_dict):
    try:
        # write new testsuite_settings.py into models folder
        models_fname = "applications/runestone/models/testsuite_settings.py"
        with open(models_fname, "w") as f:
            for key, value in six.iteritems(settings_dict):
                f.write("{} = {}\n".format(key, value))
        yield None
    finally:
        os.remove(models_fname)
