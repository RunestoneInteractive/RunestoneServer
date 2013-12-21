# Setup sqlite database to support query logging from web_exec.py

import os, sqlite3

DB_FILE = 'opt-query-log.sqlite3'

def create_db():
  con = sqlite3.connect(DB_FILE)
  cur = con.cursor()

  cur.execute('''CREATE TABLE query_log
    (id INTEGER PRIMARY KEY,
     timestamp TEXT,
     ip_addr TEXT,
     http_user_agent TEXT,
     http_referer TEXT,
     user_script TEXT,
     cumulative_mode INTEGER)''')
  con.commit()
  cur.close()


if __name__ == "__main__":
  assert not os.path.exists(DB_FILE)
  create_db()
  print('Created ' + DB_FILE)

