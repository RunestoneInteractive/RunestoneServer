# Docker Deployment

Using [docker-compose](https://docs.docker.com/compose/install/) and [Docker](https://docs.docker.com/install/) 
we can easily bring up the server without needing to install dependencies 
on the host. If you haven't yet, visit the links to install both docker-compose and docker.

## Setup

### 1. Add Books

You can add any [books](https://github.com/RunestoneInteractive) that you want 
installed in the application into the [books](../books) folder. 
They will be installed upon start or restart. For example, here is how I might
add the [thinkcspy](https://github.com/RunestoneInteractive/thinkcspy) lesson:

```bash
cd books
git clone https://github.com/RunestoneInteractive/thinkcspy.git
```

### 2. Add Users

If you have an instructors.csv or students.csv that you want to add to the database, 
put them in a folder called "configs" in the root of the repository:

```bash
$ mkdir -p 
```

### 3. Build

First, build the application container.

```bash
$ docker build -t runstone/server .
```

This build step *only needs to be done once* and only again if you need
to update dependencies in the container (and don't want to shell inside and update
them manually). We will show you how to do that further below. The build
creates an image that you can create instances of (the instances are the containers)
using the docker-compose file.

### 4. Environment

For a development deployment (meaning on your local machine to test and develop)
you can use the docker-compose file as is, **no changes are necessary**. 
However, if you want to deploy a production Runestone Server, you will need
to change the default usernames and passwords. Notice how there are environment
variables for the database (POSTGRES_*) in the `environment` section of the
uwsgi and db images:

```bash
    environment:
      POSTGRES_PASSWORD: 'runestone'
      POSTGRES_USER: 'runestone'
      POSTGRES_DB: 'runestone'
```

These will be provided to the containers that are created to initialize the postgres
database. For a production deployment, you have a few options. You can change
these variables (and *do not* commit the file to GitHub) or you can create an
environment variable file on your host, here is `.env`:

```bash
POSTGRES_PASSWORD=topsecret
POSTGRES_USER=mrcheese
POSTGRES_DB=quesodb
export POSTGRES_PASSWORD POSTGRES_USER POSTGRES_DB
```

and then in your docker-compose file, remove the `environment` section from each
of the `db` and `uwsgi` images and replace with:

```bash
    env_file:
     - .env
```

Once your environment is ready to go (again, for development you can leave the 
defaults), use docker-compose to bring the containers up.

```bash
$ docker-compose up -d
```

And go to [http://0.0.0.0:8080](http://0.0.0.0:8080) to see the application.

## Development Tips

### 1. Updating Books or Runestone

If you look at the docker-compose file, you'll notice that subfolders of
the root of the respository bind to `/srv/web2py/applications/runestone/<subfolder>` in the container.

```bash
    volumes:
      - ./books:/srv/web2py/applications/runestone/books
      - ./controllers:/srv/web2py/applications/runestone/controllers
    ...
```

With these volume in place, it means that if you make changes to the repository root
(the runestone application) they will also be made in the container! The reason
we don't bind the entire runestone folder is that some files are generated when the
container is built (that are unlikely to be changed) and need to persist in the container.

However, for things like books, binding the "books" folder makes development easy.
For example, if you add a new book, the files will also be in the container.
You won't need to rebuild the container, however, to properly get the book running, 
you *will* need to restart it.

```bash
$ docker-compose restart runestone
```

Notice how I am restarting runestone above? This is the way that you can selectively
restart one of the containers. Sometimes they can get out of sync, and it's best to restart all
of them:

```bash
$ docker-compose restart
```

or to stop them, and then bring them up again (this should not erase data from the database)

```bash
$ docker-compose stop
$ docker-compose up -d
```

### 2. Removing Containers

If you really want to remove all containers and start over (hey, it happens) then
you can stop and remove:

```bash
$ docker-compose stop
$ docker-compose rm
```

### 3. Testing the Entrypoint

If you want to test the [entrypoint.sh](entrypoint.sh) script, the easiest thing
to do is add a command to the docker-compose to disable it, and then run commands
interactively by shelling into the container. For example, add a command line like
this to the "runestone" container:

```
  runestone:
    image: runestone/server
    command: tail -F peanutbutter
...
```

Bring up the containers:

```bash
$ docker-compose up -d
```

And then when the container is running, find it's id by doing:

```bash
CONTAINER_ID=$(echo `docker-compose ps -q runestone` |  cut -c1-12)
```

And then shell inside (see next section). Once inside, you can then issue commands 
to test the entrypoint - since the others were started
with docker-compose (postgres) everything is ready to go.

### 4. Shelling Inside

You can shell into the container to look around, or otherwise test. When you enter,
you'll be in the web2py folder, where runstone is an application under applications:

```bash
$ docker exec -it $CONTAINER_ID bash
root@60e279f00b2e:/srv/web2py# 
```

Remember that the folder under web2py applications/runestone is bound to your host,
so **do not edit files from inside the container** otherwise they will have a change in
permissions on the host. 
