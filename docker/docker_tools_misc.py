# *************************************
# |docname| - Misc CLI tools for Docker
# *************************************
# This is imported by `docker_tools.py`.
#
# Imports
# =======
# These are listed in the order prescribed by PEP 8, with exceptions noted below.
#
# There's a fair amount of bootstrap code here to download and install required imports and their dependencies.
#
# Standard library
# ----------------
from pathlib import Path
import sys

# Third-party
# -----------
import click

# Local application
# -----------------
from ci_utils import env, xqt


# Subcommands for the CLI
# ========================
#
# ``bookserver``
# --------------
@click.command()
@click.option(
    "--dev/--no-dev",
    default=False,
    help="Run the server in development mode, auto-reloading if the code changes.",
)
def bookserver(dev: bool) -> None:
    """
    Run the bookserver. This should only be called inside the Docker container.
    """

    run_bookserver(dev)


# Since click changes the way argument passing works, have a non-click version that's easily callable from Python code.
def run_bookserver(dev: bool) -> None:
    assert in_docker()
    w2p_parent = Path(env.WEB2PY_PATH).parent
    bookserver_path = Path(f"{w2p_parent}/BookServer")
    # See the `Volume detection strategy`_.
    dev_bookserver = (bookserver_path / "bookserver").is_dir()
    run_bookserver_kwargs = dict(cwd=bookserver_path) if dev_bookserver else {}
    run_bookserver_venv = (
        "poetry run " if dev_bookserver else f"{sys.executable} -m "
    ) + "bookserver "
    xqt(
        run_bookserver_venv + "--root /ns "
        "--error_path /tmp "
        "--gconfig /etc/gunicorn/gunicorn.conf.py "
        "--bind unix:/run/gunicorn.sock " + ("--reload " if dev else "") + "&",
        **run_bookserver_kwargs,
    )


# ``stop_servers``
# ----------------
# Shut down the web servers, typ
@click.command()
def stop_servers() -> None:
    """
    Shut down the web servers and celery, typically before running tests which involve the web servers. This should only be called inside the Docker container.
    """
    assert in_docker()
    xqt(
        "pkill celery",
        "pkill nginx",
        "pkill -9 uwsgi",
        "pkill -f gunicorn",
        check=False,
    )


# Misc
# ----
# Determine if we're running in a Docker container
def in_docker() -> bool:
    # From a `site <https://www.baeldung.com/linux/is-process-running-inside-container>`__.
    return "docker" in Path("/proc/1/cgroup").read_text()
