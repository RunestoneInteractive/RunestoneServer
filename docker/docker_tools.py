#!/usr/bin/env python3
#
# ************************************************************************
# |docname| - Tools for building and using the Runestone Servers in Docker
# ************************************************************************
# This script provides a set of Docker-related command-line tools. Run ``docker-tools --help`` for details.
#
# .. contents:: Contents
#   :local:
#
#
# Design goals
# ============
# - Bootstrap (the ``init command``): this script is designed to be downloaded then executed as a single file. In this case, bootstrap code downloads dependencies, the repo it belongs in, etc. This makes it easy to create a development or production environment from a fresh install of the host OS.
#
# - Multiple modes (the ``build command``): this script builds two distinctly different containers.
#
#   -   Single-container: these commands creates a container designed to execute on a single server. The Dockerized applications associated with it include Jobe, Redis, and Postgres. A volume is used to persist data, such as updates to the server.
#
#       -   Production mode (the default): ``docker-tool build --single`` creates a container designed for production (which includes obtaining an HTTPS certificate).
#
#       -   Development mode: ``docker-tools build --single-dev`` creates a container supporting a development mode, which provides additional tools and installs the BookServer and Runestone Components from github, instead of from releases on PyPI.
#
#   -   Multi-container: ``docker-tools build --multi`` creates a container designed for cluster operation, when many instances of this container accept requests passed on by a load balancer. In this mode, no volumes are mounted; HTTPS certificates cannot be requested, since this is the responsibility of the load balancer.
#
# - Flexible: the build process supports a number of options to customize the build. Writing in Python provides the ability to support this complexity.
#
# - Minimal: this tool only contains functions specifically related to Docker. Tools which apply more generally reside in `../rsmanage/toctree`.
#
# - No loops: unlike earlier approaches, this script doesn't cause the container to restart if something goes wrong. Instead, it catches all errors in a try/except block then stops executing so you can see what happened.
#
# - venv: all Python installs are placed in a virtual environment managed by Poetry.
#
#
# Build approach
# ==============
# To build a container, this script walks through three steps:
#
# #.    The first step occurs when this script is invoked from the terminal/command line, outside Docker. It does some preparation, then invokes the Docker build.
# #.    Next, Docker invokes this script from the `../Dockerfile`. This script installs everything it can.
# #.    Finally, Docker invokes this when the container is run. On the first run, this script completes container configuration, then runs the servers. After that, it only runs the servers, since the first-run configuration step is time-consuming.
#
# Since some files are built into the container in step 1 or run only once in step 2, simply editing a file in this repo may not update the file inside the container. Look through the source here to see which files this applies to.
#
#
# Imports and bootstrap
# =====================
# These are listed in the order prescribed by PEP 8, with exceptions noted below.
#
# There's a fair amount of bootstrap code here to download and install required imports and their dependencies.
#
# Standard library
# ----------------
import datetime
from enum import auto, Enum
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from time import sleep
from traceback import print_exc
from typing import Dict, Tuple
from textwrap import dedent

# Local application bootstrap
# ---------------------------
# Everything after this depends on Unix utilities. We can't use ``is_win`` because we don't know if ``ci_utils`` is available.
if sys.platform == "win32":
    sys.exit("ERROR: You must run this program in WSL/VirtualBox/VMWare/etc.")

# Globals
# ^^^^^^^
# True if we're root.
IS_ROOT = (
    subprocess.run(
        ["id", "-u"], capture_output=True, text=True, check=True
    ).stdout.strip()
    == "0"
)

# True if this script is running in a Python virtual environment.
IN_VENV = sys.prefix != sys.base_prefix

# The working directory of this script.
wd = Path(__file__).resolve().parent

# True if this script is executing from the Runestone repository; otherwise, we assume only this script was downloaded as a part of the bootstrap process.
IN_REPO = (wd / "nginx").is_dir()


# Supporting functions
# ^^^^^^^^^^^^^^^^^^^^
# Check to see if a program is installed; if not, install it.
def check_install(
    # The command to run to check if the program is installed.
    check_cmd: str,
    # The name of the package containing this program.
    install_package: str,
) -> None:
    print(f"Checking for '{check_cmd}'...")
    try:
        subprocess.run(check_cmd, check=True, shell=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Not found. Installing...")
        subprocess.run(
            # Only run with ``sudo`` if we're not root.
            ([] if IS_ROOT else ["sudo"])
            + [
                "apt",
                "install",
                "-y",
                "--no-install-recommends",
                install_package,
            ],
            check=True,
        )
    else:
        print("Found.")


# We need curl for some (possibly missing) imports -- make sure it's installed.
def check_install_curl() -> None:
    check_install("curl --version", "curl")


# Outside a venv, install locally.
def pip_user() -> str:
    return "" if IN_VENV else "--user"


# Bootstrap ``ci_utils``
# ^^^^^^^^^^^^^^^^^^^^^^
# Bootstrap check: if we're not in the repo, do some tidying.
if not IN_REPO:
    print("Creating directory rsdocker/ to store all Runestone files.")
    wd = wd / "rsdocker"
    wd.mkdir(exist_ok=True)
    os.chdir(wd)
    # Add this directory -- which is where the ci_utils will be downloaded -- to the path; otherwise, ci_utils won't be found.
    sys.path.append(str(wd))


sys.path.append(str(wd / "../tests"))
try:
    # This unused import triggers the script download if it's not present. This only happens outside the container.
    import ci_utils  # noqa: F401
except ImportError:
    assert not os.environ.get("IN_DOCKER")
    check_install_curl()
    print("Downloading supporting script ci_utils.py...")
    subprocess.run(
        [
            "curl",
            "-fLO",
            "https://raw.githubusercontent.com/RunestoneInteractive/RunestoneServer/master/tests/ci_utils.py",
        ],
        check=True,
    )
from ci_utils import chdir, env, is_darwin, is_linux, pushd, xqt  # noqa: E402

# Third-party bootstrap
# ---------------------
# This comes after importing ``ci_utils``, since we use that to install click if necessary.
try:
    import click
except ImportError:
    import site
    from importlib import reload

    # Ensure ``pip`` is installed before using it.
    check_install(f"{sys.executable} -m pip --version", "python3-pip")

    print("Installing Python dependencies...")
    # Outside a venv, install locally.
    user = " " if IN_VENV else "--user "
    xqt(
        f"{sys.executable} -m pip install {pip_user()} --upgrade pip",
        f"{sys.executable} -m pip install {pip_user()} --upgrade click",
    )
    # If pip is upgraded, it won't find click. `Re-load sys.path <https://stackoverflow.com/a/25384923/16038919>`_ to fix this.
    reload(site)
    import click


# Local application
# -----------------
# When bootstrapping, this import fails. This is fine, since these commands require a working container before they're usable.
try:
    from docker_tools_misc import (
        add_commands,
        get_ready_file,
        in_docker,
        SERVER_START_FAILURE_MESSAGE,
        SERVER_START_SUCCESS_MESSAGE,
        _start_servers,
    )
except ImportError:
    print("Note: this must be an initial install; additional commands missing.")


# Global variables
# ================
# Update the following versions regularly.
CHROMEDRIVER_VERSION = "103.0.5060.53"
WEB2PY_VERSION = "2.21.1"
XC16_VERSION = "xc16-v1.70-full-install-linux64-installer.run"
MPLABX_VERSION = "MPLABX-v6.00-linux-installer.tar"
# These are sometimes not the same base name (depends on the MPLABX release).
MPLABX_SH_NAME = "MPLABX-v6.00-linux-installer.sh"


# CLI
# ===
# Create a series of subcommands for this CLI.
@click.group()
def cli() -> None:
    pass


# Add the subcommands defined in `docker_tools_misc.py`, if it's available.
try:
    add_commands(cli)
except NameError:
    pass


# ``init`` command
# ================
@cli.command()
@click.option(
    "--clone-rs",
    default="RunestoneInteractive",
    nargs=1,
    metavar="<USERNAME>",
    help="Clone RunestoneServer repo with USERNAME",
)
def init(
    clone_rs: str,
) -> None:
    """
    Install prereqs needed for all other commands available in this tool.
    """
    # Did we add the current user to a group?
    did_group_add = False

    # True if running a Docker container requires use of ``sudo``.
    docker_sudo = False

    # Ensure Docker is installed.
    try:
        xqt("docker --version")
    except subprocess.CalledProcessError as e:
        print(f"Unable to run docker: {e}")
        # Ensure the Docker Desktop is running if we're running in WSL or OS X. On Windows, the ``docker`` command doesn't exist when the Docker Desktop isn't running.
        if (is_linux and "WSL" in Path("/proc/version").read_text()) or is_darwin:
            sys.exit(
                "ERROR: Docker Desktop not detected. You must install and run this\n"
                "before proceeding."
            )

        check_install_curl()
        print("Installing Docker...")
        # Use the `convenience script <https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script>`_.
        xqt(
            "curl -fsSL https://get.docker.com -o get-docker.sh",
            "sudo sh ./get-docker.sh",
            "rm get-docker.sh",
        )

    # Linux only: Ensure the user is in the ``docker`` group. This follows the `Docker docs <https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>`__. Put this step here, instead of after the Docker install, for people who manually installed Docker but skipped this step.
    if is_linux:
        print("Checking to see if the current user is in the docker group...")
        if "docker" not in xqt("groups", capture_output=True, text=True).stdout:
            # Per the `Docker docs <https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>`_, enable running Docker as a non-root user.
            #
            # Ignore errors if the groupadd fails; the group may already exist.
            xqt('sudo groupadd docker', check=False)
            xqt('sudo usermod -a -G docker $USER')

            # Until group privileges to take effect, use ``sudo`` to run Docker.
            docker_sudo = True
            # The group add doesn't take effect until the user logs out then back in. Work around it for now.
            did_group_add = True

    # Ensure the Docker Desktop is running if this is OS X. On OS X, the ``docker`` command exists, but can't run the hello, world script. It also serves as a sanity check for the other platforms.
    print("Checking that Docker works...")
    try:
        xqt(f"{'sudo' if docker_sudo else ''} docker run hello-world")
    except subprocess.CalledProcessError as e:
        sys.exit(
            f"ERROR: Unable to execute docker run hello-world: {e}"
            + (
                (
                    "\n"
                    "Docker Desktop not detected or not working. You must install and run\n"
                    "this before proceeding."
                )
                if is_darwin
                else ""
            )
        )

    # Make sure git's installed.
    try:
        xqt("git --version")
    except Exception as e:
        print(f"Unable to run git: {e} Installing...")
        xqt("sudo apt install -y --no-install-recommends git")
    # Are we inside the Runestone repo?
    if not IN_REPO:
        change_dir = True
        # No, we must be running from a downloaded script. Clone the runestone repo.
        print("Didn't find the runestone repo. Cloning...")
        try:
            # Check if possible to clone RunestoneServer with Custom Repo
            xqt(
                f"export GIT_TERMINAL_PROMPT=0 && git clone https://github.com/{clone_rs}/RunestoneServer.git"
            )
        except subprocess.CalledProcessError:
            # Exit script with Git Clone Error
            sys.exit(
                f"ERROR: Unable to clone RunestoneServer remote repository via User - {clone_rs}"
            )
        chdir("RunestoneServer")
    else:
        # Make sure we're in the root directory of the web2py repo.
        chdir(wd.parent)
        change_dir = False

    # Ensure the user is in the ``www-data`` group.
    print("Checking to see if the current user is in the www-data group...")
    if "www-data" not in xqt("groups", capture_output=True, text=True).stdout:
        if is_darwin:
            xqt(
                "sudo dscl . create /Groups/www-data",
                "sudo dscl . create /Groups/www-data gid 799",
                "sudo dseditgroup -o edit -a $USER -t user www-data",
                "sudo dscl . append /Groups/www-data GroupMembership $USER",
            )
        else:
            xqt('sudo usermod -a -G www-data $USER')
        did_group_add = True

    # Provide server-related CLIs. While installing this sooner would be great, we can't assume that the prereqs (the downloaded repo) are available.
    check_install(f"{sys.executable} -m pip --version", "python3-pip")
    xqt(
        # Note: Sometimes, OS X installs these into a place that's not in the default $PATH, making the scripts ``docker-tools`` and ``rsmanage`` not work unless the user manually adds the path. Add the ``--verbose`` flag to the install commands below to see where the scripts are placed on OS X.
        f"{sys.executable} -m pip install {pip_user()} -e docker",
        f"{sys.executable} -m pip install {pip_user()} -e rsmanage",
    )

    # Print these messages last; otherwise, it will be lost in all the build noise.
    if change_dir:
        print(
            "\n" + "*" * 80 + "\n"
            "Downloaded the RunestoneServer repo. You must \n"
            '"cd RunestoneServer" before running this script again.'
        )
    if did_group_add:
        print(
            "\n" + "*" * 80 + "\n"
            "Added the current user to the www-data and/or docker group(s).\n"
            "You must reboot for this to take effect."
        )


# ``build`` command
# =================
class BuildConfiguration(Enum):
    MULTI = auto()
    SINGLE = auto()
    SINGLE_DEV = auto()

    def is_dev(self):
        return self is self.SINGLE_DEV

    def is_single(self):
        return self in (self.SINGLE, self.SINGLE_DEV)


@cli.command()
# Allow users to pass args directly to the underlying ``docker build`` command -- see the `click docs <https://click.palletsprojects.com/en/8.0.x/arguments/#option-like-arguments>`_.
@click.argument("passthrough", nargs=-1, type=click.UNPROCESSED)
# Define the build configuration.
@click.option(
    "--multi",
    "build_config_name",
    flag_value=BuildConfiguration.MULTI.name,
    help="Build a worker image for multi-server production deployment.",
)
@click.option(
    "--single",
    "build_config_name",
    flag_value=BuildConfiguration.SINGLE.name,
    default=True,
    help="Build an image for single-server production deployment.",
)
@click.option(
    "--single-dev",
    "build_config_name",
    flag_value=BuildConfiguration.SINGLE_DEV.name,
    help="Build an image for single-server development.",
)
# Provide options for cloning from another repo.
@click.option(
    "-c",
    "--clone-all",
    nargs=1,
    metavar="<USERNAME>",
    help="Clone all System components from repos with specified USERNAME",
)
@click.option(
    "--clone-bks",
    nargs=1,
    metavar="<USERNAME>",
    help="Clone BookServer repo with USERNAME",
)
@click.option(
    "--clone-rc",
    nargs=1,
    metavar="<USERNAME>",
    help="Clone RunestoneComponents repo with USERNAME",
)
# Provide additional build options.
@click.option("--arm/--no-arm", default=False, help="Install the ARMv7 toolchain.")
@click.option(
    "--pic24/--no-pic24",
    default=False,
    help="Install tools needed for development with the PIC24/dsPIC33 family of microcontrollers.",
)
@click.option("--rust/--no-rust", default=False, help="Install the Rust toolchain.")
@click.option("--tex/--no-tex", default=False, help="Install LaTeX and related tools.")
def build(
    passthrough: Tuple,
    build_config_name: str,
    clone_all: str,
    clone_bks: str,
    clone_rc: str,
    arm: bool,
    pic24: bool,
    rust: bool,
    tex: bool,
) -> None:
    """
    When executed outside a Docker build, build a Docker container for the Runestone webservers.

        PASSTHROUGH: These arguments are passed directly to the underlying "docker build" command. To pass options to this command, prefix this argument with "--". For example, use "docker_tools.py build -- -no-cache" instead of "docker_tools.py build -no-cache" (which produces an error).

        WARNING: if the flag '-c / --clone-all' is passed an argument, then it will override any other clone flags specified.

    Inside a Docker build, install all dependencies as root.
    """

    phase = env.IN_DOCKER
    build_config = BuildConfiguration[build_config_name]
    # Phase 0 -- prepare then start the container build.
    if not phase:
        _build_phase_0(
            passthrough,
            build_config,
            clone_all,
            clone_bks,
            clone_rc,
            arm,
            pic24,
            rust,
            tex,
        )
    # Phase 1 -- build the container.
    elif phase == "1":
        _build_phase_1(build_config, arm, pic24, rust, tex)
    # Phase 2 - run the startup script for container.
    if phase == "2":
        base_ready_text = dedent(
            """\
            This file reports the status of the Docker containerized
            application.

            The container is starting up...
            """
        )
        get_ready_file().write_text(base_ready_text)
        try:
            _build_phase_2_core(build_config, arm, pic24, rust, tex)
        except Exception:
            msg = SERVER_START_FAILURE_MESSAGE
            print_exc()
        else:
            msg = SERVER_START_SUCCESS_MESSAGE
        print(msg)
        get_ready_file().write_text(base_ready_text + msg)

        # Notify listener user we're done.
        print("=-=-= Runestone setup finished =-=-=")
        # If this script exits, then Docker re-runs it. So, loop forever.
        while True:
            # Flush now, so that text won't stay hidden in Python's buffers.
            sys.stdout.flush()
            sys.stderr.flush()
            sleep(1)


# Phase 0: Prepare then start the container build
# -----------------------------------------------
def _build_phase_0(
    passthrough: Tuple,
    build_config: BuildConfiguration,
    clone_all: str,
    clone_bks: str,
    clone_rc: str,
    arm: bool,
    pic24: bool,
    rust: bool,
    tex: bool,
) -> None:
    # If the ``clone-all`` flag is set, override the other ``clone-xxx`` flags.
    if clone_all:
        click.secho(
            "Warning: Clone-all flag was initialized and will override any other clone flag specified!",
            fg="red",
        )
        # Set each individual flag to the clone-all argument
        clone_bks = clone_all
        clone_rc = clone_all

    # Create the ``docker/.env`` if it doesn't already exist. TODO: keep a dict of {file name, checksum} and save as JSON. Use this to detect if a file was hand-edited; if not, we can simply replace it.
    if not Path(".env").is_file():
        xqt("cp docker/.env.prototype .env")

    # Do the same for ``1.py``.
    one_py = Path("models/1.py")
    if not one_py.is_file():
        one_py.write_text(
            replace_vars(
                Path("models/1.py.prototype").read_text(),
                dict(BUILD_CONFIG_SINGLE=build_config.is_single()),
            )
        )

    dc = Path("docker-compose.override.yml")
    if not build_config.is_single():
        # Remove this if it exists (probably from an earlier build without ``--multi``). This file is only correct for ``--single(-dev)`` builds.
        dc.unlink(True)
    else:
        # For single-server operation, include additional services.
        # Define dev-only replacements for this file.
        d = {
            "DEV_MISC": dedent(
                """\
                # Set the base dedent; this defines column 0. The following section of the file should be indented by 2 tabs.
                        # Set up for VNC.
                        environment:
                            # I don't know how to correctly forward X11 traffic (see notes on VNC), so ignore the X11 ``DISPLAY`` outside the container.
                            DISPLAY: ":0"
                        ports:
                            # For VNC.
                            -   "5900:5900"
                            # For the CodeChat System (author toolkit)
                            -   "27377-27378:27377-27378"
                """
            )
            if build_config.is_dev()
            else "",
            "DEV_VOLUMES": dedent(
                """\
                # Set the base dedent; this defines column 0. The following section of the file should be indented by 3 tabs.
                            -   ../RunestoneComponents/:/srv/RunestoneComponents
                            -   ../BookServer/:/srv/BookServer
                            # To make Chrome happy.
                            -   /dev/shm:/dev/shm
                            -   /run/dbus/system_bus_socket:/run/dbus/system_bus_socket
                """
            )
            if build_config.is_dev()
            else "",
        }
        dc.write_text(
            replace_vars(
                dedent(
                    """\
                # WARNING: this file is automatically generated and is overwritten on each invocation of ``docker-tools build``.
                version: "3"

                services:
                    db:
                        image:
                            postgres:13
                        restart: always
                        environment:
                            POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
                            POSTGRES_USER: ${POSTGRES_USER}
                            POSTGRES_DBNAME: ${POSTGRES_DBNAME}

                    redis:
                        image: redis
                        restart: always

                    runestone:
                        ${DEV_MISC}
                        volumes:
                            # This must agree with ``$RUNESTONE_PATH`` in the `Dockerfile`. There's no easy way to share this automatically.
                            -   ./:/srv/web2py/applications/runestone
                            # For certbot, store certificates outside the (ephemeral) write layer.
                            -   ./docker/letsencrypt:/etc/letsencrypt
                            ${DEV_VOLUMES}
                        links:
                        -   db
                        -   redis
                """
                ),
                d,
            )
        )

    if build_config.is_dev():
        with pushd(".."):
            bks = Path("BookServer")
            if not bks.exists():
                print(f"Dev mode: since {bks} doesn't exist, cloning the BookServer...")
                if not clone_bks:
                    sys.exit(
                        "ERROR: in development mode, you must provide\n"
                        "either --clone-all or --clone-bks."
                    )
                try:
                    # Check if possible to clone BookServer with Custom Repo
                    xqt(
                        f"export GIT_TERMINAL_PROMPT=0 && git clone https://github.com/{clone_bks}/BookServer.git"
                    )
                except subprocess.CalledProcessError:
                    # Exit script with Git Clone Error
                    sys.exit(
                        "ERROR: Unable to clone BookServer remote repository\n"
                        f"via user {clone_bks}."
                    )
            rsc = Path("RunestoneComponents")
            if not rsc.exists():
                print(
                    f"Dev mode: since {rsc} doesn't exist, cloning the Runestone Components..."
                )
                if not clone_rc:
                    sys.exit(
                        "ERROR: in development mode, you must provide\n"
                        "either --clone-all or --clone-rc."
                    )
                try:
                    # Check if possible to clone RunestoneComponents with Custom Repo
                    xqt(
                        f"export GIT_TERMINAL_PROMPT=0 && git clone https://github.com/{clone_rc}/RunestoneComponents.git"
                    )
                except subprocess.CalledProcessError:
                    # Exit script with Git Clone Error
                    sys.exit(
                        "ERROR: Unable to clone RunestoneComponents remote\n"
                        f"repository via user {clone_rc}."
                    )

    # Run the Docker build.
    xqt(
        f'ENABLE_BUILDKIT=1 docker build -t runestone/server . --build-arg DOCKER_BUILD_ARGS="{" ".join(sys.argv[1:])}" --progress plain {" ".join(passthrough)}'
    )


# Phase 1: install Runestone dependencies
# ---------------------------------------
# This is run inside the Docker build, from the `../Dockerfile`.
def _build_phase_1(
    build_config: bool,
    arm: bool,
    pic24: bool,
    rust: bool,
    tex: bool,
):
    assert in_docker()

    # Set up apt correctly; include Postgres repo.
    xqt(
        "apt update",
        "apt install -y --no-install-recommends eatmydata lsb-release",
        """echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | tee  /etc/apt/sources.list.d/pgdg.list""",
        "wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -",
        "apt update",
    )
    apt_install = "eatmydata apt install -y --no-install-recommends"
    # This uses apt; run it after apt is set up.
    check_install_curl()

    # Install required packages
    # ^^^^^^^^^^^^^^^^^^^^^^^^^
    if build_config.is_dev():
        # Add in Chrome repo. Copied from https://tecadmin.net/setup-selenium-with-chromedriver-on-debian/.
        # Unless we are on an ARM64 processor, then we will fall back to using chromium.
        xqt(
            "curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -",
        )
        if platform.uname().machine == "x86_64":
            Path("/etc/apt/sources.list.d/google-chrome.list").write_text(
                "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main"
            )
            browser = "google-chrome-stable"
        else:
            browser = "chromium"
        # Add node.js per the `instructions <https://github.com/nodesource/distributions/blob/master/README.md#installation-instructions>`_.
        xqt(
            "curl -fsSL https://deb.nodesource.com/setup_current.x | bash -",
            "apt update",
            f"{apt_install} nodejs",
        )
    xqt(
        # All one big command! Therefore, there are no commas after each line, but instead a trailing space.
        f"{apt_install} gcc unzip "
        # For jobe's runguard.
        "sudo "
        # Some books use the `Sphinx graphviz extension <https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html>`_, which needs the ``graphviz``` binary.
        "graphviz "
        # TODO: What is this for?
        "libfreetype6-dev "
        # Required for postgres.
        "postgresql-client-13 "
        # TODO: should this only be installed in the dev image?
        "libpq-dev libxml2-dev libxslt1-dev "
        "certbot python3-certbot-nginx "
        "rsync wget nginx "
        # For use with runguard -- must call ``setfacl``.
        "acl "
        # Useful tools for debug.
        "nano less ",
    )

    # Build runguard and set up Jobe users. Needed by BookServer's ``internal/scheduled_builder.py```.
    xqt("mkdir /var/www/jobe")
    chdir("/var/www/jobe")
    xqt(
        "cp -r $RUNESTONE_PATH/docker/runguard .",
        f"{sys.executable} $RUNESTONE_PATH/docker/runguard-install.py",
    )

    if arm:
        xqt(
            # Install the ARM tools (and the QEMU emulator).
            f"{apt_install} qemu-system-arm gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential",
        )

    if build_config.is_dev():
        xqt(
            # Tests use `html5validator <https://github.com/svenkreiss/html5validator>`_, which requires the JDK.
            f"{apt_install} openjdk-11-jre-headless git xvfb x11-utils {browser} lsof emacs-nox",
            # Install Chromedriver. Based on https://tecadmin.net/setup-selenium-with-chromedriver-on-debian/.
            f"wget --no-verbose https://chromedriver.storage.googleapis.com/{CHROMEDRIVER_VERSION}/chromedriver_linux64.zip",
            "unzip chromedriver_linux64.zip",
            "rm chromedriver_linux64.zip",
            "mv chromedriver /usr/bin/chromedriver",
            "chown root:root /usr/bin/chromedriver",
            "chmod +x /usr/bin/chromedriver",
            # Provide VNC access. TODO: just pass the correct DISPLAY value and ports and use X11 locally, but how? Here's the `best info <http://wiki.ros.org/docker/Tutorials/GUI>`_ I've found. Notes on my failures:
            #
            # - Including ``network_mode: host`` in `../docker-compose.yml` works. However, this breaks everything else (port mapping, links, etc.). It suggests that the correct networking setup would make this work.
            # - Passing ``volume: - /tmp/.X11-unix:/tmp/.X11-unix`` has no effect (on a Ubuntu 20.03.4 LTS host). Per the previous point, it seems that X11 is using TCP as its transport.
            # - Mapping X11 ports via ``ports: - "6000-6063:6000-6063"`` doesn't work.
            # - Setting ``DISPLAY`` to various values (from the host's ``hostname -I``, or various names to route to the host) doesn't work.
            #
            # Install a VNC server plus a simple window manager.
            f"{apt_install} x11vnc icewm",
        )

    if pic24:
        # When changing the xc16 version, update the string below **and** the path added at the end of this block.
        xqt(
            # Install the xc16 compiler.
            f"eatmydata wget --no-verbose https://ww1.microchip.com/downloads/en/DeviceDoc/{XC16_VERSION}",
            f"chmod a+x {XC16_VERSION}",
            # The installer complains if the netserver name isn't specified. This option isn't documented in the ``--help``. So, supply junk, and it seems to work.
            f"eatmydata ./{XC16_VERSION} --mode unattended --netservername foo",
            f"rm {XC16_VERSION}",
            # MPLAB X install
            #
            # Needed to run sim30: per https://unix.stackexchange.com/questions/486806/steam-missing-32-bit-libraries-libx11-6, enable 32-bit libs.
            "eatmydata dpkg --add-architecture i386",
            "eatmydata apt update",
            "eatmydata apt install -y lib32stdc++6 libc6:i386",
            # Then download and install MPLAB X.
            f'eatmydata wget --no-verbose "https://ww1.microchip.com/downloads/en/DeviceDoc/{MPLABX_VERSION}"',
            f'eatmydata tar -xf "{MPLABX_VERSION}"',
            f'rm "{MPLABX_VERSION}"',
            # Install just the IDE and the 16-bit tools. This program checks to see if this is being run by root by looking at the ``USER`` env var, which Docker doesn't set. Fake it out.
            f'USER=root eatmydata "./{MPLABX_SH_NAME}" -- --mode unattended --ipe 0 --8bitmcu 0 --32bitmcu 0 --othermcu 0',
            f'rm "{MPLABX_SH_NAME}"',
        )
        # Add the path to the xc16 tools. Note that ``/root/.bashrc`` doesn't get sourced when Docker starts up; therefore, the `../Dockerfile` invokes bash when running the startup script.
        with open("/root/.bashrc", "a", encoding="utf-8") as f:
            f.write("\nexport PATH=$PATH:/opt/microchip/xc16/v1.70/bin\n")
        # Just symlink mdb, since that's the only tool we use.
        xqt(
            "ln -sf /opt/microchip/mplabx/v5.50/mplab_platform/bin/mdb.sh /usr/local/bin/mdb"
        )

        # Microchip tools (mdb) needs write access to these directories.
        mchp_packs = "/var/www/.mchp_packs"
        java = "/var/www/.java"
        for path in (mchp_packs, java):
            xqt(f"mkdir {path}", f"eatmydata chown www-data:www-data {path}")

    if tex:
        xqt(f"{apt_install} texlive-full xsltproc pdf2svg")

    if rust:
        xqt(f"{apt_install} cargo")

    # Install web2py and Poetry
    # ^^^^^^^^^^^^^^^^^^^^^^^^^
    xqt(
        "mkdir -p $WEB2PY_PATH",
        # Make the www-data the owner and place its files in the www-data group. This is because web2py needs to write to this directory tree (log, errors, etc.).
        "eatmydata chown www-data:www-data $WEB2PY_PATH",
        # Make any newly created directories have the www-group. Give the group write permission.
        "eatmydata chmod g+ws $WEB2PY_PATH",
    )
    w2p_parent = Path(env.WEB2PY_PATH).parent
    xqt(
        f"eatmydata wget --no-verbose https://mdipierro.pythonanywhere.com/examples/static/{WEB2PY_VERSION}/web2py_src.zip",
        "eatmydata unzip -q web2py_src.zip",
        "rm -f web2py_src.zip",
        cwd=w2p_parent,
    )

    chdir(env.RUNESTONE_PATH)
    xqt(
        # Clean up after web2py install.
        "rm -rf $WEB2PY_PATH/.cache/*",
        "cp scripts/routes.py $WEB2PY_PATH/routes.py",
        # `Install Poetry <https://python-poetry.org/docs/master/#installing-with-the-official-installer>`_, putting it in a location already in ``$PATH``.
        "eatmydata curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python3 -",
    )

    # Set up config files
    # ^^^^^^^^^^^^^^^^^^^
    xqt(
        "mkdir -p $WEB2PY_PATH/logs",
        "cp $RUNESTONE_PATH/docker/wsgihandler.py $WEB2PY_PATH/wsgihandler.py",
        # Set up nginx (partially -- more in step 3 below).
        "rm /etc/nginx/sites-enabled/default",
        "ln -sf $RUNESTONE_PATH/docker/nginx/sites-available/runestone /etc/nginx/sites-enabled/runestone",
        # Send celery, gunicorn, and nginx logs to Docker's stdout/stderr, so they'll show up in Docker logs even after restarting the servers. (Linking to ``/dev/stdout`` and ``/dev/stderr`` means that on restart, these links point not to Docker, but to the console which invoked the restart). See a `related issue on Github <https://github.com/moby/moby/issues/19616#issuecomment-174355979>`_.
        "ln -sf /proc/1/fd/1 /var/log/nginx/access.log",
        "ln -sf /proc/1/fd/2 /var/log/nginx/error.log",
        "mkdir -p /var/log/celery",
        "ln -sf /proc/1/fd/1 /var/log/celery/access.log",
        "ln -sf /proc/1/fd/2 /var/log/celery/error.log",
        "mkdir -p /var/log/gunicorn",
        "ln -sf /proc/1/fd/1 /var/log/gunicorn/access.log",
        "ln -sf /proc/1/fd/2 /var/log/gunicorn/error.log",
        # Set up web2py routing.
        "cp $RUNESTONE_PATH/docker/routes.py $WEB2PY_PATH",
        # ``sphinxcontrib.paverutils.run_sphinx`` lacks venv support -- it doesn't use ``sys.executable``, so it doesn't find ``sphinx-build`` in the system path when executing ``/srv/venv/bin/runestone`` directly, instead of activating the venv first (where it does work). As a huge, ugly hack, symlink it to make it available in the system path.
        "ln -sf $RUNESTONE_PATH/.venv/bin/sphinx-build /usr/local/bin",
        # Deal with a different subdirectory layout inside the container (mandated by web2py) and outside the container by adding these symlinks.
        "ln -sf $BOOK_SERVER_PATH $WEB2PY_PATH/applications/BookServer",
        # We can't use ``$BOOK_SERVER_PATH`` here, since we need ``/srv/bookserver-dev`` in lowercase, not CamelCase.
        "ln -sf /srv/bookserver-dev $WEB2PY_PATH/applications/bookserver-dev",
        "ln -sf /srv/RunestoneComponents $WEB2PY_PATH/applications/RunestoneComponents",
        "ln -sf /srv/runestone-dev $WEB2PY_PATH/applications/runestone-dev",
    )

    # Record info about this build. We can't provide ``git`` info, since the repo isn't available (the ``${RUNSTONE_PATH}.git`` directory is hidden, so it's not present at this time). Likewise, volumes aren't mapped, so ``git`` info for the Runestone Components and BookServer isn't available.
    Path("/srv/build_info.txt").write_text(
        f"Built on {datetime.datetime.now(datetime.timezone.utc)} using arguments {env.DOCKER_BUILD_ARGS}.\n"
    )

    xqt(
        # Do any final updates.
        "eatmydata sudo apt -y update",
        "eatmydata sudo apt -y upgrade",
        # Clean up after install.
        "eatmydata sudo apt -y autoclean",
        "eatmydata sudo apt -y autoremove",
        "rm -rf /tmp/* /var/tmp/*",
    )

    if build_config.is_single():
        # Remove all the files from the local repo, since they will be replaced by the volume. This must be the last step, since it deletes the script as well.
        xqt("rm -rf $RUNESTONE_PATH")
    else:
        # For the multi-container build, there's no volume. Install everything that must be saved to disk.
        run_poetry(build_config.is_dev())


# Phase 2 core: Final installs / run servers
# ------------------------------------------
def _build_phase_2_core(
    build_config: bool,
    arm: bool,
    pic24: bool,
    rust: bool,
    tex: bool,
):
    # Check the environment.
    assert env.POSTGRES_PASSWORD, "Please export POSTGRES_PASSWORD."
    assert env.RUNESTONE_HOST, "Please export RUNESTONE_HOST."

    # Install all required Python packages, then switch to this venv. The multi-container build already did the installs.
    if build_config.is_single():
        run_poetry(build_config.is_dev())
    activate_this_path = f"{env.RUNESTONE_PATH}/.venv/bin/activate_this.py"
    exec(open(activate_this_path).read(), {"__file__": activate_this_path})

    w2p_parent = Path(env.WEB2PY_PATH).parent

    # Misc setup
    # ^^^^^^^^^^
    if build_config.is_dev():
        # Since I don't know how to forard the X11 ``$DISPLAY`` correctly (see notes on VNC access), run a virtual frame buffer in the container and provide access via VNC. TODO: only do this if the provided ``$DISPLAY`` is not set.
        xqt(
            # Sometimes, previous runs leave this file behind, which causes Xvfb to output ``Fatal server error: Server is already active for display 0. If this server is no longer running, remove /tmp/.X0-lock and start again.``
            f"rm -f /tmp/.X{env.DISPLAY.split(':', 1)[1]}-lock",
            "Xvfb &",
            # Wait a bit for Xvfb to start up before running the following X applications.
            "sleep 1",
            "x11vnc -forever &",
            "icewm-session &",
        )

    # nginx config
    # ^^^^^^^^^^^^
    # Overwrite the nginx config file unless there is certbot data to preserve. This helps to prevent old builds from leaving behind incorrect config files.
    has_cert = Path(f"/etc/letsencrypt/live/{env.RUNESTONE_HOST}").is_dir()
    # A cert should only be preserved if there's a cert e-mail address and an existing cert file for that e-mail address. Overwrite the file otherwise.
    overwrite = not (env.CERTBOT_EMAIL and has_cert)
    # _`Set up nginx based on env vars.` See `nginx/sites-available/runestone.template`.
    nginx_conf = Path(f"{env.RUNESTONE_PATH}/docker/nginx/sites-available/runestone")
    # Since certbot (if enabled) edits this file, avoid overwriting it.
    if overwrite or not nginx_conf.is_file():
        nginx_conf_template = nginx_conf.with_suffix(".template")
        txt = replace_vars(
            nginx_conf_template.read_text(),
            dict(RUNESTONE_HOST=env.RUNESTONE_HOST, WEB2PY_PATH=env.WEB2PY_PATH),
        )
        nginx_conf.write_text(txt)

    # web2py config
    # ^^^^^^^^^^^^^
    # Create a default auth key for web2py.
    print("Creating auth key")
    xqt("mkdir -p $RUNESTONE_PATH/private")

    (Path(env.RUNESTONE_PATH) / "private/auth.key").write_text(env.WEB2PY_SALT)
    # Write the ads.txt file
    (Path(env.RUNESTONE_PATH) / "static/ads.txt").write_text(env.ADS_FILE)
    # Write the admin password.
    xqt(
        dedent(
            f"""\
            {sys.executable} -c \\
            "from gluon.main import save_password
            save_password(
                '$WEB2PY_ADMIN_PASSWORD',
                {'443' if env.CERTBOT_EMAIL else '80'}
            )"
            """
        ),
        cwd=env.WEB2PY_PATH,
    )
    # Set up admin interface access.
    admin_1_py = Path(f"{env.WEB2PY_PATH}/applications/admin/models/1.py")
    if env.CERTBOT_EMAIL:
        # This isn't needed when HTTPS is available.
        admin_1_py.unlink(True)
    else:
        # Allow admin access in HTTP mode only.
        # Change to False otherwise this allows admin on build --multi
        admin_1_py.write_text("DEMO_MODE = False")

    # Do dev installs
    # ^^^^^^^^^^^^^^^
    rsc = Path(f"{w2p_parent}/RunestoneComponents")
    if build_config.is_dev():
        chdir(rsc)
        # Build the webpack after the Runestone Components are installed.
        xqt("npm install", "npm run build")

    xqt(
        f"chgrp www-data {Path(env.RUNESTONE_PATH)}",
        f"chmod g+w {Path(env.RUNESTONE_PATH)}",
    )

    for folder in ["databases", "errors", "modules", "build"]:
        # web2py needs write access to databases, errors, modules, build
        tmp_path = Path(env.RUNESTONE_PATH) / folder
        if tmp_path.exists():
            xqt(
                f"chgrp -R www-data {tmp_path}",
                f"chmod -R g+w {tmp_path}",
            )
        else:
            print(f"Cannot set permissions for {tmp_path}")

    # Set up Postgres database
    # ^^^^^^^^^^^^^^^^^^^^^^^^
    # Wait until Postgres is ready using `pg_isready <https://www.postgresql.org/docs/current/app-pg-isready.html>`_. Note that its ``--timeout`` parameter applies only when it's waiting for a response from the Postgres server, not to the time spent retrying a refused connection.
    print("Waiting for Postgres to start...")
    if env.WEB2PY_CONFIG == "production":
        effective_dburl = env.DBURL
    elif env.WEB2PY_CONFIG == "test":
        effective_dburl = env.TEST_DBURL
    else:
        effective_dburl = env.DEV_DBURL
    for junk in range(5):
        try:
            xqt(f'pg_isready --dbname="{effective_dburl}"')
            break
        except Exception:
            sleep(1)
    else:
        assert False, "Postgres not available."

    print("Creating database if necessary...")
    try:
        xqt(f"psql {effective_dburl} -c ''")
    except Exception:
        # The expected format of a DBURL is ``postgresql://user:password@netloc/dbname``, a simplified form of the `connection URI <https://www.postgresql.org/docs/9.6/static/libpq-connect.html#LIBPQ-CONNSTRING>`_.
        junk, dbname = effective_dburl.rsplit("/", 1)
        xqt(
            f"PGPASSWORD=$POSTGRES_PASSWORD PGUSER=$POSTGRES_USER PGHOST=db createdb {dbname}"
        )

    print("Checking the State of Database and Migration Info")
    p = xqt(f"psql {effective_dburl} -c '\\d'", capture_output=True, text=True)
    if p.stderr == "Did not find any relations.\n":
        # Remove any existing web2py migration data, since this is out of date and confuses web2py (an empty db, but migration files claiming it's populated). TODO: rsmanage should do this eventually; it doesn't right now.
        xqt("rm -f $RUNESTONE_PATH/databases/*")
        print("Populating database...")
        xqt("rsmanage initdb --force", cwd=env.WEB2PY_PATH)
        xqt("alembic stamp head", cwd=env.BOOK_SERVER_PATH)
    else:
        print("Database already populated.")
        # TODO: any checking to see if the db is healthy? Perhaps run Alembic autogenerate to see if it wants to do anything?

    # Start the servers
    # ^^^^^^^^^^^^^^^^^
    print("Starting web servers.")
    _start_servers(build_config.is_dev())

    # cerbot
    # ^^^^^^
    # Certbot requires nginx to be running to succeed, hence its placement here.
    if env.CERTBOT_EMAIL:
        # See if there's already a certificate for this host. If not, get one.
        if not has_cert:
            xqt(
                'certbot -n --agree-tos --email "$CERTBOT_EMAIL" --nginx --redirect -d "$RUNESTONE_HOST"'
            )
        else:
            # Renew the certificate in case it's near its expiration date. Per the `certbot docs <https://certbot.eff.org/docs/using.html#renewing-certificates>`_, ``renew`` supports automated use, renewing only when a certificate is near expiration.
            xqt("certbot renew")
        print("You should be good for https")
    else:
        print("CERTBOT_EMAIL not set will not attempt certbot setup -- NO https!!")


# Utilities
# =========
# A utility to replace all instances of ``${var_name}`` in  a string, where the variables are provided in ``vars_``. This is an alternative to the build-in ``str.format()`` which doesn't require escaping all the curly braces.
def replace_vars(str_: str, vars_: Dict[str, str]) -> str:
    def repl(matchobj: re.Match):
        var_name = matchobj.group(1)
        return (
            # Perform a replacement if the ``var_name`` is in ``vars_``.
            str(vars_[var_name])
            if var_name in vars_
            # Otherwise, perform no replacement.
            else matchobj.group(0)
        )

    # Search for a ``${var_name}``.
    pattern = r"\${(\w+)}"
    return re.sub(pattern, repl, str_)


# Run Poetry and associated tools.
def run_poetry(is_dev: bool):
    no_dev_arg = "" if is_dev else " --no-dev"
    xqt(
        # Update dependencies. See `scripts/poetry_fix.py`. This must come before Poetry, since it will check for the existence of the project created by these commands. (Even calling ``poetry config`` will perform this check!)
        f"{sys.executable} -m pip install --user toml",
        f"{sys.executable} runestone_poetry_project/poetry_fix.py{no_dev_arg}",
        # By default, Poetry creates a venv in the home directory of the current user (root). However, this isn't accessible when running as ``www-data``. So, tell it to create the venv in a `subdirectory of the project <https://python-poetry.org/docs/configuration/#virtualenvsin-project>`_ instead, which is accessible and at a known location (``./.venv``).
        "poetry config virtualenvs.in-project true",
        f"poetry install{no_dev_arg}",
        cwd=env.RUNESTONE_PATH,
    )


if __name__ == "__main__":
    cli()
