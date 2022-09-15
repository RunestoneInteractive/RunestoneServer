# archive data from runestone database that is more than 2 years old
import os
from sqlalchemy import create_engine

dburl = os.environ["DBURL"]
eng = create_engine(dburl)

for tbl in [
    "clickablearea_answers",
    "codelens_answers",
    "dragndrop_answers",
    "fitb_answers",
    "mchoice_answers",
    "parsons_answers",
    "shortanswer_answers",
    "unittest_answers",
    "code",
    "unittest",
][:1]:
    res = eng.execute(
        f"""select id from {tbl} where timestamp = now()::date - interval '2 years' limit 1""",
        eng,
    ).first()

    max_id = res[0]
    print(f"copying rows from {tbl} before {max_id}")
    # this has to be run on the database server machine or it will fail.  Other options including
    # using pandas may be better if we want to run remotely
    num = eng.execute(
        f"""copy (select * from {tbl} where id < {max_id}) to '{os.environ["HOME"]}/archive_{tbl}_{max_id}.csv' csv header""",
        eng,
    ).first()
    if num and num[0] < 1:
        print("No records copied removing file")
        # remove the file

    print(f"Copied {num}")

    res = eng.execute(f"""delete from {tbl} where id < {max_id}""")
    print(f"deleted {res}")


# To load the csv into the main table ignoring duplicates follow this pattern
# CREATE TEMP TABLE tmp_table
#     ON COMMIT DROP -- omit if doing from psql
#     AS
#     SELECT *
#     FROM main_table
#     WITH NO DATA;
#
#     COPY tmp_table FROM 'full/file/name/here';
#
#     INSERT INTO main_table
#     SELECT DISTINCT ON (PK_field) *
#     FROM tmp_table
#     ORDER BY (some_fields)

# There may also be an option for an ON CONFLiCT DO NOTHING
