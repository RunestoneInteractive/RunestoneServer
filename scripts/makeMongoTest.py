__author__ = 'bmiller'

# Proof of concept for converting the relational database into a document
# oriented database

from sqlalchemy import create_engine, MetaData, select
from pymongo import MongoClient


engine = create_engine('postgresql://bmiller:grouplens@localhost/runestone')
conn = engine.connect()

client = MongoClient()
db = client.test



# Use metadata to load all existing tables
meta = MetaData()
meta.reflect(bind=engine)
useinfo = meta.tables['useinfo']
user_sub_chapter_progress = meta.tables['user_sub_chapter_progress']
visited_pages = conn.execute(select([user_sub_chapter_progress]).where(user_sub_chapter_progress.c.user_id == 11 and user_sub_chapter_progress.c.status == 0))


for apage in visited_pages:
    sub_chapter_id = apage['sub_chapter_id']

    page = { 'pageShortName': sub_chapter_id,
             'assessments': [],
             'activecodes': [],
             'highlights': [],
             }

    subchapter_divs = conn.execute("select div_type, div_id from div_ids where subchapter = '{}' and course_name = '{}'".format(sub_chapter_id,'bmillernb3') )


    for row in subchapter_divs:
        rr = conn.execute("select * from useinfo where sid = '{}' and div_id = '{}' ".format('bmiller',row['div_id'])).fetchone()
        if rr is not None:
            if row['div_type'] == 'activecode':
                page['activecodes'].append({'activecode_id': rr['div_id'],
                                            'timestamp': rr['timestamp'],
                                            })
            elif row['div_type'] == 'mchoicemf':
                page['assessments'].append({
                    'assessment_id': rr['div_id'],
                    'timestamp': rr['timestamp'],
                    'answer': rr['act'],
                })

    print(db.trialpages.insert_one(page).inserted_id)
    print(db.collection_names())