# ***********************************
# |docname| - Work around Poetry bugs
# ***********************************
# This script contains two fixes for Poetry bugs: one bug which manifests when the ``--no-dev`` flag is passed to ``poetry install/update`` and another which occurs when the ``--no-dev`` flag isn't passed.
#
#
# TODO
# ====
# - Make this a poetry plugin, so it would auto-update this on any changes to the project's ``pyproject.toml``. It looks like plugins aren't supported until v1.2.0, though.
#
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8`_.
#
# Standard library
# ----------------
import subprocess
from pathlib import Path
from typing import Set

# Third-party imports
# -------------------
import click
import toml

# Local application imports
# -------------------------
# None.
#
#
# Fix for ``dev-dependencies`` in subprojects
# ===========================================
# Given a main Poetry ``pyproject.toml``, these functions look for all subprojects included via path depdencies, creating additional subprojects namd ``projectname-dev`` in which the subproject's dev-dependencies become dependencies in the newly-created subproject. This is a workaround for Poetry's inability to install the dev dependencies for a sub project included via a path requirement. To use this, in the main project, do something like:
#
# .. code-block:: TOML
#   :number-lines:
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
    poetry_dict,
    # True to look at dependencies; False to look at dev-dependencies.
    is_deps,
    # See `project_path`.
    project_path: Path,
    # See `walked_paths_set`.
    walked_paths_set: Set[Path],
):
    key = "dependencies" if is_deps else "dev-dependencies"
    for dep in poetry_dict.get(key, {}).values():
        pth = dep.get("path", "") if isinstance(dep, dict) else None
        if pth:
            walk_pyproject(project_path / pth, walked_paths_set)


# Given a ``pyproject.toml``, optionally create a dev dependencies project and walk all requirements with path dependencies.
def walk_pyproject(
    # The path where a ``pyproject.toml`` exists.
    project_path: Path,
    # _`walked_paths_set`: a set of Paths already walked.
    walked_paths_set: Set[Path],
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
    tp = d["tool"]["poetry"]
    walk_dependencies(tp, True, project_path, walked_paths_set)
    walk_dependencies(tp, False, project_path, walked_paths_set)

    # (Usually) process this file.
    if not is_root:
        create_dev_dependencies(project_path)


# Core function: run the whole process on the ``pyproject.toml`` in the current directory.
def make_dev_pyproject():
    walk_pyproject(Path("."), set(), True)


# Fix for the main ``pyproject.toml``
# ===================================
# This function updates the ``pyproject.toml`` in the current directory by switching between a section named ``[tool.poetry.dev-dependencies]`` when in development mode or ``[tool.no-poetry.dev-dependencies]`` when not in development mode. Next, it run ``poetry update`` if a change was made, to update the ``poetry.lock`` file.
#
# Reason: sadly, Poetry v1.1.11 is broken in some important ways. Specifically, `path based dev-dependencies break 'install --no-dev' when the directory does not exist <https://github.com/python-poetry/poetry/issues/668>_. In addition, if a dependency exists both in the ``[tool.poetry.dependencies]`` and the same dependency with a path in ``[tool.poetry.dev-dependencies]`` sections, this version of Poetry will place the path in the resulting ``poetry.lock`` file even when the ``--no-dev`` option is passed, causing Poetry to install the dev version or fail if it's not available.
#
# As a workaround, this function renames the ``[tool.poetry.dependencies]``  section, effectively hiding it, for ``--no-dev`` option, and un-hides it otherwise. It then reruns ``poetry update`` if it makes a change.
def rewrite_pyproject(is_dev: bool) -> None:
    # Determine the current mode by setting ``has_dev``.
    pyproject = Path("pyproject.toml")
    pp_text = pyproject.read_text()
    must_update = False
    dev_section = "\n[tool.poetry.dev-dependencies]\n"
    no_dev_section = "\n[tool.no-poetry.dev-dependencies]\n"
    if dev_section in pp_text:
        has_dev = True
    elif no_dev_section in pp_text:
        has_dev = False
    else:
        print(f"Error: there is no [tool.(no-)poetry.dev-dependencies] section in {pyproject.resolve()}.")

    # Update accordingly.
    if is_dev and not has_dev:
        pp_text = pp_text.replace(no_dev_section, dev_section)
    elif not is_dev and has_dev:
        pp_text = pp_text.replace(dev_section, no_dev_section)
    else:
        # No update neded. We're done.
        return
    pyproject.write_text(pp_text)
    subprocess.run(f"poetry update{'' if has_dev else ' --no-dev'} --lock", check=True, shell=True)


# CLI interface
# =============
@click.command()
@click.option("--no-dev", is_flag=True, help="Prepare for running poetry install/update --no-dev.")
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
