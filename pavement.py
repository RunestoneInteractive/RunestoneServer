import paver
import paver.misctasks
from paver.path import path
from paver.easy import *
import paver.setuputils
paver.setuputils.install_distutils_tasks()

from sphinxcontrib import paverutils

options(
    sphinx = Bunch(
        docroot=".",
        builddir="static/everyday",
        sourcedir="everyday",
        ),

    everyday = Bunch(
        outdir="static/everyday",
        template_args={'course_id':'everyday',
                       'login_required':'false',
                       'appname':'runestone',
                       'loglevel':10,
                       'course_url':'http://127.0.0.1:8000' }
        ),

    thinkcspy = Bunch(
        builddir="static/thinkcspy",
        sourcedir="source",
        outdir="static/thinkcspy",
        template_args={'course_id':'thinkcspy',
                       'login_required':'false',
                       'appname':'courselib',
                       'loglevel':10,
                       'course_url':'http://127.0.0.1:8000' }

    )
)

@task
def everyday(options):
    paverutils.run_sphinx(options,'everyday')

@task
def thinkcspy(options):
    paverutils.run_sphinx(options,'thinkcspy')
