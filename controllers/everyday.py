import datetime
import os.path

def index():
    try:
        f = open(os.path.join(request.folder,'everyday/latest.txt'))
        latest = f.readline()[:-1]
        f.close()
        path = "http://%s/%s/static/everyday/%s" % (request.env.http_host,request.application,latest)
    except:
        path = "http://%s/%s/static/everyday/%s" % (request.env.http_host,request.application,'index.html')

    redirect(path)
