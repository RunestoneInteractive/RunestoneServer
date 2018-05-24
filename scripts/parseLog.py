#!/usr/bin/env python3

# {address space usage: 359067648 bytes/342MB} {rss usage: 107823104 bytes/102MB} [pid: 11266|app: 0|req: 99163/885977] 64.208.17.170 () {48 vars in 1249 bytes} [Thu Feb 15 16:28:43 2018] GET /runestone/ajax/getnumonline => generated 16 bytes in 2553 msecs (HTTP/1.1 200) 8 headers in 381 bytes (1 switches on core 0)

import re, sys

timepat = re.compile(r'.*\[((Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*\d\d\d\d)\].*/runestone/ajax/(\w+)(\s|\?).*\s(\d+)\s+msecs.*')
logfile = open(sys.argv[1], 'r')

for line in logfile:
    g = timepat.match(line)
    if g:
        print("{},{},{}".format(g.group(1),g.group(4), g.group(6)))

