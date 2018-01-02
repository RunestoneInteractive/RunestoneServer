import subprocess, os
import click

class Config(object):
    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)

# configuration
REQ_ENV = ['WEB2PY_CONFIG', 'DBURL']
OPT_ENV = ['TEST_DBURL','WEB2PY_MIGRATE']
APP = 'runestone'
APP_PATH = 'applications/{}'.format(APP)

@click.group()
@click.option("--verbose", is_flag=True, help="More verbose output")
@pass_config
def cli(config, verbose):
    checkEnvironment()
    config.verbose = verbose

@cli.command()
@click.option("--list_tables", is_flag=True, help="List all of the defined tables when done")
@pass_config
def initdb(config, list_tables):
    os.chdir(findProjectRoot())
    click.echo(message='Initializing the database', file=None, nl=True, err=False, color=None)
    list_tables = "-A --list_tables" if config.verbose or list_tables else ""
    cmd = "python web2py.py -S {} -M -R {}/rsmanage/initialize_tables.py {}".format(APP, APP_PATH, list_tables)
    click.echo("Running: {}".format(cmd))
    res = subprocess.call(cmd, shell=True)

    if res != 0:
        click.echo(message="Database Initialization Failed")

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
