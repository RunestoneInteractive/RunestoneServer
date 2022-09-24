#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Usage:  install_new_image.sh <release no>"
    exit
fi

set -e

cd /home/bmiller/Runestone/RunestoneServer/production

if [[ $PWD != */production ]]; then
    echo 'you need to be in the production folder for this'
    exit 
fi

# pull the latest
git pull
docker pull registry.digitalocean.com/runestone-registry/production_server:version$1

docker compose stop
docker compose up -d

echo "Pruning old images"
docker image prune -f
