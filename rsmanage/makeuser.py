# running in the context of a web2py shell
import json
import sys
from psycopg2 import IntegrityError
import click
import datetime


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
        db.commit()
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
