import os
import psycopg2
from collections import OrderedDict



def findFullTitle(ftext, start):
    found = False
    while not found and start > 0:
        if ":::" in ftext[start]:
            return ftext[start-1]
        start -= 1
    return ""


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
            # todo: Need to get full subchapter name
            res = cursor.execute('''INSERT INTO sub_chapters(sub_chapter_name,chapter_id, sub_chapter_label)
                                    VALUES(%(subchaptername)s, %(currentRowId)s, %(subChapterLabel)s)''',
                                 {"subchaptername":subchaptername , "currentRowId" : str(currentRowId), "subChapterLabel": subchaptername })
        db.commit()



if __name__ == '__main__':
    # todo:  get file, and course_id from environment
    scd,ct = findChaptersSubChapters('index.rst')
    addChapterInfoToDB(scd,ct,'pythonds')
