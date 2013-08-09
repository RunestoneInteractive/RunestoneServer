import paver
import paver.misctasks
from paver.path import path
from paver.easy import *
import paver.setuputils
paver.setuputils.install_distutils_tasks()
import os, sys
import subprocess

from sphinxcontrib import paverutils

sys.path.append(os.getcwd())

# You will want to change these for your own environment in .gitignored paverconfig.py
try:
    from paverconfig import master_url, master_app, minify_js
except:
    print 'NOTICE:  You are using default values for master_* Make your own paverconfig.py file'
    master_url = 'http://127.0.0.1:8000'
    master_app = 'runestone'
    minify_js = False

options(
    sphinx = Bunch(
        docroot=".",
        ),
)

@task
@cmdopts([('all','a','rebuild everything')])
def everyday(options):
    os.chdir("everyday")
    if 'all' in options.everyday:
        subprocess.call(["paver","build", "-a",
                         "--masterapp", master_app,
                         "--masterurl", master_url])
    else:
        subprocess.call(["paver", "build",
                         "--masterapp", master_app,
                         "--masterurl", master_url])

@task
@cmdopts([('all','a','rebuild everything')])
def thinkcspy(options):
    os.chdir("thinkcspy")
    if 'all' in options.thinkcspy:
        subprocess.call(["paver","build", "-a",
                            "--masterapp", master_app,
                            "--masterurl", master_url])
    else:
        subprocess.call(["paver", "build",
                            "--masterapp", master_app,
                            "--masterurl", master_url])

    if minify_js:
        sh('./minifyjs.py %s' % options.thinkcspy.outdir)

@task
@cmdopts([('all','a','rebuild everything')])
def pythonds(options):
    os.chdir("pythonds")
    if 'all' in options.pythonds:
        subprocess.call(["paver","build", "-a",
                            "--masterapp", master_app,
                            "--masterurl", master_url])
    else:
        subprocess.call(["paver", "build",
                            "--masterapp", master_app,
                            "--masterurl", master_url])

    if minify_js:
        sh('./minifyjs.py %s' % options.pythonds.outdir)

@task
@cmdopts([('all','a','rebuild everything')])
def overview(options):
    os.chdir("overview")
    if 'all' in options.overview:
        subprocess.call(["paver","build", "-a",
                            "--masterapp", master_app,
                            "--masterurl", master_url])
    else:
        subprocess.call(["paver", "build",
                            "--masterapp", master_app,
                            "--masterurl", master_url])

    if minify_js:
        sh('./minifyjs.py %s' % options.overview.outdir)

@task
@cmdopts([('all','a','rebuild everything')])
def devcourse(options):
    os.chdir("devcourse")
    if 'all' in options.devcourse:
        subprocess.call(["paver","build", "-a",
                            "--masterapp", master_app,
                            "--masterurl", master_url])
    else:
        subprocess.call(["paver", "build",
                            "--masterapp", master_app,
                            "--masterurl", master_url])

    if minify_js:
        sh('./minifyjs.py %s' % options.devcourse.outdir)

@task
@cmdopts([('all','a','rebuild everything')])
def java4python(options):
    os.chdir("java4python")
    if 'all' in options.java4python:
        subprocess.call(["paver","build", "-a",
                         "--masterapp", master_app,
                         "--masterurl", master_url])
    else:
        subprocess.call(["paver", "build",
                         "--masterapp", master_app,
                         "--masterurl", master_url])

@task
@cmdopts([('all','a','rebuild everything')])
def allbooks(options):
    if 'all' in options.allbooks:
        opts = Bunch(all=True)
    else:
        opts = Bunch()

    options.thinkcspy = opts
    options.pythonds = opts
    options.overview = opts

    thinkcspy(options)
    os.chdir("..")

    pythonds(options)
    os.chdir("..")

    overview(options)
    os.chdir("..")

