from sqlalchemy import create_engine, Table, MetaData, select
import datetime
import os, re


def insertAnswer(sid, divid, ts, course, correct, passed, failed):
    print("inserting ", sid, divid, course, ts, passed, failed)
    s = unit_answers.insert().values(
        timestamp=ts,
        div_id=divid,
        sid=sid,
        course_name=course,
        correct=correct,
        passed=passed,
        failed=failed,
    )
    engine.execute(s)


engine = create_engine(os.environ["DEV_DBURL"])

meta = MetaData()
useinfo = Table("useinfo", meta, autoload=True, autoload_with=engine)
unit_answers = Table("unittest_answers", meta, autoload=True, autoload_with=engine)

s = select([useinfo]).where(useinfo.c.event == "unittest").order_by(useinfo.c.id)
result = engine.execute(s)

for row in result:
    # ignore sid's of the form:  1423153196780@199.185.67.12 or 208.191.24.178@anon.user
    if re.match(r"^\d+@[\d\.]+$", row["sid"]):
        continue

    try:
        statslist = row["act"].split(":")
        pct = float(statslist[1])
        passed = int(statslist[3])
        failed = int(statslist[5])
        if pct >= 99.99999:
            correct = "T"
        else:
            correct = "F"
    except:
        print(f"bad act data {row['act']}")
        continue
    insertAnswer(
        row["sid"],
        row["div_id"],
        row["timestamp"],
        row["course_id"],
        correct,
        passed,
        failed,
    )
