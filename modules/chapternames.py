import os
import psycopg2
from collections import OrderedDict
import sys


def findFullTitle(ftext, start):
    found = False
    while not found and start > 0:
        if ":::" in ftext[start]:
            return ftext[start - 1]
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
                chapter, subchapter = ftext[j][:-5].split('/')
                chapter = chapter.strip()
                subchapter = subchapter.strip()
                if chapter not in chdict:
                    chdict[chapter] = []
                    ft = findFullTitle(ftext, start)
                    chtitles[chapter] = ft
                chdict[chapter].append(subchapter)

    return chdict, chtitles


def addChapterInfoToDB(subChapD, chapTitles, course_id):
    uname = os.environ['USER']
    db = psycopg2.connect(database="runestone", user=uname)
    cursor = db.cursor()
    cursor.execute("DELETE from chapters where course_id='%s'" % course_id)
    db.commit()
    for chapter in subChapD:
        print chapter
        res = cursor.execute(
            "INSERT INTO chapters(chapter_name,course_id,chapter_label) VALUES(%(chapter)s, %(course_id)s, %(chapterLabel)s) returning id",
            {"chapter": chapTitles[chapter], "course_id": course_id, "chapterLabel": chapter})
        db.commit()
        currentRowId = cursor.fetchone()[0]
        for subchaptername in subChapD[chapter]:
            res = cursor.execute('''INSERT INTO sub_chapters(sub_chapter_name,chapter_id, sub_chapter_label)
                                    VALUES(%(subchaptername)s, %(currentRowId)s, %(subChapterLabel)s)''',
                                 {"subchaptername": unCamel(subchaptername),
                                  "currentRowId": str(currentRowId), "subChapterLabel": subchaptername})
        db.commit()


def addChapterInfoUsingDAL(subChapD, chapTitles, course_id):
    sys.path.insert(0, os.path.join('..', '..', '..'))
    try:
        from gluon.dal import DAL, Field
    except ImportError:
        print "... WARNING ..."
        print "Cannot Update Chapter and Subchapter Tables in Database"
        print "Because I am unable to import DAL from web2py"
        print "In order to update, this application should be installed"
        print "in the applications folder of a web2py installation"
        return False

    module_path = os.path.abspath(os.path.dirname(__file__))
    dbpath = os.path.join(module_path, '..', 'databases')

    sys.path.insert(0, os.path.join('..', 'models'))
    _temp = __import__('0', globals(), locals())
    settings = _temp.settings
    execfile(os.path.join('..', 'models', '1.py'), globals(), locals())

    db = DAL(settings.database_uri, folder=dbpath, auto_import=False)
    execfile(os.path.join('..', 'models', 'db_ebook_chapters.py'))

    addChapterInfoFromScheduler(subChapD, chapTitles, course_id, db)


def addChapterInfoFromScheduler(subChapD, chapTitles, course_id, db):
    myset = db(db.chapters.course_id == course_id)
    myset.delete()
    db.commit()
    print "Adding Chapter Info to DB"
    for chapter in subChapD:
        print chapter
        currentRowId = db.chapters.insert(chapter_name=chapTitles[chapter], course_id=course_id, chapter_label=chapter)
        for subchaptername in subChapD[chapter]:
            db.sub_chapters.insert(sub_chapter_name=unCamel(subchaptername),
                                   chapter_id=currentRowId,
                                   sub_chapter_label=subchaptername)
        db.commit()


def populateChapterInfo(project_name, index_file):
    scd, ct = findChaptersSubChapters(index_file)
    # addChapterInfoToDB(scd, ct, project_name)
    addChapterInfoUsingDAL(scd, ct, project_name)


if __name__ == '__main__':
    # todo:  get file, and course_id from environment
    populateChapterInfo('pythonds', 'index.rst')
