from .activecode import *
from .animation import *
from .assess import *
from .blockly import *
from .codelens import *
from .datafile import *
from .disqus import *
from .livecode import *
from .meta import *
from .parsons import *
from .poll import *
from .reveal import *
from .tabbedStuff import *
from .video import *

import os
def runestone_static_dirs():
    basedir = os.path.dirname(__file__)
    module_paths = [ x for x in os.listdir(basedir) if os.path.isdir(os.path.join(basedir,x))]
    module_static_js = ['%s/js' % os.path.join(basedir,x) for x in module_paths if os.path.exists('%s/js' % os.path.join(basedir,x))]
    module_static_css = ['%s/css' % os.path.join(basedir,x) for x in module_paths if os.path.exists('%s/css' % os.path.join(basedir,x))]
    module_static_image = ['%s/images' % os.path.join(basedir,x) for x in module_paths if os.path.exists('%s/images' % os.path.join(basedir,x))]
    module_static_bootstrap = ['%s/bootstrap' % os.path.join(basedir,x) for x in module_paths if os.path.exists('%s/bootstrap' % os.path.join(basedir,x))]        

    return module_static_js + module_static_css + module_static_image + module_static_bootstrap


def runestone_extensions():
    basedir = os.path.dirname(__file__)
    module_paths = [ x for x in os.listdir(basedir) if os.path.isdir(os.path.join(basedir,x))]
    modules = [ 'runestone.{}'.format(x) for x in module_paths if os.path.exists('{}/__init__.py'.format(os.path.join(basedir,x)))]
    print "MODULES = ", modules
    return modules
