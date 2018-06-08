"Routes for managing mail"
import arrow
import flask
from ixstates import util

blueprint = flask.Blueprint(  # pylint: disable=invalid-name
    "api.mail", __name__)

ADD_USER_QUERY = """
INSERT OR IGNORE INTO users2mails (mail_uid, user_uid)
SELECT ?, users.uid FROM users
WHERE users.username LIKE ?
"""


@blueprint.route("/mail/send", methods=["POST"])
@util.requires_login
def send():
    "Send a message to another user"
    uid = flask.request.form.get("mail_uid")
    if uid is None:
        util.queue_message("Missing `mail_uid` in input.")
        return util.redirect("ui.mail.index")
    if flask.request.form.get('archive') is not None:
        util.executeSQL("UPDATE mails SET archived = 1 WHERE uid = ?", (uid,))
        return util.redirect("ui.mail.index")
    elif flask.request.form.get('unarchive') is not None:
        util.executeSQL("UPDATE mails SET archived = 0 WHERE uid = ?", (uid,))
    elif flask.request.form.get('send_reply') is not None:
        user = flask.session.get("uid")
        message = flask.request.form.get("reply")
        date = arrow.get().timestamp
        util.executeSQL(
            ("INSERT INTO messages2mails (mail_uid, user_uid, text, date) "
             "VALUES (?, ?, ?, ?)"),
            (uid, user, message, date))
        util.executeSQL("UPDATE mails SET last_date = ? WHERE uid = ?",
                        (arrow.get().timestamp, uid))
    return util.redirect("ui.mail.index")


@blueprint.route("/mail/new", methods=["POST"])
@util.requires_login
def new():
    "Start a new mail conversation"
    try:
        users = list((item.strip()
                      for item in flask.request.form["users"].split(",")))
        user_uid = flask.session["uid"]
        message = flask.request.form["message"]
        date = arrow.get().timestamp
        if len(users) < 1:
            util.queue_message("Not enough users")
            return util.redirect("ui.mail.index")
        util.executeSQL("INSERT INTO mails (subject, last_date)"
                        "VALUES (?, ?)", (flask.request.form["subject"], date))
        mail_uid = next(util.querySQL(
            "SELECT uid FROM mails ORDER BY uid DESC LIMIT 1"))["uid"]
        util.executeSQL("INSERT INTO users2mails (mail_uid, user_uid) "
                        "VALUES (?, ?)", (mail_uid, user_uid))
        for user in users:
            util.executeSQL(ADD_USER_QUERY, (mail_uid, user))
        util.executeSQL("INSERT INTO messages2mails (mail_uid, user_uid, "
                        "text, date) VALUES (?, ?, ?, ?)",
                        (mail_uid, user_uid, message, date))
    except KeyError:
        util.queue_message("API did not receive correct parameters")
    return util.redirect("ui.mail.index")
