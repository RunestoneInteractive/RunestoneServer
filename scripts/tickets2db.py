#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import hashlib
import os
import pathlib
import pickle
import shutil
import stat
import sys
import time

from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm.session import sessionmaker

SLEEP_MINUTES = 5

errors_path = os.path.join(request.folder, "errors")
tickets_path = pathlib.Path(request.folder, "books", "tickets")
tickets_path.mkdir(exist_ok=True)

if os.environ["WEB2PY_CONFIG"] == "production":
    db_string = os.environ["DBURL"]
elif os.environ["WEB2PY_CONFIG"] == "development":
    db_string = os.environ["DEV_DBURL"]
else:
    # no need to run during testing
    sys.exit(0)

engine = create_engine(db_string)
Session = sessionmaker()
engine.connect()
Session.configure(bind=engine)
sess = Session()
meta = MetaData()
# the traceback table is defined by bookserver.models
traceback = Table("traceback", meta, autoload=True, autoload_with=engine)

hashes = {}

while 1:

    for file in os.listdir(errors_path):
        filename = os.path.join(errors_path, file)

        modified_time = os.stat(filename)[stat.ST_MTIME]
        modified_time = datetime.datetime.fromtimestamp(modified_time)
        with open(filename, "rb") as f:
            ticket_data = pickle.load(f)
        ticket_id = file
        traceback_str = ticket_data["traceback"]
        emess = ticket_data["output"]
        try:
            soup = BeautifulSoup(ticket_data["snapshot"]["request"].text)
            path = ""
            query_string = ""
            for row in soup.find_all("tr"):
                if row.get_text().startswith("raw_uri"):
                    path = row.get_text()
                if row.get_text().startswith("query_string"):
                    query_string = row.get_text()
            if path:
                path = path.split(":")[-1]
            if query_string:
                query_string = query_string.split(":")[-1]
        except:
            path = ""
            query_string = ""
        newtb = traceback.insert().values(
            traceback=traceback_str,
            timestamp=datetime.datetime.utcnow(),
            err_message=ticket_data["output"],
            hostname="web2py",
            path=path,
            query_string=query_string,
            hash=hashlib.md5(traceback_str.encode("utf8")).hexdigest(),
        )
        sess.execute(newtb)
        sess.commit()
        shutil.move(filename, tickets_path)

    time.sleep(SLEEP_MINUTES * 60)
