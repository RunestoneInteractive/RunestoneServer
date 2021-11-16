# *****************************************************************************************
# |docname| - Create a dummy Poetry project consisting only of development dependencies.
# *****************************************************************************************
# This program takes a Poetry ``pyproject.toml`` and removes the dependencies, replacing them with the dev dependencies. This is a workaround for Poetry's inability to install the dev dependencies for a sub project included via a path requirement. So, this create a fake project named ``projectname-dev`` which has the dev dependencies as regular dependencies. To use this, in the main project, do something like:
#
# .. code-block:: TOML
#   :number-lines:
#
#   [tool.poetry.dev-dependencies]
#   sub = { path = "../sub", develop = true }
#   sub-dev = { path = "../sub-dev", develop = true }
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
from pathlib import Path
from typing import Set

# Third-party imports
# -------------------
import toml


# Local application imports
# -------------------------
# None.
#
#
# Core code
# =========
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


def main():
    walk_pyproject(Path("."), set(), True)


if __name__ == "__main__":
    main()
