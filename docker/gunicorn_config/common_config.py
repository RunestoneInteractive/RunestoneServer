# **************************************************
# |docname| - common gunicorn configuration settings
# **************************************************
# This file contains common configuration settings for gunicorn.
#
# See also the `gunicorn config docs <https://docs.gunicorn.org/en/stable/configure.html#configuration-file>`_.
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8`_.
#
# Standard library
# ----------------
# None.

# Third-party imports
# -------------------
# None.
#
# Local application imports
# -------------------------
# None.


# Configuration
# =============
# `user <https://docs.gunicorn.org/en/stable/settings.html#user>`_: Switch worker processes to run as this user.
user = "www-data"

# `group <https://docs.gunicorn.org/en/stable/settings.html#group>`_: Switch worker process to run as this group.
group = "www-data"

# `max_requests <https://docs.gunicorn.org/en/stable/settings.html#max-requests>`_: The maximum number of requests a worker will process before restarting. This is a good way to prevent memory "leaks" in Python to keep things from eventually crashing.
max_requests = 500

# `max_requests_jitter <https://docs.gunicorn.org/en/stable/settings.html#max-requests-jitter>`_: The maximum jitter to add to the max_requests setting. Ensures that everything doesn't restart in lock step.
max_requests_jitter = 30

# `timeout <https://docs.gunicorn.org/en/stable/settings.html#timeout>`_: Workers silent for more than this many seconds are killed and restarted. Restart processes that haven't produced any output for 60 seconds.
timeout = 60
