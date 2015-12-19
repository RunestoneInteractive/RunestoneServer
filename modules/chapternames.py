from __future__ import print_function
import os
from sqlalchemy import create_engine, Table, MetaData, select, delete
from collections import OrderedDict
import sys
from functools import reduce


def findFullTitle(ftext, start):
    found = False
    while not found and start > 0:
        if ":::" in ftext[start]:
            return ftext[start - 1].strip()
        start -= 1
    return ""


def unCamel(x):
    return reduce(lambda a, b: a + ((b.upper() == b and
                                     (len(a) and a[-1].upper() != a[-1])) and
                                    (' ' + b) or b), x, '')


def findChaptersSubChapters(tocfile):
    ftext = open(tocfile, 'r').readlines()
    toclines = [x for x in range(len(ftext)) if 'toctree' in ftext[x]]
    chdict = OrderedDict()
    chtitles = {}
    for i in range(len(toclines)):
        start = toclines[i]
        if i + 1 == len(toclines):
            stop = len(ftext)
        else:
            stop = toclines[i + 1]
        for j in range(start, stop):
            if ".rst" in ftext[j] and "/" in ftext[j]:
                chapter, subchapter = ftext[j].strip()[:-4].split('/')
                chapter = chapter.strip()
                subchapter = subchapter.strip()
                if chapter not in chdict:
                    chdict[chapter] = []
                    ft = findFullTitle(ftext, start)
                    chtitles[chapter] = ft
                chdict[chapter].append(subchapter)

    return chdict, chtitles


def addChapterInfoToDB(subChapD, chapTitles, course_id):
    dbname = 'runestone'
    uname = os.environ['USER']
    if uname == 'bnmnetp':
        uname = 'bnmnetp_courselib'
        dbname = 'bnmnetp_courselib'

    dburl = 'postgresql://{}@localhost/{}'.format(uname,dbname)
    engine = create_engine(dburl)
    meta = MetaData()
    chapters = Table('chapters', meta, autoload=True, autoload_with=engine)
    sub_chapters = Table('sub_chapters', meta, autoload=True, autoload_with=engine)

    engine.execute(chapters.delete().where(chapters.c.course_id == course_id))

    for chapter in subChapD:
        print(chapter)
        ins = chapters.insert().values(chapter_name=chapTitles[chapter],
                                       course_id=course_id, chapter_label=chapter)
        res = engine.execute(ins)
        currentRowId = res.inserted_primary_key[0]
        for subchaptername in subChapD[chapter]:
            ins = sub_chapters.insert().values(sub_chapter_name=unCamel(subchaptername),
                                               chapter_id=str(currentRowId),
                                               sub_chapter_label=subchaptername)
            engine.execute(ins)

def addChapterInfoUsingDAL(subChapD, chapTitles, course_id):
    sys.path.insert(0, os.path.join('..', '..', '..', '..','gluon'))
    from dal import DAL, Field

    module_path = os.path.abspath(os.path.dirname(__file__))
    dbpath = os.path.join(module_path, '..', 'databases')

    sys.path.insert(0, os.path.join('..', 'models'))
    _temp = __import__('0', globals(), locals())
    settings = _temp.settings
    exec(compile(open(os.path.join('..', 'models', '1.py')).read(), os.path.join('..', 'models', '1.py'), 'exec'), globals(), locals())

    db = DAL(settings.database_uri, folder=dbpath, auto_import=False)
    exec(compile(open(os.path.join('..', 'models', 'db_ebook_chapters.py')).read(), os.path.join('..', 'models', 'db_ebook_chapters.py'), 'exec'))

    addChapterInfoFromScheduler(subChapD, chapTitles, course_id, db)


def addChapterInfoFromScheduler(subChapD, chapTitles, course_id, db):
    myset = db(db.chapters.course_id == course_id)
    myset.delete()
    db.commit()
    print("Adding Chapter Info to DB")
    for chapter in subChapD:
        print(chapter)
        currentRowId = db.chapters.insert(chapter_name=chapTitles[chapter], course_id=course_id, chapter_label=chapter)
        for subchaptername in subChapD[chapter]:
            db.sub_chapters.insert(sub_chapter_name=unCamel(subchaptername),
                                   chapter_id=currentRowId,
                                   sub_chapter_label=subchaptername)
        db.commit()


def populateChapterInfo(project_name, index_file):
    scd, ct = findChaptersSubChapters(index_file)
    # addChapterInfoToDB(scd, ct, project_name)
    try:
        addChapterInfoUsingDAL(scd, ct, project_name)
    except Exception as e:
        print("trying alternative database access due to ", e)
        try:
            addChapterInfoToDB(scd, ct, project_name)
        except Exception as e:
            print("Chapter Information DB not updated due to ", e)


if __name__ == '__main__':
    # todo:  get file, and course_id from environment
    populateChapterInfo('pythonds', 'index.rst')
