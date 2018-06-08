"Module for managing user accounts - registration and logins."
import sqlite3
import arrow
import flask
from ixstates import util

blueprint = flask.Blueprint(  # pylint: disable=invalid-name
    "api.blog", __name__)

NEW_POST_QUERY = """INSERT INTO posts (poster, date, title, content)
VALUES (?, ?, ?, ?);"""


@blueprint.route("/post", methods=["POST"])
@util.requires_login
def post():
    "End route for user logins."
    title = flask.request.form["post_title"]
    body = flask.request.form["post_body"]
    timestamp = arrow.now().replace(second=0).timestamp
    try:
        util.executeSQL(NEW_POST_QUERY,
                        [flask.session["uid"], timestamp, title, body])
        util.queue_message("New post made: %r" % title)
    except sqlite3.IntegrityError:
        util.queue_message("Post failed: %r; too many in one minute" % title)
    return util.redirect("ui.index.index")
