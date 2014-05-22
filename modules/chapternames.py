import os
import psycopg2
from collections import OrderedDict
import sys

def findFullTitle(ftext, start):
    found = False
    while not found and start > 0:
        if ":::" in ftext[start]:
            return ftext[start-1]
        start -= 1
    return ""

def unCamel(x): return reduce(lambda a,b: a + ((b.upper() == b and
                                (len(a) and a[-1].upper() != a[-1])) and
                                (' ' + b) or b), x, '')


def findChaptersSubChapters(tocfile):
    ftext = open(tocfile,'r').readlines()
    toclines = [x for x in range(len(ftext)) if 'toctree' in ftext[x]]
    chdict = OrderedDict()
    chtitles = {}
    for i in range(len(toclines)):
        start = toclines[i]
        if i+1 == len(toclines):
            stop=len(ftext)
        else:
            stop = toclines[i+1]
        for j in range(start,stop):
            if ".rst" in ftext[j]:
                chapter,subchapter = ftext[j][:-5].split('/')
                chapter = chapter.strip()
                subchapter = subchapter.strip()
                if chapter not in chdict:
                    chdict[chapter] = []
                    ft = findFullTitle(ftext,start)
                    chtitles[chapter] = ft
                chdict[chapter].append(subchapter)

    return chdict, chtitles


def addChapterInfoToDB(subChapD, chapTitles, course_id):
    uname = os.environ['USER']
    db = psycopg2.connect(database="runestone",user=uname)
    cursor=db.cursor()
    cursor.execute("DELETE from chapters where course_id='%s'" % course_id)
    db.commit()
    for chapter in subChapD:
        print chapter
        res = cursor.execute("INSERT INTO chapters(chapter_name,course_id,chapter_label) VALUES(%(chapter)s, %(course_id)s, %(chapterLabel)s) returning id",
                            {"chapter": chapTitles[chapter], "course_id": course_id, "chapterLabel": chapter})
        db.commit()
        currentRowId = cursor.fetchone()[0]
        for subchaptername in subChapD[chapter]:
            res = cursor.execute('''INSERT INTO sub_chapters(sub_chapter_name,chapter_id, sub_chapter_label)
                                    VALUES(%(subchaptername)s, %(currentRowId)s, %(subChapterLabel)s)''',
                                 {"subchaptername": unCamel(subchaptername) ,
                                  "currentRowId": str(currentRowId), "subChapterLabel": subchaptername })
        db.commit()


def addChapterInfoUsingDAL(subChapD, chapTitles, course_id):
    sys.path.insert(0, '../../../')
    from gluon.dal import DAL, Field

    module_path = os.path.abspath(os.path.dirname(__file__))
    dbpath = module_path + '/../databases/'

    print "dbpath = ", dbpath
    #db = DAL('sqlite://storage.sqlite', folder=dbpath)

    db = DAL('postgres:psycopg2://bmiller@localhost/runestone', folder=dbpath, auto_import=False)
    execfile('../models/db_ebook_chapters.py')
    print "Adding Chapter Info to DB"
    for chapter in subChapD:
        print chapter
        currentRowId = db.chapters.insert(chapter_name=chapTitles[chapter],course_id=course_id,chapter_label=chapter)
        for subchaptername in subChapD[chapter]:
            db.sub_chapters.insert(sub_chapter_name=unCamel(subchaptername),
                                   chapter_id=currentRowId,
                                   sub_chapter_label=subchaptername)
        db.commit()


def populateChapterInfo(project_name, index_file):
    scd, ct = findChaptersSubChapters(index_file)
    #addChapterInfoToDB(scd, ct, project_name)
    addChapterInfoUsingDAL(scd, ct, project_name)

if __name__ == '__main__':
    # todo:  get file, and course_id from environment
    populateChapterInfo('pythonds','index.rst')
