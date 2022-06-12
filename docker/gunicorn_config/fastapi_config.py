# ***********************************************************
# |docname| - gunicorn configuration for FastAPI / BookServer
# ***********************************************************
# This file configures gunicorn to use Uvicorn to run FastAPI which runs the BookServer.
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
from common_config import *


# Configuration
# =============
# `chdir <https://docs.gunicorn.org/en/stable/settings.html#chdir>`_: Change directory to specified directory before loading apps. Otherwise gunicorn does not know where to look for changes to your code.
if os.environ["BOOK_SERVER_CONFIG"] == "development":
    chdir = "/srv/BookServer"

# `wsgi_app <https://docs.gunicorn.org/en/stable/settings.html#wsgi-app>`_: A WSGI application path in pattern ``$(MODULE_NAME):$(VARIABLE_NAME)``.
wsgi_app = "bookserver.main:app"

# `workers <https://docs.gunicorn.org/en/stable/settings.html#workers>`_: The number of worker processes for handling requests. Pick this based on CPU count.
workers = multiprocessing.cpu_count() * 2 + 1

# `worker_class <https://docs.gunicorn.org/en/stable/settings.html#worker-class>`_: The type of workers to use. Use `uvicorn's worker class for gunicorn <https://www.uvicorn.org/deployment/#gunicorn>`_.
worker_class = "uvicorn.workers.UvicornWorker"

# Detach and run in the background
daemon = True
capture_output = True
enable_stdio_inheritance = True
pidfile = "/srv/books.pid"
# reload_engine = "inotify"
