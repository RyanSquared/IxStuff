"Module for managing user accounts - registration and logins."
import sqlite3
import bcrypt
import flask
from ixstates import util

blueprint = flask.Blueprint(  # pylint: disable=invalid-name
    "api.user_management", __name__)


LOGIN_QUERY = "SELECT * FROM users WHERE username LIKE ?;"
REGISTER_QUERY = "INSERT INTO users (username, password) VALUES (?, ?);"


@blueprint.route("/login", methods=["POST"])
def handler():
    "End route for user logins."
    form = flask.request.form
    if flask.request.form.get("login") is not None:
        try:
            user = next(util.querySQL(LOGIN_QUERY,
                                      (form["username"],)))
            password = form["password"].encode("ascii")
            if bcrypt.checkpw(password, user["password"].encode("ascii")):
                flask.session["user"] = user["username"]
                flask.session["uid"] = user["uid"]
                util.queue_message("Login successful for " +
                                   repr(user["username"]))
            else:
                util.queue_message(
                    "Login failed: Incorrect password for " +
                    repr(user["username"]))
        except KeyError as err:
            util.queue_message("Invalid POST data for logging in.")
            flask.session["error"] = repr(err)
            return flask.abort(400)
        except StopIteration:
            util.queue_message("Login failed: No user found: " + repr(
                form["username"]))
            return util.redirect("ui.index.index")
    elif flask.request.form.get("register") is not None:
        password = form["password"].encode("ascii")
        try:
            util.executeSQL(REGISTER_QUERY,
                            (form["username"],
                             bcrypt.hashpw(password, bcrypt.gensalt())))
        except sqlite3.IntegrityError:
            util.queue_message("User already exists: " +
                               repr(form["username"]))
    else:
        util.queue_message("Invalid form information.")
        flask.session["error"] = "login|register not in " + repr(
            flask.request.form)
    return util.redirect("ui.index.index")


@blueprint.route("/error")
def get_error():
    "Return an error stored in the session"
    return flask.session.get("error") or ""
