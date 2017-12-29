"Mail view for IxStates."
import arrow
import flask
from ixstates import util

blueprint = flask.Blueprint('ui.mail',  # pylint: disable=invalid-name
                            __name__)


MAIL_QUERY = """SELECT * FROM mails
LEFT JOIN users2mails ON (users2mails.mail_uid = mails.uid)
WHERE users2mails.user_uid = ?
"""
USERS_MAIL_QUERY = """SELECT users.username username FROM users2mails
LEFT JOIN users ON (users.uid = users2mails.user_uid)
WHERE mail_uid = ?"""
MESSAGES_MAIL_QUERY = """SELECT
    messages2mails.text text,
    messages2mails.date date,
    messages2mails.user_uid user_uid,
    users.username user
FROM messages2mails
LEFT JOIN users ON (messages2mails.user_uid = users.uid)
WHERE mail_uid = ?"""


def map_date(entry):
    "Convert a timestamp into an Arrow for a SQL date"
    entry["date"] = arrow.get(entry["date"])
    return entry


def get_mails(uid):
    "Get unarchived mails for a user"
    if uid is None:
        return
    for mail in util.querySQL(MAIL_QUERY, (uid,)):
        users = [x["username"]
                 for x in util.querySQL(USERS_MAIL_QUERY, (mail["uid"],))]
        messages = list(
            map(map_date, util.querySQL(MESSAGES_MAIL_QUERY, (mail["uid"],))))
        mail.update([("users", users), ("messages", messages)])
        yield mail


@blueprint.route("/")
@util.requires_login
def index():
    "Mail page."
    return util.render_template('ui.mail.index', "mail.html",
                                mails=get_mails(flask.session.get("uid")))
