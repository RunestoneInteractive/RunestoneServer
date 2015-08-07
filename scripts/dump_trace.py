#!/usr/bin/env python
__author__ = 'bmiller'

import cPickle
import sys

sys.path.insert(0,'/Users/bmiller/Beta/web2py')

with open(sys.argv[1]) as f:
    trace_data = cPickle.load(f)

print(trace_data['traceback'])