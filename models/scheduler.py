from gluon.scheduler import Scheduler
import shutil
from os import path
import os
import sys
import re
from paver.easy import sh
from sphinx.application import Sphinx

################
## This task will run as a scheduled task using the web2py scheduler.
## It's dispached from build() and build_custom() in controllers/designer.py
################
def run_sphinx(rvars=None, folder=None, application=None, http_host=None):
    # workingdir is the application folder
    workingdir = folder

    # sourcedir holds the all sources temporarily
    sourcedir = path.join(workingdir,rvars['projectname'])

    # create the custom_courses dir if it doesn't already exist
    if not os.path.exists(path.join(workingdir, 'custom_courses')):
        os.mkdir(path.join(workingdir, 'custom_courses'))

    # confdir holds the conf and index files
    confdir = path.join(workingdir, 'custom_courses', rvars['projectname'])
    custom_dir = confdir
    if not os.path.exists(confdir):
        os.mkdir(confdir)

    ########
    # We're building a custom course.
    # Generate an index.rst and copy conf.py from devcourse.
    ########
    if rvars['coursetype'] == 'custom':
        row = db(db.projects.projectcode==rvars['projectname']).select()
        title = row[0].description

        # this is the temporary source dir for this build
        os.mkdir(sourcedir)

        # The conf and index files will be archived in custom_courses/coursename
        # so that the course can be rebuilt at a later date.
        # Copy the conf.py file from devcourse into our custom course.
        shutil.copy(path.join(workingdir, 'devcourse', 'conf.py'),
                    path.join(confdir, 'conf.py'))
        shutil.copy(path.join(workingdir, 'devcourse', 'conf.py'),
                    path.join(sourcedir, 'conf.py'))

        # generate index.rst and copy modules from source
        f = open(path.join(sourcedir,"index.rst"),"w")

        f.write('''.. Copyright (C)  Brad Miller, David Ranum
       Permission is granted to copy, distribute and/or modify this document
       under the terms of the GNU Free Documentation License, Version 1.3 or
       any later version published by the Free Software Foundation; with
       Invariant Sections being Forward, Prefaces, and Contributor List,
       no Front-Cover Texts, and no Back-Cover Texts.  A copy of the license
       is included in the section entitled "GNU Free Documentation License".''' + "\n\n")

        f.write("="*len(title) + "\n")
        f.write(title + "\n")
        f.write("="*len(title) + "\n\n")

        toc = rvars['toc']
        parts = toc.split(" ")

        idx = 0
        while idx<len(parts):
            item = parts[idx]
            if ".rst" in item:
                f.write("   "+item+"\n")
                idx=idx+1
                moduleDir = item.split('/')[0]
                try:
                    shutil.copytree(path.join(workingdir,'source',moduleDir),
                                    path.join(sourcedir,moduleDir))
                except:
                    print 'copying %s again' % moduleDir
            else:
                topic = ""
                while idx<len(parts) and ".rst" not in parts[idx]:
                    if topic != "":
                        topic =topic + " " + parts[idx]
                    else:
                        topic = topic + parts[idx]
                    idx=idx+1
                f.write("\n" + topic + "\n" + ":"*len(topic) + "\n\n")
                f.write('''.. toctree::
       :maxdepth: 2 \n\n''')

        f.write('''\nAcknowledgements
    ::::::::::::::::

    .. toctree::
       :maxdepth: 1

       FrontBackMatter/copyright.rst
       FrontBackMatter/prefaceinteractive.rst
       FrontBackMatter/foreword.rst
       FrontBackMatter/preface.rst
       FrontBackMatter/preface2e.rst
       FrontBackMatter/contrib.rst
       FrontBackMatter/fdl-1.3.rst''' + "\n")

        f.close()

        # archive the index file so the course can be rebuilt later
        shutil.copy(path.join(sourcedir, 'index.rst'), path.join(confdir, 'index.rst'))

        shutil.copytree(path.join(workingdir,'source','FrontBackMatter'),
                        path.join(sourcedir,'FrontBackMatter'))

    #########
    # We're rebuilding a course
    #########
    elif rvars['coursetype'] == 'rebuildcourse':
        try:
            # copy all the sources into the temporary sourcedir
            shutil.copytree(path.join(workingdir,'source'),sourcedir)

            # copy the index and conf files to the sourcedir
            shutil.copy(path.join(confdir, 'conf.py'), path.join(sourcedir, 'conf.py'))
            shutil.copy(path.join(confdir, 'index.rst'), path.join(sourcedir, 'index.rst'))
        except OSError:
            # Either the sourcedir already exists (meaning this is probably devcourse, thinkcspy, etc,
            # or the conf.py or index.rst files are missing for some reason.
            raise OSError



    ########
    # we're just copying one of the pre-existing books
    ########
    else:
        # copy all the sources into the temporary sourcedir
        shutil.copytree(path.join(workingdir,'source'),sourcedir)

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



    ###########
    # Set up and run Sphinx
    ###########
    coursename = rvars['projectname']
    confdir = sourcedir # Sphinx build actually gets conf stuff from temp sourcedir
    outdir = path.join(folder, 'static' , coursename)
    doctreedir = path.join(outdir,'doctrees')
    buildername = 'html'
    confoverrides = {}
    confoverrides['html_context.appname'] = application
    confoverrides['html_context.course_id'] = coursename
    confoverrides['html_context.loglevel'] = 10
    confoverrides['html_context.course_url'] = 'http://' + http_host

    cwd = os.getcwd()
    os.chdir(path.join('applications',application))
    build_info = sh("git describe --long", capture=True)
    bi = open(path.join('custom_courses',coursename,'build_info'),'w')
    bi.write(build_info)
    bi.close()
    os.chdir(cwd)    
    build_split = build_info.split('-')
    confoverrides['html_context.build_info'] = build_split[0]

    if 'loginreq' in rvars:
        confoverrides['html_context.login_required'] = 'true'
    else:
        confoverrides['html_context.login_required'] = 'false'
    status = sys.stdout
    warning = sys.stdout
    freshenv = True
    warningiserror = False
    tags = []

    sys.path.insert(0,path.join(folder,'modules'))
    from chapternames import addChapterInfoFromScheduler, findChaptersSubChapters

    force_all = True
    filenames = []

    app = Sphinx(sourcedir, confdir, outdir, doctreedir, buildername,
                confoverrides, status, warning, freshenv,
                warningiserror, tags)
    app.build(force_all, filenames)

    if rvars['coursetype'] == 'thinkcspy':
        idxname = 'toc.rst'
    else:
        idxname = 'index.rst'
    scd, ct = findChaptersSubChapters(path.join(sourcedir, idxname))
    addChapterInfoFromScheduler(scd, ct, rvars['projectname'],db)

    shutil.rmtree(sourcedir)

    donefile = open(os.path.join(custom_dir, 'done'), 'w')
    donefile.write('success')
    donefile.close()



scheduler = Scheduler(db)
