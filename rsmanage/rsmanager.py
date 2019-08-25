import subprocess, os, re, signal, json, sys, csv, shutil
import click
from sqlalchemy import create_engine
from pkg_resources import resource_string, resource_filename


class Config(object):
    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)

# configuration
REQ_ENV = ['WEB2PY_CONFIG', 'DBURL']
OPT_ENV = ['WEB2PY_MIGRATE']
APP = 'runestone'
APP_PATH = 'applications/{}'.format(APP)
DBSDIR = '{}/databases'.format(APP_PATH)
BUILDDIR = '{}/build'.format(APP_PATH)
PRIVATEDIR = '{}/private'.format(APP_PATH)
CUSTOMDIR = '{}/custom_courses'.format(APP_PATH)

@click.group(chain=True)
@click.option("--verbose", is_flag=True, help="More verbose output")
@click.option("--if_clean", is_flag=True, help="only run if database is uninitialized")
@pass_config
def cli(config, verbose, if_clean):
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

    config.conf = conf
    config.dbname = re.match(r'postgres.*//.*?@.*?/(.*)', config.dburl).group(1)
    config.dbhost = re.match(r'postgres.*//.*?@(.*?)/(.*)', config.dburl).group(1)
    config.dbuser = re.match(r'postgres.*//(.*?):.*?@(.*?)/(.*)', config.dburl).group(1)

    if verbose:
        echoEnviron(config)

    if if_clean:
        count = check_db_for_useinfo(config)
        if count != 0:
            click.echo("The database is already inititlized Exiting")
            sys.exit()


    config.verbose = verbose

#
#    initdb
#
@cli.command()
@click.option("--list_tables", is_flag=True, help="List all of the defined tables when done")
@click.option("--reset", is_flag=True, help="drop database and delete all migration information")
@click.option("--fake", is_flag=True, help="perform a fake migration")
@click.option("--force", is_flag=True, help="answer Yes to confirm questions")
@pass_config
def initdb(config, list_tables, reset, fake, force):
    """Initialize and optionally reset the database"""
    os.chdir(findProjectRoot())
    if not os.path.exists(DBSDIR):
        click.echo("Making databases folder")
        os.mkdir(DBSDIR)

    if not os.path.exists(PRIVATEDIR):
        click.echo("Making private directory for auth")
        os.mkdir(PRIVATEDIR)

    if reset:
        if not force:
            click.confirm("Resetting the database will delete the database and the contents of the databases folder.  Are you sure?", default=False, abort=True, prompt_suffix=': ', show_default=True, err=False)
        res = subprocess.call("dropdb --if-exists --host={} --username={} {}".format(config.dbhost, config.dbuser, config.dbname),shell=True)
        if res == 0:
            res = subprocess.call("createdb --echo --host={} --username={} {}".format(config.dbhost, config.dbuser, config.dbname),shell=True)
        else:
            click.echo("Failed to drop the database do you have permission?")
            sys.exit(1)

        click.echo("Removing all files in databases/")
        table_migrate_prefix = 'runestone_'
        if config.conf == 'test':
            table_migrate_prefix = 'test_runestone_'
        for the_file in os.listdir(DBSDIR):
            file_path = os.path.join(DBSDIR, the_file)
            try:
                if os.path.isfile(file_path) and file_path.startswith(os.path.join(DBSDIR,table_migrate_prefix)):
                    print("removing ", file_path)
                    os.unlink(file_path)
            except Exception as e:
                print(e)


    if len(os.listdir("{}/databases".format(APP_PATH))) > 1 and not fake and not force:
        click.confirm("It appears you already have database migration information do you want to proceed?", default=False, abort=True, prompt_suffix=': ', show_default=True, err=False)

    click.echo(message='Initializing the database', file=None, nl=True, err=False, color=None)

    if fake:
        os.environ['WEB2PY_MIGRATE'] = 'fake'

    list_tables = "-A --list_tables" if config.verbose or list_tables else ""
    cmd = "python web2py.py --no-banner -S {} -M -R {}/rsmanage/initialize_tables.py {}".format(APP, APP_PATH, list_tables)
    click.echo("Running: {}".format(cmd))
    res = subprocess.call(cmd, shell=True)

    if res != 0:
        click.echo(message="Database Initialization Failed")

@cli.command()
@click.option("--fake", is_flag=True, help="perform a fake migration")
@pass_config
def migrate(config, fake):
    "Startup web2py and load the models with Migrate set to Yes"
    os.chdir(findProjectRoot())

    if fake:
        os.environ['WEB2PY_MIGRATE'] = 'fake'
    else:
        os.environ['WEB2PY_MIGRATE'] = 'Yes'

    subprocess.call("python web2py.py -S runestone -M -R applications/runestone/rsmanage/migrate.py", shell=True)


#
#    run
#

@cli.command()
@click.option("--with-scheduler", is_flag=True, help="Star the background task scheduler too")
@pass_config
def run(config, with_scheduler):
    """Starts up the runestone server and optionally scheduler"""
    os.chdir(findProjectRoot())
    res = subprocess.Popen("python -u web2py.py --ip=0.0.0.0 --port=8000 --password='<recycle>' -d rs.pid -K runestone --nogui -X", shell=True)

#
#    shutdown
#

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

#
#    addcourse
#

@cli.command()
@click.option("--course-name", help="The name of a course to create")
@click.option("--basecourse", help="The name of the basecourse")
@click.option("--start-date", default='2001-01-01', help="Start Date for the course in YYYY-MM-DD")
@click.option("--python3", is_flag=True, default=True, help="Use python3 style syntax")
@click.option("--login-required", is_flag=True, default=True, help="Only registered users can access this course?")
@click.option("--institution", default='Anonymous', help="Your institution")
@click.option("--language", default="python", help="Default Language for your course")
@click.option("--host", default="runestone.academy", help="runestone server host name")
@click.option("--allow_pairs", is_flag=True, default=False, help="enable experimental pair programming support")
@pass_config
def addcourse(config, course_name, basecourse, start_date, python3, login_required,
     institution, language, host, allow_pairs):
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
            python3 = 'T' if click.confirm("Use Python3 style syntax?", default='T') else 'F'
        else:
            python3 = 'T' if python3 else 'F'
        if not basecourse and not use_defaults:
            basecourse = click.prompt("Base Course")
        if not start_date and not use_defaults:
            start_date = click.prompt("Start Date YYYY-MM-DD")
        if not institution and not use_defaults:
            institution = click.prompt("Your institution")
        if not login_required and not use_defaults:
            login_required = 'T' if click.confirm("Require users to log in", default='T') else 'F'
        else:
            login_required = 'T' if login_required else 'F'
        if not allow_pairs and not use_defaults:
            allow_pairs = 'T' if click.confirm("Enable pair programming support", default=False) else 'F'
        else:
            allow_pairs = 'T' if allow_pairs else 'F'

        res = eng.execute("select id from courses where course_name = '{}'".format(course_name)).first()
        if not res:
            done = True
        else:
            click.confirm("Course {} already exists continue with a different name?".format(course_name), default=True, abort=True)

    eng.execute("""insert into courses (course_name, base_course, python3, term_start_date, login_required, institution, allow_pairs)
                values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
                """.format(course_name, basecourse, python3, start_date, login_required, institution, allow_pairs ))

    click.echo("Course added to DB successfully")


#
#    build
#

@cli.command()
@click.option("--course", help="The name of a course that should already exist in the DB")
@click.option("--repo",  help="URL to a git repository with the book to build")
@click.option("--skipclone", is_flag=True, help="avoid recloning when directory is already there")
@pass_config
def build(config, course, repo, skipclone):
    """Build the book for an existing course"""
    os.chdir(findProjectRoot())  # change to a known location
    eng = create_engine(config.dburl)
    res = eng.execute("select id from courses where course_name = '{}'".format(course)).first()
    if not res:
        click.echo("Error:  The course {} must already exist in the database -- use rsmanage addcourse".format(course), color='red')
        exit(1)

    os.chdir(BUILDDIR)
    if not skipclone:
        res = subprocess.call("git clone {}".format(repo), shell=True)
        if res != 0:
            click.echo("Cloning the repository failed, please check the URL and try again")
            exit(1)

    proj_dir = os.path.basename(repo).replace(".git","")
    click.echo("Switching to project dir {}".format(proj_dir))
    os.chdir(proj_dir)
    paver_file = os.path.join("..","..",'custom_courses',course,'pavement.py')
    click.echo("Checking for pavement {}".format(paver_file))
    if os.path.exists(paver_file):
        shutil.copy(paver_file, 'pavement.py')
    else:
        cont = click.confirm("WARNING -- NOT USING CUSTOM PAVEMENT FILE - continue")
        if not cont:
            sys.exit()

    try:
        if os.path.exists('pavement.py'):
            sys.path.insert(0, os.getcwd())
            from pavement import options, dest
        else:
            click.echo("I can't find a pavement.py file in {} you need that to build".format(os.getcwd()))
            exit(1)
    except ImportError as e:
        click.echo("You do not appear to have a good pavement.py file.")
        print(e)
        exit(1)

    if options.project_name != course:
        click.echo("Error: {} and {} do not match.  Your course name needs to match the project_name in pavement.py".format(course, project_name))
        exit(1)

    res = subprocess.call("runestone build --all", shell=True)
    if res != 0:
        click.echo("building the book failed, check the log for errors and try again")
        exit(1)
    click.echo("Build succeedeed... Now deploying to static")
    if dest != "../../static":
        click.echo("Incorrect deployment directory.  dest should be ../../static in pavement.py")
        exit(1)

    res = subprocess.call("runestone deploy", shell=True)
    if res == 0:
        click.echo("Success! Book deployed")
    else:
        click.echo("Deploy failed, check the log to see what went wrong.")

    click.echo("Cleaning up")
    os.chdir("..")
    subprocess.call("rm -rf {}".format(proj_dir), shell=True)


#
#    inituser
#

@cli.command()
@click.option("--instructor", is_flag=True, help="Make this user an instructor")
@click.option("--fromfile", default=None, type=click.File(mode="r"), help="read a csv file of users of the form username, email, first_name, last_name, password, course")
@click.option("--username", help="Username, must be unique")
@click.option("--password", help="password - plaintext -- sorry")
@click.option("--first_name", help="Real first name")
@click.option("--last_name", help="Real last name")
@click.option("--email", help="email address for password resets")
@click.option("--course", help="course to register for")
@pass_config
def inituser(config, instructor, fromfile, username, password, first_name, last_name, email, course):
    """Add a user (or users from a csv file)"""
    os.chdir(findProjectRoot())

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
            userinfo['username'] = line[0]
            userinfo['password'] = line[4]
            userinfo['first_name'] = line[2]
            userinfo['last_name'] = line[3]
            userinfo['email'] = line[1]
            userinfo['course'] = line[5]
            userinfo['instructor'] = False
            os.environ['RSM_USERINFO'] = json.dumps(userinfo)
            res = subprocess.call("python web2py.py --no-banner -S runestone -M -R applications/runestone/rsmanage/makeuser.py", shell=True)
            if res != 0:
                click.echo("Failed to create user {} error {} fix your data and try again".format(line[0], res))
                exit(1)
    else:
        userinfo = {}
        userinfo['username'] = username or click.prompt("Username")
        userinfo['password'] = password or click.prompt("Password", hide_input=True)
        userinfo['first_name'] = first_name or click.prompt("First Name")
        userinfo['last_name'] = last_name or click.prompt("Last Name")
        userinfo['email'] = email or click.prompt("email address")
        userinfo['course'] = course or click.prompt("course name")
        if not instructor:
            if username and course:  # user has supplied other info via CL parameter safe to assume False
                userinfo['instructor'] = False
            else:
                userinfo['instructor'] = click.confirm("Make this user an instructor", default=False)

        os.environ['RSM_USERINFO'] = json.dumps(userinfo)
        res = subprocess.call("python web2py.py --no-banner -S runestone -M -R applications/runestone/rsmanage/makeuser.py", shell=True)
        if res != 0:
            click.echo("Failed to create user {} error {} fix your data and try again. Use --verbose for more detail".format(userinfo['username'], res))
            exit(1)
        else:
            click.echo("Success")

@cli.command()
@click.option("--username", help="Username, must be unique")
@click.option("--password", help="password - plaintext -- sorry")
@pass_config
def resetpw(config, username, password):
    """Utility to change a users password. Useful If they can't do it through the normal mechanism"""
    userinfo = {}
    userinfo['username'] = username or click.prompt("Username")
    userinfo['password'] = password or click.prompt("Password", hide_input=True)
    eng = create_engine(config.dburl)
    res = eng.execute("select * from auth_user where username = %s", userinfo['username']).first()
    if not res:
        click.echo("ERROR - User: {} does not exist.".format(userinfo['username']))
        exit(1)

    os.environ['RSM_USERINFO'] = json.dumps(userinfo)
    res = subprocess.call("python web2py.py --no-banner -S runestone -M -R applications/runestone/rsmanage/makeuser.py -A --resetpw", shell=True)
    if res != 0:
        click.echo("Failed to create user {} error {} fix your data and try again. Use --verbose for more detail".format(userinfo['username'], res))
        exit(1)
    else:
        click.echo("Success")

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

    print("Exiting with result of {}".format(dbinit|dbdir))

    sys.exit(dbinit|dbdir)


@cli.command()
@click.option("--username", help="user to promote to instructor")
@click.option("--course", help="name of course")
@pass_config
def addinstructor(config, username, course):
    """
    Add an existing user as an instructor for a course
    """
    eng = create_engine(config.dburl)
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
        print("Sorry, your system does not have the instructor role setup -- this is bad")
        sys.exit(-1)

    res = eng.execute("select * from auth_membership where user_id=%s and group_id=%s", userid, role ).first()
    if not res:
        eng.execute("insert into auth_membership (user_id, group_id) values (%s, %s)", userid, role)
        print("made {} an instructor".format(username))
    else:
        print("{} is already an instructor".format(username))

    # if needed insert a row into user_courses
    res = eng.execute("select * from user_courses where user_id=%s and course_id=%s ", userid, courseid).first()
    if not res:
        eng.execute("insert into user_courses (user_id, course_id) values (%s, %s)", userid, courseid)
        print("enrolled {} in {}".format(username, course))
    else:
        print("{} is already enrolled in {}".format(username, course))

    # if needed insert a row into course_instructor
    res = eng.execute("select * from course_instructor where instructor=%s and course=%s ", userid, courseid).first()
    if not res:
        eng.execute("insert into course_instructor (instructor, course) values (%s, %s)", userid, courseid)
        print("made {} and instructor for {}".format(username, course))
    else:
        print("{} is already an instructor for {}".format(username, course))


@cli.command()
@click.option("--name",help="Name of the course")
@pass_config
def courseinfo(config, name):
    """
    List all information for a single course

    """
    eng = create_engine(config.dburl)
    if not name:
        name = click.prompt("What course do you want info about?")

    course = eng.execute("""select id, term_start_date, institution, base_course from courses where course_name = %s""", name).first()
    cid = course[0]
    start_date = course[1]
    inst = course[2]
    bc = course[3]

    s_count = eng.execute("""select count(*) from user_courses where course_id=%s""",cid).first()[0]

    res = eng.execute("""select username, first_name, last_name, email, courses.course_name 
    from auth_user 
    join course_instructor ON course_instructor.instructor = auth_user.id 
    join courses ON courses.id = course_instructor.course
    where course_instructor.course = %s
    order by username;""", cid)

    print("Course Information for {} -- ({})".format(name, cid))
    print(inst)
    print("Base course: {}".format(bc))
    print("Start date: {}".format(start_date))
    print("Number of students: {}".format(s_count))
    print("Instructors:")
    for row in res:
        print(" ".join(row[:-1]))
 
@cli.command()
@click.option("--course", help="The name of a course that should already exist in the DB")
@pass_config
def instructors(config, course):
    """
    List instructor information for all courses or just for a single course

    """
    eng = create_engine(config.dburl)
    where_clause = ""
    if course:
        where_clause = "where courses.course_name = '{}'".format(course)
    
    res = eng.execute("""select username, first_name, last_name, email, courses.course_name 
    from auth_user 
    join course_instructor ON course_instructor.instructor = auth_user.id 
    join courses ON courses.id = course_instructor.course
    {}
    order by username;""".format(where_clause))
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
@click.option("--course", help="The name of a course that should already exist in the DB")
@click.option("--pset", help="Database ID of the Problem Set")
@pass_config
def grade(config, course, pset, enforce):
    """Grade a problem set; hack for long-running grading processes"""
    os.chdir(findProjectRoot())

    userinfo = {}
    userinfo['course'] = course if course else click.prompt("Name of course")
    userinfo['pset'] = pset if pset else click.prompt("Problem Set ID")
    userinfo['enforce_deadline'] = enforce if enforce else click.confirm("Enforce deadline?", default=True)
    os.environ['RSM_USERINFO'] = json.dumps(userinfo)

    subprocess.call("python web2py.py -S runestone -M -R applications/runestone/rsmanage/grade.py", shell=True)


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
    query = '''
    select username, first_name, last_name, email
from auth_user join course_instructor on auth_user.id = instructor join courses on course = courses.id
where courses.course_name = %s order by last_name
'''
    res = eng.execute(query, course)

    if res:
        for row in res:
            print("{} {} {} {}").format(row.first_name, row.last_name, row.email, row.username)
    else:
        print("No instructors found for {}".format(course))
#
# Utility Functions Below here
#

def checkEnvironment():
    """
    Check the list of required and optional environment variables to be sure they are defined.
    """
    stop = False
    assert os.environ['WEB2PY_CONFIG']
    config = os.environ['WEB2PY_CONFIG']

    if config  == 'production':
        for var in REQ_ENV:
            if var not in os.environ:
                stop = True
                click.echo("Missing definition for {} environment variable".format(var))
    elif config == 'test':
        if 'TEST_DBURL' not in os.environ:
            stop = True
            click.echo("Missing definition for TEST_DBURL environment variable")
    elif config == 'development':
        if 'DEV_DBURL' not in os.environ:
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
        if os.path.exists(os.path.join(start,'web2py.py')):
            return start
        prevdir = start
        start = os.path.dirname(start)
    raise IOError("You must be in a web2py application to run rsmanage")


#
#    fill_practice_log_missings
#

@cli.command()
@pass_config
def fill_practice_log_missings(config):
    """Only for one-time use to fill out the missing values of the columns that we added to user_topic_practice_log table during the semester."""
    os.chdir(findProjectRoot())

    subprocess.call("python web2py.py -S runestone -M -R applications/runestone/rsmanage/fill_practice_log_missings.py", shell=True)


def check_db_for_useinfo(config):
    eng = create_engine(config.dburl)
    res = eng.execute("select count(*) from pg_class where relname = 'useinfo'")
    count = res.first()[0]
    return count
