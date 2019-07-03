# ***************************************************************
# ci_utils.py - Utilities supporting continuous integration tests
# ***************************************************************
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
from __future__ import print_function
from subprocess import check_call
import sys
import os
import os.path
#
# OS detection
# ============
# This follows the `Python recommendations <https://docs.python.org/3/library/sys.html#sys.platform>`_.
is_win = sys.platform == 'win32'
is_linux = sys.platform.startswith('linux')
is_darwin = sys.platform == 'darwin'

# Copied from https://docs.python.org/3.5/library/platform.html#cross-platform.
is_64bits = sys.maxsize > 2**32
#
# Support code
# ============
# xqt
# ---
# Pronounced "execute": provides a simple way to execute a system command.
def xqt(
  # Commands to run. For example, ``'foo -param firstArg secondArg', 'bar |
  # grep alpha'``.
  *cmds,
  # Optional keyword arguments to pass on to `subprocess.check_call <https://docs.python.org/3/library/subprocess.html#subprocess.check_call>`_.
  **kwargs):

    # Although https://docs.python.org/3/library/subprocess.html#subprocess.Popen
    # states, "The only time you need to specify ``shell=True`` on Windows is
    # when the command you wish to execute is built into the shell (e.g.
    # **dir** or **copy**). You do not need ``shell=True`` to run a batch file
    # or console-based executable.", use ``shell=True`` to both allow shell
    # commands and to support simple redirection (such as ``blah > nul``,
    # instead of passing ``stdout=subprocess.DEVNULL`` to ``check_call``).
    for _ in cmds:
        # Per http://stackoverflow.com/questions/15931526/why-subprocess-stdout-to-a-file-is-written-out-of-order,
        # the ``check_call`` below will flush stdout and stderr, causing all
        # the subprocess output to appear first, followed by all the Python
        # output (such as the print statement above). So, flush the buffers to
        # avoid this.
        flush_print(_)
        # Use bash instead of sh, so that ``source`` and other bash syntax
        # works. See https://docs.python.org/3/library/subprocess.html#subprocess.Popen.
        executable = ('/bin/bash' if is_linux or is_darwin
                      else None)
        check_call(_, shell=True, executable=executable, **kwargs)
#
# pushd
# -----
# A context manager for pushd.
class pushd:
    def __init__(self,
      # The path to change to upon entering the context manager.
      path):

        self.path = path

    def __enter__(self):
        flush_print('pushd {}'.format(self.path))
        self.cwd = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, type_, value, traceback):
        flush_print('popd - returning to {}.'.format(self.cwd))
        os.chdir(self.cwd)
        return False
#
# Common tools
# ============
#
# chdir
# -----
def chdir(path):
    flush_print('cd ' + path)
    os.chdir(path)
#
# mkdir
# -----
def mkdir(path):
    flush_print('mkdir ' + path)
    os.mkdir(path)
#
# flush_print
# -----------
# Anything sent to ``print`` won't be printed until Python flushes its buffers,
# which means what CI logs report may be reflect what's actually being executed
# -- until the buffers are flushed.
def flush_print(*args, **kwargs):
    print(*args, **kwargs)
    # Flush both buffers, just in case there's something in ``stdout``.
    sys.stdout.flush()
    sys.stderr.flush()
#
# isfile
# ------
def isfile(f):
    _ = os.path.isfile(f)
    flush_print('File {} {}.'.format(f, 'exists' if _ else 'does not exist'))
    return _
#
# isfile
# ------
def isdir(f):
    _ = os.path.isdir(f)
    flush_print('Directory {} {}.'.format(f, 'exists' if _ else 'does not exist'))
    return _
