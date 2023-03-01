# ***********************************
# |docname| - Work around Poetry bugs
# ***********************************
# This script contains workarounds for Poetry design decisions and bugs:
#
# #.    Poetry doesn't support either/or dependencies, but this project needs them. Specifically, we want to install either the released, PyPI-published version of the RunestoneComponents and the BookServer, or the development version of these projects which are cloned to the local filesystem. The RunestoneServer ``pyproject.toml`` file therefore contains (with all other dependencies removed for clarity):
#
#       .. code-block:: text
#
#           [tool.poetry.dependencies]
#           bookserver = "^1.0.0"
#           runestone = "^6.1.0"
#
#           [tool.poetry.dev-dependencies]
#           bookserver = { path = "../BookServer", develop = true }
#           runestone = { path = "../RunestoneComponents", develop = true }
#
#       This breaks Poetry, since it looks for BOTH dependencies during dependency resolution. To work around this, `rename_pyproject <rename_pyproject>` changes this to:
#
#       .. code-block:: text
#
#           [tool.poetry.dependencies]
#           bookserver = "^1.0.0"
#           runestone = "^6.1.0"
#
#           [tool.no-poetry.dev-dependencies]   # <== CHANGED!
#           bookserver = { path = "../BookServer", develop = true }
#           runestone = { path = "../RunestoneComponents", develop = true }
#
#       ...in production mode; it does the opposite (changes ``[tool.poetry.dev-dependencies]`` to ``[tool.no-poetry.dev-dependencies]``) in development mode. This hides the modified section from Poetry, so the file now looks like an either/or project.
#
#
# TODO
# ====
# - Make this a poetry plugin, so it would auto-update this on any changes to the project's ``pyproject.toml``. It looks like plugins aren't supported until v1.2.0, though.
#
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8 <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
from pathlib import Path

# Third-party imports
# -------------------
import click


# Local application imports
# -------------------------
# None.
#
# .. _rename_pyproject:
#
# Workaround for the main ``pyproject.toml``
# ==========================================
# This function updates the ``pyproject.toml`` in the current directory by switching between a section named ``[tool.poetry.dev-dependencies]`` when in development mode or ``[tool.no-poetry.dev-dependencies]`` when not in development mode. This is because Poetry does not support either/or dependencies: either resolve dependency x in dev mode, or dependency y when not in dev mode. Instead, it takes a both/and approach: during its dependency resolution phase, it resolves ALL dependencies, then installs a subset (such all non-dev dependencies, or dev and non-dev dependencies). Quoting from the `manual <https://python-poetry.org/docs/master/managing-dependencies/>`_:
#
#   All dependencies must be compatible with each other across groups since they will be resolved regardless of whether they are required for installation or not (see Installing group dependencies).
#
#   Think of dependency groups as labels associated with your dependencies: they don’t have any bearings on whether their dependencies will be resolved and installed by default, they are simply a way to organize the dependencies logically.
#
# Therefore, `path based dev-dependencies break 'install --no-dev' when the directory does not exist <https://github.com/python-poetry/poetry/issues/668>`_. In addition, if a dependency exists both in the ``[tool.poetry.dependencies]`` and the same dependency with a path in ``[tool.poetry.dev-dependencies]`` sections, this version of Poetry will place the path in the resulting ``poetry.lock`` file even when the ``--no-dev`` option is passed, causing Poetry to install the dev version or fail if it's not available.
#
# As a workaround, this function renames the ``[tool.poetry.dependencies]``  section, effectively hiding it, for ``--no-dev`` option, and un-hides it otherwise. It then deletes ``poetry.lock`` if it makes a change, ensuring that poetry will the run ``poetry update`` with these changed dependencies.
def rewrite_pyproject(is_dev: bool) -> None:
    # Determine the current mode by setting ``has_dev``.
    pyproject = Path("pyproject.toml")
    pp_text = pyproject.read_text()
    dev_section = "\n[tool.poetry.dev-dependencies]\n"
    no_dev_section = "\n[tool.no-poetry.dev-dependencies]\n"
    if dev_section in pp_text:
        has_dev = True
    elif no_dev_section in pp_text:
        has_dev = False
    else:
        print(
            f"Error: there is no [tool.(no-)poetry.dev-dependencies] section in {pyproject.resolve()}."
        )

    # Update accordingly.
    if is_dev and not has_dev:
        pp_text = pp_text.replace(no_dev_section, dev_section)
    elif not is_dev and has_dev:
        pp_text = pp_text.replace(dev_section, no_dev_section)
    else:
        # No update needed. We're done.
        return
    pyproject.write_text(pp_text)
    # Ideally, we'd run ``poetry update`` here. However, we're blocked from doing so by circular dependencies:
    #
    # #.    In a clean install, the command ``poetry config virtualenvs.in-project true`` has not executed yet.
    # #.    Running this command will first check the dependencies in the existing ``poetry.lock`` file and report that directories such as ``../BookServer`` don't exist. (Why does Poetry do this?)
    # #.    To update ``poetry.lock``, we can run ``poetry update``.
    # #.    But ``poetry update`` will update the wrong venv, since ``poetry config virtualenvs.in-project true`` hasn't run yet.
    # #.    Go to step 1.
    #
    # So, just delete the lock file and let Poetry rebuild it; don't complain if the file's already been deleted.
    Path("poetry.lock").unlink(missing_ok=True)


# CLI interface
# =============
@click.command()
@click.option(
    "--no-dev", is_flag=True, help="Prepare for running poetry install/update --no-dev."
)
def main(no_dev: bool):
    """
    This script works around Poetry limitations to provide support of either/or dependencies.
    """
    is_dev = not no_dev
    rewrite_pyproject(is_dev)


if __name__ == "__main__":
    main()
