# syntax=docker/dockerfile:1
#
# See the `syntax parser directive <https://docs.docker.com/engine/reference/builder/#syntax>`_. It must be the first line of the file.
#
# ************************************************************
# |docname| - create a container hosting the Runestone servers
# ************************************************************
# To build, execute `docker-tools <docker/docker_tools.py>` ``build``.

FROM python:3.9-bullseye

LABEL authors="@bnmnetp,@vsoch,@yarikoptic,@bjones1"

# `docker/docker_tools.py` passes this when invoking a ``docker build``.
ARG DOCKER_BUILD_ARGS
# It must be an ``ENV`` so that it exists when the ``CMD`` is run by ``docker-compose up``.
ENV DOCKER_BUILD_ARGS=${DOCKER_BUILD_ARGS}

# Define some ARGs which could be passed into while building.
#
# **Warning:** Changing this path will require changes in many other places: the Docker volume locations, the paths in ``pyproject.toml``, paths used to run tests, etc.
ENV WEB2PY_PATH=/srv/web2py
ENV RUNESTONE_PATH=${WEB2PY_PATH}/applications/runestone
ENV BOOK_SERVER_PATH=/srv/BookServer

# Click needs these encodings for Python 3.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# To prevent interactive debconf during installations.
ARG DEBIAN_FRONTEND=noninteractive

# We need the entire Runstone server repo for the build.
COPY . ${RUNESTONE_PATH}
RUN \
    # Tell the script this is the build phase of the process.
    IN_DOCKER=1 \
    # Run the main script.
    python3 ${RUNESTONE_PATH}/docker/docker_tools.py ${DOCKER_BUILD_ARGS}

# Allow path changes by running bash -- see `docker/docker_tools.py`.
# Run the script again, in the run phase of the process.
CMD ["bash","-c","source ~/.profile; IN_DOCKER=2 python3 ${RUNESTONE_PATH}/docker/docker_tools.py ${DOCKER_BUILD_ARGS}"]
