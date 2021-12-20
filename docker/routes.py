# ******************************
# |docname| - routing for web2py
# ******************************
# Provide a default application, so that accessing "https://my-site-name.edu" works, instead of requiring "https://my-site-name.edu/runestone".
#
# See the `web2py manual <http://web2py.com/books/default/chapter/29/04/the-core#Parameter-based-system>`_.
routers = dict(
    BASE=dict(
        default_application="runestone",
    )
)
