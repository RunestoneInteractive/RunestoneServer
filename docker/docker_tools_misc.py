# *************************************
# |docname| - Misc CLI tools for Docker
# *************************************
# This files provides most of the subcommands for `docker_tools.py`.
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
import subprocess
from time import sleep
from typing import Optional

# Third-party
# -----------
import click

# Local application
# -----------------
from ci_utils import chdir, env, xqt


# Globals
# =======
# The name of the container running the Runestone servers.
res = subprocess.run(
    'docker ps --filter "ancestor=runestone/server"  --format "{{.Names}}"',
    shell=True,
    capture_output=True,
    text=True,
)
RUNESTONE_CONTAINER_NAME = res.stdout.strip()
SERVER_START_SUCCESS_MESSAGE = "Success! The Runestone servers are running."
SERVER_START_FAILURE_MESSAGE = "Failed to start the Runestone servers."


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
    Run the bookserver.
    """
    run_bookserver(dev)


# .. _run_bookserver:
#
# run_bookserver
# --------------
# Since click changes the way argument passing works, have a non-click version that's easily callable from Python code.
def run_bookserver(dev: bool) -> None:
    ensure_in_docker()
    xqt(
        "poetry run bookserver --root /ns "
        "--error_path /tmp "
        "--gconfig $RUNESTONE_PATH/docker/gunicorn_config/fastapi_config.py "
        # This much match the address in `../nginx/sites-available/runestone.template`.
        "--bind unix:/run/fastapi.sock " + ("--reload " if dev else "") + "&",
        cwd=env.RUNESTONE_PATH,
    )


# ``book_build``
# --------------
@click.command()
@click.argument("book_sub_name")
def book_build(book_sub_name) -> None:
    """
    Build a Runestone e-book, where BOOK_SUB_NAME provides the name of the subdirectory where a book resides.
    """
    ensure_in_docker()
    chdir(f"{env.RUNESTONE_PATH}/books/{book_sub_name}")
    xqt(
        f"{sys.executable} -m runestone build --all",
        f"{sys.executable} -m runestone deploy",
    )


# ``shell``
# ---------
@click.command()
def shell() -> None:
    """
    Open a Bash shell in the Docker container. Do not run this from the GUI -- there's no way to interact with the resulting terminal.
    """
    if in_docker():
        print("Already in Docker. Doing nothing.")
        return
    ensure_in_docker(True)
    xqt("bash")


# ``stop_servers``
# ----------------
# Shut down the web servers.
@click.command()
def stop_servers() -> None:
    """
    Shut down the web servers and celery, typically before running tests which involve the web servers.
    """
    ensure_in_docker()
    xqt(
        "pkill celery",
        "pkill nginx",
        "pkill -f gunicorn",
        check=False,
    )


# ``wait``
# --------
@click.command()
def wait() -> None:
    """
    Wait until the server is running, then report success or failure through the program's exit code.
    """
    ensure_in_docker()
    ready_file = get_ready_file()
    # Wait for success or failure.
    while True:
        txt = ready_file.read_text() if ready_file.is_file() else ""
        if txt.endswith(SERVER_START_FAILURE_MESSAGE):
            sys.exit(1)
        if txt.endswith(SERVER_START_SUCCESS_MESSAGE):
            sys.exit(0)


# Misc
# ----
# Add all subcommands in this file to the CLI.
def add_commands(cli) -> None:
    for cmd in (bookserver, book_build, shell, stop_servers, wait):
        cli.add_command(cmd)


# Determine if we're running in a Docker container.
def in_docker() -> bool:
    # This is difficult, and varies between OSes (Linux vs OS X) and Docker versions. Try a few different approaches and hope one works.
    # From a `site <https://www.baeldung.com/linux/is-process-running-inside-container>`__.
    try:
        if "docker" in Path("/proc/1/cgroup").read_text():
            return True
    except Exception:
        pass
    # Newer Docker versions create a file -- just look for that.
    if Path("/.dockerenv").is_file():
        return True
    # Try looking at the first process to see if it's ``sh``.
    return Path("/proc/1/sched").read_text().startswith("sh")


# If we're not in Docker, then re-run this command inside Docker.
def ensure_in_docker(
    # True to make this interactive (the ``-i`` flag in ``docker exec``.)
    is_interactive: bool = False,
) -> None:
    if in_docker():
        return
    if RUNESTONE_CONTAINER_NAME == "":
        click.echo("Error - Unable to find Runestone Server Container")
        sys.exit(1)

    # Some subtleties:
    #
    # #.    Single-quote each argument before passing it.
    # #.    Run it in the venv used when building Docker, since this avoids installing click globally.
    # #.    Use env vars defined in the `../Dockerfile`, rather than hard-coding paths. We want these env vars evaluated after the shell in Docker starts, not now, hence the use of ``\$`` and the surrounding double quotes.
    quoted_args = "' '".join(sys.argv[1:])
    xqt(
        f"docker exec -{'i' if is_interactive else ''}t {RUNESTONE_CONTAINER_NAME} bash -c "
        '"\$RUNESTONE_PATH/.venv/bin/python \$RUNESTONE_PATH/docker/docker_tools.py '
        f"'{quoted_args}'\""
    )
    # TODO: get a return code from the above statement and return that instead.
    sys.exit(0)


# Determine if the BookServer git repo is available, returning a Path to it if it exists, or ``None``` otherwise.
def get_bookserver_path() -> Optional[Path]:
    w2p_parent = Path(env.WEB2PY_PATH).parent
    bookserver_path = Path(f"{w2p_parent}/BookServer")
    # _`Volume detection strategy`: don't check just ``BookServer`` -- the volume may be mounted, but may not point to an actual filesystem path if the developer didn't clone the BookServer repo. Instead, look for evidence that there are actually some files in this path.
    dev_bookserver = (bookserver_path / "bookserver").is_dir()
    return bookserver_path if dev_bookserver else None


# Return the path to a file used to report the status of the container. Only for use inside Docker.
def get_ready_file() -> Path:
    return Path(env.RUNESTONE_PATH) / "ready.txt"
