from gluon.scheduler import Scheduler
import stat
import shutil
from os import path
import os
import sys
import re
from paver.easy import sh
import logging
from pkg_resources import resource_string, resource_filename

rslogger = logging.getLogger(settings.sched_logger)
rslogger.setLevel(settings.log_level)


################
## This task will run as a scheduled task using the web2py scheduler.
## It's dispached from build() and build_custom() in controllers/designer.py
################
def run_sphinx(rvars=None, folder=None, application=None, http_host=None, base_course=None):
    # workingdir is the application folder
    workingdir = folder
    # sourcedir holds the all sources temporarily
    sourcedir = path.join(workingdir, 'build', rvars['projectname'])

    rslogger.debug("Starting to build {}".format(rvars['projectname']))

    # create the custom_courses dir if it doesn't already exist
    if not os.path.exists(path.join(workingdir, 'custom_courses')):
        os.mkdir(path.join(workingdir, 'custom_courses'))

    # confdir holds the conf and index files
    custom_dir = path.join(workingdir, 'custom_courses', rvars['projectname'])


    if not os.path.exists(custom_dir):
        os.mkdir(custom_dir)

    # ## check for base_course  if base_course == None
    ### read conf.py and look for How to Think to determine coursetype
    if base_course == None:
        base_course = 'thinkcspy'

    # copy all the sources into the temporary sourcedir
    if os.path.exists(sourcedir):
        shutil.rmtree(sourcedir)
    shutil.copytree(path.join(workingdir, 'books', base_course), sourcedir)

    makePavement(http_host, rvars, sourcedir, base_course)
    shutil.copy(path.join(sourcedir,'pavement.py'),custom_dir)

    #########
    # We're rebuilding a course
    #########
    if rvars['coursetype'] == 'rebuildcourse':

        try:
            # copy the index and conf files to the sourcedir
            shutil.copy(path.join(custom_dir, 'pavement.py'), path.join(sourcedir, 'pavement.py'))
            shutil.copy(path.join(custom_dir, 'index.rst'), path.join(sourcedir, '_sources', 'index.rst'))
        except OSError:
            # Either the sourcedir already exists (meaning this is probably devcourse, thinkcspy, etc,
            # or the conf.py or index.rst files are missing for some reason.
            raise OSError("missing paver, index, or assignments file")

    ########
    # we're just copying one of the pre-existing books
    ########
    else:
        # Save copies of files that the instructor may customize
        shutil.copy(path.join(sourcedir,'_sources', 'index.rst'),custom_dir)

    ###########
    # Set up and run Paver build
    ###########

    from paver.tasks import main as paver_main
    old_cwd = os.getcwd()
    os.chdir(sourcedir)
    paver_main(args=["build"])
    rslogger.debug("Finished build of {}".format(rvars['projectname']))
    try:
        shutil.copy('build_info',custom_dir)
    except IOError as copyfail:
        rslogger.debug("Failed to copy build_info_file")
        rslogger.debug(copyfail.message)
        idxname = 'index.rst'

    #
    # move the sourcedir/build/projectname folder into static
    #
    shutil.rmtree(os.path.join(workingdir,'static',rvars['projectname']),ignore_errors=True)
    shutil.move(os.path.join(sourcedir,'build',rvars['projectname']),
                os.path.join(workingdir,'static',rvars['projectname']) )
    #
    # clean up
    #

    # This will remove a directory that's versioned by Git, which marks some of its files as read-only on Windows. This causes rmtree to fail. So, provide a workaround per `SO <https://stackoverflow.com/questions/21261132/shutil-rmtree-to-remove-readonly-files>`_.
    def del_rw(function, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
    # Change away from sourcedir, to avoid an error like ``WindowsError: [Error 32] The process cannot access the file because it is being used by another process: 'E:\\Runestone\\web2py\\applications\\runestone\\build\\test_book10'``.
    os.chdir(old_cwd)
    shutil.rmtree(sourcedir, onerror=del_rw)
    rslogger.debug("Completely done with {}".format(rvars['projectname']))


def makePavement(http_host, rvars, sourcedir, base_course):
    paver_stuff = resource_string('runestone', 'common/project_template/pavement.tmpl')
    opts = {'master_url': settings.server_type + http_host,
            'project_name': rvars['projectname'],
            'build_dir': 'build',
            'log_level': 10,
            'use_services': 'true',
            'dburl': settings.database_uri,
            'basecourse': base_course,
            'default_ac_lang': rvars.get('default_ac_lang') if rvars.get('default_ac_lang',False) else 'python',
            'downloads_enabled': rvars.get('downloads_enabled','false'),
            'enable_chatcodes': 'false'
            }
    if 'loginreq' in rvars:
        opts['login_req'] = 'true'
    else:
        opts['login_req'] = 'false'
    if 'python3' in rvars:
        opts['python3'] = 'true'
    else:
        opts['python3'] = 'false'

    opts['dest'] = '../../static'

    paver_stuff = paver_stuff % opts
    with open(path.join(sourcedir, 'pavement.py'), 'w') as fp:
        fp.write(paver_stuff)

scheduler = Scheduler(db, migrate='runestone_')
