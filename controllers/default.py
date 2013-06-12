# -*- coding: utf-8 -*-
### required - do no delete
import json


def user(): 
    form = auth()
    
    env = request['wsgi']['environ']

    # parse the referring URL to see if we can prepopulate the course_id field in 
    # the registration form
    if 'HTTP_REFERER' in env:
        ref = env['HTTP_REFERER']

        if '_next' in ref:
            ref = ref.split("_next")
            url_parts = ref[1].split("/")
            
            for i in range(len(url_parts)):
                if "static" in url_parts[i]:
                    try:
                        course_id = url_parts[i+1]
                        form.vars.course_id = course_id
                        form.process()
                        break
                    except KeyError:
                        # I have no idea if this case of a malformed URL will ever happen
                        break

    return dict(form=form)

def download(): return response.download(request,db)
def call(): return service()
### end requires

@auth.requires_login()
def index():
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_id).first()
    redirect('/%s/static/%s/index.html' % (request.application,course.course_id))

    # web_support = WebSupport(datadir=settings.sphinx_datadir,
    #                 staticdir=settings.sphinx_staticdir,
    #                 docroot=settings.sphinx_docroot)
    # doc = 'index'
    # contents = web_support.get_document(doc)
    # # build seems to create a script entry with duplicates due to different extensions.
    # # need to remove the duplicates.
    # script = contents['script'].split('\n')
    # contents['css'] = contents['css'].replace('/static/','/eds/static/')
    # newl = []
    # for l in script:
    #     if l.strip() == '</script>':
    #         newl.append(l)
    #     elif l not in newl:
    #         newl.append(l)
    # contents['script'] = "\n".join(newl).replace('/static/','/eds/static/')
    # contents['body'] = contents['body'].replace('/static/','/eds/static/')
    # contents['body'] = contents['body'].replace('href="','href="/eds/view/chapter/')    
    # return contents


def error():
    return dict()

def about():
    return dict()

def ack():
    return dict()

    
