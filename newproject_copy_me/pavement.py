import paver
from paver.easy import *
import paver.setuputils
paver.setuputils.install_distutils_tasks()
import os, sys

from sphinxcontrib import paverutils

sys.path.append(os.getcwd())

######## CHANGE THIS ##########
project_name = "<project_name>"
###############################

master_url = 'http://127.0.0.1:8000'
master_app = 'runestone'

options(
    sphinx = Bunch(docroot=".",),

    build = Bunch(
        builddir="../static/"+project_name,
        sourcedir=".",
        outdir="../static/"+project_name,
        confdir=".",
        template_args={'course_id':project_name,
                       'login_required':'false',
                       'appname':master_app,
                       'loglevel':10,
                       'course_url':master_url }
    )
)

@task
@cmdopts([('all','a','rebuild everything')])
def build(options):

    if 'all' in options.build:
      options['force_all'] = True
      options['freshenv'] = True
    
    paverutils.run_sphinx(options,'build')

