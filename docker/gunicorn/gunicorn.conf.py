# ***********************************
# |docname| - gunincorn configuration
# ***********************************
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
# `wsgi_app <https://docs.gunicorn.org/en/stable/settings.html#wsgi-app>`_: A WSGI application path in pattern ``$(MODULE_NAME):$(VARIABLE_NAME)``.
wsgi_app = "bookserver.main:app"

# `user <https://docs.gunicorn.org/en/stable/settings.html#user>`_: Switch worker processes to run as this user.
user = "www-data"

# `group <https://docs.gunicorn.org/en/stable/settings.html#group>`_: Switch worker process to run as this group.
group = "www-data"

# `workers <https://docs.gunicorn.org/en/stable/settings.html#workers>`_: The number of worker processes for handling requests. Pick this based on CPU count.
workers = multiprocessing.cpu_count() * 2 + 1

# `worker_class <https://docs.gunicorn.org/en/stable/settings.html#worker-class>`_: The type of workers to use. Use `uvicorn's worker class for gunicorn <https://www.uvicorn.org/deployment/#gunicorn>`_.
worker_class = "uvicorn.workers.UvicornWorker"
