FROM library/python:3.7-stretch

LABEL authors="@bnmnetp,@vsoch,@yarikoptic"

# docker build -t runstone/server .
# TODO: convert generation to neurodocker call after all is cool

# Define some ARGs which could be passed into while building
# TODO: in reality there some hardcoding already probably present
#       in the entrypoint.sh script.
ARG WEB2PY_PATH=/srv/web2py
ARG WEB2PY_APPS_PATH=${WEB2PY_PATH}/applications
ARG WEB2PY_PORT=8080
ARG DBHOST=db

# And export some as env vars so they could be available at run time
ENV WEB2PY_PATH=${WEB2PY_PATH}
ENV RUNESTONE_PATH=${WEB2PY_APPS_PATH}/runestone
ENV BOOKS_PATH=${RUNESTONE_PATH}/books
ENV WEB2PY_VERSION=2.18.4

# Click needs these encodings for Python 3
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Expose that port on the network
EXPOSE ${WEB2PY_PORT}

# To prevent interactive debconf during installations
ARG DEBIAN_FRONTEND=noninteractive

# Components from requirements.txt which are available in Debian
# Missing ones:
#  runestone -- is the RunestoneComponents, https://pypi.org/project/runestone/, may be install from Git?
#  paver -- too old in Debian  filed bug report
#  selenium -- also a bit too old (2.53.2+dfsg1-1)
#  sphinxcontrib-paverutils -- N/A
#  sphinx -- we need stretch-backports
#  pytz ... ?
# A few missing ones
#  rsync is needed when deploying a built book
#  vim - just for pleasure of being able to do any changes right within
#  wget - just in case
RUN apt-get update && \
    apt-get install -y eatmydata && \
    eatmydata apt-get update && echo "count 1" && \
    eatmydata apt-get install -y --no-install-recommends \
        gcc \
        git \
        unzip \
        emacs-nox \
        libfreetype6-dev postgresql-common postgresql postgresql-contrib \
        libpq-dev libxml2-dev libxslt1-dev \
        rsync wget nginx && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# The rest could be done and ran under a regular (well, staff for installing under /usr/local) user
RUN useradd -s /bin/bash -M -g staff --home-dir ${WEB2PY_PATH} runestone && \
    mkdir -p /srv

# Install additional components
RUN git clone https://github.com/web2py/web2py ${WEB2PY_PATH} && \
    cd ${WEB2PY_PATH} && \
    git submodule update --init --recursive

RUN mkdir -p ${RUNESTONE_PATH}
ADD . ${RUNESTONE_PATH}
WORKDIR ${RUNESTONE_PATH}

# Question: should this come from an envar?
# Set docker_institution_mode = True so that instructors can use thinkcspy and other
# base courses as their course when using docker to host their own courses.
RUN mkdir -p private && \
    echo "sha512:16492eda-ba33-48d4-8748-98d9bbdf8d33" > private/auth.key && \
    pip3 install -r requirements.txt && \
    pip3 install -r requirements-test.txt && \
    pip3 install uwsgi && \
    rm -rf ${WEB2PY_PATH}/.cache/* && \
    cp ${RUNESTONE_PATH}/scripts/run_scheduler.py ${WEB2PY_PATH}/run_scheduler.py && \
    cp ${RUNESTONE_PATH}/scripts/routes.py ${WEB2PY_PATH}/routes.py

WORKDIR ${WEB2PY_PATH}

# All configuration will be done within entrypoint.sh upon initial run
# of the container
COPY docker/entrypoint.sh /usr/local/sbin/entrypoint.sh

# Copy configuration files to get nginx and uwsgi up and running
RUN mkdir -p /etc/nginx/sites-enabled
COPY docker/nginx/sites-available/runestone /etc/nginx/sites-enabled/runestone
COPY docker/uwsgi/sites/runestone.ini /etc/uwsgi/sites/runestone.ini
COPY docker/systemd/system/uwsgi.service /etc/systemd/system/uwsgi.service
COPY docker/wsgihandler.py /srv/web2py/wsgihandler.py
RUN ln -s /etc/systemd/system/uwsgi.service /etc/systemd/system/multi-user.target.wants/uwsgi.service
RUN rm /etc/nginx/sites-enabled/default

CMD /bin/bash /usr/local/sbin/entrypoint.sh
