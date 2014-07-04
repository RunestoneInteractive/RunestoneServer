__author__ = 'bmiller'

import psycopg2
import os.path
import re
from pylint import epylint as lint
(pylint_stdout, pylint_stderr) = lint.py_run('module_name.py', True)
sid = 'opdajo01'
divid = 'ex_3_10'

q = '''select id, timestamp, sid, div_id, code, emessage
       from acerror_log
       where sid = '%s' and div_id='%s'
       order by timestamp
''' % ('opdajo01', 'ex_3_10')

conn = psycopg2.connect(database='runestone',user='bmiller',host='localhost')
curs = conn.cursor()

curs.execute(q)
rows = curs.fetchall()

for row in rows:
    code = row[4]
    fn = os.path.join('/tmp',sid+divid+'.py')
    tfile = open(fn,'w')
    tfile.write(code)
    tfile.close()

    pyl_opts = ' --msg-template="{C}: {symbol}: {msg_id}:{line:3d},{column}: {obj}: {msg}" '
    pyl_opts += ' --reports=y '
    (pylint_stdout, pylint_stderr) = lint.py_run(fn + pyl_opts, True, script='pylint')

    for line in pylint_stdout:
        g = re.match(r"^([RCWEF]):\s(.*?):\s([RCWEF]\d+):\s+(\d+),(\d+):(.*?):\s(.*)$",line)
        if g:
            print g.groups()
            ins = '''insert into coach_hints (category,symbol,msg_id,line,col,obj,msg,source)
             values('%s','%s','%s',%s,%s,'%s','%s',%d)''' % (g.groups()[:-1] + (g.group(7).replace("'",''), row[0],))
            #print ins
            curs.execute(ins)
    conn.commit()
