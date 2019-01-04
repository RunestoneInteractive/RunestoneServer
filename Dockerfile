FROM debian:stretch-backports
MAINTAINER Yaroslav O. Halchenko <debian@onerussian.com>

ARG WEB2PY_PATH=/srv/web2py
ARG WEB2PY_APPS_PATH=${WEB2PY_PATH}/applications

# TODO: Figure out the whole desired setup.  
#  - Books probably should live outside an be bind mounted inside (/srv/runstone/books?)
#  - or may be the entire server be bind mounted from outside?

# TODO: convert generation to neurodocker call after all is cool

# To prevent interactive debconf during installations
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y eatmydata

RUN eatmydata apt-get update && echo "count 1" && \
    eatmydata apt-get install -y --no-install-recommends \
        git \
        python-pip libfreetype6-dev postgresql-common postgresql postgresql-contrib \
        libpq-dev libxml2-dev libxslt1-dev

# Components from requirements.txt which are available in Debian
# Missing ones:
#  runestone -- is the RunestoneComponents, https://pypi.org/project/runestone/, may be install from Git?
#  paver -- too old in Debian  filed bug report
#  selenium -- also a bit too old (2.53.2+dfsg1-1)
#  sphinxcontrib-paverutils -- N/A
#  sphinx -- we need stretch-backports
#  pytz ... ?
RUN eatmydata apt-get install -y --no-install-recommends \
        python-diff-match-patch \
        python-lxml \
        python-numpy \
        python-numpy \
        python-psycopg2 \
        pylint \
        python-dateutil \
        python-requests \
        python-selenium \
        python-six \
        python-sphinx \
        python-sqlalchemy \
        python-cssselect \
        python-oauth2client
    

# Install additional components
RUN git clone --recursive https://github.com/web2py/web2py /usr/local/lib/web2py && \
    ln -s /usr/local/lib/web2py/web2py.py /usr/local/bin/web2py.py

# A few missing ones
RUN eatmydata apt-get install -y --no-install-recommends \
        python-wheel

# The rest could be done by a regular user
RUN useradd -s /bin/bash -M --home-dir ${WEB2PY_PATH} runestone
RUN mkdir -p ${WEB2PY_PATH} && \
    chown runestone ${WEB2PY_PATH}

USER postgres
RUN service postgresql start && \
  psql postgres -c "CREATE USER runestone superuser password '${DB_PASSWORD}';" && \
  service postgresql stop

USER runestone
WORKDIR ${WEB2PY_PATH}

RUN mkdir -p ${WEB2PY_APPS_PATH} && \
    cd ${WEB2PY_APPS_PATH} && \
    git clone https://github.com/RunestoneInteractive/RunestoneServer runestone


RUN cd ${WEB2PY_APPS_PATH}/runestone && \
    pip install -r requirements.txt

USER root
ARG WEB2PY_PORT=8080

# Start configuration
EXPOSE ${WEB2PY_PORT}

CMD service postgresql start && su -c /bin/bash runestone 
#RUN apt-get clean
