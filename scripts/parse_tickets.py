__author__ = 'bmiller'

import cPickle
import os
import datetime
import sys
from collections import Counter

sys.path.insert(0,'../../../')  #pickle needs gluon??
all = True
outset = Counter()
outlist = []

tickets = os.listdir('../errors')
for t in tickets:
    nparts = t.split('.')
    d = datetime.date(*[int(x) for x in nparts[4].split('-')])
    if datetime.datetime.now().date() == d or all == True:
        f = open('../errors/'+t, 'rb')
        tick_data = cPickle.load(f)
        outlist.append(tick_data['output'])


outset = Counter(outlist)

for m in outset.most_common(10):
    print(m)
    