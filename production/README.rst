Production Configuration Instructions
=====================================

This document tells you how to configure a runestone server environment with multiple containers running the runestone server and bookserver

Here is how Runestone is configured on Digital Ocean for Runestone Academy

1. A small droplet running nginx as a load balancer.  This may be overkill, just not sure if I need a dedicated host for this, but seems to be a best practice.  I am not using docker or any containers on this host.
2. A medium size droplet running postgresql AND Redis -- I really don't think redis needs its own host. -- Again, no docker or containers I simply installed Postgres 13 and Redis 6
3. Several medium droplets that use docker compose and our RunestoneServer image along with the Jobe image.  I think this will scale nicely, but we will probably need to tweak configurations as we get into production.  How many processes for web2py?  How many for book server?  Can one JOBE for each machine keep up?  (I think it can with the load spread out evenly over five machines) -- We DO need a different `docker-config.yml` file for this production setup and I will be happy to provide what I have.
4. Digital Ocean provides a private container registry for us to push and pull containers for our production droplets.  It is also possible that using Digital Ocean's load balancer service could also be easier than running our own dedicated droplet.

Included in this folder are the configuration files and the `docker-compose.yml` file I use for the production environment.

* `env.template` you can rename this to .env and update the values of the variables.
* `docker-compose.yml` should not require any modifications if you set the variable in `.env`
* `load_balancer_default` The default configuration file to place in your `nginx/sites-available` folder.


Setting up the Load balancer
----------------------------

1. Create a droplet on digitial ocean or a bare machine on your preferred hosting provider.
2. Install nginx
3. Install certbot
4. copy the `load_balancer_default` file into your new nginx setup.  Update names to reflect your domain.
5. Using certbot obtain certificates for your domain.  Do not use the option to have certbot update the nginx config file. That is done.


Setting up Postgresql and Redis
-------------------------------

1. Create a droplet on digital ocean or a bare machine on your preferred hosting provider.
2. Follow the instructions from digital ocean to install postgresql 13
3. Install redis   

If you are migrating from a previous production setup do a backup of your old database and load it into this new machine.

If this is your first time using the new bookserver you will need to:
1. Run the rename_indices.sql script in the alembic folder of bookserver
2. Run the migrations in alembic to fix constraints and indexes used in the new bookserver


Deploying Several RunestoneServer containers
--------------------------------------------

You will need a private docker container registry.  Either sign up for one with digital ocean or if your hosting provider does that, or follow one of the many tutorials for building your own machine as a private registry.

On one machine you will need to set up a build environment by cloning RunestoneServer.

1. run `docker/docker_tools.py --multi` to build an image
2. run `docker commit` to commit this image
3. push the saved image to the container registry

Now on each of your production machines you can pull this image from the registry and then use `docker compose up -d` to start everything.
