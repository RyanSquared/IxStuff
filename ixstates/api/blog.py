"Module for managing user accounts - registration and logins."
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
    util.executeSQL(NEW_POST_QUERY,
                    [flask.session["uid"], arrow.now().timestamp, title, body])
    util.queue_message("New post made: %r" % title)
    return util.redirect("ui.index.index")
