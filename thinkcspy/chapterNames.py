import lxml.etree
import lxml.html
import urllib2
import os
import sqlite3
import sys 



os.chdir("..\\static\\thinkcspy")
course_id = '1';
file_url = "file:///"+os.getcwd()+"\\toc.html"

teste =  urllib2.urlopen(file_url).read()
tree = lxml.etree.HTML(teste)
tds = tree.xpath('//div[@class="section"]')

os.chdir(sys.path[0]+"\\..\\databases")
db = sqlite3.connect('storage.sqlite')
cursor=db.cursor()

db.execute("DELETE from chapters")
db.execute("DELETE from sqlite_sequence where name='chapters'")
db.execute("DELETE from sub_chapters")
db.execute("DELETE from sqlite_sequence where name='sub_chapters'")
db.commit()

for section in tds[1:-3]:

    checkFlag = 0
    for subchapter in section.xpath('div/ul/li/a'):
        subchaptername =  "".join(subchapter.xpath('descendant-or-self::text()')) #get only the text content of the selected node, ignoring all tags
        #print subchaptername.encode('ascii', 'ignore') #use encode to eliminate unicodeenodeerror
        urlArray = (subchapter.attrib['href']).split("/")
        subChapterLabel = urlArray[1].split(".")[0]
        if checkFlag == 0:
            checkFlag = 1
            chapter = section.xpath('h1')[0].text
            cursor = db.execute("INSERT INTO chapters('chapter_name','course_id','chapter_label') VALUES(:chapter, :course_id, :chapterLabel)", {"chapter": chapter, "course_id": course_id, "chapterLabel": urlArray[0]})
            db.commit()    
            currentRowId = cursor.lastrowid #get id of last inserted row
        cursor = db.execute("INSERT INTO sub_chapters('sub_chapter_name','chapter_id', 'sub_chapter_label') VALUES(:subchaptername, :currentRowId, :subChapterLabel)", {"subchaptername":subchaptername , "currentRowId" : str(currentRowId), "subChapterLabel": subChapterLabel })
        db.commit()
    checkFlag = 0