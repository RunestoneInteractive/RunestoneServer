#!/bin/bash

# TODO - this location also allow to do needed copying etc to keep DB outside as well
stamp=/var/lib/postgresql/9.6/main/initialized.stamp

# Fail early upon error
set -eu

info () {
    echo "I: $@"
}

# Start service(s)
info "Starting the DB server"
service postgresql start
trap "service postgresql stop" 0

export WEB2PY_CONFIG=production
export WEB2PY_MIGRATE=Yes
export DBURL=postgresql://runestone:${DB_PASSWORD}@localhost/runestone

if [ ! -e "$stamp" ]; then
    info "Initializing"
    su -c "psql postgres -c \"CREATE USER runestone superuser password '${DB_PASSWORD}';\"" postgres
    su -c "createdb --owner=runestone runestone" postgres
    cd "$BOOKS_PATH/.."
    su -c "rsmanage initdb" runestone
    cp $WEB2PY_PATH/applications/runestone/scripts/run_scheduler.py $WEB2PY_PATH/

    # Let's use https
    # Wouldn't "just work" magically.  Requires certificates etc. Eventually!
    # echo -e '\nsettings.server_type = "https://"' >> $WEB2PY_PATH/applications/runestone/models/0.py

    # Setup students
    if [ -e '/srv/configs/instructors.csv' ]; then
        info "Setting up instructors"
        su -c "rsmanage inituser --fromfile /srv/configs/instructors.csv" runestone
        cut -d, -f1,6 /srv/configs/instructors.csv \
        | tr ',' ' ' \
        | while read n c ; do
            su -c "rsmanage addinstructor  --username $n --course $c" runestone;
        done
    fi
    if [ -e '/srv/configs/students.csv' ]; then
        info "Setting up students"
        su -c "rsmanage inituser --fromfile /srv/configs/students.csv" runestone
        info "Students were provided -- disabling signup!"
        # Disable signup
        echo -e "\nauth.settings.actions_disabled.append('register')" >> $WEB2PY_PATH/applications/runestone/models/db.py
    fi
    touch "$stamp"
else
    info "Already initialized"
fi

# Go through all books and do what needs to be done
info "Building & Deploying books"
cd "${BOOKS_PATH}"
/bin/ls | while read b; do
    (
        cd $b;
        su -c "runestone build && runestone deploy" runestone;
    );
done

# for debugging
# su -c 'bash' runestone

# Run the beast
info "Starting the server"
cd "$WEB2PY_PATH"
su -c "python web2py.py --ip=0.0.0.0 --port=8080 --password='$DB_PASSWORD' -K runestone --nogui -X" runestone  &
sleep 3
info "Starting the scheduler"
su -c "python run_scheduler.py" runestone
