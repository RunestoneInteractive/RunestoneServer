#!/bin/bash

# Fail early upon error
set -eu

info () {
    echo "I: $@"
}

# This file will exist if we've initialized postgres
stamp=/var/lib/postgresql/9.6/main/initialized.stamp

# Ensure the user starting the container has provided a password
if [ -z "$POSTGRES_PASSWORD" ]
then
    echo "Please export \${POSTGRES_PASSWORD}"
    exit 1
fi

# The RUNESTONE_HOST will be used by pavement.py files of
# runestone books to set the correct host for so that
# Browser and Server agree on a CORS compliant host for API calls
if [ -z "$RUNESTONE_HOST" ]; then
    echo "Please export \${RUNESTONE_HOST} set to the hostname"
    exit 1
fi

# For development make sure we are up to date with the latest from github.
if [ $WEB2PY_CONFIG == "development" ]; then
    pip install --upgrade git+git://github.com/RunestoneInteractive/RunestoneComponents.git
fi

# Initialize the database
if [ ! -f "$stamp" ]; then

    info "Install rsmanage local module"
    pip install -e ${RUNESTONE_PATH}/rsmanage

    info "Creating auth key"
    mkdir -p ${RUNESTONE_PATH}/private
    echo "sha512:16492eda-ba33-48d4-8748-98d9bbdf8d33" > ${RUNESTONE_PATH}/private/auth.key

    info "Creating pgpass file"
    echo "db:5432:*:$POSTGRES_USER:$POSTGRES_PASSWORD" > /root/.pgpass
    chmod 600 /root/.pgpass

    # add a new setting so that institutions can run using a base book like thinkcspy as their
    # course.  On Runestone.academy we don't let anyone be an instructor for the base courses
    # because they are open to anyone.  This makes for a much less complicated deployment strategy
    # for an institution that just wants to run their own server and use one or two books.
    if [ ! -f "${RUNESTONE_PATH}/models/1.py" ]; then
        touch "${RUNESTONE_PATH}/models/1.py"
    fi
    echo "settings.docker_institution_mode = True" >> "${RUNESTONE_PATH}/models/1.py"

    touch "${stamp}"
else
    info "Already initialized"
fi

RETRIES=10
set +e
until psql $DBURL -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 2
done

info "Checking the State of Database and Migration Info"
rsmanage env --checkdb
dbstate="$?"
info "Got result of $dbstate"
set -e

case $dbstate in
    0)
        info "Initializing DB and databases"
        rsmanage initdb
        ;;
    1)
        info "Removing databases folder and initializing"
        rsmanage initdb --reset --force
        ;;
    2)
        info "Warning -- Database initialized but missing databases/ Trying a fake migration"
        rsmanage migrate --fake
        ;;
    3)
        info "All is good, no initialization needed"
        ;;
    *)
        info "Unexpected result from checkdb"
        exit 1

esac

info "Updating file ownership"
chown -R www-data /srv/web2py
mkdir -p /run/uwsgi
chown -R www-data /run/uwsgi


# Setup instructors, if the file exists
if [ -f "${RUNESTONE_PATH}/configs/instructors.csv" -a "${RUNESTONE_PATH}/configs/instructors.csv" -nt iadd.stamp ]; then
    info "Setting up instructors"
    rsmanage inituser --fromfile ${RUNESTONE_PATH}/configs/instructors.csv
    cut -d, -f1,6 ${RUNESTONE_PATH}/configs/instructors.csv \
    | tr ',' ' ' \
    | while read n c ; do
        rsmanage addinstructor  --username $n --course $c  || echo "unable to add instructor"
    done
    touch iadd.stamp
fi

# Setup students, again if the file exists
if [ -f "${RUNESTONE_PATH}/configs/students.csv" -a "${RUNESTONE_PATH}/configs/students.csv" -nt sadd.stamp ]; then
    info "Setting up students"
    rsmanage inituser --fromfile ${RUNESTONE_PATH}/configs/students.csv
    info "Students were provided -- disabling signup!"
    # Disable signup
    echo -e "\nauth.settings.actions_disabled.append('register')" >> $WEB2PY_PATH/applications/runestone/models/db.py
    touch sadd.stamp
fi

# Uncomment for debugging
# /bin/bash

# Run the beast
info "Starting the server"
cd "$WEB2PY_PATH"

# To just run the development server Do this:
# python web2py.py --ip=0.0.0.0 --port=8080 --password="${POSTGRES_PASSWORD}" -K runestone --nogui -X  &

# To start in a mode more consistent with deployment Do this:
info "starting nginx"
service nginx start

info "starting uwsgi"
/usr/local/bin/uwsgi --ini /etc/uwsgi/sites/runestone.ini &


## Go through all books and build
info "Building & Deploying books"
cd "${BOOKS_PATH}"
/bin/ls | while read book; do
    (
        cd $book;
        if [ ! -f NOBUILD ]; then
            runestone build && runestone deploy
        else
            info "skipping $book due to NOBUILD file"
        fi
    );
done


tail -F ${WEB2PY_PATH}/logs/uwsgi.log

