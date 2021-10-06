#!/usr/bin/env python3
#
# ******************************************************************
# |docname| - Create a Docker container for the Runestone webservers
# ******************************************************************
# This script provides a user-friendly install process for creating a multi-container Docker application running the Runestone system. It's planned to contain all Docker-related command-line scripts.
#
#
# Build approach
# ==============
# To build a container, this script walks through three steps:
#
# #.    The first step occurs when this script is invoked from the terminal/command line, outside Docker. It does some preparation, then invokes the Docker build.
# #.    Next, Docker invokes this script from the ``../Dockerfile``. This script installs everything it can.
# #.    Finally, Docker invokes this when the container is run. On the first run, this script completes container configuration, then runs the servers. After that, it only runs the servers, since the first-run configuration step is time-consuming.
#
# Since some files are built into the container in step 1 or run only once in step 2, simply editing a file in this repo may not update the file inside the container. Look through the source here to see which files this applies to.
#
# No loops
# --------
# Unlike earlier approaches, this script doesn't cause the container to restart if something goes wrong. Instead, it catches all errors in a try/except block then stops executing so you can see what happened.
#
#
# venvs
# =====
# All Python installs are placed in a virtual environment -- ``/root/venv`` and also (for dev builds) in a venv managed by Poetry. Before running Python scripts, be sure to activate the relevant venv.
#
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
import re
import subprocess
import sys
from time import sleep
from traceback import print_exc
from typing import Dict, Tuple
from textwrap import dedent

# Local application
# -----------------
# Everything after this depends on Unix utilities.
if sys.platform == "win32":
    print("Run this program in WSL/VirtualBox/VMWare/etc.")
    #sys.exit()


# We need curl for some (possibly missing) imports -- make sure it's installed.
def get_curl():
    print("Checking for curl...")
    try:
        subprocess.run(["curl", "--version"], check=True)
    except:
        print("Installing curl...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "curl"], check=True)
    else:
        print("Curl found.")

# The working directory of this script.
wd = Path(__file__).resolve().parent
sys.path.append(str(wd / "../tests"))
try:
    # This unused import triggers the script download if it's not present.
    import ci_utils
except ImportError:
    get_curl()
    print("Downloading supporting script ci_utils.py...")
    subprocess.run([
        "curl",
        "-fsSLO",
        "https://raw.githubusercontent.com/RunestoneInteractive/RunestoneServer/master/tests/ci_utils.py",
    ], check=True)
from ci_utils import chdir, env, mkdir, xqt

# Third-party
# -----------
# This comes after importing ``ci_utils``, since we use that to install click if necessary.
in_venv = sys.prefix != sys.base_prefix
try:
    import click
except ImportError:
    print("Installing click...")
    # Outside a venv, install locally.
    user = '' if in_venv else '--user'
    xqt(
        f"{sys.executable} -m pip install {user} --upgrade pip",
        f"{sys.executable} -m pip install {user} --upgrade click",
    )
    # If pip is upgraded, it won't find click. `Re-load sys.path <https://stackoverflow.com/a/25384923/16038919>`_ to fix this.
    import site
    from importlib import reload
    reload(site)
    import click


# CLI interface
# =============
@click.group()
def cli():
    pass


# ``build`` command
# =================
@cli.command()
# Allow users to pass args directly to the underlying ``docker build`` command -- see the `click docs <https://click.palletsprojects.com/en/8.0.x/arguments/#option-like-arguments>`_.
@click.argument("passthrough", nargs=-1, type=click.UNPROCESSED)
@click.option("--arm/--no-arm", default=False, help="Install the ARMv7 toolchain.")
@click.option("--dev/--no-dev", default=False, help="Install tools needed for development with the Runestone.")
@click.option("--pic24/--no-pic24", default=False, help="Install tools needed for development with the PIC24/dsPIC33 family of microcontrollers.")
@click.option("--rust/--no-rust", default=False, help="Install the Rust toolchain.")
@click.option("--tex/--no-tex", default=False, help="Instal LaTeX and related tools.")
def build(arm: bool, dev: bool, passthrough: Tuple, pic24: bool, tex: bool, rust: bool):
    """
    When executed outside a Docker build, build a Docker container for the Runestone webservers.

        PASSTHROUGH: These arguments are passed directly to the underlying "docker build" command. To pass options to this command, prefix this argument with "--". For example, use "docker_tools.py build -- -no-cache" instead of "docker_tools.py build -no-cache" (which produces an error).

    Inside a Docker build, install all dependencies as root.
    """

    # Are we inside the Docker build?
    phase = env.IN_DOCKER
    if not phase:
        # No -- this is the first step in the install.
        #
# Step 1: prepare to run the Docker build
# ---------------------------------------
        # Did we add the current user to a group?
        did_group_add = False
        # Do we need to use ``sudo`` to execute Docker?
        docker_sudo = False
        # Check to make sure Docker is installed.
        try:
            xqt("docker --version")
        except subprocess.CalledProcessError as e:
            get_curl()
            print(f"Unable to run docker: {e} Installing Docker...")
            # Use the `convenience script <https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script>`_.
            xqt(
                "curl -fsSL https://get.docker.com -o get-docker.sh",
                "sudo sh ./get-docker.sh",
                "rm get-docker.sh",
                # This follows the `Docker docs <https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>`__.`
                "sudo usermod -aG docker ${USER}",
            )
            # The group add doesn't take effect until the user logs out then back in. Work around it for now.
            did_group_add = True
            docker_sudo = True

        # ...and docker-compose.
        try:
            xqt("docker-compose --version")
        except subprocess.CalledProcessError as e:
            print("Unable to run docker-compose: {e} Installing...")
            # This is from the `docker-compose install instructions <https://docs.docker.com/compose/install/#install-compose-on-linux-systems>`_.
            xqt(
                'sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose',
                "sudo chmod +x /usr/local/bin/docker-compose",
            )

        # Are we inside the Runestone repo?
        if not (wd / "uwsgi").is_dir():
            change_dir = True
            # No, we must be running from a downloaded script. Clone the runestone repo.
            try:
                xqt("git --version")
            except Exception as e:
                print(f"Unable to run git: {e} Installing...")
                xqt("sudo apt-get install -y git")
            print("Didn't find the runestone repo. Cloning...")
            # Make this in a path that can eventually include web2py.
            mkdir("web2py/applications", parents=True)
            chdir("web2py/applications")
            xqt("git clone https://github.com/RunestoneInteractive/RunestoneServer.git runestone")
            chdir("runestone")
        else:
            # Make sure we're in the root directory of the web2py repo.
            chdir(wd.parent)
            change_dir = False

        # Make sure the ``docker/.env`` file exists.
        if not Path(".env").is_file():
            xqt("cp docker/.env.prototype .env")

        # Do the same for ``1.py``.
        one_py = Path("models/1.py")
        if not one_py.is_file():
            # add a new setting so that institutions can run using a base book like thinkcspy as their course.  On Runestone.academy we don't let anyone be an instructor for the base courses because they are open to anyone.  This makes for a much less complicated deployment strategy for an institution that just wants to run their own server and use one or two books.
            one_py.write_text(dedent("""
                settings.docker_institution_mode = True
                settings.jobe_key = ''
                settings.jobe_server = 'http://jobe'
                settings.bks = "ns"
                settings.python_interpreter = "/srv/venv/bin/python3"
                # This must match the secret in the BookServer's ``config.py`` ``settings.secret``.
                settings.secret = "supersecret"
            """))

        # For development, include extra volumes.
        dc = Path("docker-compose.override.yml")
        if dev and not dc.is_file():
            dc.write_text(dedent("""
                version: "3"

                services:
                runestone:
                    volumes:
                    - ../../../RunestoneComponents/:/srv/RunestoneComponents
                    - ../../../BookServer/:/srv/BookServer
            """))

        # Ensure the user is in the ``www-data`` group.
        print("Checking to see if the current user is in the www-data group...")
        if "www-data" not in xqt("groups", capture_output=True, text=True).stdout:
            xqt('sudo usermod -a -G www-data "$USER"')
            did_group_add = True

        # Run the Docker build.
        xqt(f'ENABLE_BUILDKIT=1 {"sudo" if docker_sudo else ""} docker build -t runestone/server . --build-arg DOCKER_BUILD_ARGS="{" ".join(sys.argv[1:])}" --progress plain {" ".join(passthrough)}')

        # Print thesse messages last; otherwise, it will be lost in all the build noise.
        if change_dir:
            print('\nDownloaded the RunestoneServer repo. You must "cd web2py/applications/runestone" before running this script again.')
        if did_group_add:
            print('\nAdded the current user to the www-data and/or docker group(s). You must log out and log back in for this to take effect, or run "su -s ${USER}".')
        return

    # Step 3 - startup script for container.
    if phase == "2":
        try:
            _build_phase2(arm, dev, pic24, tex, rust)
            print("Success! The Runestone servers are running.")
        except Exception:
            print(f"Failed to start the Runestone servers:")
            print_exc()

# Notify listener (see `cli-up`) we're done
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        print("=-=-= Runestone setup finished =-=-=")
        sys.stdout.flush()
        sys.stderr.flush()
        # If this script exits, then Docker re-runs it. So, loop forever.
        while True:
            sleep(1000)

# Step 2: install Runestone dependencies
# ---------------------------------------
    # This is run inside the Docker build, from the `Dockerfile`.
    assert phase == "1", f"Unknown value of IN_DOCKER={phase}"

    # It should always be `run in a venv <https://stackoverflow.com/a/1883251/16038919>`_.
    assert in_venv, "This should be running in a Python virtual environment."

# Install required packages
# ^^^^^^^^^^^^^^^^^^^^^^^^^
    # Add in Chrome repo. Copied from https://tecadmin.net/setup-selenium-with-chromedriver-on-debian/.
    xqt(
        "curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -",
    )
    Path("/etc/apt/sources.list.d/google-chrome.list").write_text("deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main")
    # Add node.js per the `instructions <https://github.com/nodesource/distributions/blob/master/README.md#installation-instructions>`_.
    xqt("curl -fsSL https://deb.nodesource.com/setup_current.x | bash -")
    xqt(
        "apt-get update",
        "apt-get install -y eatmydata",

        # All one big command! Therefore, there are no commas after each line, but instead a trailing space.
        "eatmydata apt-get install -y --no-install-recommends "
            "gcc unzip "
            # For jobe's runguard.
            "sudo "
            # Some books use the `Sphinx graphviz extension <https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html>`_, which needs the ``graphviz``` binary.
            "graphviz "
            # TODO: What is this for?
            "libfreetype6-dev "
            "postgresql-client "
            # Just installing ``nodejs`` fails with messages about unmet dependencies. Adding ``yarn`` (which is never used) makes it happy. Solution from `SO <https://stackoverflow.com/a/67329755/16038919>`__.
            "nodejs yarn "
            # TODO: should this only be installed in the dev image?
            "libpq-dev libxml2-dev libxslt1-dev "
            "certbot python-certbot-nginx "
            "rsync wget nginx "
            # Useful tools for debug.
            "nano less "
    )

    # Build runguard and set up jobe users.
    xqt("mkdir /var/www/jobe")
    chdir("/var/www/jobe")
    xqt(
        "cp -r $RUNESTONE_PATH/docker/runguard .",
        f"{sys.executable} $RUNESTONE_PATH/docker/runguard-install.py",
    )

    if arm:
        xqt(
            # Get the ``add-apt-repository`` tool.
            "eatmydata apt-get install -y software-properties-common",
            # Use it to add repo for the ARM tools.
            "eatmydata add-apt-repository -y ppa:canonical-server/server-backports",
            # Then install the ARM tools (and the QEMU emulator).
            "eatmydata apt-get install -y qemu-system-arm gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential",
        )

    if dev:
        xqt(
            # Tests use `html5validator <https://github.com/svenkreiss/html5validator>`_, which requires the JDK.
            "eatmydata apt-get install -y --no-install-recommends openjdk-11-jre-headless git xvfb x11-utils google-chrome-stable lsof emacs-nox",
            # Install Chromedriver. Based on https://tecadmin.net/setup-selenium-with-chromedriver-on-debian/.
            "wget --no-verbose https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_linux64.zip",
            "unzip chromedriver_linux64.zip",
            "rm chromedriver_linux64.zip",
            "mv chromedriver /usr/bin/chromedriver",
            "chown root:root /usr/bin/chromedriver",
            "chmod +x /usr/bin/chromedriver",
        )

    if pic24:
        # When changing the xc16 version, update the string below **and** the path added at the end of this block.
        xc16_ver = "xc16-v1.70-full-install-linux64-installer.run"
        mplabx_ver = "MPLABX-v5.50(1)-linux-installer.tar"
        mplabx_sh = "MPLABX-v5.50-linux-installer.sh"
        xqt(
            # Install the xc16 compiler.
            f"eatmydata wget --no-verbose https://ww1.microchip.com/downloads/en/DeviceDoc/{xc16_ver}",
            f"chmod a+x {xc16_ver}",
            # The installer complains if the netserver name isn't specified. This option isn't documented in the ``--help``. So, supply junk, and it seems to work.
            f"eatmydata ./{xc16_ver} --mode unattended --netservername foo",
            f"rm {xc16_ver}",
            # MPLAB X install
            #
            # No longer required: per https://unix.stackexchange.com/questions/486806/steam-missing-32-bit-libraries-libx11-6, enable 32-bit libs.
            #"eatmydata dpkg --add-architecture i386",
            #"eatmydata apt-get update",
            # No longer required: per https://microchipdeveloper.com/install:mplabx-lin64, install prereqs. The xc16 compiler is 32-bit.
            #"eatmydata apt-get install -y lib32stdc++6 libc6:i386 libx11-6:i386 libxext6:i386 libstdc++6:i386 libexpat1:i386",
            # Then download and install MPLAB X.
            f'eatmydata wget --no-verbose "https://ww1.microchip.com/downloads/en/DeviceDoc/{mplabx_ver}"',
            f'eatmydata tar -xf "{mplabx_ver}"',
            f'rm "{mplabx_ver}"',
            # Install just the IDE and the 16-bit tools. This program check to see if this is being run by root by looking at the ``USER`` env var, which Docker doesn't set. Fake it out.
            f'USER=root eatmydata "./{mplabx_sh}" -- --mode unattended --ipe 0 --8bitmcu 0 --32bitmcu 0 --othermcu 0',
            f'rm "{mplabx_sh}"',
        )
        # Add the path to the xc16 tools.
        with open("/root/.bashrc", "a", encoding="utf-8") as f:
            f.write(dedent("""
                export PATH=$PATH:/opt/microchip/xc16/v1.70/bin
            """))
        # Just symlink mdb, since that's the only tool we use.
        xqt(
            "ln -sf /opt/microchip/mplabx/v5.50/mplab_platform/bin/mdb.sh /usr/local/bin/mdb",
        )

        # Microchip tools (mdb) needs write access to these directories.
        mchp_packs = "/var/www/.mchp_packs"
        java = "/var/www/.java"
        for path in (mchp_packs, java):
            xqt(
                f"mkdir {path}",
                f"chown www-data:www-data {path}",
        )

    if tex:
        xqt("eatmydata apt-get install -y texlive-full xsltproc pdf2svg")

    if rust:
        xqt("eatmydata apt-get install -y cargo")

# Python/pip-related installs
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Install web2py
    xqt(
        "mkdir -p $WEB2PY_PATH",
        # Make the www-data the owner and place its files in the www-data group. This is because web2py needs to write to this directory tree (log, errors, etc.).
        "chown www-data:www-data $WEB2PY_PATH",
        # Make any newly created directories have the www-group. Give the group write permission.
        "chmod g+ws $WEB2PY_PATH",
    )
    w2p_parent = Path(env.WEB2PY_PATH).parent
    xqt(
        # Install additional components
        "eatmydata wget --no-verbose https://mdipierro.pythonanywhere.com/examples/static/web2py_src.zip",
        "eatmydata unzip -q web2py_src.zip",
        "rm -f web2py_src.zip",
        cwd=w2p_parent,
    )

    # Wheel helps several other packages (uwsgi, etc.) build more cleanly. Otherwise, we get ``Using legacy 'setup.py install' for uwsgi, since package 'wheel' is not installed.``
    xqt(f"eatmydata {sys.executable} -m pip install --upgrade wheel")

    chdir(env.RUNESTONE_PATH)
    if dev:
        # The dev requirements include the main requirements file as well.
        xqt(f"eatmydata {sys.executable} -m pip install -r requirements-dev.txt")
        # For development purposes, `install Poetry <https://python-poetry.org/docs/master/#osx--linux--bashonwindows-install-instructions>`_.
        xqt("curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/usr/local python -")
    else:
        xqt(f"eatmydata {sys.executable} -m pip install -r requirements.txt")

    xqt(
        f"eatmydata {sys.executable} -m pip install uwsgi uwsgitop bookserver myst-parser sphinx-reredirects",
        "rm -rf $WEB2PY_PATH/.cache/*",
        "cp scripts/routes.py $WEB2PY_PATH/routes.py",
    )

# Set up config files
# ^^^^^^^^^^^^^^^^^^^
    xqt(
        # Set up for uwsgi
        "mkdir -p $WEB2PY_PATH/logs",
        "mkdir -p /run/uwsgi",
        "mkdir -p /etc/uwsgi/sites",
        "cp $RUNESTONE_PATH/docker/uwsgi/sites/runestone.ini /etc/uwsgi/sites/runestone.ini",
        # TODO: is this ever used?
        "cp $RUNESTONE_PATH/docker/systemd/system/uwsgi.service /etc/systemd/system/uwsgi.service",
        "ln -sf /etc/systemd/system/uwsgi.service /etc/systemd/system/multi-user.target.wants/uwsgi.service",
        "cp $RUNESTONE_PATH/docker/wsgihandler.py $WEB2PY_PATH/wsgihandler.py",
        # Set up nginx (partially -- more in step 3 below).
        "rm /etc/nginx/sites-enabled/default",
        # Send nginx logs to stdout/stderr, so they'll show up in Docker logs.
        "ln -sf /dev/stdout /var/log/nginx/access.log",
        "ln -sf /dev/stderr /var/log/nginx/error.log",
        # Set up gunicorn
        "mkdir -p /etc/gunicorn",
        "cp $RUNESTONE_PATH/docker/gunicorn/gunicorn.conf.py /etc/gunicorn",
        # Set up web2py routing.
        "cp $RUNESTONE_PATH/docker/routes.py $WEB2PY_PATH",
        # ``sphinxcontrib.paverutils.run_sphinx`` lacks venv support -- it doesn't use ``sys.executable``, so it doesn't find ``sphinx-build`` in the system path when executing ``/srv/venv/bin/runestone`` directly, instead of activating the venv first (where it does work). As a huge, ugly hack, symlink it to make it available in the system path.
        "ln -sf /srv/venv/bin/sphinx-build /usr/local/bin",
    )

    # Clean up after install.
    xqt("rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*")
    # Remove all the files from the local repo, since they will be replaced by the volume. This must be the last step, since it deletes the script as well.
    xqt("rm -rf $RUNESTONE_PATH")


# Step 3: Final installs / run servers
# ------------------------------------
def _build_phase2(arm: bool, dev: bool, pic24: bool, tex: bool, rust: bool):
    # Check the environment.
    assert env.POSTGRES_PASSWORD, "Please export POSTGRES_PASSWORD."
    assert env.RUNESTONE_HOST, "Please export RUNESTONE_HOST."

    # This should always be `run in a venv`_.
    assert sys.prefix != sys.base_prefix, "This should be running in a Python virtual environment."

    w2p_parent = Path(env.WEB2PY_PATH).parent
    bookserver_path = Path(f"{w2p_parent}/BookServer")
    # _`Volume detection strategy`: don't check just ``BookServer`` -- the volume may be mounted, but may not point to an actual filesystem path if the developer didn't clone the BookServer repo. Instead, look for evidence that there are actually some files in this path.
    dev_bookserver = (bookserver_path / '/bookserver').is_dir()
    run_bookserver_kwargs = dict(cwd=bookserver_path) if dev_bookserver else {}

    # Use a marker to run final install steps. These depend on volumes mounted/env vars/other containers that are only availabe when the container is run, so they can't be performed in the previous phase.
    stamp = Path("/root/initialized.stamp")
    if stamp.is_file():
        print(f"Skipping one-time initialization (install dev directories, init db, etc.) To re-run this, delete the file {stamp} then re-run this.")
    else:
        xqt(
            f"{sys.executable} -m pip install -e $RUNESTONE_PATH/rsmanage",
        )

        print("Creating auth key")
        if not Path(f"{env.RUNESTONE_PATH}/private").is_dir():
            xqt("mkdir $RUNESTONE_PATH/private")
        (Path(env.RUNESTONE_PATH) / "private/auth.key").write_text("sha512:16492eda-ba33-48d4-8748-98d9bbdf8d33")

        print("Creating pgpass file")
        Path("/root/.pgpass").write_text(f"db:5432:*:{env.POSTGRES_USER}:{env.POSTGRES_PASSWORD}")
        xqt("chmod 600 /root/.pgpass")

        # _`Set up nginx based on env vars.` See `nginx/sites-available/runestone`.
        nginx_conf = Path(f"{env.RUNESTONE_PATH}/docker/nginx/sites-available/runestone")
        txt = replace_vars(nginx_conf.read_text(), dict(
            RUNESTONE_HOST=env.RUNESTONE_HOST,
            WEB2PY_PATH=env.WEB2PY_PATH,
            LISTEN_PORT=443 if env.CERTBOT_EMAIL else 80,
            PRODUCTION_ONLY=dedent("""
                # `server (http) <http://nginx.org/en/docs/http/ngx_http_core_module.html#server>`_: set configuration for a virtual server. This server closes the connection if there's no host match to prevent host spoofing.
                server {
                    # `listen (http) <http://nginx.org/en/docs/http/ngx_http_core_module.html#listen>`_: Set the ``address`` and ``port`` for IP, or the ``path`` for a UNIX-domain socket on which the server will accept requests.
                    #
                    # I think that omitting the server_name_ directive causes this to match any host name not otherwise matched. TODO: does the use of ``default_server`` play into this? What is the purpose of ``default_server``?
                    listen 80 default_server;
                    # Also look for HTTPS connections.
                    listen 443 default_server;
                    # `return <https://nginx.org/en/docs/http/ngx_http_rewrite_module.html#return>`_: define a rewritten URL for the client. The non-standard code 444 closes a connection without sending a response header.
                    return 444;
                }
            """) if env.WEB2PY_CONFIG == "production" else "",
            FORWARD_HTTP=dedent("""
                # Redirect from http to https. Copied from an `nginx blog <https://www.nginx.com/blog/creating-nginx-rewrite-rules/#https>`_.
                server {
                    listen 80;
                    server_name ${RUNESTONE_HOST};
                    return 301 https://${RUNESTONE_HOST}$request_uri;
                }
            """) if env.CERTBOT_EMAIL else "",
        ))
        Path("/etc/nginx/sites-available/runestone").write_text(txt)
        xqt(
            "ln -sf /etc/nginx/sites-available/runestone /etc/nginx/sites-enabled/runestone",
        )

        if env.CERTBOT_EMAIL:
            xqt('certbot -n  --agree-tos --email "$CERTBOT_EMAIL" --nginx --redirect -d "$RUNESTONE_HOST"')
            print("You should be good for https")
        else:
            print("CERTBOT_EMAIL not set will not attempt certbot setup -- NO https!!")

# Do dev installs
# ^^^^^^^^^^^^^^^
        if dev_bookserver:
            assert dev, "You must run ``docker-tools.py build --dev`` in order to install the dev version of the BookServer."
            print("Installing development Version of the BookServer.")
            xqt(
                # By default, Poetry creates a venv in the home directory of the current user (root). However, this isn't accessible when running as ``www-data``. So, tell it to create the venv in a `subdirectory of the project <https://python-poetry.org/docs/configuration/#virtualenvsin-project>`_ instead, which is accessible.
                "poetry config virtualenvs.in-project true",
                "poetry install",
                cwd=bookserver_path
            )

        rsc = Path(f"{w2p_parent}/RunestoneComponents")
        # Use the same `volume detection strategy`_ as the BookServer.
        if (rsc / "runestone").is_dir():
            chdir(rsc)
            # If the bookserver is in dev mode, then the Runestone Components is already installed there in dev mode. Install it again in the venv so that both are up to date.
            # Otherwise, install them now.
            if not dev:
                print("Warning: you're installing a dev version of the components without running ``docker-tools.py build --dev``. The usual dev tools aren't installed.")
            print("Installing Development Version of Runestone Components")
            xqt(
                f"{sys.executable} -m pip install --upgrade -e .",
                f"{sys.executable} -m runestone --version",
            )
            # Build the webpack after the Runestone Components are installed.
            xqt(
                "npm install",
                "npm run build",
            )

        xqt(
            # web2py needs write access to update logs, database schemas, etc. Give it group ownership with write permission to allow this.
            f"chgrp -R www-data {Path(env.RUNESTONE_PATH).parent}",
            f"chmod -R g+w {Path(env.RUNESTONE_PATH).parent}",
        )

# Set up Postgres database
# ^^^^^^^^^^^^^^^^^^^^^^^^
        # Wait until Postgres is ready using `pg_isready <https://www.postgresql.org/docs/current/app-pg-isready.html>`_.
        print("Waiting for Postgres to start...")
        # TODO: use ``bookserver.config.settings._sync_database_url`` instead?
        if env.WEB2PY_CONFIG == "production":
            effective_dburl = env.DBURL
        elif env.WEB2PY_CONFIG == "test":
            effective_dburl = env.TEST_DBURL
        else:
            effective_dburl = env.DEV_DBURL
        xqt(f'pg_isready --dbname="{effective_dburl}"')

        print("Checking the State of Database and Migration Info")
        p = xqt(f"psql {effective_dburl} -c '\d'", capture_output=True, text=True)
        if p.stderr == "Did not find any relations.\n":
            print("Populating database...")
            # Populate the db with courses, users.
            populate_script = dedent('''
                from bookserver.main import app
                from fastapi.testclient import TestClient
                with TestClient(app) as client:
                    pass
            ''')
            xqt(f'BOOK_SERVER_CONFIG=development DROP_TABLES=Yes {"poetry run python" if dev_bookserver else sys.executable} -c "{populate_script}"', **run_bookserver_kwargs)
            # Remove any existing web2py migration data, since this is out of date and confuses web2py (an empty db, but migration files claiming it's populated).
            xqt("rm $RUNESTONE_PATH/databases/*")
        else:
            print("Database already populated.")
            # TODO: any checking to see if the db is healthy? Perhaps run Alembic autogenerate to see if it wants to do anything?

        # Write the stamp only after everything completed successfully, so it will be re-run if there's a failure.
        stamp.write_text("")

# Start the servers
# ^^^^^^^^^^^^^^^^^
    print("Starting the servers")

    print("Starting Celery...")
    # sudo doesn't pass root's env vars; provide only the env vars Celery needs when invoking it.
    xqt('sudo -u www-data env "PATH=$PATH" "REDIS_URI=$REDIS_URI" /srv/venv/bin/celery --app=scheduled_builder worker --pool=threads --concurrency=3 --loglevel=info &', cwd=f"{env.RUNESTONE_PATH}/modules")

    print("starting nginx")
    xqt("service nginx start")

    print("starting uwsgi")
    # Use uwsgi's "--virtualenv" option, since running it from a venv doesn't cause it to run apps in the same venv.
    xqt("/srv/venv/bin/uwsgi --virtualenv /srv/venv --ini /etc/uwsgi/sites/runestone.ini &", cwd=env.WEB2PY_PATH)
    # To manually test out web2py, first ``service nginx stop`` then run ``python3 web2py.py --ip=0.0.0.0 --port=80 --password="$POSTGRES_PASSWORD" -K runestone --no_gui -X``.

    print("Starting FastAPI server")
    run_bookserver_venv = ("poetry run " if dev_bookserver else f"{sys.executable} -m ") + "bookserver "
    xqt(
        run_bookserver_venv +
        "--book_path $RUNESTONE_PATH/books "
        "--root /ns "
        "--bks_config development "
        "--error_path /tmp "
        "--gconfig /etc/gunicorn/gunicorn.conf.py "
        "--bind unix:/run/gunicorn.sock "
        "--web2py $RUNESTONE_PATH "
        # Uncomment this to log to a file instead of stdio.
        ##"> ${WEB2PY_PATH}/logs/asgi.log 2>&1 "
        "&",
        **run_bookserver_kwargs,
    )


# A utility to replace all instances of ``${var_name}`` in  a string, where the variables are provided in ``vars_``. This is an alternative to the build-in ``str.format()`` which doesn't require escaping all the curly braces.
def replace_vars(str_: str, vars_: Dict[str, str]):
    def repl(matchobj: re.Match):
        var_name = matchobj.group(1)
        return (
            # Perform a replacement if the ``var_name`` is in ``vars_``.
            str(vars_[var_name]) if var_name in vars_
            # Otherwise, perform no replacement.
            else matchobj.group(0)
        )

    # Search for a ``${var_name}``.
    pattern = r"\${(\w+)}"
    return re.sub(pattern, repl, str_)


if __name__ == "__main__":
    cli()