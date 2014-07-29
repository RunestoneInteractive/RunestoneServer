__author__ = 'bmiller'

# find all valid divs in the source and populate a database table containing them
#

import os
from os.path import join
import re
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SOURCE_PATH = '../source'

div_re = re.compile(
    r'\.\.\s+(activecode|codelens|mchoicemf|mchoicema|parsonsprob|animation|actex|fillintheblank|mcmfrandom|video)\s*::\s+(.*)$'
)

engine = create_engine('postgresql+psycopg2://bmiller@localhost/bmiller')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Divs(Base):
    __tablename__ = 'div_ids'
    id = Column(Integer, primary_key=True)
    chapter = Column(String)
    subchapter = Column(String)
    div_type = Column(String)
    div_id = Column(String)


Base.metadata.create_all(engine)


def populateSubchapter(fpath, fn, fh):
    chapter = fpath.replace(SOURCE_PATH+'/', '')
    subchapter = fn.replace('.rst', '')
    for line in fh:
        mo = div_re.match(line)
        if mo:
            print chapter, subchapter, mo.group(1), mo.group(2)
            div = Divs(chapter=chapter, subchapter=subchapter, div_type=mo.group(1), div_id=mo.group(2))
            session.add(div)

    session.commit()

for root, dirs, files in os.walk(SOURCE_PATH):
    for fn in files:
        if fn.endswith('.rst'):
                fh = open(join(root, fn), 'r')
                populateSubchapter(root, fn, fh)



# delete chapter = Test and ExtraStuff and ../source
session.query(Divs).filter(Divs.chapter=='Test').delete()
session.query(Divs).filter(Divs.chapter=='ExtraStuff').delete()
session.query(Divs).filter(Divs.chapter==SOURCE_PATH).delete()
session.commit()
