# running in the context of a web2py shell
import json
import sys
from psycopg2 import IntegrityError
import click
import datetime


def createUser(username, password, fname, lname, email, course_name, instructor=False):
    cinfo = db(db.courses.course_name == course_name).select().first()
    if not cinfo:
        raise ValueError("Course {} does not exist".format(course_name))
    pw = CRYPT(auth.settings.hmac_key)(password)[0]
    uid = db.auth_user.insert(
        username=username,
        password=pw,
        first_name=fname,
        last_name=lname,
        email=email,
        course_id=cinfo.id,
        course_name=course_name,
        active="T",
        created_on=datetime.datetime.now(),
    )

    db.user_courses.insert(user_id=uid, course_id=cinfo.id)

    sect = (
        db((db.sections.course_id == cinfo.id) & (db.sections.name == "default"))
        .select(db.sections.id)
        .first()
    )
    db.section_users.update_or_insert(auth_user=uid, section=sect)

    if instructor:
        irole = db(db.auth_group.role == "instructor").select(db.auth_group.id).first()
        db.auth_membership.insert(user_id=uid, group_id=irole)
        db.course_instructor.insert(course=cinfo.id, instructor=uid)

    db.commit()


def resetpw(username, password):
    pw = CRYPT(auth.settings.hmac_key)(password)[0]
    db(db.auth_user.username == username).update(password=pw)


### Main ###

if "--userfile" in sys.argv:
    # find the file (.csv) iterate over each line and call createUser
    pass

userinfo = json.loads(os.environ["RSM_USERINFO"])

if "--resetpw" in sys.argv:
    try:
        resetpw(userinfo["username"], userinfo["password"])
    except Exception as e:
        click.echo("Password reset failed for user {}".format(userinfo["username"]))
        click.echo("Details: {}".format(e))
else:
    try:
        createUser(
            userinfo["username"],
            userinfo["password"],
            userinfo["first_name"],
            userinfo["last_name"],
            userinfo["email"],
            userinfo["course"],
            userinfo["instructor"],
        )
    except ValueError as e:
        click.echo("Value Error: ", e)
        sys.exit(1)
    except IntegrityError as e:
        click.echo("Caught an integrity error: ", e)
        sys.exit(2)
    except Exception as e:
        click.echo("Unexpected Error: ", e)
        sys.exit(3)

    click.echo("Exiting normally")
