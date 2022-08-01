import sys
from pathlib import Path

# Launch into the Docker container before attempting imports that are only installed there. (If Docker isn't installed, we assume the current venv already contains the necessary packages.)
wd = (Path(__file__).parents[1]).resolve()
sys.path.extend([str(wd / "docker"), str(wd / "tests")])
try:
    # Assume that a development version of the Runestone Server -- meaning the presence of `../docker/docker_tools_misc.py` -- implies Docker.
    from docker_tools_misc import ensure_in_docker, in_docker

    ensure_in_docker(True)
except ModuleNotFoundError:
    pass

import asyncio
import click
import csv
import json
import os
import re
import shutil
import signal
import subprocess
import redis
import xml.etree.ElementTree as ET
from xml.etree import ElementInclude

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from pgcli.main import cli as clipg
from psycopg2.errors import UniqueViolation

from bookserver.crud import create_initial_courses_users
from bookserver.db import init_models, term_models
from bookserver.config import settings
from runestone.pretext.chapter_pop import manifest_data_to_db
from runestone.server.utils import _build_runestone_book, _build_ptx_book


class Config(object):
    def __init__(self):
        self.verbose = False


pass_config = click.make_pass_decorator(Config, ensure=True)

# configuration
REQ_ENV = ["WEB2PY_CONFIG", "DBURL"]
OPT_ENV = ["WEB2PY_MIGRATE"]
APP = "runestone"
APP_PATH = "applications/{}".format(APP)
DBSDIR = "{}/databases".format(APP_PATH)
BUILDDIR = "{}/build".format(APP_PATH)
PRIVATEDIR = "{}/private".format(APP_PATH)
BOOKSDIR = f"{APP_PATH}/books"


@click.group(chain=True)
@click.option("--verbose", is_flag=True, help="More verbose output")
@click.option("--if_clean", is_flag=True, help="only run if database is uninitialized")
@pass_config
def cli(config, verbose, if_clean):
    """Type subcommand --help for help on any subcommand"""
    checkEnvironment()

    conf = os.environ.get("WEB2PY_CONFIG", "production")

    if conf == "production":
        config.dburl = os.environ.get("DBURL")
    elif conf == "development":
        config.dburl = os.environ.get("DEV_DBURL")
    elif conf == "test":
        config.dburl = os.environ.get("TEST_DBURL")
    else:
        click.echo("Incorrect WEB2PY_CONFIG")
        sys.exit(1)

    # DAL uses "postgres:", while SQLAlchemy (and the PostgreSQL spec) uses "postgresql:". Fix.
    remove_prefix = "postgres://"
    if config.dburl.startswith(remove_prefix):
        config.dburl = "postgresql://" + config.dburl[len(remove_prefix) :]

    config.conf = conf
    config.dbname = re.match(r"postgres.*//.*?@.*?/(.*)", config.dburl).group(1)
    config.dbhost = re.match(r"postgres.*//.*?@(.*?)/(.*)", config.dburl).group(1)
    if conf != "production":
        config.dbuser = re.match(
            r"postgres.*//(.*?)(:.*?)?@(.*?)/(.*)", config.dburl
        ).group(1)
    else:
        config.dbuser = re.match(
            r"postgres.*//(.*?):(.*?)@(.*?)/(.*)", config.dburl
        ).group(1)

    config.dbpass = os.environ.get("POSTGRES_PASSWORD")
    if verbose:
        echoEnviron(config)

    if if_clean:
        count = check_db_for_useinfo(config)
        if count != 0:
            click.echo("The database is already inititlized Exiting")
            sys.exit()

    config.verbose = verbose


def _initdb(config):
    # Because click won't natively support making commands async we can use this simple method
    # to call async functions.
    # Since we successfully dropped the database we need to initialize it here.
    async def async_funcs():
        await init_models()
        await create_initial_courses_users()
        await term_models()

    asyncio.run(async_funcs())

    os.environ["WEB2PY_MIGRATE"] = "Yes"
    subprocess.call(
        f"{sys.executable} web2py.py -S runestone -M -R applications/runestone/rsmanage/noop.py",
        shell=True,
    )

    eng = create_engine(config.dburl)
    eng.execute("""insert into auth_group (role) values ('instructor')""")
    eng.execute("""insert into auth_group (role) values ('editor')""")


#
#    initdb
#
@cli.command()
@click.option(
    "--list_tables", is_flag=True, help="List all of the defined tables when done"
)
@click.option(
    "--reset", is_flag=True, help="drop database and delete all migration information"
)
@click.option("--fake", is_flag=True, help="perform a fake migration")
@click.option("--force", is_flag=True, help="answer Yes to confirm questions")
@pass_config
def initdb(config, list_tables, reset, fake, force):
    """Initialize and optionally reset the database"""
    os.chdir(findProjectRoot())
    if not os.path.exists(DBSDIR):
        click.echo("Making databases folder")
        os.mkdir(DBSDIR)

    if reset:
        if not force:
            click.confirm(
                "Resetting the database will delete the database and the contents of the databases folder.  Are you sure?",
                default=False,
                abort=True,
                prompt_suffix=": ",
                show_default=True,
                err=False,
            )
        # If PGPASSWORD is not set in the environment then it will prompt for password
        res = subprocess.call(
            f"dropdb --if-exists --force --host={config.dbhost} --username={config.dbuser} {config.dbname}",
            shell=True,
        )
        res = subprocess.call(
            f"createdb --host={config.dbhost} --username={config.dbuser} --owner={config.dbuser} {config.dbname}",
            shell=True,
        )
        if res != 0:
            click.echo("Failed to drop the database do you have permission?")
            sys.exit(1)

        click.echo("Removing all files in databases/")
        table_migrate_prefix = "runestone_"
        if config.conf == "test":
            table_migrate_prefix = "test_runestone_"
        for the_file in os.listdir(DBSDIR):
            file_path = os.path.join(DBSDIR, the_file)
            try:
                if os.path.isfile(file_path) and file_path.startswith(
                    os.path.join(DBSDIR, table_migrate_prefix)
                ):
                    print(f"removing {file_path}")
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        # Because click won't natively support making commands async we can use this simple method
        # to call async functions.
        # Since we successfully dropped the database we need to initialize it here.
        settings.drop_tables = "Yes"
        _initdb(config)
        click.echo("Created new tables")

    if len(os.listdir("{}/databases".format(APP_PATH))) > 1 and not fake and not force:
        click.confirm(
            "It appears you already have database migration information do you want to proceed?",
            default=False,
            abort=True,
            prompt_suffix=": ",
            show_default=True,
            err=False,
        )

    click.echo(
        message="Initializing the database", file=None, nl=True, err=False, color=None
    )

    if not reset:
        _initdb(config)


@cli.command()
@click.option("--fake", is_flag=True, help="perform a fake migration")
@pass_config
def migrate(config, fake):
    "Startup web2py and load the models with Migrate set to Yes"
    os.chdir(findProjectRoot())

    if fake:
        os.environ["WEB2PY_MIGRATE"] = "fake"
    else:
        os.environ["WEB2PY_MIGRATE"] = "Yes"

    subprocess.call(
        f"{sys.executable} web2py.py -S runestone -M -R applications/runestone/rsmanage/migrate.py",
        shell=True,
    )


#
#    addcourse
#


@cli.command()
@click.option("--course-name", help="The name of a course to create")
@click.option("--basecourse", help="The name of the basecourse")
@click.option(
    "--start-date", default="2001-01-01", help="Start Date for the course in YYYY-MM-DD"
)
@click.option("--python3/--no-python3", default=True, help="Use python3 style syntax")
@click.option(
    "--login-required/--no-login-required",
    help="Only registered users can access this course?",
)
@click.option("--institution", help="Your institution")
@click.option("--courselevel", help="Your course level", default="unknown")
@click.option("--allowdownloads", help="enable download button", default="F")
@click.option("--language", default="python", help="Default Language for your course")
@click.option("--host", default="runestone.academy", help="runestone server host name")
@click.option(
    "--newserver/--no-newserver", default=True, help="use the new book server"
)
@click.option(
    "--allow_pairs/--no-allow-pairs",
    default=False,
    help="enable experimental pair programming support",
)
@pass_config
def addcourse(
    config,
    course_name,
    basecourse,
    start_date,
    python3,
    login_required,
    institution,
    courselevel,
    allowdownloads,
    language,
    host,
    newserver,
    allow_pairs,
):
    """Create a course in the database"""

    os.chdir(findProjectRoot())  # change to a known location
    eng = create_engine(config.dburl)
    done = False
    if course_name:
        use_defaults = True
    else:
        use_defaults = False
    while not done:
        if not course_name:
            course_name = click.prompt("Course Name")
        if not python3 and not use_defaults:
            python3 = (
                "T" if click.confirm("Use Python3 style syntax?", default="T") else "F"
            )
        else:
            python3 = "T" if python3 else "F"
        if not basecourse and not use_defaults:
            basecourse = click.prompt("Base Course")
        if not start_date and not use_defaults:
            start_date = click.prompt("Start Date YYYY-MM-DD")
        if not institution and not use_defaults:
            institution = click.prompt("Your institution")
        # TODO: these prompts make no sense -- only ask for them if the option was False??? Looks like a copy-and-paste error.
        if not login_required and not use_defaults:
            login_required = (
                "T" if click.confirm("Require users to log in", default="T") else "F"
            )
        else:
            login_required = "T" if login_required else "F"
        if not allow_pairs and not use_defaults:
            allow_pairs = (
                "T"
                if click.confirm("Enable pair programming support", default=False)
                else "F"
            )
        else:
            allow_pairs = "T" if allow_pairs else "F"

        res = eng.execute(
            "select id from courses where course_name = '{}'".format(course_name)
        ).first()
        if not res:
            done = True
        else:
            click.confirm(
                "Course {} already exists continue with a different name?".format(
                    course_name
                ),
                default=True,
                abort=True,
            )

    eng.execute(
        f"""insert into courses
           (course_name, base_course, python3, term_start_date, login_required, institution, courselevel, downloads_enabled, allow_pairs, new_server)
                values ('{course_name}',
                '{basecourse}',
                '{python3}',
                '{start_date}',
                '{login_required}',
                '{institution}',
                '{courselevel}',
                '{allowdownloads}',
                '{allow_pairs}',
                '{"T" if newserver else "F"}')
                """
    )

    click.echo("Course added to DB successfully")


#
#    build
#


@cli.command()
@click.option("--clone", default=None, help="clone the given repo before building")
@click.option("--ptx", is_flag=True, help="Build a PreTeXt book")
@click.option(
    "--gen", is_flag=True, help="Build PreTeXt generated assets (a one time thing)"
)
@click.option("--manifest", default="runestone-manifest.xml", help="Manifest file")
@click.argument("course", nargs=1)
@pass_config
def build(config, clone, ptx, gen, manifest, course):
    """
    rsmanage build [options] COURSE
    Build the book for an existing course
    """
    os.chdir(findProjectRoot())  # change to a known location
    eng = create_engine(config.dburl)
    res = eng.execute(
        "select id from courses where course_name = '{}'".format(course)
    ).first()
    if not res:
        click.echo(
            "Error:  The course {} must already exist in the database -- use rsmanage addcourse".format(
                course
            ),
            color="red",
        )
        exit(1)

    os.chdir(BOOKSDIR)
    if clone:
        if os.path.exists(course):
            click.echo("Book repo already cloned, skipping")
        else:
            res = subprocess.call("git clone {}".format(clone), shell=True)
            if res != 0:
                click.echo(
                    "Cloning the repository failed, please check the URL and try again"
                )
                exit(1)

    # proj_dir = os.path.basename(repo).replace(".git", "")
    click.echo("Switching to book dir {}".format(course))
    os.chdir(course)
    if ptx:
        _build_ptx_book(config, gen, manifest, course)

    else:
        _build_runestone_book(course)


#
#    inituser
#


@cli.command()
@click.option("--instructor", is_flag=True, help="Make this user an instructor")
@click.option(
    "--fromfile",
    default=None,
    type=click.File(mode="r"),
    help="read a csv file of users of the form username, email, first_name, last_name, password, course",
)
@click.option("--username", help="Username, must be unique")
@click.option("--password", help="password - plaintext -- sorry")
@click.option("--first_name", help="Real first name")
@click.option("--last_name", help="Real last name")
@click.option("--email", help="email address for password resets")
@click.option("--course", help="course to register for")
@click.option(
    "--ignore_dupes",
    is_flag=True,
    help="ignore duplicate student errors and keep processing",
)
@pass_config
def adduser(
    config,
    instructor,
    fromfile,
    username,
    password,
    first_name,
    last_name,
    email,
    course,
    ignore_dupes,
):
    """Add a user (or users from a csv file)"""
    os.chdir(findProjectRoot())
    mess = [
        "Success",
        "Value Error -- check the format of your CSV file",
        "Duplicate User -- Check your data or use --ignore_dupes if you are adding students to an existing CSV",
        "Unknown Error -- check the format of your CSV file",
    ]
    if fromfile:
        # if fromfile then be sure to get the full path name NOW.
        # csv file should be username, email first_name, last_name, password, course
        # users from a csv cannot be instructors
        for line in csv.reader(fromfile):
            if len(line) != 6:
                click.echo("Not enough data to create a user.  Lines must be")
                click.echo("username, email first_name, last_name, password, course")
                exit(1)
            if "@" not in line[1]:
                click.echo("emails should have an @ in them in column 2")
                exit(1)
            userinfo = {}
            userinfo["username"] = line[0]
            userinfo["password"] = line[4]
            userinfo["first_name"] = line[2]
            userinfo["last_name"] = line[3]
            userinfo["email"] = line[1]
            userinfo["course"] = line[5]
            userinfo["instructor"] = False
            os.environ["RSM_USERINFO"] = json.dumps(userinfo)
            res = subprocess.call(
                f"{sys.executable} web2py.py --no-banner -S runestone -M -R applications/runestone/rsmanage/makeuser.py",
                shell=True,
            )
            if res != 0:
                click.echo(
                    "Failed to create user {} error {}".format(line[0], mess[res])
                )
                if res == 2 and ignore_dupes:
                    click.echo(f"ignoring duplicate user {userinfo['username']}")
                    continue
                else:
                    exit(res)

    else:
        userinfo = {}
        userinfo["username"] = username or click.prompt("Username")
        userinfo["password"] = password or click.prompt("Password", hide_input=True)
        userinfo["first_name"] = first_name or click.prompt("First Name")
        userinfo["last_name"] = last_name or click.prompt("Last Name")
        userinfo["email"] = email or click.prompt("email address")
        userinfo["course"] = course or click.prompt("course name")
        if not instructor:
            if (
                username and course
            ):  # user has supplied other info via CL parameter safe to assume False
                userinfo["instructor"] = False
            else:
                userinfo["instructor"] = click.confirm(
                    "Make this user an instructor", default=False
                )

        os.environ["RSM_USERINFO"] = json.dumps(userinfo)
        res = subprocess.call(
            f"{sys.executable} web2py.py --no-banner -S runestone -M -R applications/runestone/rsmanage/makeuser.py",
            shell=True,
        )
        if res != 0:
            click.echo(
                "Failed to create user {} error {} fix your data and try again. Use --verbose for more detail".format(
                    userinfo["username"], res
                )
            )
            exit(1)
        else:
            click.echo("Success")


@cli.command()
@click.option("--username", help="Username, must be unique")
@click.option("--password", help="password - plaintext -- sorry")
@pass_config
def resetpw(config, username, password):
    """Utility to change a users password. Useful If they can't do it through the normal mechanism"""
    os.chdir(findProjectRoot())
    userinfo = {}
    userinfo["username"] = username or click.prompt("Username")
    userinfo["password"] = password or click.prompt("Password", hide_input=True)
    eng = create_engine(config.dburl)
    res = eng.execute(
        "select * from auth_user where username = %s", userinfo["username"]
    ).first()
    if not res:
        click.echo("ERROR - User: {} does not exist.".format(userinfo["username"]))
        exit(1)

    os.environ["RSM_USERINFO"] = json.dumps(userinfo)
    res = subprocess.call(
        f"{sys.executable} web2py.py --no-banner -S runestone -M -R applications/runestone/rsmanage/makeuser.py -A --resetpw",
        shell=True,
    )
    if res != 0:
        click.echo(
            "Failed to create user {} error {} fix your data and try again. Use --verbose for more detail".format(
                userinfo["username"], res
            )
        )
        exit(1)
    else:
        click.echo("Success")


@cli.command()
@click.option("--username", help="Username, must be unique")
@pass_config
def rmuser(config, username):
    """Utility to remove a user from the system completely."""
    os.chdir(findProjectRoot())
    sid = username or click.prompt("Username")

    eng = create_engine(config.dburl)
    eng.execute("delete from auth_user where username = %s", sid)
    eng.execute("delete from useinfo where sid = %s", sid)
    eng.execute("delete from code where sid = %s", sid)
    for t in [
        "clickablearea",
        "codelens",
        "dragndrop",
        "fitb",
        "lp",
        "mchoice",
        "parsons",
        "shortanswer",
    ]:
        eng.execute("delete from {}_answers where sid = '{}'".format(t, sid))


@cli.command()
@click.option("--checkdb", is_flag=True, help="check state of db and databases folder")
@pass_config
def env(config, checkdb):
    """Print out your configured environment
    If --checkdb is used then env will exit with one of the following exit codes
        0: no database, no database folder
        1: no database but databases folder
        2: database exists but no databases folder
        3: both database and databases folder exist
    """
    os.chdir(findProjectRoot())
    dbinit = 0
    dbdir = 0
    if checkdb:
        count = check_db_for_useinfo(config)
        if count == 0:
            dbinit = 0
            print("Database not initialized")
        else:
            dbinit = 2
            print("Database is initialized")

        if os.path.exists(DBSDIR):
            dbdir = 1
            print("Database migration folder exists")
        else:
            dbdir = 0
            print("No Database Migration Folder")

    if not checkdb or config.verbose:
        echoEnviron(config)

    print("Exiting with result of {}".format(dbinit | dbdir))

    sys.exit(dbinit | dbdir)


@cli.command()
@click.option("--username", default=None, help="user to promote to instructor")
@click.option("--course", default=None, help="name of course")
@pass_config
def addinstructor(config, username, course):
    """
    Add an existing user as an instructor for a course
    """
    eng = create_engine(config.dburl)
    username = username or click.prompt("Username")
    course = course or click.prompt("Course name")

    res = eng.execute("select id from auth_user where username=%s", username).first()
    if res:
        userid = res[0]
    else:
        print("Sorry, that user does not exist")
        sys.exit(-1)

    res = eng.execute("select id from courses where course_name=%s", course).first()
    if res:
        courseid = res[0]
    else:
        print("Sorry, that course does not exist")
        sys.exit(-1)

    # if needed insert a row into auth_membership
    res = eng.execute("select id from auth_group where role='instructor'").first()
    if res:
        role = res[0]
    else:
        print(
            "Sorry, your system does not have the instructor role setup -- this is bad"
        )
        sys.exit(-1)

    res = eng.execute(
        "select * from auth_membership where user_id=%s and group_id=%s", userid, role
    ).first()
    if not res:
        eng.execute(
            "insert into auth_membership (user_id, group_id) values (%s, %s)",
            userid,
            role,
        )
        print("made {} an instructor".format(username))
    else:
        print("{} is already an instructor".format(username))

    # if needed insert a row into user_courses
    res = eng.execute(
        "select * from user_courses where user_id=%s and course_id=%s ",
        userid,
        courseid,
    ).first()
    if not res:
        eng.execute(
            "insert into user_courses (user_id, course_id) values (%s, %s)",
            userid,
            courseid,
        )
        print("enrolled {} in {}".format(username, course))
    else:
        print("{} is already enrolled in {}".format(username, course))

    # if needed insert a row into course_instructor
    res = eng.execute(
        "select * from course_instructor where instructor=%s and course=%s ",
        userid,
        courseid,
    ).first()
    if not res:
        eng.execute(
            "insert into course_instructor (instructor, course) values (%s, %s)",
            userid,
            courseid,
        )
        print("made {} and instructor for {}".format(username, course))
    else:
        print("{} is already an instructor for {}".format(username, course))


@cli.command()
@click.option("--username", help="user to promote to instructor")
@click.option("--basecourse", help="name of base course")
@pass_config
def addeditor(config, username, basecourse):
    """
    Add an existing user as an instructor for a course
    """
    eng = create_engine(config.dburl)
    res = eng.execute("select id from auth_user where username=%s", username).first()
    if res:
        userid = res[0]
    else:
        click.echo("Sorry, that user does not exist", color="red")
        sys.exit(-1)

    res = eng.execute(
        "select id from courses where course_name=%s and base_course=%s",
        basecourse,
        basecourse,
    ).first()
    if not res:
        click.echo("Sorry, that base course does not exist", color="red")
        sys.exit(-1)

    # if needed insert a row into auth_membership
    res = eng.execute("select id from auth_group where role='editor'").first()
    if res:
        role = res[0]
    else:
        click.echo(
            "Sorry, your system does not have the editor role setup -- this is bad",
            color="red",
        )
        sys.exit(-1)

    res = eng.execute(
        "select * from auth_membership where user_id=%s and group_id=%s", userid, role
    ).first()
    if not res:
        eng.execute(
            "insert into auth_membership (user_id, group_id) values (%s, %s)",
            userid,
            role,
        )
        click.echo("made {} an editor".format(username), color="green")
    else:
        click.echo("{} is already an editor".format(username), color="red")

    # if needed insert a row into user_courses
    res = eng.execute(
        "select * from editor_basecourse where editor=%s and base_course=%s ",
        userid,
        basecourse,
    ).first()
    if not res:
        eng.execute(
            "insert into editor_basecourse (editor, base_course) values (%s, %s)",
            userid,
            basecourse,
        )
        click.echo(
            "made {} an editor for {}".format(username, basecourse), color="green"
        )
    else:
        click.echo(
            "{} is already an editor for {}".format(username, basecourse), color="red"
        )


@cli.command()
@click.option("--name", help="Name of the course")
@pass_config
def courseinfo(config, name):
    """
    List all information for a single course

    """
    eng = create_engine(config.dburl)
    if not name:
        name = click.prompt("What course do you want info about?")

    course = eng.execute(
        """select id, term_start_date, institution, base_course from courses where course_name = %s""",
        name,
    ).first()
    cid = course[0]
    start_date = course[1]
    inst = course[2]
    bc = course[3]

    s_count = eng.execute(
        """select count(*) from user_courses where course_id=%s""", cid
    ).first()[0]

    res = eng.execute(
        """select username, first_name, last_name, email, courses.course_name
    from auth_user
    join course_instructor ON course_instructor.instructor = auth_user.id
    join courses ON courses.id = course_instructor.course
    where course_instructor.course = %s
    order by username;""",
        cid,
    )

    print("Course Information for {} -- ({})".format(name, cid))
    print(inst)
    print("Base course: {}".format(bc))
    print("Start date: {}".format(start_date))
    print("Number of students: {}".format(s_count))
    print("Instructors:")
    for row in res:
        print(" ".join(row[:-1]))


@cli.command()
@click.option("--student", default=None, help="Name of the student")
@pass_config
def studentinfo(config, student):
    """
    display PII and all courses enrolled for a username
    """
    eng = create_engine(config.dburl)

    if not student:
        student = click.prompt("Student Id: ")

    res = eng.execute(
        f"""
        select auth_user.id, first_name, last_name, email, courses.course_name, courses.id 
        from auth_user join user_courses ON user_courses.user_id = auth_user.id 
        join courses on courses.id = user_courses.course_id where username = '{student}'"""
    )
    print(f"res = {res}")
    # fetchone fetches the first row without closing the cursor.
    first = res.fetchone()
    print(student)
    print("id\tFirst\tLast\temail")
    print("\t".join(str(x) for x in first[:4]))
    print("")
    print("         Course        cid")
    print("--------------------------")
    print(f"{first[-2].rjust(15)} {str(first[-1]).rjust(10)}")
    if res:
        for row in res:
            print(f"{row[-2].rjust(15)} {str(row[-1]).rjust(10)}")


@cli.command()
@click.option("--course", default=None, help="Name of the course")
@click.option("--attr", default=None, help="Attribute to add")
@click.option("--value", default=None, help="Attribute Value")
@pass_config
def addattribute(config, course, attr, value):
    """
    Add an attribute to the `course_attributes` table

    """
    course = course or click.prompt("Name of the course ")
    attr = attr or click.prompt("Attribute to set: ")
    value = value or click.prompt(f"Value of {attr}: ")

    eng = create_engine(config.dburl)

    res = eng.execute("select id from courses where course_name=%s", course).first()
    if res:
        course_id = res[0]
    else:
        print("Sorry, that course does not exist")
        sys.exit(-1)
    try:
        res = eng.execute(
            f"""insert into course_attributes (course_id, attr, value)
        values ({course_id}, '{attr}', '{value}')"""
        )
    except UniqueViolation:
        click.echo(f"Can only have one attribute {attr} per course")
    except IntegrityError:
        click.echo(f"Can only have one attribute {attr} per course")

    click.echo("Success")


@cli.command()
@click.option(
    "--course", help="The name of a course that should already exist in the DB"
)
@pass_config
def instructors(config, course):
    """
    List instructor information for all courses or just for a single course

    """
    eng = create_engine(config.dburl)
    where_clause = ""
    if course:
        where_clause = "where courses.course_name = '{}'".format(course)

    res = eng.execute(
        """select username, first_name, last_name, email, courses.course_name
    from auth_user
    join course_instructor ON course_instructor.instructor = auth_user.id
    join courses ON courses.id = course_instructor.course
    {}
    order by username;""".format(
            where_clause
        )
    )
    outline = ""
    row = next(res)
    current = row[0]
    outline = "{:<10} {:<10} {:<10} {:<20} {}".format(*row)
    for row in res:
        if row[0] == current:
            outline += " {}".format(row[-1])
        else:
            print(outline)
            outline = "{:<10} {:<10} {:<10} {:<20} {}".format(*row)
            current = row[0]
    print(outline)


#
#    grade
#


@cli.command()
@click.option("--enforce", is_flag=True, help="Enforce deadline when grading")
@click.option(
    "--course", help="The name of a course that should already exist in the DB"
)
@click.option("--pset", help="Database ID of the Problem Set")
@pass_config
def grade(config, course, pset, enforce):
    """Grade a problem set; hack for long-running grading processes"""
    os.chdir(findProjectRoot())

    userinfo = {}
    userinfo["course"] = course if course else click.prompt("Name of course")
    userinfo["pset"] = pset if pset else click.prompt("Problem Set ID")
    userinfo["enforce_deadline"] = (
        enforce if enforce else click.confirm("Enforce deadline?", default=True)
    )
    os.environ["RSM_USERINFO"] = json.dumps(userinfo)

    subprocess.call(
        f"{sys.executable} web2py.py -S runestone -M -R applications/runestone/rsmanage/grade.py",
        shell=True,
    )


@cli.command()
@click.option("--course", help="name of course")
@pass_config
def findinstructor(config, course):
    """
    Print the PII of the instructor for a given course.
    """
    if not course:
        course = click.prompt("enter the course name")
    eng = create_engine(config.dburl)
    query = """
    select username, first_name, last_name, email
from auth_user join course_instructor on auth_user.id = instructor join courses on course = courses.id
where courses.course_name = %s order by last_name
"""
    res = eng.execute(query, course)

    if res:
        for row in res:
            print("{} {} {} {}").format(
                row.first_name, row.last_name, row.email, row.username
            )
    else:
        print("No instructors found for {}".format(course))


@cli.command()
@pass_config
def db(config):
    """
    Connect to the database based on the current configuration
    """
    # replace argv[1] which is 'db' with the url to connect to
    sys.argv[1] = config.dburl
    sys.exit(clipg())


#
# Utility Functions Below here
#


def checkEnvironment():
    """
    Check the list of required and optional environment variables to be sure they are defined.
    """
    stop = False
    assert os.environ["WEB2PY_CONFIG"]
    config = os.environ["WEB2PY_CONFIG"]

    if config == "production":
        for var in REQ_ENV:
            if var not in os.environ:
                stop = True
                click.echo("Missing definition for {} environment variable".format(var))
    elif config == "test":
        if "TEST_DBURL" not in os.environ:
            stop = True
            click.echo("Missing definition for TEST_DBURL environment variable")
    elif config == "development":
        if "DEV_DBURL" not in os.environ:
            stop = True
            click.echo("Missing definition for DEV_DBURL environment variable")

    for var in OPT_ENV:
        if var not in os.environ:
            click.echo("You may want to define the {} environment variable".format(var))

    if stop:
        sys.exit(1)


def echoEnviron(config):
    click.echo("WEB2PY_CONFIG is {}".format(config.conf))
    click.echo("The database URL is configured as {}".format(config.dburl))
    click.echo("DBNAME is {}".format(config.dbname))


def findProjectRoot():
    start = os.getcwd()
    prevdir = ""
    while start != prevdir:
        if os.path.exists(os.path.join(start, "web2py.py")):
            return start
        prevdir = start
        start = os.path.dirname(start)
    if in_docker():
        return "/srv/web2py"

    raise IOError("You must be in a web2py application to run rsmanage")


#
#    fill_practice_log_missings
#


@cli.command()
@pass_config
def fill_practice_log_missings(config):
    """Only for one-time use to fill out the missing values of the columns that we added to user_topic_practice_log table during the semester."""
    os.chdir(findProjectRoot())

    subprocess.call(
        f"{sys.executable} web2py.py -S runestone -M -R applications/runestone/rsmanage/fill_practice_log_missings.py",
        shell=True,
    )


def check_db_for_useinfo(config):
    eng = create_engine(config.dburl)
    res = eng.execute("select count(*) from pg_class where relname = 'useinfo'")
    count = res.first()[0]
    return count


@cli.command()
@click.option("--course", help="name of course")
def peergroups(course):
    r = redis.from_url(os.environ.get("REDIS_URI", "redis://redis:6379/0"))
    ap = r.hgetall(f"partnerdb_{course}")
    if len(ap) > 0:
        for x in ap.items():
            click.echo(x)
    else:
        click.echo(f"No Peer Groups found for {course}")


if __name__ == "__main__":
    cli()
