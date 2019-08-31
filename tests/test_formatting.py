import sys
import os
from .ci_utils import xqt, pushd


def tests_black_format_check():
    cwd = os.getcwd()
    print("CWD = ", cwd)
    if cwd.endswith("tests"):
        pd = "../"
    else:
        pd = "applications/runestone"
    with pushd(pd):
        rc = xqt(
            "{} -m black --check controllers models modules tests --exclude 1.py".format(
                sys.executable
            ),
            universal_newlines=True,
        )
        print(rc.stdout + rc.stderr)
        assert rc.returncode == 0


def test_flake8_lint():
    cwd = os.getcwd()
    print("CWD = ", cwd)
    if cwd.endswith("tests"):
        pd = "../"
    else:
        pd = "applications/runestone"
    with pushd(pd):
        controllers = os.listdir("controllers")
        models = os.listdir("models")
        controllers = [x for x in controllers + models if x.endswith(".py")]
        for c in controllers:
            print(c)
            rc = xqt(
                "{} -m flake8 controllers/{}".format(sys.executable, c),
                universal_newlines=True,
            )
            print(rc.stdout + rc.stderr)
            assert rc.returncode == 0
