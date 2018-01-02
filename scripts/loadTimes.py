#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import re, sys
logfile = open(sys.argv[1], 'r')
i = 0
haripat = re.compile(r'^HARAKIRI.*/runestone/ajax/(\w+).*')
timepat = re.compile(r'.*/runestone/ajax/(\w+)(\s|\?).*\s(\d+)\s+msecs.*')
pagepat = re.compile(r'.*GET\s+/.*/(\w+)\.(html|js|css|png|jpg).*\s(\d+)\s+msecs.*')
kills = {}
runtimes = {}
pagetimes = {}
for line in logfile:
    hg = haripat.match(line)
    if hg:
        kills[hg.group(1)] = kills.get(hg.group(1),0) + 1
    gt = timepat.match(line)
    if gt:
        if gt.group(1) not in runtimes:
            runtimes[gt.group(1)] = []
        runtimes[gt.group(1)].append(int(gt.group(3)))
    gt = pagepat.match(line)
    if gt:
        page = gt.group(1) + '.' + gt.group(2)
        if page not in pagetimes:
            pagetimes[page] = []
        pagetimes[page].append(int(gt.group(3)))

print("KILLS")
for k in kills:
    print(k,kills[k])
print("\n ---  AJAX TIMES  ---\n")
for k in sorted(runtimes,key=lambda x: sum(runtimes[x])/len(runtimes[x] )):
    print("%20s\t%7d\t%6.3f\t%7d"%(k,len(runtimes[k]),sum(runtimes[k])/len(runtimes[k]),max(runtimes[k])))

print("\n --- PAGE TIMES --- \n")
for k in sorted(pagetimes,key=lambda x: sum(pagetimes[x])/len(pagetimes[x] )):
    print("%20s\t%7d\t%6.3f\t%7d"%(k,len(pagetimes[k]),sum(pagetimes[k])/len(pagetimes[k]),max(pagetimes[k])))
