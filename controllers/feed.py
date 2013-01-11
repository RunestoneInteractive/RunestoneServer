import os, os.path

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
                ttext = open("%s/%s"%(dname,f)).readline()[:-1]
            else:
                ttext=""
            f = f.replace(".rst",".html")
            args.append(dict(title=ttext,
                             link="http://interactivepython.org%s/%s" %(lname,f),
                             description=""))
    entry_list = []

    os.path.walk("applications/%s/everyday/2013"%request.application,get_posts,entry_list)
    return dict(title="Everyday Python",
                link = "http://interactivepython.org/courselib/feed/everyday",
                description="Everyday Python, Lessons in Python programming",
                entries=entry_list
        )
