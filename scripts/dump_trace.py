#!/usr/bin/env python
__author__ = 'bmiller'

import cPickle
import sys
import pprint

sys.path.insert(0,'/home/bnmnetp/webapps/uwsgi_runestone/web2py')

with open(sys.argv[1]) as f:
    trace_data = cPickle.load(f)

print(trace_data['traceback'])
pprint.pprint(trace_data['snapshot']['locals'])
for i in trace_data['snapshot']['frames']:
    print("============")
    pprint.pprint(i)

