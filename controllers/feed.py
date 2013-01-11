import os, os.path
import time

def everyday():
    def get_posts(args, dname, flist):
        print dname
        l = flist[:]
        for f in l:
            if "~" in f:
                flist.remove(f)
        lname = dname.replace('everyday','static/everyday')
        lname = lname.replace('applications','')
        for f in flist:
            if ".rst" in f:
                efile = open("%s/%s"%(dname,f))
                ttext = efile.readline()[:-1]
                efile.close()
                stime = os.path.getmtime("%s/%s"%(dname,f))
                mtime = time.ctime(stime)
                f = f.replace(".rst",".html")
                args.append(dict(title=ttext,
                                 link="http://interactivepython.org%s/%s" %(lname,f),
                                 description="",
                                 created_on=mtime,
                                 sort_time=stime
                                 ))
    entry_list = []
    os.path.walk("applications/%s/everyday/2013"%request.application,get_posts,entry_list)
    entry_list.sort(key=lambda x: x['sort_time'])
    return dict(title="Everyday Python",
                link = "http://interactivepython.org/courselib/feed/everyday.rss",
                description="Everyday Python, Lessons in Python programming",
                entries=entry_list
        )
