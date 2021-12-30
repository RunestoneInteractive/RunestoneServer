#!/bin/bash

set -e

# Make sure all services are stopped
docker compose -f docker-compose.yml stop
docker compose -f production/docker-compose.yml stop

# Run a production build of a new image
./docker/docker_tools.py build --multi

# start the newly built image
docker compose -f docker-compose.yml up -d
sleep 5

# commit the built image (with startup changes) as we want to use what is now running across all servers
prod_id=`docker ps |grep runestone/server|awk '{ print $1 }'`
docker commit $prod_id runestone/server/prod

# push the image to our private registry
docker image tag runestone/server/prod registry.digitalocean.com/runestone-registry/production_server:latest
docker push registry.digitalocean.com/runestone-registry/production_server:latest
