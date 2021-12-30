#!/bin/bash

set -e

if [[ $PWD != */production ]]; then
    echo 'you need to be in the production folder for this'
    exit 
fi

# pull the latest
docker pull registry.digitalocean.com/runestone-registry/production_server:latest

docker compose stop
docker compose up -d
