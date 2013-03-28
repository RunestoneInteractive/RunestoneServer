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
        ),

    everyday = Bunch(
        outdir="static/everyday",
        sourcedir="everyday",
        builddir="static/everyday",
        confidir="everyday",
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
        confdir="thinkcspy",
        template_args={'course_id':'thinkcspy',
                       'login_required':'false',
                       'appname':'runestone',
                       'loglevel':10,
                       'course_url':'http://127.0.0.1:8000' }

    ),

    pythonds = Bunch(
        builddir="static/pythonds",
        sourcedir="source",
        outdir="static/pythonds",
        confdir="pythonds",
        template_args={'course_id':'pythonds',
                       'login_required':'false',
                       'appname':'runestone',
                       'loglevel':10,
                       'course_url':'http://127.0.0.1:8000' }

    ),

    overview = Bunch(
        builddir="static/overview",
        sourcedir="overview",
        outdir="static/overview",
        confdir="overview",
        template_args={'course_id':'overview',
                       'login_required':'false',
                       'appname':'runestone',
                       'loglevel':10,
                       'course_url':'http://127.0.0.1:8000' }

    )

)

@task
def everyday(options):
    paverutils.run_sphinx(options,'everyday')

@task
def thinkcspy(options):
    sh('cp %s/index.rst %s' % (options.thinkcspy.confdir,options.thinkcspy.sourcedir))

    paverutils.run_sphinx(options,'thinkcspy')

@task
def pythonds(options):
    sh('cp %s/index.rst %s' % (options.pythonds.confdir,options.pythonds.sourcedir))

    paverutils.run_sphinx(options,'pythonds')

@task
def overview(options):
    paverutils.run_sphinx(options,'overview')

