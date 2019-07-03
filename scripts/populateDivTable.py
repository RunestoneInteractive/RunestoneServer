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
    r'\s*\.\.\s+(activecode|codelens|mchoicemf|mchoicema|parsonsprob|animation|actex|fillintheblank|mcmfrandom|video)\s*::\s+(.*)$'
)

odd_ex_list = [
'ch02_ex1',
'ex_2_3',
'ex_2_5',
'ex_2_7',
'ex_2_9',
'ex_2_11',
'ex_3_1',
'ex_3_3',
'ex_3_5',
'ex_3_7',
'ex_3_9',
'ex_3_11',
'ex_3_13',
'mod_q1',
'ex_5_1',
'ex_5_3',
'ex_5_5',
'ex_5_7',
'ex_5_9',
'ex_5_11',
'ex_5_13',
'ex_5_15',
'ex_5_17',
'ex_6_1',
'ex_6_3',
'ex_6_5',
'ex_6_7',
'ex_6_9',
'ex_6_11',
'ex_6_13',
'ex_7_7',
'ex_7_9',
'ex_7_13',
'ex_7_15',
'ex_7_17',
'ex_7_19',
'ex_7_21',
'ex_7_23',
'ex_7_10',
'ex_8_3',
'ex_8_6',
'ex_8_8',
'ex_8_10',
'ex_8_12',
'ex_8_14',
'ex_8_16',
'ex_8_18',
'ex_8_20',
'ex_9_3',
'ex_9_5',
'ex_9_6',
'ex_9_8',
'ex_9_10',
'ex_9_12',
'ex_9_14',
'ex_6_1',
'ex_6_3',
'ex_10_5',
'ex_11_01',
'ex_11_02',
'ex_11_04',
'ex_rec_1',
'ex_rec_3',
'ex_rec_5',
'ex_rec_7']

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
            print(chapter, subchapter, mo.group(1), mo.group(2))
            divt = mo.group(1)
            divid = mo.group(2)
            if divt == 'actex' and divid in odd_ex_list:
                divt = 'actex_answered'
            div = Divs(chapter=chapter, subchapter=subchapter, div_type=divt, div_id=divid)
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



