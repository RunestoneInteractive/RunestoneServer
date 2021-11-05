# syntax=docker/dockerfile:1
#
# See the `syntax parser directive <https://docs.docker.com/engine/reference/builder/#syntax>`_. It must be the first line of the file.
#
# ************************************************************
# |docname| - create a container hosting the Runestone servers
# ************************************************************
# To build, execute `docker-tools <docker/docker_tools.py>` ``build``.

FROM python:3.8-buster

LABEL authors="@bnmnetp,@vsoch,@yarikoptic,@bjones1"

# `docker/docker_tools.py` passes this when invoking a ``docker build``.
ARG DOCKER_BUILD_ARGS
# It must be an ``ENV`` so that it exits when the ``CMD`` is run by ``docker-compose up``.
ENV DOCKER_BUILD_ARGS=${DOCKER_BUILD_ARGS}

# Define some ARGs which could be passed into while building
ARG WEB2PY_PATH=/srv/web2py
# And export some as env vars so they could be available at run time
ENV WEB2PY_PATH=${WEB2PY_PATH}
ENV RUNESTONE_PATH=${WEB2PY_PATH}/applications/runestone

# Click needs these encodings for Python 3.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# To prevent interactive debconf during installations.
ARG DEBIAN_FRONTEND=noninteractive

# We need the entire Runstone server repo for the build.
COPY . ${RUNESTONE_PATH}
RUN \
    # Put everything in a venv.
    python -m venv /srv/venv && \
    # Tell the script this is the build phase of the process.
    IN_DOCKER=1 \
    # Run the main script.
    /srv/venv/bin/python ${RUNESTONE_PATH}/docker/docker_tools.py ${DOCKER_BUILD_ARGS}

# This also must start in the venv in the built container.
CMD IN_DOCKER=2 /srv/venv/bin/python ${RUNESTONE_PATH}/docker/docker_tools.py ${DOCKER_BUILD_ARGS}
