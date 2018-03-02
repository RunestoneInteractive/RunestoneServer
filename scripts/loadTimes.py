#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#
# {address space usage: 359067648 bytes/342MB} {rss usage: 107823104 bytes/102MB} [pid: 11266|app: 0|req: 99163/885977] 64.208.17.170 () {48 vars in 1249 bytes} [Thu Feb 15 16:28:43 2018] GET /runestone/ajax/getnumonline => generated 16 bytes in 2553 msecs (HTTP/1.1 200) 8 headers in 381 bytes (1 switches on core 0)
import re, sys
from dateutil.parser import parse
if len(sys.argv) > 2:
    dday = parse(sys.argv[2]).date()
else:
    dday = None

logfile = open(sys.argv[1], 'r')
i = 0
haripat = re.compile(r'^HARAKIRI.*/runestone/ajax/(\w+).*')
timepat = re.compile(r'.*/runestone/ajax/(\w+)(\s|\?).*\s(\d+)\s+msecs.*')
pagepat = re.compile(r'.*GET\s+/.*/(\w+)\.(html|js|css|png|jpg).*\s(\d+)\s+msecs.*')
datepat = re.compile(r'.*\[((Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*\d\d\d\d)\].*')
print(dday)
kills = {}
runtimes = {}
pagetimes = {}
for line in logfile:
    currentday = None
    gd = datepat.match(line)
    if dday and gd:
        currentday = parse(gd.group(1))

    if (currentday and dday == currentday.date()) or dday == None:
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
