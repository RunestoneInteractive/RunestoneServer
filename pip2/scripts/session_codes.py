## This file is a utility for finding the divids associated with particular class sessions, in order to do checkmark grading
import psycopg2
import connection_string
# make DB connection; import connection string from other file,
# "dbname= user= password=" 
conn = psycopg2.connect(connection_string.connection)
cur = conn.cursor()

def get_codes(fnames):
    res = []
  
    for fname in fnames:
        fname = fname[:-4]  # get rid of '.rst'
        # append the URL for the subchapter as an activity, so that when the user opens that subchapter, it counts as an activity
        res.append("/runestone/static/pip2/" + fname + ".html")
        
        # extract the Chapter and Subchapter labels
        [ch, sub_ch] = fname.split("/")
        # get all the div_ids for problems in the chapter and append them as well
        cur.execute("select div_id from div_ids where chapter = %s and subchapter = %s", (ch, sub_ch))
        for row in cur.fetchall():
            res.append(row[0])
    return res

# For each session, provide a list of subchapter .rst files (find them in the toc.rst file)

sessions = {}
sessions[2] = ["GeneralIntro/intro-TheWayoftheProgram.rst", "GeneralIntro/Algorithms.rst", "GeneralIntro/ThePythonProgrammingLanguage.rst", "GeneralIntro/SpecialWaystoExecutePythoninthisBook.rst", "GeneralIntro/MoreAboutPrograms.rst", "GeneralIntro/WhatisDebugging.rst", "GeneralIntro/Syntaxerrors.rst", "GeneralIntro/RuntimeErrors.rst", "GeneralIntro/SemanticErrors.rst", "GeneralIntro/ExperimentalDebugging.rst", "GeneralIntro/FormalandNaturalLanguages.rst", "GeneralIntro/ATypicalFirstProgram.rst", "GeneralIntro/Comments.rst", "GeneralIntro/Glossary.rst"]


f = open('session_codes.txt', 'w')
g = open('json_sessin_codes.txt', 'w')

for k in sessions:
    codes = get_codes(sessions[k])
    #print "session%d\t%d\t%s" % (k, len(codes), ', '.join(codes))
    f.write("session%d\t%d\t%s\n" % (k, len(codes), ', '.join(codes)))
    g.write("session%d\t%d\t%s\n" % (k, len(codes), codes))

f.close()
g.close()