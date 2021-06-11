# Docker Deployment

Using Docker,
we can easily bring up the server without needing to install dependencies
on the host.

## Setup

### 0. Install Docker

1. Follow the [Docker installation guide](https://docs.docker.com/install/#supported-platforms). On Linux, make sure to also perform the [post-installation steps](https://docs.docker.com/install/linux/linux-postinstall/).
2. [Install Docker Compose](https://docs.docker.com/compose/install/).

### 1. Add Books

You can add any [books](https://github.com/RunestoneInteractive) that you want
installed in the application into the [books](../books) folder.
They will be installed upon start or restart. For example, here is how I might
add the [thinkcspy](https://github.com/RunestoneInteractive/thinkcspy) lesson:

```bash
cd books
git clone https://github.com/RunestoneInteractive/thinkcspy.git
```

A better method is to set the environment variable `BUILD_BOOKS` to no and then use the `dbuild` command found in the scripts folder to rebuild any books when you want them built.   Having runestone automatically rebuild all books upon startup makes the startup longer and is fragile. If a book fails to rebuild for any reason, then the runestone container will restart itself.  This will go on endlessly.

After cloning the book edit the pavement.py file. It is **critical** that the `master_url` variable in that file is set correctly. If you are running docker and doing your development on the same machine then `http://localhost` will work. If you are running docker on a remote host then make sure to set it to the name of the remote host. `master_url` is the URL that the API calls in the browser will use to connect to the server running in the docker container.

### 2. Add Users

If you have an `instructors.csv` or `students.csv` that you want to add to the database,
put them in a folder called `configs` in the root of the repository. The format of the csv files is to have one person per line with the format of each line as follows:

```
username,email,first_name,last_name,pw,course
```

This will create usernames for each person and pre-register them for the course. In the case of instructors it register and make them instructors for the course. From the `$RUNESTONE_PATH` directory (top level of runestone) you can exectue the following commands:

```bash
$ mkdir -p configs
$ cp instructors.csv configs
$ cp students.csv configs
```

### 3. Configure Email (Optional)

If you are going to use this with a live class you will probably want to configure an email to handle forgotten passwords and usernames. You do this by creating or editing the `models/1.py` file. I found that a simple gmail account can be configured to handle this task. However you will want to configure that account so that 2-factor authentication is turned on, AND you will need to create an application specific password for your server. After creating the app specific password add the following lines to 1.py

```python
settings.email_server = "smtp.gmail.com:587"
settings.email_sender = "youraccount@gmail.com"
settings.email_login = "youraccount@gmail.com:APP-SECIFIC-PW-HERE"
```

### 3. Build

First, build the application container.

```bash
$ docker build -t runestone/server .
```

This build step _only needs to be done once_ and only again if you need
to update dependencies in the container (and don't want to shell inside and update
them manually). We will show you how to do that further below. The build
creates an image that you can create instances of (the instances are the containers)
using the docker-compose file.

### 4. Environment

For a development deployment (meaning on your local machine to test and develop)
you can use the docker-compose file as is, **no changes are necessary**. You will need to set 2 Environment variables.

```bash
export RUNESTONE_HOST=localhost
export POSTGRES_PASSWORD=runestone
```

If you want to test using a secure port you can set the `CERTBOT_EMAIL` environment variable and we will automatically aquire a certificate.


If you are doing **development work** You will want to install the RunestoneComponents in development mode as well. clone https://github.com/RunestoneInteractive/RunestoneComponents.git as a sibling of the RunestoneServer directory. As the components also use npm to build the runestone.js file you will want to **follow the directions** in the README for that. If you do not then you will be **missing runestone.js** and nothing is going to work right! If you are not developing the components then don't worry about it, docker will already have the latest released version of runestone installed.

Create a docker-compose.override.yml in the same directory as the docker-compose.yml file. It should look like this:

```yml
version: "3"

services:
    runestone:
        volumes:
            - ../RunestoneComponents:/srv/RunestoneComponents
```

The entrypoint.sh file will notice that you have this volume mounted and reinstall the development version of Runestone.

Developers can now skip to step 5.

If you want to deploy a production Runestone Server, you will need
to change the default usernames and passwords. Notice how there are environment
variables for the database (POSTGRES\_\*) in the `environment` section of the
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
these variables (and _do not_ commit the file to GitHub) or you can create an
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

And go to [http://$RUNESTONE_HOST](http://localhost/runestone) to see the application.

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
you _will_ need to restart it.

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

### 2. Creating Questions from the Web Interface

If you want to write questions from the web interface you will need to make sure
that `settings.python_interpreter` is set to a real python. In the uwsgi environment uwsgi tends to replace python in `sys.executable` with itself, which is pretty annoying.

### 2. Running the Runestone Server Unit Tests

You can run the unit tests in the container using the following command.

```
docker exec -it runestoneserver_runestone_1 bash -c 'cd applications/runestone/tests; python run_tests.py'
```

The `scripts` folder has a nice utility called `dtest` that does this for you and also supports the `-k` option for you to run a single test.

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

You can simplify this by using the `dshell` script found in the scripts folder.

Remember that the folder under web2py applications/runestone is bound to your host,
so **do not edit files from inside the container** otherwise they will have a change in permissions on the host.

### 7. Restarting uwsgi/web2py

Controllers are reloaded automatically every time they are used. However if you are making changes to code in the `modules` folder you will need to restart web2py or else it is likely that a cached version of that code will be used. You can restart web2py easily by first shelling into the container and then running the command `touch /srv/web2py/reload_server`

### 8. File Permissions (especially on Linux)

File permissions can seem a little strange when you start this container on Linux. Primarily because both nginx and uwsgi run as the `www-data` user. So you will suddenly find your files under RunestoneServer owned by `www-data` . The container's entrypoint script updates permissions to allow both you and the container enough privileges to do your work.

## 9. If you are writing your own book

If you are writing your own book you will want to get that book set up properly in the runestone system. You need to do the following:

1. Run the command `dmanage addcourse` Use the project name you configured in `pavement.py` as the name of BOTH the course and the basecourse when it asks.  The dmanage command is in the scripts folder of RunestoneServer.
2. Now that your course is registered rebuild it using the `dbuild` command found in the RunestoneServer `scripts` folder use the command `dbuild bookname`
3. If this book is a PreTeXt book you will need to navigate to the directory that contains the `runestone-manifest.xml` file and run the command `runestone process-manifest --course <yourcourse> --manifest runestone-manifest.xml`
   **Note** if you are missing `runestone-manifest.xml` then you need to rebuild your PreTeXt book with `runestone` as the publisher. See the PreTeXt docs for how do do this.
4. If this book is a PreTeXt book you should put run `touch NOBUILD` in the root directory for this book. Otherwise when the container restarts it will try to build this book using runestone build and it will fail, causing an endless cycle of container restarts.

## Debugging

There are a couple of ways to get at the logger output:

1.  Shell into the container and then look at `/srv/web2py/logs/uwsgi.log`
2.  Run `docker-compose logs --follow` This will give you the continuous stream of log information coming out of the container including the uwsgi/web2py log.
