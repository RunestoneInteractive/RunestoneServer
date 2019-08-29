import sys
from .ci_utils import xqt, pushd


def tests_black_format_check():
    with pushd("../"):
        rc = xqt(
            "{} -m black --check controllers models modules tests --exclude 1.py".format(
                sys.executable
            ),
            universal_newlines=True,
        )
        print(rc.stdout + rc.stderr)
        assert rc.returncode == 0
