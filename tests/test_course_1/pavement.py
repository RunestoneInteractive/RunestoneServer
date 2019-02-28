import paver
from paver.easy import *
import paver.setuputils
paver.setuputils.install_distutils_tasks()
import os, sys
from runestone.server import get_dburl
from sphinxcontrib import paverutils
import pkg_resources
from socket import gethostname

sys.path.append(os.getcwd())

# The project name, for use below.
project_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
# True if this project uses Runestone services.
use_services = True
# The root directory for ``runestone serve``.
serving_dir = "./build/" + project_name
# The destination directory for ``runestone deploy``.
dest = "./published"

options(
    sphinx = Bunch(docroot=".",),

    build = Bunch(
        builddir=serving_dir,
        sourcedir="_sources",
        outdir=serving_dir,
        confdir=".",
        template_args={'login_required':'true',
                       'loglevel': 10,
                       'python3': 'false',
                       'dburl': 'postgresql://user:password@localhost/runestone',
                       'default_ac_lang': 'python',
                       'jobe_server': 'http://jobe2.cosc.canterbury.ac.nz',
                       'proxy_uri_runs': '/jobe/index.php/restapi/runs/',
                       'proxy_uri_files': '/jobe/index.php/restapi/files/',
                       'downloads_enabled': 'false',
                       'enable_chatcodes': 'False',
                       'allow_pairs': 'False',

                       'use_services': use_services,
                       'basecourse': project_name,
                       # If ``use_services`` is 'true', then the following values are ignored, since they're provided by the server.
                       'course_id': project_name,
                       'appname': 'runestone',
                       'course_url': '',
                      }
    )
)

# if we are on runestone-deploy then use the proxy server not canterbury
if gethostname() == 'runestone-deploy':
    del options.build.template_args['jobe_server']
    del options.build.template_args['proxy_uri_runs']
    del options.build.template_args['proxy_uri_files']

version = pkg_resources.require("runestone")[0].version
options.build.template_args['runestone_version'] = version

# If DBURL is in the environment override dburl
options.build.template_args['dburl'] = get_dburl(outer=locals())

from runestone import build  # build is called implicitly by the paver driver.
