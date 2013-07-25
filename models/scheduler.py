from gluon.scheduler import Scheduler
import shutil
from os import path
import os
import sys
import re

from sphinx.application import Sphinx



def run_sphinx(rvars=None, folder=None, application=None, http_host=None):
    print ("WORKINGGGGGGG")
    # sourcedir holds the all sources temporarily
    # confdir holds the files needed to rebuild the course
    workingdir = folder
    sourcedir = path.join(workingdir,rvars['projectname'])

    if not os.path.exists(path.join(workingdir, 'custom_courses')):
        os.mkdir(path.join(workingdir, 'custom_courses'))
    confdir = path.join(workingdir, 'custom_courses', rvars['projectname'])
    if os.path.exists(sourcedir) \
            or re.search(r'[ &]',rvars['projectname']) \
            or os.path.exists(confdir):
        return dict(mess='You may not use %s for your course name'%rvars['projectname'],success=False)

    # copy all the sources into the temporary sourcedir
    shutil.copytree(path.join(workingdir,'source'),sourcedir)

    os.mkdir(confdir)

    # copy the config file. We save it in confdir (to allow rebuilding the course at a later date),
    # and we also copy it to the sourcedir (which will be used for this build and then deleted.
    shutil.copy(path.join(workingdir,rvars['coursetype'],'conf.py'),
                path.join(confdir,'conf.py'))
    shutil.copy(path.join(workingdir,rvars['coursetype'],'conf.py'),
                path.join(sourcedir,'conf.py'))

    # copy the index file. Save in confdir (to allow rebuilding the course at a later date),
    # and copy to sourcedir for this build.
    shutil.copy(path.join(workingdir,rvars['coursetype'],'index.rst'),
                path.join(confdir,'index.rst'))
    shutil.copy(path.join(workingdir,rvars['coursetype'],'index.rst'),
                path.join(sourcedir,'index.rst'))

    # set the courseid
    # set the url
    # build the book
    coursename = rvars['projectname']
    confdir = sourcedir  # the Sphinx build actually gets the conf stuff from the temp sourcedir
    outdir = path.join(folder, 'static' , coursename)
    doctreedir = path.join(outdir,'doctrees')
    buildername = 'html'
    confoverrides = {}
    confoverrides['html_context.appname'] = application
    confoverrides['html_context.course_id'] = coursename
    confoverrides['html_context.loglevel'] = 10
    confoverrides['html_context.course_url'] = 'http://' + http_host
    if rvars['loginreq'] == 'yes':
        confoverrides['html_context.login_required'] = 'true'
    else:
        confoverrides['html_context.login_required'] = 'false'
    status = sys.stdout
    warning = sys.stdout
    freshenv = True
    warningiserror = False
    tags = []

    sys.path.insert(0,path.join(folder,'modules'))

    force_all = True
    filenames = []

    app = Sphinx(sourcedir, confdir, outdir, doctreedir, buildername,
                confoverrides, status, warning, freshenv,
                warningiserror, tags)
    app.build(force_all, filenames)

    shutil.copy(path.join(outdir, '_static', 'jquery-1.10.2.min.js'),
            path.join(outdir, '_static', 'jquery.js'))

    shutil.rmtree(sourcedir)


scheduler = Scheduler(db)
