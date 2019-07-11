# *******************************
# |docname| - route to a textbook
# *******************************
# This controller provides routes to a specific textbook.
#
# The expected URL is:
#
## base_course/path/subpath/.../book.html
##  args[0]     1     2     ... len(args) - 1


# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
import os
import posixpath
import json
import logging

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

# Third-party imports
# -------------------
# None.
#
# Local application imports
# -------------------------
# None.
#
#
# Supporting functions
# ====================
def _route_book(is_published=True, is_open=False):
    # Get the base course for this book.
    try:
        base_course = request.args[0]
    except:
        raise HTTP(404)

    # See `caching selects <http://web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#Caching-selects>`_.
    cache_kwargs = dict(cache=(cache.ram, 3600), cacheable=True)

    # Ensure the user has access to this book.
    if is_open == False and is_published and not db((db.user_courses.user_id == auth.user.id) &
        (db.user_courses.course_id == auth.user.course_id)).select(
        db.user_courses.id, **cache_kwargs).first():
        session.flash = "Sorry you are not registered for this course.  You can view most Open courses if you log out"
        redirect(URL(c='default', f='courses'))

    # Look up the course name.
    if is_open == False:
        course = db(db.courses.id == auth.user.course_id).select(
            db.courses.course_name, db.courses.base_course, **cache_kwargs).first()
    else:
        course = db(db.courses.course_name == base_course).select(
            db.courses.course_name, db.courses.base_course, **cache_kwargs).first()

    # Make sure this actually refers to the provided base course.
    if course.base_course != base_course:
        redirect(URL(c='default', f='courses'))

    user_is_instructor = 'true' if auth.user and verifyInstructorStatus(auth.user.course_name, auth.user) else 'false'

    # Make this an absolute path.
    book_path = safe_join(os.path.join(request.folder, 'books', base_course,
        'published' if is_published else 'build', base_course),
        *request.args[1:])
    if not book_path:
        raise HTTP(404)

    # See if this is static content. By default, the Sphinx static directory name is ``_static``.
    if len(request.args) > 1 and request.args[1] in ['_static', '_images']:
        # See the `response <http://web2py.com/books/default/chapter/29/04/the-core#response>`_. Warning: this is slow. Configure a production server to serve this statically.
        return response.stream(book_path, 2**20, request=request)
    else:
        # It's HTML -- use the file as a template.
        #
        # Make sure the file exists. Otherwise, the rendered "page" will look goofy.
        if not os.path.isfile(book_path):
            raise HTTP(404)
        response.view = book_path
        chapter = os.path.split(os.path.split(book_path)[0])[1]
        subchapter = os.path.basename(os.path.splitext(book_path)[0])
        div_counts = {}
        if auth.user:
            user_id = auth.user.username
            email = auth.user.email
            is_logged_in = 'true'
            # Get the necessary information to update subchapter progress on the page
            page_divids = db((db.questions.subchapter == subchapter) &
                             (db.questions.base_course == base_course)).select(db.questions.name)
            div_counts = {q.name:0 for q in page_divids}
            sid_counts = db((db.questions.subchapter == subchapter) &
                            (db.questions.base_course == base_course) &
                            (db.questions.name == db.useinfo.div_id) &
                            (db.useinfo.course_id == auth.user.course_name) &
                            (db.useinfo.sid == auth.user.username)).select(db.useinfo.div_id, distinct=True)
            for row in sid_counts:
                div_counts[row.div_id] = 1
        else:
            user_id = 'Anonymous'
            email = ''
            is_logged_in = 'false'

        if session.readings:
            reading_list = session.readings
        else:
            reading_list = 'null'

        # TODO: - Add log entry for page view
        try:
            db.useinfo.insert(sid=user_id, act='view', div_id=book_path,
                event='page', timestamp=datetime.datetime.utcnow(),
                course_id=course.course_name)
        except:
            logger.debug('failed to insert log record for {} in {} : {} {} {}'.format(sid, course, div_id, event, act))

        return dict(course_name=course.course_name, base_course=base_course, is_logged_in=is_logged_in,
                    user_id=user_id, user_email=email, is_instructor=user_is_instructor, readings=XML(reading_list),
                    activity_info=json.dumps(div_counts), subchapter_list=_subchaptoc(base_course, chapter))


# This is copied verbatim from https://github.com/pallets/werkzeug/blob/master/werkzeug/security.py#L30.
_os_alt_seps = list(sep for sep in [os.path.sep, os.path.altsep]
                    if sep not in (None, '/'))

def _subchaptoc(course, chap):
    res = db( (db.chapters.id == db.sub_chapters.chapter_id) &
            (db.chapters.course_id == course ) &
            (db.chapters.chapter_label == chap) ).select(db.chapters.chapter_num,
                    db.sub_chapters.sub_chapter_num,
                    db.chapters.chapter_label,
                    db.sub_chapters.sub_chapter_label,
                    db.sub_chapters.sub_chapter_name, orderby=db.sub_chapters.sub_chapter_num,
                    cache=(cache.ram, 3600), cacheable=True)
    toclist = []
    for row in res:
        sc_url = "{}.html".format(row.sub_chapters.sub_chapter_label)
        title = "{}.{} {}".format(row.chapters.chapter_num,
                                 row.sub_chapters.sub_chapter_num,
                                 row.sub_chapters.sub_chapter_name)
        toclist.append(dict(subchap_uri=sc_url, title=title))

    return toclist


# This is copied verbatim from https://github.com/pallets/werkzeug/blob/master/werkzeug/security.py#L216.
def safe_join(directory, *pathnames):
    """Safely join `directory` and one or more untrusted `pathnames`.  If this
    cannot be done, this function returns ``None``.
    :param directory: the base directory.
    :param pathnames: the untrusted pathnames relative to that directory.
    """
    parts = [directory]
    for filename in pathnames:
        if filename != '':
            filename = posixpath.normpath(filename)
        for sep in _os_alt_seps:
            if sep in filename:
                return None
        if os.path.isabs(filename) or \
           filename == '..' or \
           filename.startswith('../'):
            return None
        parts.append(filename)
    return posixpath.join(*parts)


# Endpoints
# =========
# This serves pages directly from the book's build directory. Therefore, restrict access.
@auth.requires(lambda: verifyInstructorStatus(auth.user.course_name, auth.user), requires_login=True)
def draft():
    return _route_book(False)


# Serve from the ``published`` directory, instead of the ``build`` directory.
def published():
    if auth.user:
        return _route_book()
    else:
        base_course = request.args(0)
        course = db(db.courses.course_name == base_course).select(cache=(cache.ram, 3600), cacheable=True).first()
        if course:
            if course.login_required == 'T':
                if auth.user:
                    return _route_book()
                else:
                    redirect(URL(c='default', f='user'))
            else:
                return _route_book(is_open=True)
        else:
            redirect(URL(c='default', f='user'))
