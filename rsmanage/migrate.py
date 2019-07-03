import re, datetime, os.path
import click
from dateutil.parser import parse

res = db.executesql("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public' AND table_type='BASE TABLE'""")

click.echo("The following migration actions were taken today")
with open(os.path.join('applications','runestone','databases','sql.log')) as action_file:
    last_match = 0
    now = datetime.datetime.now()
    line = action_file.readline()
    while line:
        g = re.match('^timestamp:\s(.*)$', line)
        if g:
            mdate = parse(g.group(1))
            if mdate.year == now.year and mdate.month == now.month and mdate.day == now.day:
                done = False
                while line and not done:
                    line = action_file.readline()
                    click.echo(line, nl=False)
                    if re.match('^success!',line):
                        done = True
        line = action_file.readline()

