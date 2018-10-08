__author__ = 'bmiller'

try:
    import psycopg2
except ImportError:
    print("Cannot import psycopg2, lintMany will fail.")
import os
import re
from pylint import epylint as lint


def get_lint(code, divid, sid):
    try:
        fn = os.path.join('/tmp', sid + divid + '.py')
        tfile = open(fn, 'w')
        tfile.write(code)
        tfile.close()
    except Exception as e:
        print("failed to open/write file ", sid, divid)
        print(str(e))

    pyl_opts = ' --msg-template="{C}: {symbol}: {msg_id}:{line:3d},{column}: {obj}: {msg}" '
    pyl_opts += ' --reports=n '
    pyl_opts += ' --rcfile='+os.path.join(os.getcwd(), "applications/runestone/pylintrc")
    #pyl_opts += ' --rcfile=' + os.path.join(os.getcwd(), "../pylintrc")
    try:
        (pylint_stdout, pylint_stderr) = lint.py_run(fn + pyl_opts, True, script='pylint')
    except:
        print("lint failed")
        pylint_stdout = ""

    try:
        os.unlink(fn)
    except:
        pass
    return pylint_stdout


def lint_one(code, conn, curs, divid, row, sid):
    pylint_stdout = get_lint(code, divid, sid)
    for line in pylint_stdout:
        g = re.match(r"^([RCWEF]):\s(.*?):\s([RCWEF]\d+):\s+(\d+),(\d+):(.*?):\s(.*)$", line)
        if g:
            ins = '''insert into coach_hints (category,symbol,msg_id,line,col,obj,msg,source)
                 values('%s','%s','%s',%s,%s,'%s','%s',%d)''' % (
            g.groups()[:-1] + (g.group(7).replace("'", ''), row[0],))
            # print(ins)
            curs.execute(ins)
    conn.commit()



def lintMany():

    q = '''select id, timestamp, sid, div_id, code, emessage
           from acerror_log
           order by timestamp
    '''

    conn = psycopg2.connect(database='runestone', user='bmiller', host='localhost')
    curs = conn.cursor()

    curs.execute(q)
    rows = curs.fetchall()

    for row in rows:
        code = row[4]
        divid = row[3]
        sid = row[2]
        lint_one(code, conn, curs, divid, row, sid)


if __name__ == '__main__':
    lintMany()

