# -*- coding: utf-8 -*-
### required - do no delete
import json


def user(): 
    form = auth()

    # this looks horrible but it seems to be the only way to add a CSS class to the submit button
    # TODO reenable form.element(_id='submit_record__row')[1][0]['_class']='btn btn-small'

    # parse the referring URL to see if we can prepopulate the course_id field in 
    # the registration form
    if 'register' in request.args(0):
        ref = request.env.http_referer
        if ref:
            if '_next' in ref:
                ref = ref.split("_next")
                url_parts = ref[1].split("/")
            else:
                url_parts = ref.split("/")
            
            for i in range(len(url_parts)):
                if "static" in url_parts[i]:
                    try:
                        course_id = url_parts[i+1]
                        form.vars.course_id = course_id
                        form.process()
                        break
                    except (KeyError, AttributeError), e:
                        # Handle a KeyError (malformed URL) or an AttributeError 
                        # (no form.vars.course_id, i.e. it's a normal login form and not a registration form)
                        break

    if 'profile' in request.args(0):
        form.vars.course_id = auth.user.course_name
        if form.process().accepted:
            # for some reason the auth.user session object doesn't automatically update
            auth.user.update(course_id=form.vars.course_id) 

            redirect(URL('default', 'index'))

    return dict(form=form)

def download(): return response.download(request,db)
def call(): return service()
### end requires

@auth.requires_login()
def index():
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_id).first()

    print "Auth.user.course_id: " + str(auth.user.course_id)
    print "Course: " + str(course)

    if not course:
        # If the login process was handled by Janrain, the user didn't have a chance to choose the course_id
        # so we redirect them to the profile page to choose one
        redirect('/%s/default/user/profile?_next=/%s/default/index' % (request.application, request.application))
    else:
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

    
