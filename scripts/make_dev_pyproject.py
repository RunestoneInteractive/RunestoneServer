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
# Make this a poetry plugin, so it would auto-update this on any changes to the project's ``pyproject.toml``.


# Imports
# =======
from pathlib import Path

import click
import toml


# Core code
# =========
@click.command()
@click.argument("project_path", required=False)
def main(
    # An optional path to the project.
    project_path: str = ".",
) -> None:
    # Create a dev-only flavor.
    _project_path = Path(project_path)
    d = toml.load(_project_path / "pyproject.toml")
    tp = d["tool"]["poetry"]
    project_name = tp["name"] = tp["name"] + "-dev"
    dd = "dev-dependencies"
    tp["dependencies"] = tp.get(dd, {})
    del tp[dd]

    # Put the output in a ``project_name-dev/`` directory.
    dev = _project_path.parent / project_name
    dev.mkdir(exist_ok=True)
    (dev / "pyproject.toml").write_text(toml.dumps(d))

    # Create a minimal project to make Poetry happy.
    p = dev / project_name
    p.mkdir(exist_ok=True)
    (p / "__init__.py").write_text("")


if __name__ == "__main__":
    main()
