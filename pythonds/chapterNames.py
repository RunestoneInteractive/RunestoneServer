import lxml.etree
import lxml.html
import urllib2
import os
import sqlite3
import sys
import psycopg2


os.chdir("../static/pythonds")
course_id = '3'
file_url = "file:///"+os.getcwd()+"/index.html"

teste =  urllib2.urlopen(file_url).read()
tree = lxml.etree.HTML(teste)
tds = tree.xpath('//div[@class="section"]')

#os.chdir(sys.path[0]+"\\..\\databases")
db = sqlite3.connect('storage.sqlite')
uname = os.environ['USER']
db = psycopg2.connect(database="runestone",user=uname)
cursor=db.cursor()
cursor.execute("DELETE from chapters where course_id=%s" % course_id)
#cursor.execute("SELECT setval('chapters_id_seq', 1);")
#cursor.execute("DELETE from sqlite_sequence where name='chapters'")
#cursor.execute("DELETE from sub_chapters where course_id" % course_id)
#cursor.execute("SELECT setval('sub_chapters_id_seq', 1);")
#cursor.execute("DELETE from sqlite_sequence where name='sub_chapters'")
db.commit()

for section in tds[:-2]:

    checkFlag = 0
    currentRowId = 1
    for subchapter in section.xpath('div/ul/li/a'):
        subchaptername =  "".join(subchapter.xpath('descendant-or-self::text()')) #get only the text content of the selected node, ignoring all tags
        #print subchaptername.encode('ascii', 'ignore') #use encode to eliminate unicodeenodeerror
        urlArray = (subchapter.attrib['href']).split("/")
        subChapterLabel = urlArray[1].split(".")[0]
        if checkFlag == 0:
            checkFlag = 1
            chapter = section.xpath('h1')[0].text
            print "Chapter = ", chapter, urlArray[0]
            res = cursor.execute("INSERT INTO chapters(chapter_name,course_id,chapter_label) VALUES(%(chapter)s, %(course_id)s, %(chapterLabel)s) returning id", {"chapter": chapter, "course_id": course_id, "chapterLabel": urlArray[0]})
            db.commit()
#            currentRowId = cursor.lastrowid #get id of last inserted row
            currentRowId = cursor.fetchone()[0]
        print subchaptername, subChapterLabel
        res = cursor.execute("INSERT INTO sub_chapters(sub_chapter_name,chapter_id, sub_chapter_label) VALUES(%(subchaptername)s, %(currentRowId)s, %(subChapterLabel)s)", {"subchaptername":subchaptername , "currentRowId" : str(currentRowId), "subChapterLabel": subChapterLabel })
        db.commit()
    checkFlag = 0
