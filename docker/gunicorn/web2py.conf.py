# ********************************************************************
# |docname| - gunicorn configuration for web2py / the Runestone Server
# ********************************************************************
# This file configures gunicorn to run the web2py-based (old) Runestone Server.
#
# See also the `gunicorn config docs <https://docs.gunicorn.org/en/stable/configure.html#configuration-file>`_.
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8`_.
#
# Standard library
# ----------------
import multiprocessing
import os

# Third-party imports
# -------------------
# None.
#
# Local application imports
# -------------------------
# None.
#
#
# Configuration
# =============
# `chdir <https://docs.gunicorn.org/en/stable/settings.html#chdir>`_: Change directory to specified directory before loading apps. Point this to the location of ``wsgihandler.py``, which must be copied to the web2py root directory.
chdir = os.environ["WEB2PY_PATH"]

# `wsgi_app <https://docs.gunicorn.org/en/stable/settings.html#wsgi-app>`_: A WSGI application path in pattern ``$(MODULE_NAME):$(VARIABLE_NAME)``.
wsgi_app = "wsgihandler:application"

# `user <https://docs.gunicorn.org/en/stable/settings.html#user>`_: Switch worker processes to run as this user.
user = "www-data"

# `group <https://docs.gunicorn.org/en/stable/settings.html#group>`_: Switch worker process to run as this group.
group = "www-data"

# `workers <https://docs.gunicorn.org/en/stable/settings.html#workers>`_: The number of worker processes for handling requests. Pick this based on CPU count.
workers = multiprocessing.cpu_count()

# `bind <https://docs.gunicorn.org/en/stable/settings.html#bind>`_: The socket to bind. This must match the socket nginx sends to.
bind = "unix:/run/web2py.sock"
