"Index view for IxStates."
import arrow
import flask
from ixstates import util

blueprint = flask.Blueprint('ui.index',  # pylint: disable=invalid-name
                            __name__)

APP_QUERY = ("SELECT * FROM posts LEFT JOIN users ON "
             "posts.poster = users.uid ORDER BY posts.date DESC;")


def add_arrow(post):
    "Give a post an Arrow object given a post with a timestamp."
    post["date"] = arrow.get(post["date"])
    return post


@blueprint.route("/")
def index():
    "Index page."
    posts = (add_arrow(post) for post in util.querySQL(APP_QUERY))
    return util.render_template('ui.index.index', "index.html",
                                posts=posts)
