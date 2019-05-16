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

After cloning the book edit the pavement.py file.  It is **critical** that the `master_url` variable in that file is set correctly.  If you are running docker and doing your development on the same machine then `http://localhost` will work. If you are running docker on a remote host then make sure to set it to the name of the remote host. `master_url` is the URL that the API calls in the browser will use to connect to the server running in the docker container.

### 2. Add Users

If you have an instructors.csv or students.csv that you want to add to the database,
put them in a folder called "configs" in the root of the repository:  The format of the csv files is to have one person per line with the format of each line as follows:

```
username,email,first_name,last_name,pw,course
```

This will create usernames for each person and pre-register them for the course.  In the case of instructors it register and make them instructors for the course.


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
you can use the docker-compose file as is, **no changes are necessary**.  You can skip
to step 5 at this point.

If you want to deploy a production Runestone Server, you will need
to change the default usernames and passwords. Notice how there are environment
variables for the database (POSTGRES_*) in the `environment` section of the
uwsgi and db images:

```bash
    environment:
      POSTGRES_PASSWORD: 'runestone'
      POSTGRES_USER: 'runestone'
      POSTGRES_DB: 'runestone'
      RUNESTONE_HOST: 'hostname of the host running docker'
```

These will be provided to the containers that are created to initialize the postgres
database. For a production deployment, you have a few options. You can change
these variables (and *do not* commit the file to GitHub) or you can create an
environment variable file on your host, here is `.env`:

```bash
POSTGRES_PASSWORD=topsecret
POSTGRES_USER=mrcheese
POSTGRES_DB=quesodb
RUNESTONE_HOST=`hostname`
export POSTGRES_PASSWORD POSTGRES_USER POSTGRES_DB RUNESTONE_HOST
```

and then in your docker-compose file, remove the `environment` section from each
of the `db` and `uwsgi` images and replace with:

```bash
    env_file:
     - .env
```

### 5. Start Everything

Once your environment is ready to go (again, for development you can leave the
defaults), use docker-compose to bring the containers up.

```bash
$ docker-compose up -d
```

And go to [http://$RUNESTONE_HOST:8080](http://0.0.0.0:8080) to see the application.

## Development Tips

### 1. Updating Books or Runestone

If you look at the docker-compose file, you'll notice that the root of the repository
is bound as a volume to the container:

```bash
    volumes:
      - .:/srv/web2py/applications/runestone
    ...
```

This means that if you make changes to the repository root
(the runestone application) they will also be made in the container!
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
### 2. Running the Runestone Server Unit Tests

You can run the unit tests in the container using the following command.

```
docker exec -it runestoneserver_runestone_1 bash -c 'cd applications/runestone/tests; python run_tests.py'
```

### 3. Removing Containers

If you really want to remove all containers and start over (hey, it happens) then
you can stop and remove:

```bash
$ docker-compose stop
$ docker-compose rm
```

This is probably only necessary if you are making changes to the Dockerfile or files that are used to create the container.

### 4. Previous Database

Once you create the containers, you'll notice a "databases" subfolder is generated
on the host. This happens after the initialization, as the runestone folder
is bound to the host. If you remove the containers and try to bring them up
without removing this folder, you'll see an error (and the container won't start):

```bash
$ docker-compose logs runestone
/srv/web2py/applications/runestone/databases exists, cannot init until removed from the host.
sudo rm -rf databases
```

The message tells you to remove the databases folder. Since the container is restarting
on its own, you should be able to remove it, and then wait, and it will start cleanly.
As an alternative, you can stop and rebuild the container, changing the `WEB2PY_MIGRATE`
variable to be Fake in [entrypoint.sh](entrypoint.sh) and try again:

```bash
export WEB2PY_MIGRATE=Fake
```

You would rebuild the container like this:

```bash
$ docker build -t runestone/server .
```

For now, it's recommended to remove the folder. Hopefully we will
develop a cleaner solution to handle migrations.


### 5. Testing the Entrypoint

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

### 6. Shelling Inside

You can shell into the container to look around, or otherwise test. When you enter,
you'll be in the web2py folder, where runstone is an application under applications:

```bash
$ docker exec -it $CONTAINER_ID bash
root@60e279f00b2e:/srv/web2py#
```

Remember that the folder under web2py applications/runestone is bound to your host,
so **do not edit files from inside the container** otherwise they will have a change in
permissions on the host.
