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
mkdir -p 
```

## Build

First, build the application container.

```bash
docker build -t runstone/server .
```

Next, you need to export a database password to the environment. If it's not found,
 you will get an error when starting the containers with docker-compose.

```bash
$ export POSTGRES_PASSWORD=runestone
```

Then, use docker-compose to bring the containers up.

```bash
docker-compose up -d
```

## Development Tips

### 1. Testing the Entrypoint

If you want to test the [entrypoint.sh](entrypoint.sh) script, the easiest thing
to do is add a command to the docker-compose to disable it, and then run commands
interactively by shelling into the container. For example, add a command line like
this to the "runestone" container:

```
  runestone:
    image: runestone/server
    command: tail -F peanutbutter
    volumes:
      - .:/code
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

And then shell inside. You'll be in the web2py folder, where runstone is an
application under applications:

```bash
$ docker exec -it $CONTAINER_ID bash
root@60e279f00b2e:/srv/web2py# 
```

You can then issue commands to test the entrypoint - since the others were started
with docker-compose (postgres, nginx) everything is ready to go.

### 2. Testing uwsgi

The uwsgihander.py script is moved into the root of the web2py folder when the
container is built, and this script will help to serve the application
with wsgi. To test wsgi, you can do this:

```bash
$ uwsgi --http :8000 --chdir ${WEB2PY_PATH} -w wsgihandler:application
```

**under development**
