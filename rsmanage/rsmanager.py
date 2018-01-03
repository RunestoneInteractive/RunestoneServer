import subprocess, os, re, signal
import click
from sqlalchemy import create_engine

class Config(object):
    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)

# configuration
REQ_ENV = ['WEB2PY_CONFIG', 'DBURL']
OPT_ENV = ['TEST_DBURL','WEB2PY_MIGRATE']
APP = 'runestone'
APP_PATH = 'applications/{}'.format(APP)
DBSDIR = '{}/databases'.format(APP_PATH)


@click.group()
@click.option("--verbose", is_flag=True, help="More verbose output")
@pass_config
def cli(config, verbose):
    """Type subcommand --help for help on any subcommand"""
    checkEnvironment()

    conf = os.environ.get("WEB2PY_CONFIG", "production")

    if conf == 'production':
        config.dburl = os.environ.get("DBURL")
    elif conf == 'development':
        config.dburl = os.environ.get("DEV_DBURL")
    elif conf == 'test':
        config.dburl = os.environ.get("TEST_DBURL")
    else:
        click.echo("Incorrect WEB2PY_CONFIG")
        sys.exit(1)

    config.dbname = re.match(r'postgres.*//.*?@.*?/(.*)', config.dburl).group(1)

    if verbose:
        click.echo("WEB2PY_CONFIG is {}".format(conf))
        click.echo("DBURL is {}".format(config.dburl))
        click.echo("DBNAME is {}".format(config.dbname))

    config.verbose = verbose

@cli.command()
@click.option("--list_tables", is_flag=True, help="List all of the defined tables when done")
@click.option("--reset", is_flag=True, help="drop database and delete all migration information")
@pass_config
def initdb(config, list_tables, reset):
    """Initialize and optionally reset the database"""
    os.chdir(findProjectRoot())
    if not os.path.exists(DBSDIR):
        click.echo("Making databases folder")
        os.mkdir(DBSDIR)

    if reset:
        click.confirm("Resetting the database will delete the database and the contents of the databases folder.  Are you sure?", default=False, abort=True, prompt_suffix=': ', show_default=True, err=False)
        res = subprocess.call("dropdb {}".format(config.dbname),shell=True)
        if res == 0:
            res = subprocess.call("createdb --echo {}".format(config.dbname),shell=True)
        else:
            click.echo("Failed to drop the database do you have permission?")
            sys.exit(1)

        click.echo("Removing all files in databases/")
        for the_file in os.listdir(DBSDIR):
            file_path = os.path.join(DBSDIR, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)


    if len(os.listdir("{}/databases".format(APP_PATH))) > 1:
        click.confirm("It appears you already have database migration information do you want to proceed?", default=False, abort=True, prompt_suffix=': ', show_default=True, err=False)

    click.echo(message='Initializing the database', file=None, nl=True, err=False, color=None)

    list_tables = "-A --list_tables" if config.verbose or list_tables else ""
    cmd = "python web2py.py -S {} -M -R {}/rsmanage/initialize_tables.py {}".format(APP, APP_PATH, list_tables)
    click.echo("Running: {}".format(cmd))
    res = subprocess.call(cmd, shell=True)

    if res != 0:
        click.echo(message="Database Initialization Failed")

@cli.command()
@click.option("--with-scheduler", is_flag=True, help="Star the background task scheduler too")
@pass_config
def run(config, with_scheduler):
    """Starts up the runestone server and optionally scheduler"""
    os.chdir(findProjectRoot())
    res = subprocess.Popen("python -u web2py.py --ip=0.0.0.0 --port=8000 --password='<recycle>' -d rs.pid -K runestone --nogui -X", shell=True)

@cli.command()
@pass_config
def shutdown(config):
    """Shutdown the server and any schedulers"""
    os.chdir(findProjectRoot())
    with open('rs.pid', 'r') as pfile:
        pid = int(pfile.read())

    click.echo("killing process {}".format(pid))
    os.kill(pid, signal.SIGINT)

    # select worker_name from scheduler_worker;
    # iterate over results to kill all schedulers
    eng = create_engine(config.dburl)
    res = eng.execute("select worker_name from scheduler_worker")
    for row in res:
        # result will be form of hostname#pid
        os.kill(int(row[0].split("#")[1]), signal.SIGINT)

@cli.command()
@pass_config
def addbook(config):
    """Create a course and build the book -- coming soon"""
    pass

@cli.command()
@click.option("--instructor", is_flag=True, help="Make this user an instructor")
@click.option("--fromfile", default="-", type=click.File(mode="r"), help="Make this user an instructor")
@pass_config
def inituser(config):
    """Add a user (or users)-- coming soon"""
    pass


# Utility Functions Below here

def checkEnvironment():
    """
    Check the list of required and optional environment variables to be sure they are defined.
    """
    stop = False
    for var in REQ_ENV:
        if var not in os.environ:
            stop = True
            click.echo("Missing definition for {} environment variable".format(var))

    for var in OPT_ENV:
        if var not in os.environ:
            click.echo("You may want to define the {} environment variable".format(var))

    if stop:
        sys.exit(1)


def findProjectRoot():
    start = os.getcwd()
    prevdir = ""
    while start != prevdir:
        if os.path.exists(os.path.join(start,'web2py.py')):
            return start
        prevdir = start
        start = os.path.dirname(start)
    raise IOError("You must be in a web2py application to run rsmanage")
