# *******************************
# |docname| - route to a textbook
# *******************************
# This controller provides routes to a specific textbook page.
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
import datetime
import importlib
import random

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

# Third-party imports
# -------------------
# None.
#
# Local application imports
# -------------------------
# None.


# Supporting functions
# ====================
def _route_book(is_published=True, is_custom=False, directory_name=None):
    motd = ""
    donated = False
    attrdict = {}
    settings.show_rs_banner = False
    courseless_custom_published = (
        False
    )  # for custom published books, they should be visible if you are enrolled in a course for them, but also if you are the owner and not in a course for them (the latter is when this is set to True)
    if (not is_custom) or (
        is_custom and request.args[0] == "published"
    ):  # try displaying the book as part of a course
        while (
            True
        ):  # used to break out of this section early when dealing with published versions of custom books (they can be displayed courselessly)
            # Get the base course passed in ``request.args[0]``, or return a 404 if that argument is missing.
            base_course = (
                (request.args(1) + "/" + request.args(2))
                if is_custom
                else request.args(0)
            )
            if not base_course:
                raise HTTP(404)

            # Does this book originate as a Runestone book or a PreTeXt book.
            # if it is pretext book we use different delimiters for the templates
            # as LaTeX is full of {{
            # These values are set by the runestone process-manifest command
            res = getCourseOrigin(base_course)
            if res and res.value == "PreTeXt":
                response.delimiters = settings.pretext_delimiters

            # See `caching selects <http://web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#Caching-selects>`_.
            cache_kwargs = dict(cache=(cache.ram, 3600), cacheable=True)
            allow_pairs = "false"
            downloads_enabled = "false"
            # Find the course to access.
            if auth.user:
                # Given a logged-in user, use ``auth.user.course_id``.
                response.cookies["last_course"] = auth.user.course_name
                response.cookies["last_course"]["expires"] = (
                    24 * 3600 * 90
                )  # 90 day expiration
                response.cookies["last_course"]["path"] = "/"

                # Get `course info <courses table>`.
                course = (
                    db(db.courses.id == auth.user.course_id)
                    .select(
                        db.courses.id,
                        db.courses.course_name,
                        db.courses.base_course,
                        db.courses.allow_pairs,
                        db.courses.downloads_enabled,
                        db.courses.term_start_date,
                        db.courses.courselevel,
                        # **cache_kwargs, ###TODO uncomment this. caching should be used, but as it is currently implemented causes problems when the name of a custom book is changed. The new value for the base_course of a course does not match the cached value
                    )
                    .first()
                )
                if auth.user.donated:
                    donated = True

                # If we cannot properly get the course for a published custom book, break from this loop and try serving it courselessly
                course_error = (not course) or course.base_course != base_course
                if course_error and (
                    is_custom
                    and request.args[0] == "published"
                    and request.args[1] == auth.user.username
                ):
                    courseless_custom_published = True
                    break
                # Ensure the base course in the URL agrees with the base course in ``course``.
                # If not, ask the user to select a course.
                if course_error:
                    session.flash = "{} is not the course you are currently in,  switch to or add it to go there".format(
                        base_course
                    )
                    redirect(URL(c="default", f="courses"))

                attrdict = getCourseAttributesDict(course.id)
                # set defaults for various attrs
                if "enable_compare_me" not in attrdict:
                    attrdict["enable_compare_me"] = "true"

                # Determine if we should ask for support
                # Trying to do banner ads during the 2nd and 3rd weeks of the term
                # but not to high school students or if the instructor has donated for the course
                now = datetime.datetime.utcnow().date()
                week2 = datetime.timedelta(weeks=2)
                week4 = datetime.timedelta(weeks=4)
                if (
                    now >= (course.term_start_date + week2)
                    and now <= (course.term_start_date + week4)
                    and course.base_course != "csawesome"
                    and course.courselevel != "high"
                    and getCourseAttribute(course.id, "supporter") is None
                ):
                    settings.show_rs_banner = True
                elif (
                    course.course_name == course.base_course and random.random() <= 0.2
                ):
                    # Show banners to base course users 20% of the time.
                    settings.show_rs_banner = True

                allow_pairs = "true" if course.allow_pairs else "false"
                downloads_enabled = "true" if course.downloads_enabled else "false"
                # Ensure the user has access to this book.
                if (
                    is_published
                    and not db(
                        (db.user_courses.user_id == auth.user.id)
                        & (db.user_courses.course_id == auth.user.course_id)
                    )
                    .select(db.user_courses.id, **cache_kwargs)
                    .first()
                ):
                    session.flash = "Sorry you are not registered for this course.  You can view most Open courses if you log out"
                    redirect(URL(c="default", f="courses"))

            else:
                # Get the base course from the URL.
                if "last_course" in request.cookies:
                    last_base = (
                        db(
                            db.courses.course_name
                            == request.cookies["last_course"].value
                        )
                        .select(db.courses.base_course)
                        .first()
                    )
                    if last_base and last_base.base_course == base_course:
                        # The user is trying to access the base course for the last course they logged in to
                        # there is a 99% chance this is an error and we should make them log in.
                        session.flash = (
                            "You most likely want to log in to access your course"
                        )
                        redirect(URL(c="default", f="courses"))
                response.serve_ad = True
                course = (
                    db(db.courses.course_name == base_course)
                    .select(
                        db.courses.id,
                        db.courses.course_name,
                        db.courses.base_course,
                        db.courses.login_required,
                        db.courses.allow_pairs,
                        db.courses.downloads_enabled,
                        **cache_kwargs,
                    )
                    .first()
                )

                if not course:
                    # This course doesn't exist.
                    raise HTTP(404)

                attrdict = getCourseAttributesDict(course.id)
                # set defaults for various attrs
                if "enable_compare_me" not in attrdict:
                    attrdict["enable_compare_me"] = "true"

                # Require a login if necessary.
                if course.login_required:
                    # Ask for a login by invoking the auth decorator.
                    @auth.requires_login()
                    def dummy():
                        pass

                    dummy()
                    # This code should never run!
                    assert False
                # Make this an absolute path.
            if not is_custom:
                book_path = safe_join(
                    os.path.join(
                        request.folder,
                        "books",
                        base_course,
                        "published" if is_published else "build",
                        directory_name if directory_name else base_course,
                    ),
                    *request.args[1:],
                )
            else:
                book_path = safe_join(
                    os.path.join(
                        request.folder,
                        "custom_books",
                        request.args[0],
                        request.args[1],
                        request.args[2],
                        "published" if is_published else "build",
                        directory_name,
                    ),
                    *request.args[3:],
                )
            break
    if (
        is_custom and request.args[0] == "published" and courseless_custom_published
    ) or (is_custom and request.args[0] == "drafts"):
        book_path = safe_join(
            os.path.join(
                request.folder,
                "custom_books",
                request.args[0],
                request.args[1],
                request.args[2],
                "published" if is_published else "build",
                directory_name,
            ),
            *request.args[3:],
        )
    if not book_path:
        logger.error("No Safe Path for {}".format(request.args[1:]))
        raise HTTP(404)

    # See if this is static content. By default, the Sphinx static directory names are ``_static`` and ``_images``.
    if request.args(3 if is_custom else 1) in [
        "_static",
        "_images",
    ] or book_path.endswith(("css", "png", "jpg")):
        # See the `response <http://web2py.com/books/default/chapter/29/04/the-core#response>`_.
        # Warning: this is slow. Configure a production server to serve this statically.
        return response.stream(book_path, 2 ** 20, request=request)

    # It's HTML -- use the file as a template.
    #
    # Make sure the file exists. Otherwise, the rendered "page" will look goofy.
    if not os.path.isfile(book_path):
        logger.error("Bad Path for {} given {}".format(book_path, request.args[1:]))
        raise HTTP(404)
    response.view = book_path
    chapter = os.path.split(os.path.split(book_path)[0])[1]
    subchapter = os.path.basename(os.path.splitext(book_path)[0])
    div_counts = {}
    # only for displaying with a course
    if auth.user and (
        (not is_custom)
        or (
            is_custom
            and request.args[0] == "published"
            and not courseless_custom_published
        )
    ):
        user_id = auth.user.username
        email = auth.user.email
        is_logged_in = "true"
        # Get the necessary information to update subchapter progress on the page
        page_divids = db(
            (db.questions.subchapter == subchapter)
            & (db.questions.chapter == chapter)
            & (db.questions.from_source == True)  # noqa: E712
            & ((db.questions.optional == False) | (db.questions.optional == None))
            & (db.questions.base_course == base_course)
        ).select(db.questions.name)
        div_counts = {q.name: 0 for q in page_divids}
        sid_counts = db(
            (db.questions.subchapter == subchapter)
            & (db.questions.chapter == chapter)
            & (db.questions.base_course == base_course)
            & (db.questions.from_source == True)  # noqa: E712
            & ((db.questions.optional == False) | (db.questions.optional == None))
            & (db.questions.name == db.useinfo.div_id)
            & (db.useinfo.course_id == auth.user.course_name)
            & (db.useinfo.sid == auth.user.username)
        ).select(db.useinfo.div_id, distinct=True)
        for row in sid_counts:
            div_counts[row.div_id] = 1
    else:
        user_id = "Anonymous"
        email = ""
        is_logged_in = "false"

    if session.readings:
        reading_list = session.readings
    else:
        reading_list = "null"
    # only for displaying with a course
    if (not is_custom) or (
        is_custom and request.args[0] == "published" and not courseless_custom_published
    ):
        try:
            db.useinfo.insert(
                sid=user_id,
                act="view",
                div_id=book_path,
                event="page",
                timestamp=datetime.datetime.utcnow(),
                course_id=course.course_name,
            )
        except Exception as e:
            logger.error(
                "failed to insert log record for {} in {} : {} {} {}".format(
                    user_id, course.course_name, book_path, "page", "view"
                )
            )
            logger.error("Database Error Detail: {}".format(e))

        user_is_instructor = (
            "true"
            if auth.user and verifyInstructorStatus(auth.user.course_name, auth.user)
            else "false"
        )
    # Support Runestone Campaign
    #
    # settings.show_rs_banner = True  # debug only
    banner_num = None
    if donated:
        banner_num = 0  # Thank You Banner
    else:
        if settings.num_banners > 0:
            banner_num = random.randrange(
                1, settings.num_banners + 1
            )  # select a random banner
        else:
            settings.show_rs_banner = False

    questions = None
    if subchapter == "Exercises":
        questions = _exercises(base_course, chapter)
    logger.debug("QUESTIONS = {} {}".format(subchapter, questions))
    # display as part of a course
    if (not is_custom) or (
        is_custom and request.args[0] == "published" and not courseless_custom_published
    ):
        return dict(
            course_name=course.course_name,
            base_course=base_course,
            is_logged_in=is_logged_in,
            user_id=user_id,
            user_email=email,
            is_instructor=user_is_instructor,
            allow_pairs=allow_pairs,
            readings=XML(reading_list),
            activity_info=json.dumps(div_counts),
            downloads_enabled=downloads_enabled,
            subchapter_list=_subchaptoc(base_course, chapter),
            questions=questions,
            motd=motd,
            banner_num=banner_num,
            **attrdict,
        )
    else:  # display courselessly
        return dict(
            course_name="null",
            base_course="null",
            is_logged_in=is_logged_in,
            user_id=user_id,
            user_email=email,
            is_instructor="false",
            allow_pairs="false",
            readings=XML(reading_list),
            activity_info=json.dumps(div_counts),
            downloads_enabled="false",
            subchapter_list=[],
            questions=questions,
            motd=motd,
            banner_num=banner_num,
            enable_compare_me="true",
        )


def _subchaptoc(course, chap):
    res = db(
        (db.chapters.id == db.sub_chapters.chapter_id)
        & (db.chapters.course_id == course)
        & (db.chapters.chapter_label == chap)
    ).select(
        db.sub_chapters.sub_chapter_label,
        db.sub_chapters.sub_chapter_name,
        orderby=db.sub_chapters.sub_chapter_num,
        cache=(cache.ram, 3600),
        cacheable=True,
    )
    toclist = []
    for row in res:
        sc_url = "{}.html".format(row.sub_chapter_label)
        title = row.sub_chapter_name
        toclist.append(dict(subchap_uri=sc_url, title=title))

    return toclist


def _exercises(basecourse, chapter):
    """
    Given a base course and a chapter return the instructor generated questions
    for the Exercises subchapter.

    """
    print("{} {}".format(chapter, basecourse))
    questions = db(
        (db.questions.chapter == chapter)
        & (db.questions.subchapter == "Exercises")
        & (db.questions.base_course == basecourse)
        & (db.questions.is_private == "F")
        & (db.questions.from_source == "F")
        & (
            (db.questions.review_flag != "T") | (db.questions.review_flag == None)
        )  # noqa: E711
    ).select(
        db.questions.htmlsrc,
        db.questions.author,
        db.questions.difficulty,
        db.questions.qnumber,
        orderby=db.questions.timestamp,
    )
    return questions


# This is copied verbatim from https://github.com/pallets/werkzeug/blob/master/werkzeug/security.py#L30.
_os_alt_seps = list(
    sep for sep in [os.path.sep, os.path.altsep] if sep not in (None, "/")
)


# This is copied verbatim from https://github.com/pallets/werkzeug/blob/master/werkzeug/security.py#L216.
def safe_join(directory, *pathnames):
    """Safely join `directory` and one or more untrusted `pathnames`.  If this
    cannot be done, this function returns ``None``.
    :param directory: the base directory.
    :param pathnames: the untrusted pathnames relative to that directory.
    """
    parts = [directory]
    for filename in pathnames:
        if filename != "":
            filename = posixpath.normpath(filename)
        for sep in _os_alt_seps:
            if sep in filename:
                return None
        if os.path.isabs(filename) or filename == ".." or filename.startswith("../"):
            return None
        parts.append(filename)
    return posixpath.join(*parts)


# Endpoints
# =========

# Serve from the ``published`` directory, instead of the ``build`` directory.
def published():
    if len(request.args) == 0:
        return index()
    dn = None
    try:
        dn = os.listdir(f"applications/runestone/books/{request.args(0)}/published")[0]
    except:
        pass
    return _route_book(directory_name=dn)


@auth.requires_login()
def custom_books():
    if len(request.args) <= 3:
        return index()
    book = db(db.textbooks.path == request.args(1) + "/" + request.args(2)).select()
    if len(book) != 1:
        return index()
    book = book[0]
    # only the runestone account that has created the draft version of a textbook should be able to view it
    if request.args[0] == "draft" and book.runestone_account != auth.user.username:
        raise (403, "You are not the owner of this custom textbook")
    # every time runestone build and publish is ran on the published or draft version of the book, the corresponding directory name that is created is put in the database
    dn = (
        book.drafts_directory
        if request.args[0] == "drafts"
        else book.published_directory
    )
    try:
        # this should be the same as the value that was put into the database, but this one is certian to be accurate
        dn = os.listdir(
            f"applications/runestone/custom_books/{request.args(0)}/{request.args(1)}/{request.args(2)}/published"
        )[0]
    except:
        pass
    if not dn:
        dn = (
            book.base_book
        )  # if nothing has been found so far, hope that it is still the same name as the base book it was cloned from
    return _route_book(is_custom=True, directory_name=dn)


def index():
    """
    Called by default (and by published if no args)

    Produce a list of books based on the directory structure of runestone/books

    """

    book_list = os.listdir("applications/{}/books".format(request.application))
    book_list = [book for book in book_list if ".git" not in book]

    res = []
    for book in sorted(book_list):
        try:
            # WARNING: This imports from ``applications.<runestone application name>.books.<book name>``. Since ``runestone/books/<book_name>`` lacks an ``__init__.py``, it will be treated as a `namespace package <https://www.python.org/dev/peps/pep-0420/>`_. Therefore, odd things will happen if there are other modules named ``applications.<runestone application name>.books.<book name>`` in the Python path.
            config = importlib.import_module(
                "applications.{}.books.{}.conf".format(request.application, book)
            )
        except Exception as e:
            logger.error("Error in book list: {}".format(e))
            continue
        book_info = {}
        book_info.update(course_description="")
        book_info.update(key_words="")
        if hasattr(config, "navbar_title"):
            book_info["title"] = config.navbar_title
        elif hasattr(config, "html_title"):
            book_info["title"] = config.html_title
        elif hasattr(config, "html_short_title"):
            book_info["title"] = config.html_short_title
        else:
            book_info["title"] = "Runestone Book"
        # update course description if found in the book's conf.py
        if hasattr(config, "course_description"):
            book_info.update(course_description=config.course_description)
        # update course key_words if found in book's conf.py
        if hasattr(config, "key_words"):
            book_info.update(key_words=config.key_words)
        book_info["url"] = "/{}/books/published/{}/index.html".format(
            request.application, book
        )
        book_info["regname"] = book
        res.append(book_info)
    return dict(book_list=res)
