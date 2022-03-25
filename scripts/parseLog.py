#!/usr/bin/env python3

# {address space usage: 359067648 bytes/342MB} {rss usage: 107823104 bytes/102MB} [pid: 11266|app: 0|req: 99163/885977] 64.208.17.170 () {48 vars in 1249 bytes} [Thu Feb 15 16:28:43 2018] GET /runestone/ajax/getnumonline => generated 16 bytes in 2553 msecs (HTTP/1.1 200) 8 headers in 381 bytes (1 switches on core 0)

import re, sys

refer_pat = re.compile(r".*Referrer: (.*) Agent:.*")
logfile = open(sys.argv[1], "r")
referrers = {}

for line in logfile:
    if g := refer_pat.match(line):
        ref = g.group(1).strip('"')
        if "runestone.academy" not in ref:
            referrers[ref] = referrers.get(ref, 0) + 1


i = 0
for k, v in sorted(referrers.items(), key=lambda x: x[1], reverse=True):
    if i < 25:
        print(k, v)
        i += 1
    else:
        break
