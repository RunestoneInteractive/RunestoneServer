# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
import random, string
import datetime
import logging
from threading import Thread
import requests, json, time, re, importlib, os, hashlib, hmac

logger = logging.getLogger(settings.logger)
logger.setLevel(settings.log_level)

admin_logger(logger)
#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


@auth.requires_login()
def index():
    basicvalues = {}
    if settings.academy_mode:
        basicvalues["message"] = T("Course and Textbook Designer")
        basicvalues["descr"] = T(
            """This page allows you to select a book for your own class. You will have access to all student activities in your course.
        To begin, enter a project name below."""
        )
    return basicvalues


def logout_github():
    session.auth.user.__dict__.pop("github_oauth_token", None)
    session.auth.user.__dict__.pop("github_user", None)
    if request.args(0) == "revoke":
        redirect("https://github.com/settings/applications")
    redirect(URL("designer", "book"))


def update_local_files(path, clone_url, commit_id, oldbookname=None):
    do_async = True  ###TODO turn to true for production

    def update_async(path, clone_url, commit_id, oldbookname):
        if (
            oldbookname
        ):  # try moving from oldbookname to the last part of path, but if that does not work remove oldbookname
            os.system(
                "cd "
                + "/".join(path.split("/")[:-1])
                + f" && (mv {oldbookname} {path.split('/')[-1]} || rm -rf {oldbookname} )"
            )

        def reset_local(
            path, clone_url, commit_id
        ):  # if anything goes wrong this function is called. it deletes everything and re clones it
            os.system("rm -rf " + path)
            os.system("mkdir " + path)
            os.system(
                "cd "
                + path
                + " && cd .. && git clone "
                + clone_url
                + " "
                + path.split("/")[-1]
            )
            if commit_id:
                os.system(
                    "cd " + path + " && git fetch && git reset --hard " + commit_id
                )

        os.system("mkdir -p " + "/".join(path.split("/")[:-1]))
        try:
            x = os.system(
                "cd "
                + path
                + " && git symbolic-ref --short refs/remotes/origin/HEAD 1> /dev/null 2> /dev/null"
            )
            if (
                x != 0
                or os.system(
                    "cd "
                    + path
                    + " && git fetch 1> /dev/null 2> /dev/null && git reset --hard "
                    + commit_id
                )
                != 0
            ):
                reset_local(path, clone_url, commit_id)
        except:
            reset_local(path, clone_url, commit_id)
        os.system(
            f"cd {path} && runestone build 1> /dev/null 2> /dev/null && runestone deploy 1> /dev/null 2> /dev/null"
        )
        directory_name = None
        try:
            directory_name = os.listdir(path + "/published")[0]
        except:
            logger.error(f"error setting directory name for {path}")
        new_book_path = ("/").join(path.split("/")[4:6])
        if directory_name:
            if path.split("/")[3] == "drafts":
                db.textbooks.update_or_insert(
                    db.textbooks.path == new_book_path, drafts_directory=directory_name
                )
            else:
                db.textbooks.update_or_insert(
                    db.textbooks.path == new_book_path,
                    published_directory=directory_name,
                )

    if do_async:
        Thread(
            target=update_async, args=(path, clone_url, commit_id, oldbookname)
        ).start()
    else:
        update_async(path, clone_url, commit_id, oldbookname)


def update_books_webhook():
    verify_webhook = False  ### TODO turn to true in production
    post_data_json = request.vars
    textbook = db(
        (db.textbooks.github_account == post_data_json["repository"]["owner"]["login"])
        & (db.textbooks.github_repo_name == post_data_json["repository"]["name"])
    ).select()[0]
    computed_hash = (
        "sha256="
        + hmac.new(
            textbook.webhook_code.encode("utf-8"), request.body.read(), hashlib.sha256
        ).hexdigest()
    )
    logger.debug(request.env["HTTP_X_HUB_SIGNATURE_256"] + "   " + computed_hash)
    if verify_webhook and not request.env["HTTP_X_HUB_SIGNATURE_256"] == computed_hash:
        raise HTTP(503, "wrong hub signature!")
    if textbook and (
        "ref" not in post_data_json.keys()
        or post_data_json["repository"]["default_branch"]
        == post_data_json["ref"].split("/")[-1]
    ):
        local_path = "applications/runestone/custom_books/drafts/" + textbook.path
        if "commits" in post_data_json.keys():  # we were sent a commit
            update_local_files(
                local_path,
                post_data_json["repository"]["clone_url"],
                post_data_json["head_commit"]["id"],
            )
            db.textbooks.update_or_insert(
                db.textbooks.path == textbook.path,
                draft_commit=post_data_json["head_commit"]["id"],
            )
        else:  # we were not sent a commit (this happens on the inital fork, in this case we will just clone the repo)
            update_local_files(
                local_path, post_data_json["repository"]["clone_url"], None
            )
        raise HTTP(200, "updated successfully")
    raise HTTP(500, "internal server error")


def verify_github_login(desiredUser, retry=True):
    if "github_oauth_token" in session.auth.user.__dict__.keys():
        user = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": "token "
                + session.auth.user.__dict__["github_oauth_token"]
            },
        )
        if user.status_code != 200 and retry:
            location = (
                "https://github.com/login/oauth/authorize?scope=repo,delete_repo&client_id="
                + session.auth.user.__dict__["github_client_id"]
            )
            logger.debug(
                f"github token for {session.auth.user.username} expired, redirecting to refresh token"
            )
            session.auth.user.__dict__.pop("github_oauth_token", None)
            session.auth.user.__dict__.pop("github_user", None)
            raise HTTP(
                303,
                "You are being redirected to refresh your github token",
                Location=location,
            )
        elif user.status_code != 200 and (not retry):
            session.auth.user.__dict__.pop("github_oauth_token", None)
            session.auth.user.__dict__.pop("github_user", None)
            return False
        else:
            if user.json()["login"] == desiredUser:
                session.auth.user.__dict__["github_user"] = user.json()["login"]
                return True
            else:
                session.auth.user.__dict__.pop("github_user", None)
                session.auth.user.__dict__.pop("github_oauth_token", None)
                return False
    else:
        session.auth.user.__dict__.pop("github_user", None)
        return False


def github_book_repo(
    account, repo, oldb, renameval=None, delete=False, reset=False, create=False
):
    ret_dict = {"changed": False, "failed": True}
    auth = (
        session.auth.user.__dict__["github_user"],
        session.auth.user.__dict__["github_oauth_token"],
    )
    headers = {"Accept": "application/vnd.github.v3+json"}
    base_url = "https://api.github.com/"
    ## sanity check API is working on githubs side and we have the correct credentials
    sanity_check = requests.get(
        base_url + "users/" + account + "/repos", auth=auth, headers=headers
    )
    if not sanity_check.status_code == 200:
        ret_dict["msg"] = "unable to even connect to github API"
        return ret_dict
    ## checking that the repo in question is either found or not found
    check_existence = requests.get(
        base_url + "repos/" + account + "/" + repo, auth=auth, headers=headers
    )
    if not (check_existence.status_code == 404 or check_existence.status_code == 200):
        ret_dict[
            "msg"
        ] = "repository gave neither a 404 or a 200, some bad error occured"
        return ret_dict
    if delete or reset:
        # cant delete if nothing is there
        if check_existence.status_code == 404:
            ret_dict["msg"] = "nothing to delete"
            return ret_dict
        remove = requests.delete(
            base_url + "repos/" + account + "/" + repo, auth=auth, headers=headers
        )
        if not remove.status_code == 204:
            ret_dict["msg"] = "error with delete API request"
            return ret_dict
        elif delete:
            return {"changed": True, "failed": False}
        else:
            ret_dict["changed"] = True
    fork_existence = requests.get(
        base_url + "repos/" + account + "/" + oldb, auth=auth, headers=headers
    )
    # If we are trying to create a repository that already exists, fail
    # If we are going to fork into a repository that already exists as we create, fail
    if (
        (check_existence.status_code != 404 or fork_existence.status_code != 404)
        and create
    ) or (fork_existence.status_code != 404 and reset):
        ret_dict["msg"] = "trying to create a repo that already exists"
        return ret_dict
    if create or reset:
        fork_url = base_url + "repos/RunestoneInteractive/" + oldb + "/forks"
        requests.post(fork_url, auth=auth, headers=headers)
        retries = 30
        # wait for the fork to finish
        while (
            requests.get(
                base_url + "repos/" + account + "/" + oldb, auth=auth, headers=headers
            ).status_code
            != 200
            and retries > 0
        ):
            time.sleep(1)
            retries -= 1
        if retries == 0:
            ret_dict["msg"] = "timed out waiting for repo to be forked"
            return ret_dict
        hook_url = base_url + "repos/" + account + "/" + oldb + "/hooks"
        ret_dict["webhook_code"] = "".join(
            random.choice(string.ascii_lowercase + string.digits) for i in range(20)
        )
        hook_data = {
            "config": {
                "url": "https://runestone.academy/runestone/designer/update_books_webhook",
                "content_type": "json",
                "secret": ret_dict["webhook_code"],
            }
        }
        requests.post(hook_url, auth=auth, headers=headers, data=json.dumps(hook_data))
        requests.patch(
            base_url + "repos/" + account + "/" + oldb,
            auth=auth,
            headers=headers,
            data=json.dumps({"name": repo}),
        )
        ret_dict["changed"] = True
    if renameval and not (check_existence.status_code == 200 or create):
        ret_dict["msg"] = "trying to edit a repo that does not exist"
        return ret_dict
    if renameval:
        requests.patch(
            base_url + "repos/" + account + "/" + repo,
            auth=auth,
            headers=headers,
            data=json.dumps({"name": renameval}),
        )
        ret_dict["changed"] = True
    ret_dict["failed"] = False
    return ret_dict


@auth.requires_login()
def book_edit():
    # Verify post data is of the correct format
    for id in [
        "oldBookIdentifier",
        "newBookIdentifier",
        "baseBook",
        "newGithubRepo",
        "githubUser",
        "oldGithubRepo",
    ]:
        if request.vars[id] == "" or " " in request.vars[id] or "/" in request.vars[id]:
            session.flash = (
                f"Failed to edit book: {id} cannot be emtpy, have spaces or /"
            )
            redirect(URL("designer", "book"))
        elif not re.match(
            "^([\x30-\x39]|[\x41-\x5A]|[\x61-\x7A]|[_-])*$", request.vars[id]
        ):
            session.flash = f"Failed to edit book: {id} must be alphanumeric or _ -"
            redirect(URL("designer", "book"))
    # Create, edit, delete or publish all can work with a notion of a previous book and a new book
    old_path = session.auth.user.username + "/" + request.vars.oldBookIdentifier
    new_path = session.auth.user.username + "/" + request.vars.newBookIdentifier
    existing_old_book = db(db.textbooks.path == old_path).select().first()
    existing_new_book = db(db.textbooks.path == new_path).select().first()
    new_book_is_same = existing_old_book == existing_new_book
    # Ensure the github user that is sent in the request actually owns this repository
    if not verify_github_login(request.vars.githubUser, False):
        session.flash = f"Failed to edit book: Token expired log in again"
        redirect(URL("designer", "book"))
    if request.vars.changeType == "create":
        if existing_new_book:
            logger.error(
                f"incorrect github permissions or incorrect database when trying to {request.vars.changeType} {request.vars.oldBookIdentifier}"
            )
            redirect(URL("designer", "book"))
        changed_github = github_book_repo(
            request.vars.githubUser,
            request.vars.newGithubRepo,
            request.vars.baseBook,
            create=True,
        )
        if changed_github["failed"]:
            session.flash = f"Failed to create book: {changed_github['msg']}"
            logger.error(f"Failed to create book: {changed_github['msg']}")
            redirect(URL("designer", "book"))
        else:
            session.flash = f"Created book: {request.vars['oldBookIdentifier']}"
            db.textbooks.update_or_insert(
                db.textbooks.path == new_path,
                path=new_path,
                github_account=request.vars.githubUser,
                runestone_account=session.auth.user.username,
                github_repo_name=request.vars.newGithubRepo,
                regname=request.vars.newBookIdentifier,
                base_book=request.vars.baseBook,
                published="false",
                webhook_code=changed_github["webhook_code"],
            )
    elif request.vars.changeType == "delete":
        if (
            (not existing_old_book)
            or (not request.vars.githubUser == existing_old_book.github_account)
            or (not session.auth.user.username == existing_old_book.runestone_account)
        ):
            logger.error(
                f"incorrect github permissions or incorrect database when trying to {request.vars.changeType} {request.vars.oldBookIdentifier}"
            )
            redirect(URL("designer", "book"))
        changed_github = github_book_repo(
            request.vars.githubUser,
            request.vars.oldGithubRepo,
            request.vars.baseBook,
            delete=True,
        )
        if changed_github["failed"]:
            session.flash = f"Failed to delete book: {changed_github['msg']}"
            logger.error(f"Failed to delete book: {changed_github['msg']}")
            redirect(URL("designer", "book"))
        else:
            os.system(
                "rm -rf applications/runestone/custom_books/drafts/{}/{}".format(
                    existing_old_book.runestone_account, existing_old_book.regname
                )
            )
            os.system(
                "rm -rf applications/runestone/custom_books/published/{}/{}".format(
                    existing_old_book.runestone_account, existing_old_book.regname
                )
            )
            courses = db(db.courses.base_course == old_path).select()
            # all courses that are using the custom textbook now use the book that the custom textbook was originally cloned from
            for course in courses:
                db.courses.update_or_insert(
                    db.courses.course_name == course.course_name,
                    base_course=existing_old_book.base_book,
                )
            db(db.textbooks.path == old_path).delete()
            session.flash = f"Deleted book: {request.vars['oldBookIdentifier']}"
    elif request.vars.changeType == "edit":
        if (
            (not existing_old_book)
            or (existing_new_book and not new_book_is_same)
            or (not request.vars.githubUser == existing_old_book.github_account)
            or (not session.auth.user.username == existing_old_book.runestone_account)
        ):
            logger.error(
                f"incorrect github permissions or incorrect database when trying to {request.vars.changeType} {request.vars.oldBookIdentifier}"
            )
            redirect(URL("designer", "book"))
        if request.vars.newGithubRepo != existing_old_book.github_repo_name:
            changed_github = github_book_repo(
                request.vars.githubUser,
                request.vars.oldGithubRepo,
                request.vars.baseBook,
                renameval=request.vars.newGithubRepo,
            )
            if changed_github["failed"]:
                session.flash = f"Failed to edit book: {changed_github['msg']}"
                logger.error(f"Failed to edit book: {changed_github['msg']}")
                redirect(URL("designer", "book"))
        session.flash = f"Edited book: {request.vars['newBookIdentifier']}"
        if request.vars.oldBookIdentifier != request.vars.newBookIdentifer:
            db.textbooks.update_or_insert(
                db.textbooks.path == old_path,
                path=new_path,
                github_account=request.vars.githubUser,
                runestone_account=session.auth.user.username,
                github_repo_name=request.vars.newGithubRepo,
                regname=request.vars.newBookIdentifier,
            )
            update_local_files(
                "applications/runestone/custom_books/drafts/{}/{}".format(
                    existing_old_book.runestone_account, request.vars.newBookIdentifier
                ),
                "https://github.com/{}/{}.git".format(
                    existing_old_book.github_account, request.vars.newGithubRepo
                ),
                existing_old_book.draft_commit,
                oldbookname=request.vars.oldBookIdentifier,
            )
            if existing_old_book.published:
                update_local_files(
                    "applications/runestone/custom_books/published/{}/{}".format(
                        existing_old_book.runestone_account,
                        request.vars.newBookIdentifier,
                    ),
                    "https://github.com/{}/{}.git".format(
                        existing_old_book.github_account, request.vars.newGithubRepo
                    ),
                    existing_old_book.draft_commit,
                    oldbookname=request.vars.oldBookIdentifier,
                )
            courses = db(db.courses.base_course == old_path).select()
            # all courses that are using the custom textbook now use the new name
            for course in courses:
                db.courses.update_or_insert(
                    db.courses.course_name == course.course_name, base_course=new_path
                )
    elif request.vars.changeType == "publish":
        if (
            (not existing_old_book)
            or (not request.vars.githubUser == existing_old_book.github_account)
            or (not session.auth.user.username == existing_old_book.runestone_account)
        ):
            logger.error(
                f"incorrect github permissions or incorrect database when trying to {request.vars.changeType} {request.vars.oldBookIdentifier}"
            )
            redirect(URL("designer", "book"))
        db.textbooks.update_or_insert(
            db.textbooks.path == existing_old_book.path,
            published="true",
            published_commit=existing_old_book.draft_commit,
        )
        update_local_files(
            f"applications/runestone/custom_books/published/{existing_old_book.runestone_account}/{existing_old_book.regname}",
            f"https://github.com/{existing_old_book.github_account}/{existing_old_book.github_repo_name}.git",
            existing_old_book.draft_commit,
        )
        session.flash = f"Published book: {request.vars['oldBookIdentifier']}"
    else:
        session.flash = "invalid parameter for changeType passed to edit_book. This is an internal server error"
    redirect(URL("designer", "book"))
    ### TODO add handling for change_type "reset"


@auth.requires_login()
def callback():  # handles github oauth callback after user grants repository permiission
    if "code" in request.vars.keys():
        oauth_url = "https://github.com/login/oauth/access_token"
        oauth_data = {
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "code": request.vars.code,
        }
        oauth_headers = {"Accept": "application/json"}
        try:
            oauth = requests.post(oauth_url, json=oauth_data, headers=oauth_headers)
            if oauth.status_code == 200:
                session.auth.user.__dict__["github_oauth_token"] = oauth.json()[
                    "access_token"
                ]
                user = requests.get(
                    "https://api.github.com/user",
                    headers={"Authorization": "token " + oauth.json()["access_token"]},
                )
                session.auth.user.__dict__["github_user"] = user.json()["login"]
            else:
                session.flash = f"got {oauth.status_code} from github"
        except:
            logger.error(
                f"Failure connecting to {oauth_url} There is either a problem with your servers connectivity or githubs"
            )
    redirect(URL("designer", "book"))


def gather_book_info(book_list, username=None):
    book_list_result = []
    for book in sorted(book_list):
        try:
            # WARNING: This imports from ``applications.<runestone application name>.books.<book name>``. Since ``runestone/books/<book_name>`` lacks an ``__init__.py``, it will be treated as a `namespace package <https://www.python.org/dev/peps/pep-0420/>`_. Therefore, odd things will happen if there are other modules named ``applications.<runestone application name>.books.<book name>`` in the Python path.
            if username:
                config = importlib.import_module(
                    "applications.{}.custom_books.drafts.{}.{}.conf".format(
                        request.application, username, book
                    )
                )
            else:
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
        if not username:  # non-custom book
            book_info["url"] = "/{}/books/published/{}/index.html".format(
                request.application, book
            )
        else:  # custom book
            book_info["url"] = "/{}/books/custom_books/drafts/{}/{}/index.html".format(
                request.application, username, book
            )
            book_info[
                "published_url"
            ] = "/{}/books/custom_books/published/{}/{}/index.html".format(
                request.application, username, book
            )
            db_result = (
                db(db.textbooks.path == session.auth.user.username + "/" + book)
                .select()
                .first()
            )
            book_info["github_repo_name"] = db_result.github_repo_name
            book_info["github_account"] = db_result.github_account
            book_info["published"] = db_result.published
            book_info["path"] = session.auth.user.username + "/" + book
        book_info["regname"] = book
        book_list_result.append(book_info)
    return book_list_result


@auth.requires_login()
def book():
    os.system(
        "mkdir -p "
        + "applications/{}/custom_books/drafts/{}".format(
            request.application, session.auth.user.username
        )
    )
    os.system(
        "mkdir -p "
        + "applications/{}/custom_books/published/{}".format(
            request.application, session.auth.user.username
        )
    )
    github = {}
    session.auth.user.__dict__["github_client_id"] = os.getenv("CLIENT_ID")
    github["client_id"] = session.auth.user.__dict__["github_client_id"]
    if "github_user" in session.auth.user.__dict__.keys():
        if not verify_github_login(session.auth.user.__dict__["github_user"]):
            session.auth.user.__dict__.pop("github_user", None)
            session.auth.user.__dict__.pop("github_oauth_token", None)
            github["found"] = False
        else:
            github["user"] = session.auth.user.__dict__["github_user"]
            github["found"] = True
    else:
        github["found"] = False
    book_list = os.listdir("applications/{}/books".format(request.application))
    book_list = [book for book in book_list if ".git" not in book]
    custom_book_list = os.listdir(
        "applications/{}/custom_books/drafts/{}".format(
            request.application, session.auth.user.username
        )
    )
    custom_book_list = [book for book in custom_book_list if ".git" not in book]
    book_list_result = gather_book_info(book_list)
    custom_book_list_result = gather_book_info(
        custom_book_list, session.auth.user.username
    )
    return dict(
        book_list=book_list_result,
        custom_book_list=custom_book_list_result,
        github=github,
    )


@auth.requires_login()
def course():
    os.system(
        "mkdir -p "
        + "applications/{}/custom_books/drafts/{}".format(
            request.application, session.auth.user.username
        )
    )
    os.system(
        "mkdir -p "
        + "applications/{}/custom_books/published/{}".format(
            request.application, session.auth.user.username
        )
    )
    basicvalues = {}
    if settings.academy_mode:
        """
        example action using the internationalization operator T and flash
        rendered by views/default/index.html or views/generic.html
        """
        # response.flash = "Welcome to CourseWare Manager!"

        basicvalues["message"] = T("Build a Custom Course")
        basicvalues["descr"] = T(
            """This page allows you to select a book for your own class. You will have access to all student activities in your course.
        To begin, enter a project name below."""
        )
        # return dict(message=T('Welcome to CourseWare Manager'))
    custom_book_list = os.listdir(
        "applications/{}/custom_books/drafts/{}".format(
            request.application, session.auth.user.username
        )
    )
    custom_book_list = [book for book in custom_book_list if ".git" not in book]
    basicvalues["custom_book_list"] = gather_book_info(
        custom_book_list, session.auth.user.username
    )
    return basicvalues


@auth.requires_login()
def course_build():
    buildvalues = {}
    if settings.academy_mode:
        buildvalues["pname"] = request.vars.projectname
        buildvalues["pdescr"] = request.vars.projectdescription

        existing_course = (
            db(db.courses.course_name == request.vars.projectname).select().first()
        )
        if existing_course:
            session.flash = (
                f"course name {request.vars.projectname} has already been used"
            )
            redirect(URL("designer", "course"))

        if not request.vars.coursetype:
            session.flash = "You must select a base course."
            redirect(URL("designer", "course"))

        # if make instructor add row to auth_membership
        if "instructor" in request.vars:
            gid = (
                db(db.auth_group.role == "instructor").select(db.auth_group.id).first()
            )
            db.auth_membership.insert(user_id=auth.user.id, group_id=gid)

        base_course = request.vars.coursetype

        if request.vars.startdate == "":
            request.vars.startdate = datetime.date.today()
        else:
            date = request.vars.startdate.split("/")
            request.vars.startdate = datetime.date(
                int(date[2]), int(date[0]), int(date[1])
            )

        if not request.vars.institution:
            institution = "Not Provided"
        else:
            institution = request.vars.institution

        if not request.vars.courselevel:
            courselevel = "unknown"
        else:
            courselevel = request.vars.courselevel

        python3 = "true"

        if not request.vars.loginreq:
            login_required = "false"
        else:
            login_required = "true"

        cid = db.courses.update_or_insert(
            course_name=request.vars.projectname,
            term_start_date=request.vars.startdate,
            institution=institution,
            base_course=base_course,
            login_required=login_required,
            python3=python3,
            courselevel=courselevel,
        )

        if request.vars.invoice:
            db.invoice_request.insert(
                timestamp=datetime.datetime.now(),
                sid=auth.user.username,
                email=auth.user.email,
                course_name=request.vars.projectname,
            )

        # enrol the user in their new course
        db(db.auth_user.id == auth.user.id).update(course_id=cid)
        db.course_instructor.insert(instructor=auth.user.id, course=cid)
        auth.user.update(
            course_name=request.vars.projectname
        )  # also updates session info
        auth.user.update(course_id=cid)
        db.executesql(
            """
            INSERT INTO user_courses(user_id, course_id)
            SELECT %s, %s
            """,
            (auth.user.id, cid),
        )

        session.flash = "Course Created Successfully"
        # redirect(
        #     URL("books", "published", args=[request.vars.projectname, "index.html"])
        # )

        return dict(coursename=request.vars.projectname, basecourse=base_course)
