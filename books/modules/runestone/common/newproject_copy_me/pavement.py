import paver
from paver.easy import *
import paver.setuputils
paver.setuputils.install_distutils_tasks()
import os, sys

from sphinxcontrib import paverutils

sys.path.append(os.getcwd())

home_dir = os.getcwd()
master_url = '%(master_url)s'
master_app = 'runestone'
serving_dir = "%(build_dir)s/%(project_name)s"

options(
    sphinx = Bunch(docroot=".",),

    build = Bunch(
        builddir="%(build_dir)s/%(project_name)s",
        sourcedir="_sources",
        outdir="%(build_dir)s/%(project_name)s",
        confdir=".",
        template_args={'course_id': '%(project_name)s',
                       'login_required':'%(login_req)s',
                       'appname':master_app,
                       'loglevel':10,
                       'course_url':master_url }
    )
)


@task
@cmdopts([
    ('all','a','rebuild everything'),
    ('outputdir=', 'o', 'output static files here'),
    ('masterurl=', 'u', 'override the default master url'),
    ('masterapp=', 'p', 'override the default master app'),
])
def build(options):
    if 'all' in options.build:
      options['force_all'] = True
      options['freshenv'] = True

    # bi = sh('git describe --long',capture=True)[:-1]
    # bi = bi.split('-')[0]
    # options.build.template_args["build_info"] = bi

    if 'outputdir' in options.build:
        options.build.outdir = options.build.outputdir

    if 'masterurl' in options.build:
        options.build.template_args['course_url'] = options.build.masterurl

    if 'masterapp' in options.build:
        options.build.template_args['appname'] = options.build.masterapp

    print 'Building into ', options.build.outdir    
    paverutils.run_sphinx(options,'build')

