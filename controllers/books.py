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
def _route_book(is_published=True):
    # Get the base course for this book.
    try:
        base_course = request.args[0]
    except:
        raise HTTP(404)

    # See `caching selects <http://web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#Caching-selects>`_.
    cache_kwargs = dict(cache=(cache.ram, 3600), cacheable=True)

    # Ensure the user has access to this book.
    if is_published and not db((db.user_courses.user_id == auth.user.id) &
        (db.user_courses.course_id == auth.user.course_id)).select(
        db.user_courses.id, **cache_kwargs).first():

        redirect(URL(c='default', f='courses'))

    # Look up the course name.
    course = db(db.courses.id == auth.user.course_id).select(
        db.courses.course_name, db.courses.base_course, **cache_kwargs).first()
    # Make sure this actually refers to the provided base course.
    if course.base_course != base_course:
        redirect(URL(c='default', f='courses'))

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
        return dict(course_name=course.course_name, base_course=base_course,
                    user_id=auth.user.username, email=auth.user.email)


# This is copied verbatim from https://github.com/pallets/werkzeug/blob/master/werkzeug/security.py#L30.
_os_alt_seps = list(sep for sep in [os.path.sep, os.path.altsep]
                    if sep not in (None, '/'))


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


@auth.requires_login()
# Serve from the ``published`` directory, instead of the ``build`` directory.
def published():
    return _route_book()
