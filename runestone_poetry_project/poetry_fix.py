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
#       ...in production mode; it does the opposite (changes ``[tool.poetry.dependencies]`` to ``[tool.no-poetry.dependencies]``) in development mode. This hides the modified section from Poetry, so the file now looks like an either/or project.
#
# #.    Poetry doesn't install development dependencies in projects included through a `path dependency <https://python-poetry.org/docs/dependency-specification/#path-dependencies>`_. As a workaround, this script copies development dependencies from a project into an otherwise empty, auto-created "project", but puts them in the production dependencies section of this newly-created "project", so they will be installed. For example, the BookServer ``pyproject.toml`` contains:
#
#       .. code-block:: text
#
#           [tool.poetry.dev-dependencies]
#           black = "~= 22.0"
#           console-ctrl = "^0.1.0"
#           ...many more, which are omitted for clarity...
#
#       Poetry won't install these. Therefore, `make_dev_pyproject <make_dev_pyproject>` creates a "project" named bookserver-dev whose ``pyproject.toml`` contains a copy of the BookServer development dependencies, but placed in the production dependencies section of this ``bookserver-dev`` "project", so they will be installed. For example, the bookserver-dev ``pyproject.toml`` contains:
#
#       .. code-block:: text
#
#           [tool.poetry.dependencies]   # <== CHANGED!
#           black = "~= 22.0"
#           console-ctrl = "^0.1.0"
#           ...many more, which are omitted for clarity...
#
#       This also means that the RunestoneServer ``pyproject.toml`` file must be manually edited to include a reference to this "project":
#
#       .. code-block:: text
#
#           [tool.poetry.dev-dependencies]
#           bookserver = { path = "../BookServer", develop = true }
#           bookserver-dev = { path = "../bookserver-dev", develop = true }  # <== MANUALLY ADDED!
#
#       The final result looks like this:
#
#       .. image:: poetry_fix_diagram.png
#
# #.    Poetry generates invalid package metadata for local path dependencies, so that running ``pip show click`` results in a bunch of exceptions. This program doesn't provide a fix for this bug.
#
# ...and that's how using Poetry makes dependency management easier...
#
#
# `Invalid package METADATA <https://github.com/python-poetry/poetry/issues/3148>`_
# =====================================================================================
# Per the issue linked in the title above, Poetry generates invalid package metadata for local path dependencies (tested on Poetry v1.1.14). For example, the last few lines of ``.venv/lib/python3.8/site-packages/runestone_poetry_project-0.1.0.dist-info/METADATA`` contain:
#
# .. code-block:: text
#
#   Requires-Dist: pytz (>=2016.6.1)
#   Requires-Dist: requests (>=2.10.0)
#   Requires-Dist: rsmanage @ rsmanage
#   Requires-Dist: runestone
#   Requires-Dist: runestone-docker-tools @ docker
#   Requires-Dist: six (>=1.10.0)
#   Requires-Dist: sphinxcontrib-paverutils (>=1.17)
#   Requires-Dist: stripe (>=2.0.0,<3.0.0)
#
# This causes an exception when running a command such as ``pip show click``:
#
# .. code-block:: text
#
#   ERROR: Exception:
#   Traceback (most recent call last):
#     File "/srv/web2py/applications/runestone/.venv/lib/python3.8/site-packages/pip/_vendor/pkg_resources/__init__.py", line 3021, in _dep_map
#       return self.__dep_map
#     File "/srv/web2py/applications/runestone/.venv/lib/python3.8/site-packages/pip/_vendor/pkg_resources/__init__.py", line 2815, in __getattr__
#       raise AttributeError(attr)
#   AttributeError: _DistInfoDistribution__dep_map
#
# ... along with a long traceback of other chained exceptions.
#
# Fixing the ``METADATA`` file to be:
#
# .. code-block:: text
#
#   Requires-Dist: pytz (>=2016.6.1)
#   Requires-Dist: requests (>=2.10.0)
#   Requires-Dist: rsmanage @ file://rsmanage
#   Requires-Dist: runestone
#   Requires-Dist: runestone-docker-tools @ file://docker
#   Requires-Dist: six (>=1.10.0)
#   Requires-Dist: sphinxcontrib-paverutils (>=1.17)
#   Requires-Dist: stripe (>=2.0.0,<3.0.0)
#
# ... along with a similar fix to the ``METADATA`` for ``bookserver_dev`` allows ``pip`` to run successfully.
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
import sys
from typing import Any, Dict, Set

# Third-party imports
# -------------------
import click
import toml


# Local application imports
# -------------------------
# None.
#
# Fix for ``dev-dependencies`` in subprojects
# ===========================================
# Given a main Poetry ``pyproject.toml``, these functions look for all subprojects included via path dependencies, creating additional subprojects named ``projectname-dev`` in which the subproject's dev-dependencies become dependencies in the newly-created subproject. This is a workaround for Poetry's inability to install the dev dependencies for a sub project included via a path requirement. To use this, in the main project, do something like:
#
# .. code-block:: TOML
#   :linenos:
#
#   [tool.poetry.dev-dependencies]
#   sub = { path = "../sub", develop = true }
#   sub-dev = { path = "../sub-dev", develop = true }
#
# Create a project clone where the original project's dev-dependencies are dependencies in the clone.
def create_dev_dependencies(
    # The path to the project.
    project_path: Path,
) -> None:
    # Create a dev-only flavor.
    d = toml.load(project_path / "pyproject.toml")
    tp = d["tool"]["poetry"]
    dd = "dev-dependencies"
    # If there are no dev-dependencies, there's nothing to do. Otherwise, move them to dependencies.
    if dd not in tp:
        return
    tp["dependencies"] = tp.pop(dd)
    # Update the project name.
    project_name = tp["name"] = tp["name"] + "-dev"
    # We don't have a readme -- if it exists, Poetry will complain about the missing file it references. Remove it if it exists.
    tp.pop("readme", None)

    # Put the output in a ``project_name-dev/`` directory.
    dev = project_path.parent / project_name
    print(f"Creating {dev}...")
    dev.mkdir(exist_ok=True)
    (dev / "pyproject.toml").write_text(toml.dumps(d))

    # Create a minimal project to make Poetry happy.
    project_name = project_name.replace("-", "_")
    p = dev / project_name
    p.mkdir(exist_ok=True)
    (p / "__init__.py").write_text("")


def walk_dependencies(
    # A dict of Poetry-specific values.
    poetry_dict: Dict[str, Any],
    # True to look at dependencies; False to look at dev-dependencies.
    is_deps: bool,
    # See `project_path`.
    project_path: Path,
    # See `walked_paths_set`.
    walked_paths_set: Set[Path],
    # See `poetry_paths_set`.
    poetry_paths_set: Set[Path],
):
    key = "dependencies" if is_deps else "dev-dependencies"
    for dep in poetry_dict.get(key, {}).values():
        pth = dep.get("path", "") if isinstance(dep, dict) else None
        if pth:
            walk_pyproject(project_path / pth, walked_paths_set, poetry_paths_set)


# Given a ``pyproject.toml``, optionally create a dev dependencies project and walk all requirements with path dependencies.
def walk_pyproject(
    # The path where a ``pyproject.toml`` exists.
    project_path: Path,
    # _`walked_paths_set`: a set of Paths already walked.
    walked_paths_set: Set[Path],
    # _`poetry_paths_set`: a set of Paths that contained a Poetry project. This is a strict subset of walked_paths_set_.
    poetry_paths_set: Set[Path],
    # True if this is the root ``pyproject.toml`` file -- no dev dependencies will be created for it.
    is_root: bool = False,
):
    project_path = project_path.resolve()
    # Avoid cycles and unnecessary work.
    if project_path in walked_paths_set:
        return
    walked_paths_set.add(project_path)
    print(f"Examining {project_path} ...")

    # Process dependencies, if this is a Poetry project.
    try:
        d = toml.load(project_path / "pyproject.toml")
    except FileNotFoundError:
        return
    poetry_paths_set.add(project_path)
    tp = d["tool"]["poetry"]
    # Search both the dependencies and dev dependencies in this project for path dependencies.
    walk_dependencies(tp, True, project_path, walked_paths_set, poetry_paths_set)
    walk_dependencies(tp, False, project_path, walked_paths_set, poetry_paths_set)

    # (Usually) process this file.
    if not is_root:
        create_dev_dependencies(project_path)


# .. _make_dev_pyproject:
#
# Core function: run the whole process on the ``pyproject.toml`` in the current directory.
def make_dev_pyproject():
    project_paths_set = set()
    walk_pyproject(Path("."), set(), project_paths_set, True)

    # Check that we processed the BookServer and the RunestoneComponents.
    found_bookserver = False
    found_runestone_components = False
    for path in project_paths_set:
        name = path.name
        found_bookserver |= name == "BookServer"
        found_runestone_components |= name == "RunestoneComponents"
    if not found_bookserver:
        sys.exit("Error: did not process the BookServer Poetry project.")
    if not found_runestone_components:
        sys.exit("Error: did not process the RunestoneComponents Poetry project.")


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
    This script works around Poetry bugs related to path dependencies.
    """
    is_dev = not no_dev
    rewrite_pyproject(is_dev)
    if is_dev:
        make_dev_pyproject()


if __name__ == "__main__":
    main()
