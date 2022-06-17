# *************************************
# |docname| - Misc CLI tools for Docker
# *************************************
# This files provides most of the subcommands for `docker_tools.py`.
#
# If you want to add a new subcommand you must add it to the list in the add_commands
# function.  That command ensures that docker_tools.py knows about the commands added
# in docker_tools_misc.py
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
import os
import sys
import subprocess
from time import sleep
from typing import Optional, Tuple

# Third-party
# -----------
import click

# Local application
# -----------------
from ci_utils import env, xqt


# Globals
# =======
SERVER_START_SUCCESS_MESSAGE = "Success! The Runestone servers are running."
SERVER_START_FAILURE_MESSAGE = "Failed to start the Runestone servers."


# Subcommands for the CLI
# ========================
#
# ``shell``
# ---------
@click.command()
@click.option(
    "--venv/--no-venv",
    default=True,
    help="Open a shell within the Python virtual environment for the Runestone servers.",
)
def shell(venv: bool) -> None:
    """
    Open a Bash shell in the Docker container.
    """
    # Ask for an interactive console.
    ensure_in_docker(True)
    # Skip a check, since the user will see any failures and because this raises an exception of the last command in the shell produced a non-zero exit code.
    if venv:
        xqt("poetry run bash", cwd=env.RUNESTONE_PATH, check=False)
    else:
        xqt("bash", check=False)


# ``start_servers``
# -----------------
@click.command()
@click.option(
    "--dev/--no-dev",
    default=False,
    help="Run the BookServer in development mode, auto-reloading if the code changes.",
)
def start_servers(dev: bool) -> None:
    """
    Run the web servers -- nginx, web2py, and FastAPI -- used by Runestone. Before starting the server, it will stop any currently-running servers.
    """

    _start_servers(dev)


# Since click changes the way argument passing works, have a non-click version that's easily callable from Python code.
def _start_servers(dev: bool) -> None:
    ensure_in_docker()
    bs_config = os.environ.get("BOOK_SERVER_CONFIG", "production")
    if bs_config == "development":
        dev = True

    # sudo doesn't pass root's env vars; provide only the env vars Celery needs when invoking it.
    xqt(
        'sudo -u www-data env "PATH=$PATH" "REDIS_URI=$REDIS_URI" '
        "poetry run celery --app=scheduled_builder worker --pool=threads "
        "--concurrency=3 --loglevel=info &",
        cwd=f"{env.RUNESTONE_PATH}/modules",
    )

    xqt(
        "rm -f /srv/books.pid",
        "poetry run bookserver --root /ns "
        "--error_path /tmp "
        "--gconfig $RUNESTONE_PATH/docker/gunicorn_config/fastapi_config.py "
        # This much match the address in `./nginx/sites-available/runestone.template`.
        "--bind unix:/run/fastapi.sock "
        + ("--reload " if dev else "")
        + "2>&1 > /proc/1/fd/1 &",  # This redirect ensures output ends up in the docker log
        "service nginx start",
        "poetry run gunicorn -D --config $RUNESTONE_PATH/docker/gunicorn_config/web2py_config.py &",
        cwd=f"{env.RUNESTONE_PATH}/docker/gunicorn_config",
    )

    # Start the script to collect tickets and store them in the database. Most useful
    # for a production environment with several worker containers
    xqt(
        f"cp {env.RUNESTONE_PATH}/scripts/tickets2db.py {env.WEB2PY_PATH}",
        "python web2py.py -M -S runestone --run tickets2db.py &",
        cwd=f"{env.WEB2PY_PATH}",
    )


# ``stop_servers``
# ----------------
# Shut down the web servers.
@click.command()
def stop_servers() -> None:
    """
    Shut down the web servers and celery, typically before running tests which involve the web servers.
    """
    _stop_servers()


def _stop_servers() -> None:
    ensure_in_docker()
    xqt(
        "pkill celery",
        "pkill -f gunicorn",
        "pkill -f tickets2db.py",
        "nginx -s stop",
        check=False,
    )


@click.command()
@click.option(
    "--dev/--no-dev",
    default=False,
    help="Run the BookServer in development mode, auto-reloading if the code changes.",
)
def restart_servers(dev):
    """
    Restart the web servers and celery.
    """
    _stop_servers(dev)
    sleep(2)
    _start_servers()


@click.command()
def reloadbks() -> None:
    """
    Tell BookServer to reload the application.
    """
    ensure_in_docker()
    with open("/srv/books.pid") as pfile:
        pid = pfile.read().strip()

    pid = int(pid)
    os.kill(pid, 1)  # send the HUP signal to bookserver


# ``test``
# --------
@click.command()
@click.option("--bks/--no-bks", default=False, help="Run/skip tests on the BookServer.")
@click.option(
    "--rc/--no-rc", default=False, help="Run/skip tests on the Runestone components."
)
@click.option(
    "--rs/--no-rs", default=True, help="Run/skip tests on the Runestone server."
)
# Allow users to pass args directly to the underlying ``pytest`` command -- see the `click docs <https://click.palletsprojects.com/en/8.0.x/arguments/#option-like-arguments>`_.
@click.argument("passthrough", nargs=-1, type=click.UNPROCESSED)
def test(bks: bool, rc: bool, rs: bool, passthrough: Tuple) -> None:
    """
    Run unit tests.

        PASSTHROUGH: These arguments are passed directly to the underlying "pytest" command. To pass options to this command, prefix this argument with "--". For example, use "docker_tools.py test -- -k test_just_this" instead of "docker_tools.py test -k test_just_this" (which produces an error).

    """
    ensure_in_docker()
    _stop_servers()
    pytest = "$RUNESTONE_PATH/.venv/bin/pytest"
    passthrough_args = " ".join(passthrough)
    if bks:
        xqt(f"{pytest} -v {passthrough_args}", cwd="/srv/BookServer")
    if rc:
        xqt(f"{pytest} -v {passthrough_args}", cwd="/srv/RunestoneComponents")
    if rs:
        xqt(
            f"{pytest} -v applications/runestone/tests {passthrough_args}",
            cwd=env.WEB2PY_PATH,
        )


# ``wait``
# --------
# This is primarily used by tests to wait until the servers are running.
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
    for cmd in (
        shell,
        start_servers,
        stop_servers,
        test,
        wait,
        reloadbks,
        restart_servers,
    ):
        cli.add_command(cmd)


# Determine if we're running in a Docker container.
def in_docker() -> bool:
    # This is difficult, and varies between OSes (Linux vs OS X) and Docker versions. Try a few different approaches and hope one works. This was taken from a `site <https://www.baeldung.com/linux/is-process-running-inside-container>`__.
    cgroup = Path("/proc/1/cgroup")
    if cgroup.is_file() and "docker" in cgroup.read_text():
        return True
    # Newer Docker versions create a file -- just look for that.
    if Path("/.dockerenv").is_file():
        return True
    # Try looking at the first process to see if it's ``sh``.
    sched = Path("/proc/1/sched")
    if sched.is_file():
        return sched.read_text().startswith("sh")
    # We can't find any evidence of Docker. Assume it's not running.
    return False


# If we're not in Docker, then re-run this command inside Docker.
def ensure_in_docker(
    # True to make this interactive (the ``-i`` flag in ``docker exec``.)
    is_interactive: bool = False,
    # Return value: True if already in Docker; the function calls ``sys.exit(0)``, ending the program, otherwise.
) -> bool:
    if in_docker():
        return True
    # Get the name of the container running the Runestone servers.
    res = subprocess.run(
        'docker ps --filter "ancestor=runestone/server"  --format "{{.Names}}"',
        shell=True,
        capture_output=True,
        text=True,
    )
    runestone_container_name = res.stdout.strip()

    if not runestone_container_name:
        runestone_container_name = "production-runestone-1"

    # Some subtleties:
    #
    # #.    Single-quote each argument before passing it.
    # #.    Run it in the venv used when building Docker, since this avoids installing click globally.
    # #.    Use env vars defined in the `../Dockerfile`, rather than hard-coding paths. We want these env vars evaluated after the shell in Docker starts, not now, hence the use of ``\$`` and the surrounding double quotes.
    # #.    Use just the name, not the full path, of ``sys.argv[0]``, since the filesystem is different in Docker. We assume that this command will be either in the path (with the venv activated).
    exec_name = Path(sys.argv[0]).name
    quoted_args = "' '".join([exec_name] + sys.argv[1:])
    xqt(
        f"docker exec -{'i' if is_interactive else ''}t {runestone_container_name} bash -c "
        '"source \$RUNESTONE_PATH/.venv/bin/activate; '
        f"'{quoted_args}'\""
    )
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
