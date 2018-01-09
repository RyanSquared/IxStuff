"Routes for managing admin accounts"
import flask
from ixstates import util

blueprint = flask.Blueprint(  # pylint: disable=invalid-name
    "api.admin", __name__)


@blueprint.route("/give_admin", methods=["POST"])
@util.requires_admin
def give_admin():
    "Give administrative power to a user."
    try:
        user = flask.request.form["admin_user"]
        next(util.querySQL("SELECT uid FROM users WHERE uid = ?;", (user,)))
        util.executeSQL("UPDATE users SET admin = 1 WHERE uid = ?;", (user,))
        username = next(util.querySQL(
            "SELECT username FROM users WHERE uid = ?;", (user,)))["username"]
        util.queue_message("Updated admin status for user %r." % username)
    except StopIteration:
        util.queue_message("User not found. This should not happen. UI bug.")
    except KeyError:
        util.queue_message("UID not passed. This should not happen. UI bug.")
    return util.redirect("ui.admin.index")


@blueprint.route("/ban", methods=["POST"])
@util.requires_admin
def ban():
    "Remove login access for a user."
    try:
        user = flask.request.form["banned_user"]
        username = next(util.querySQL(
            "SELECT uid, username FROM users WHERE uid = ?;",
            (user,)))["username"]
        util.executeSQL("INSERT INTO bans (user_uid, reason) VALUES (?, ?);",
                        (user, flask.request.form["reason"]))
        util.queue_message("User %r has been banned." % username)
    except StopIteration:
        util.queue_message("User not found. This should not happen. UI bug.")
    except KeyError:
        util.queue_message("UID not passed. This should not happen. UI bug.")
    return util.redirect("ui.admin.index")
