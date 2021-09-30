# syntax=docker/dockerfile:1
# See the `syntax parser directive <https://docs.docker.com/engine/reference/builder/#syntax>`_. It must be the first line of the file.
#
# ************************************************************
# |docname| - create a container hosting the Runestone servers
# ************************************************************
# To build, execute ``ENABLE_BUILDKIT=1 docker build -t runstone/server .``

FROM python:3.8-buster

LABEL authors="@bnmnetp,@vsoch,@yarikoptic"

# `docker/docker_tools.py` passes this when invoking a ``docker build``.
ARG DOCKER_BUILD_ARGS
ENV DOCKER_BUILD_ARGS=${DOCKER_BUILD_ARGS}

ENV DBURL=${DBURL}
# Define some ARGs which could be passed into while building
ARG WEB2PY_PATH=/srv/web2py

# And export some as env vars so they could be available at run time
ENV WEB2PY_PATH=${WEB2PY_PATH}
ENV RUNESTONE_PATH=${WEB2PY_PATH}/applications/runestone

# Click needs these encodings for Python 3
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# To prevent interactive debconf during installations
ARG DEBIAN_FRONTEND=noninteractive

COPY . ${RUNESTONE_PATH}
RUN \
    # Put everything in a venv.
    python -m venv /srv/venv && \
    # Now run the main script.
    IN_DOCKER=1 /srv/venv/bin/python ${RUNESTONE_PATH}/docker/docker_tools.py ${DOCKER_BUILD_ARGS}
# Note that we don't pass args to the container's startup script -- there's no need for them. This also must start in the venv in the built container.
CMD IN_DOCKER=2 /srv/venv/bin/python ${RUNESTONE_PATH}/docker/docker_tools.py ${DOCKER_BUILD_ARGS}
