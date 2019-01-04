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
    
# So it could be available at run time
ARG WEB2PY_PORT=8080
ENV WEB2PY_PATH=${WEB2PY_PATH}
ENV BOOKS_PATH=${WEB2PY_APPS_PATH}/runestone/books
EXPOSE ${WEB2PY_PORT}

# A few missing ones
#  rsync is needed when deploying a built book
#  vim - just for pleasure of being able to do any changes right within
#  wget - just in case
RUN eatmydata apt-get install -y --no-install-recommends \
        python-wheel rsync wget


# The rest could be done and ran under a regular (well, staff for installing under /usr/local) user
RUN useradd -s /bin/bash -M -g staff --home-dir ${WEB2PY_PATH} runestone
RUN mkdir -p /srv && chown -R runestone /srv

USER runestone

# Install additional components
RUN git clone --recursive https://github.com/web2py/web2py ${WEB2PY_PATH}

RUN mkdir -p ${WEB2PY_APPS_PATH} && \
    cd ${WEB2PY_APPS_PATH} && \
    git clone https://github.com/RunestoneInteractive/RunestoneServer runestone


RUN cd ${WEB2PY_APPS_PATH}/runestone && \
    pip install --system -r requirements.txt

# TODO: various cleanups
#RUN apt-get clean
USER root
WORKDIR ${WEB2PY_PATH}

# Start configuration

COPY docker/entrypoint.sh /usr/local/sbin/entrypoint.sh
CMD /bin/bash /usr/local/sbin/entrypoint.sh
