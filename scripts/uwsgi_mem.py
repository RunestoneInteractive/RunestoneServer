#!/usr/bin/env python

import re

test_data = '''{address space usage: 309755904 bytes/295MB} {rss usage: 40689664 bytes/38MB} [pid: 14010|app: 0|req: 347/1474] 127.0.0.1 () {60 vars in 1399 bytes} [Sat Dec 15 16:23:18 2012] POST /courselib/ajax/runlog => generated 4 bytes in 114 msecs (HTTP/1.0 200) 7 headers in 345 bytes (3 switches on core 8)
{address space usage: 309776384 bytes/295MB} {rss usage: 40566784 bytes/38MB} [pid: 14008|app: 0|req: 403/1475] 127.0.0.1 () {60 vars in 1399 bytes} [Sat Dec 15 16:23:19 2012] POST /courselib/ajax/runlog => generated 4 bytes in 65 msecs (HTTP/1.0 200) 7 headers in 345 bytes (3 switches on core 11)
{address space usage: 309755904 bytes/295MB} {rss usage: 40488960 bytes/38MB} [pid: 14011|app: 0|req: 361/1476] 127.0.0.1 () {60 vars in 1399 bytes} [Sat Dec 15 16:23:20 2012] POST /courselib/ajax/runlog => generated 4 bytes in 67 msecs (HTTP/1.0 200) 7 headers in 345 bytes (3 switches on core 10)
{address space usage: 309809152 bytes/295MB} {rss usage: 40640512 bytes/38MB} [pid: 14009|app: 0|req: 366/1477] 127.0.0.1 () {54 vars in 1440 bytes} [Sat Dec 15 16:23:26 2012] GET /courselib/ajax/hsblog?event=activecode&act=edit&div_id=ex_3_3&course=thinkcspy => generated 4 bytes in 64 msecs (HTTP/1.0 200) 7 headers in 345 bytes (3 switches on core 9)
{address space usage: 309755904 bytes/295MB} {rss usage: 40689664 bytes/38MB} [pid: 14010|app: 0|req: 348/1478] 127.0.0.1 () {60 vars in 1399 bytes} [Sat Dec 15 16:23:26 2012] POST /courselib/ajax/runlog => generated 4 bytes in 106 msecs (HTTP/1.0 200) 7 headers in 345 bytes (3 switches on core 8)'''


f = open('uwsgi.log','r')
maxMem = 0
maxCmd = ''
maxSw = 0
lc = 0
swTot = 0
for line in f:
   g = re.match(r'.*rss usage: (\d+) bytes',line)
   start = line.find('GET')
   lc += 1
   if start == -1:
       start = line.find('POST')
   end = line.find('=>')
   request = line[start:end]
   if g:
       b = int(g.group(1))
       if b > maxMem:
           maxMem = b
           maxCmd = request
       if b > 50000000:
           print b/1000000, request

   g = re.match(r'.*(\d+) switches on core',line)
   if g:
       sw = int(g.group(1))
       swTot += sw


print 'Average Switches: ', float(swTot)/lc
print 'Largest Request: ', maxMem, maxCmd
