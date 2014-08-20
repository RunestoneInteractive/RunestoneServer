import paver
from paver.easy import *
import paver.setuputils
paver.setuputils.install_distutils_tasks()
import os, sys

from sphinxcontrib import paverutils

sys.path.append(os.getcwd())
sys.path.append('../modules')

updateProgressTables = True
try:
    from chapternames import populateChapterInfo
except:
    updateProgressTables = False

######## CHANGE THIS ##########
project_name = "pythonds"
###############################

master_url = 'http://127.0.0.1:8000'
master_app = 'runestone'

options(
    sphinx = Bunch(docroot=".",),

    build = Bunch(
        builddir="../static/"+project_name,
        sourcedir="./source/",
        outdir="../static/"+project_name,
        confdir=".",
        template_args={'course_id':project_name,
                       'login_required':'false',
                       'appname':master_app,
                       'loglevel':10,
                       'course_url':master_url }
    )
)

if project_name == "<project_name>":
  print "Please edit pavement.py and give your project a name"
  exit()

@task
@cmdopts([
    ('all','a','rebuild everything'),
    ('outputdir=', 'o', 'output static files here'),
    ('masterurl=', 'u', 'override the default master url'),
    ('masterapp=', 'p', 'override the default master app')
])
def build(options):
    sh('cp %s/index.rst %s' % (options.build.confdir,options.build.sourcedir))

    if 'all' in options.build:
      options['force_all'] = True
      options['freshenv'] = True

    bi = sh('git describe --long',capture=True)[:-1]
    bi = bi.split('-')[0]
    options.build.template_args["build_info"] = bi


    if 'outputdir' in options.build:
        options.build.outdir = options.build.outputdir

    if 'masterurl' in options.build:
        options.build.template_args['course_url'] = options.build.masterurl

    if 'masterapp' in options.build:
        options.build.template_args['appname'] = options.build.masterapp

    print 'Building into ', options.build.outdir    
    paverutils.run_sphinx(options, 'build')

    if updateProgressTables:
        print 'Creating Chapter Information'
        populateChapterInfo(project_name, "%s/index.rst" % options.build.confdir)
