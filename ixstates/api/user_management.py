"Module for managing user accounts - registration and logins."
import sqlite3
import bcrypt
import flask
import six
from ixstates import util

blueprint = flask.Blueprint(  # pylint: disable=invalid-name
    "api.user_management", __name__)


LOGIN_QUERY = "SELECT * FROM users WHERE username LIKE ?;"
REGISTER_QUERY = "INSERT INTO users (username, password) VALUES (?, ?);"


def convert_string(item):
    "Convert a Unicode string or bytes object to a binary type"
    if isinstance(item, six.text_type):
        return bytes(bytearray(item, "ascii"))
    return item


@blueprint.route("/login", methods=["POST"])
def handler():
    "End route for user logins."
    form = flask.request.form
    if flask.request.form.get("login") is not None:
        try:
            user = next(util.querySQL(LOGIN_QUERY,
                                      (form["username"],)))
            password = convert_string(form["password"])
            if bcrypt.checkpw(password, convert_string(user["password"])):
                flask.session["user"] = user["username"]
                flask.session["uid"] = user["uid"]
                flask.session["admin"] = user["admin"] == 1
                util.queue_message("Login successful for %r" %
                                   user["username"])
            else:
                util.queue_message(
                    "Login failed: Incorrect password for %r" %
                    user["username"])
        except KeyError as err:
            util.queue_message("Invalid POST data for logging in.")
            flask.session["error"] = repr(err)
            return flask.abort(400)
        except StopIteration:
            util.queue_message("Login failed: No user found: %r" %
                               form["username"])
            return util.redirect("ui.index.index")
    elif flask.request.form.get("register") is not None:
        password = convert_string(form["password"])
        try:
            util.executeSQL(REGISTER_QUERY,
                            (form["username"],
                             bcrypt.hashpw(password, bcrypt.gensalt())))
            util.queue_message("User registered: %r" % form["username"])
        except sqlite3.IntegrityError:
            util.queue_message("User already exists: %r" %
                               form["username"])
    else:
        util.queue_message("Invalid form information.")
        flask.session["error"] = ("login|register not in %r" %
                                  flask.request.form)
    return util.redirect("ui.index.index")


@blueprint.route("/error")
def get_error():
    "Return an error stored in the session"
    return flask.session.get("error") or ""
