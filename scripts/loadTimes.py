#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#
# {address space usage: 359067648 bytes/342MB} {rss usage: 107823104 bytes/102MB} [pid: 11266|app: 0|req: 99163/885977] 64.208.17.170 () {48 vars in 1249 bytes} [Thu Feb 15 16:28:43 2018] GET /runestone/ajax/getnumonline => generated 16 bytes in 2553 msecs (HTTP/1.1 200) 8 headers in 381 bytes (1 switches on core 0)
# 2601:2c3:8880:860:cc2b:7932:b6b5:50f9 - - - [22/Jan/2022:01:06:57 +0000] Request: "GET /ns/books/published/csawesome/_static/runtime.da9e52c73fc3d100.bundle.js?v=F2F2D427 HTTP/1.1" Status: 200 Bytes: 5199 Host: 10.136.0.8:80  ResponseTime: 0.008 Referrer: "https://runestone.academy/ns/books/published/csawesome/Unit8-2DArray/freeResponse.html" Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
# 207.163.116.25 - - - [22/Jan/2022:01:06:57 +0000] Request: "POST /assignments/autograde HTTP/1.1" Status: 200 Bytes: 103 Host: 10.136.0.2:80  ResponseTime: 0.208 Referrer: "https://runestone.academy/runestone/admin/grading" Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
# 2601:444:4100:3c00:756d:34fe:d1b0:8963 - - - [22/Jan/2022:01:06:57 +0000] Request: "GET /runestone/default/user/login?_next=/runestone/default/index HTTP/1.1" Status: 200 Bytes: 6537 Host: 10.136.0.10:80  ResponseTime: 0.052 Referrer: "-" Agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
# 76.219.135.229 - - - [22/Jan/2022:01:29:31 +0000] Request: "POST /ns/logger/bookevent HTTP/1.1" Status: 201 Bytes: 53 Host: 10.136.0.11:80  ResponseTime: 0.024 Referrer: "https://runestone.academy/ns/books/published/UCMST_APCSA_2022/Unit6-Arrays/topic-6-1-array-basics.html" Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62"

import re, sys, os
from dateutil.parser import parse
from sqlalchemy import (
        create_engine,
        MetaData,
        Table,
        Column,
        Integer,
        String,
        Date,
        Float,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

if "-date" in sys.argv:
    ix = sys.argv.index('-date') + 1
    dday = parse(sys.argv[ix]).date()
    ix += 1
else:
    dday = None
    ix = 1


i = 0
timepat = re.compile(r'.*/(dashboard|proxy|assignments|logger|assessment|books)/(\w+)(\s*|/.*?|\?.*?|\.html.*?) HTTP.*ResponseTime: (\d+\.\d+)')
datepat = re.compile(r'.*\[(\d+/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/\d\d\d\d):(.*)\].*')
statuspat = re.compile(r'.*Status:\s+(\d+)\s+.*')
hostpat = re.compile(r'.*Host:\s+(\d+\.\d+\.\d+\.\d+:\d+)\s+.*')
print(dday)
runtimes = {}
pagetimes = {}
status_counts = {}
host_counts = {}
for fname in sys.argv[ix:]:
    logfile = open(fname, 'r')
    line = logfile.readline()
    while line:
        currentday = None
        if (gd := datepat.match(line)) and dday:
            currentday = parse(gd.group(1))

        if (currentday and dday == currentday.date()) or dday == None:
            if gt := timepat.match(line):
                epkey = gt.group(2)
                if 'dashboard/index' in line:
                    epkey = 'db'+epkey
                if epkey not in runtimes:
                    runtimes[epkey] = []
                runtimes[epkey].append(float(gt.group(4)))
        
        if st := statuspat.match(line):
            status_counts[st.group(1)] = status_counts.get(st.group(1), 0) + 1
        if ht := hostpat.match(line):
            host_counts[ht.group(1)] = host_counts.get(ht.group(1), 0) + 1

        try:
            line = logfile.readline()
        except:
            continue

for k,v in sorted(status_counts.items()):
    print(k, v)

for k,v in sorted(host_counts.items()):
    print(k, v)

Base = declarative_base()

dburl = os.environ["LOGDBURL"]
engine = create_engine(
        dburl,
        echo=True
        #    "postgresql://bmiller:autocubanlobbyduck@localhost/bmiller", echo=True
    )
meta = MetaData()
Session = sessionmaker(bind=engine)


class LogEntry(Base):
        __tablename__ = "api_times"
        id = Column(Integer, primary_key=True)
        timestamp = Column(Date)
        endpoint = Column(String)
        calls = Column(Integer)
        response_average = Column(Float)
        max_response = Column(Integer)

class HostCounts(Base):
        __tablename__ = "host_counts"
        id = Column(Integer, primary_key=True)
        timestamp = Column(Date)
        host = Column(String)
        requests = Column(Integer)

class StatusCounts(Base):
        __tablename__ = "status_counts"
        id = Column(Integer, primary_key=True)
        timestamp = Column(Date)
        status = Column(String)
        requests = Column(Integer)


Base.metadata.create_all(engine)

db = Session()
today = datetime.datetime.now().date()-datetime.timedelta(days=1)

for k in sorted(runtimes,key=lambda x: sum(runtimes[x])/len(runtimes[x] )):
    e = LogEntry(endpoint=k,
                 calls=len(runtimes[k]),
                 response_average=sum(runtimes[k])/len(runtimes[k]),
                 max_response=max(runtimes[k]),
                 timestamp=today)
    db.add(e)
    print("%20s\t%7d\t%6.3f\t%7d"%(k,len(runtimes[k]),sum(runtimes[k])/len(runtimes[k]),max(runtimes[k])))

for k,v in sorted(status_counts.items()):
    e = StatusCounts(
        status=k,
        requests=v,
        timestamp=today
    )
    db.add(e)

for k,v in sorted(host_counts.items()):
    e = HostCounts(
        host=k,
        requests=v,
        timestamp=today
    )
    db.add(e)

db.commit()
