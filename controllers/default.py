# -*- coding: utf-8 -*-
### required - do no delete
import json


def user(): 
    form = auth()

    # this looks horrible but it seems to be the only way to add a CSS class to the submit button
    form.element(_id='submit_record__row')[1][0]['_class']='btn btn-small'

    if 'register' in request.args(0):
        # parse the referring URL to see if we can pre-populate the course_id field in
        # the registration form

        form.vars.course_id = '' # set it to be empty if we can't pre-populate
        ref = request.env.http_referer
        if ref:
            if '_next' in ref:
                ref = ref.split("_next")
                url_parts = ref[1].split("/")
            else:
                url_parts = ref.split("/")

            for i in range(len(url_parts)):
                if "static" in url_parts[i]:
                    course_id = url_parts[i+1]
                    form.vars.course_id = course_id
                break

    if 'profile' in request.args(0):
        form.vars.course_id = auth.user.course_name
        if form.process().accepted:
            # auth.user session object doesn't automatically update when the DB gets updated
            auth.user.update(form.vars)
            auth.user.course_name = db(db.auth_user.id == auth.user.id).select()[0].course_name
            redirect(URL('default', 'index'))

    if 'login' in request.args(0):
        # add info text re: using local auth. CSS styled to match text on Janrain form
        sign_in_text = TR(TD('Sign in with your Runestone Interactive account', _colspan='3'), _id='sign_in_text')
        form[0][0].insert(0, sign_in_text)

    return dict(form=form)

def download(): return response.download(request,db)
def call(): return service()
### end requires

@auth.requires_login()
def index():
    course = db(db.courses.id == auth.user.course_id).select(db.courses.course_id).first()
    
    if 'boguscourse' in course.course_id:
        # if login was handled by Janrain, user didn't have a chance to choose the course_id;
        # redirect them to the profile page to choose one
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

    
