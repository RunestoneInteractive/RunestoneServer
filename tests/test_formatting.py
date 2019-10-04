import sys
import os
from .ci_utils import xqt, pushd


def tests_black_format_check(runestone_name):
    with pushd("applications/{}".format(runestone_name)):
        xqt(
            "{} -m black --check controllers models modules tests --exclude 1.py".format(
                sys.executable
            )
        )


def test_flake8_lint(runestone_name):
    with pushd("applications/{}".format(runestone_name)):
        controllers = os.listdir("controllers")
        models = os.listdir("models")
        controllers = [x for x in controllers + models if x.endswith(".py")]
        for c in controllers:
            xqt("{} -m flake8 controllers/{}".format(sys.executable, c))
